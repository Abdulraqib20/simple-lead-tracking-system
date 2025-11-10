"""
FastAPI backend for Lead Tracking System.

This module provides the REST API endpoints for managing leads,
including CRUD operations, search, export, and statistics.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pathlib import Path
import os

from models import Lead, LeadCreate, LeadUpdate, LeadResponse
import database as db
import utils


app = FastAPI(
    title="Lead Tracking System",
    description="Simple lead management system with JSON storage",
    version="1.0.0"
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        db.ensure_data_file_exists()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")


# Serve static files (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"

# Only mount static files if not on Vercel
if frontend_path.exists() and not os.environ.get('VERCEL_ENV'):
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def read_root():
    """
    Serve the frontend HTML page.

    Returns:
        FileResponse: The main HTML page or API message
    """
    try:
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
    except Exception:
        pass

    return {"message": "Lead Tracking System API", "status": "running"}


@app.get("/favicon.ico")
@app.get("/favicon.png")
async def favicon():
    """
    Return 204 No Content for favicon requests to avoid errors.

    Returns:
        Response: 204 No Content response
    """
    return Response(status_code=204)


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: Status of the application
    """
    try:
        # Try to ensure database is initialized
        db.ensure_data_file_exists()
        return {"status": "healthy", "service": "lead-tracking-system"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/api/leads", response_model=List[Lead])
async def get_leads(search: Optional[str] = Query(None, description="Search by company, name, or email")):
    """
    Get all leads with optional search filtering.

    Parameters:
        search: Optional search query to filter leads

    Returns:
        List[Lead]: List of leads matching the search criteria
    """
    try:
        if search:
            leads = db.search_leads(search)
        else:
            leads = db.get_all_leads()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str):
    """
    Get a specific lead by ID.

    Parameters:
        lead_id: Unique identifier of the lead

    Returns:
        Lead: The requested lead

    Raises:
        HTTPException: If lead not found (404)
    """
    lead = db.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.post("/api/leads", response_model=LeadResponse, status_code=201)
async def create_lead(lead_data: LeadCreate):
    """
    Create a new lead with duplicate email detection warning.

    Parameters:
        lead_data: Lead information to create

    Returns:
        LeadResponse: Created lead with optional warning

    Raises:
        HTTPException: If validation fails (400) or server error (500)
    """
    try:
        # Check for duplicate email
        is_duplicate = db.check_duplicate_email(lead_data.email)
        warning = None

        if is_duplicate:
            warning = f"Warning: A lead with email {lead_data.email} already exists"

        # Create the lead
        new_lead = db.create_lead(lead_data)

        return LeadResponse(lead=new_lead, warning=warning)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/leads/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: str, lead_data: LeadUpdate):
    """
    Update an existing lead.

    Parameters:
        lead_id: ID of the lead to update
        lead_data: New lead information

    Returns:
        LeadResponse: Updated lead with optional duplicate warning

    Raises:
        HTTPException: If lead not found (404) or validation fails (400)
    """
    try:
        # Check if lead exists
        existing_lead = db.get_lead_by_id(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Check for duplicate email (excluding current lead)
        is_duplicate = db.check_duplicate_email(lead_data.email, exclude_id=lead_id)
        warning = None

        if is_duplicate:
            warning = f"Warning: Another lead with email {lead_data.email} already exists"

        # Update the lead
        updated_lead = db.update_lead(lead_id, lead_data)

        return LeadResponse(lead=updated_lead, warning=warning)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: str):
    """
    Delete a lead by ID.

    Parameters:
        lead_id: ID of the lead to delete

    Raises:
        HTTPException: If lead not found (404)
    """
    success = db.delete_lead(lead_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found")
    return Response(status_code=204)


@app.get("/api/export")
async def export_leads():
    """
    Export all leads as CSV file.

    Returns:
        Response: CSV file download
    """
    try:
        leads = db.get_all_leads()
        csv_content = utils.export_leads_to_csv(leads)

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=leads_export.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/stats")
async def get_statistics():
    """
    Get statistics about leads.

    Returns:
        dict: Statistics including total count, status breakdown, and top companies
    """
    try:
        stats = db.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tags")
async def get_all_tags():
    """
    Get all unique tags used across all leads.

    Returns:
        dict: List of all unique tags with usage count
    """
    try:
        leads = db.get_all_leads()
        tag_counts = {}

        for lead in leads:
            for tag in lead.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        tags = [
            {"name": tag, "count": count}
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Exception handler for unhandled errors
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle uncaught exceptions gracefully."""
    return Response(
        content=f'{{"error": "Internal server error: {str(exc)}}}',
        status_code=500,
        media_type="application/json"
    )


# Vercel handler
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
