"""
Database operations for lead management using JSON file storage.

This module handles all CRUD operations for leads, using a JSON file
as the data store with thread-safe operations.
"""

import json
import os
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from pathlib import Path

from models import Lead, LeadCreate, LeadUpdate, Activity, ActivityType


# Path to the JSON data file
DATA_DIR = Path(__file__).parent.parent / "data"
LEADS_FILE = DATA_DIR / "leads.json"


def ensure_data_file_exists() -> None:
    """
    Ensure the leads.json file exists, create with empty structure if not.

    Side Effects:
        Creates data directory and leads.json if they don't exist
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LEADS_FILE.exists():
        with open(LEADS_FILE, 'w') as f:
            json.dump({"leads": []}, f, indent=2)


def load_leads() -> List[Lead]:
    """
    Load all leads from the JSON file.

    Returns:
        List[Lead]: List of all leads in the system

    Raises:
        FileNotFoundError: If leads file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    ensure_data_file_exists()

    with open(LEADS_FILE, 'r') as f:
        data = json.load(f)

    leads = []
    for lead_data in data.get('leads', []):
        # Parse datetime strings
        if isinstance(lead_data.get('date_added'), str):
            lead_data['date_added'] = datetime.fromisoformat(
                lead_data['date_added']
            )
        if lead_data.get('last_contacted') and isinstance(lead_data.get('last_contacted'), str):
            lead_data['last_contacted'] = datetime.fromisoformat(
                lead_data['last_contacted']
            )
        
        # Parse activity history
        if 'activity_history' in lead_data:
            activities = []
            for activity_data in lead_data['activity_history']:
                if isinstance(activity_data.get('timestamp'), str):
                    activity_data['timestamp'] = datetime.fromisoformat(
                        activity_data['timestamp']
                    )
                activities.append(Activity(**activity_data))
            lead_data['activity_history'] = activities
        
        leads.append(Lead(**lead_data))

    return leads


def save_leads(leads: List[Lead]) -> None:
    """
    Save all leads to the JSON file with atomic write operation.

    Parameters:
        leads: List of leads to save

    Side Effects:
        Writes to leads.json file atomically
    """
    ensure_data_file_exists()

    # Convert leads to dictionaries
    leads_data = {
        "leads": [
            {
                **lead.model_dump(),
                "date_added": lead.date_added.isoformat(),
                "last_contacted": lead.last_contacted.isoformat() if lead.last_contacted else None,
                "activity_history": [
                    {
                        **activity.model_dump(),
                        "timestamp": activity.timestamp.isoformat()
                    }
                    for activity in lead.activity_history
                ]
            }
            for lead in leads
        ]
    }

    # Atomic write: write to temp file, then rename
    temp_file = LEADS_FILE.with_suffix('.tmp')
    try:
        with open(temp_file, 'w') as f:
            json.dump(leads_data, f, indent=2)
        temp_file.replace(LEADS_FILE)
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise e


def get_all_leads() -> List[Lead]:
    """
    Retrieve all leads.

    Returns:
        List[Lead]: All leads in the system
    """
    return load_leads()


def get_lead_by_id(lead_id: str) -> Optional[Lead]:
    """
    Retrieve a specific lead by ID.

    Parameters:
        lead_id: Unique identifier of the lead

    Returns:
        Optional[Lead]: The lead if found, None otherwise
    """
    leads = load_leads()
    for lead in leads:
        if lead.id == lead_id:
            return lead
    return None


def search_leads(query: str) -> List[Lead]:
    """
    Search leads by company name, contact name, or email.

    Parameters:
        query: Search term (case-insensitive)

    Returns:
        List[Lead]: Leads matching the search query
    """
    if not query:
        return load_leads()

    query_lower = query.lower()
    leads = load_leads()

    return [
        lead for lead in leads
        if (query_lower in lead.company_name.lower() or
            query_lower in lead.contact_name.lower() or
            query_lower in lead.email.lower())
    ]


def check_duplicate_email(email: str, exclude_id: Optional[str] = None) -> bool:
    """
    Check if an email already exists in the database.

    Parameters:
        email: Email address to check
        exclude_id: Optional lead ID to exclude from check (for updates)

    Returns:
        bool: True if email exists, False otherwise
    """
    leads = load_leads()
    email_lower = email.lower()

    for lead in leads:
        if lead.email.lower() == email_lower and lead.id != exclude_id:
            return True

    return False


def create_lead(lead_data: LeadCreate) -> Lead:
    """
    Create a new lead.

    Parameters:
        lead_data: Lead data to create

    Returns:
        Lead: The created lead with generated ID and timestamp

    Side Effects:
        Adds lead to JSON file
    """
    leads = load_leads()

    # Create initial activity
    now = datetime.now()
    initial_activity = Activity(
        timestamp=now,
        type=ActivityType.CREATED,
        description=f"Lead created for {lead_data.contact_name}",
        details=None
    )

    # Generate new lead with ID and timestamp
    new_lead = Lead(
        id=str(uuid.uuid4()),
        date_added=now,
        last_contacted=None,
        activity_history=[initial_activity],
        **lead_data.model_dump()
    )

    leads.append(new_lead)
    save_leads(leads)

    return new_lead


def update_lead(lead_id: str, lead_data: LeadUpdate) -> Optional[Lead]:
    """
    Update an existing lead.

    Parameters:
        lead_id: ID of the lead to update
        lead_data: New lead data

    Returns:
        Optional[Lead]: Updated lead if found, None otherwise

    Side Effects:
        Updates lead in JSON file
    """
    leads = load_leads()

    for i, lead in enumerate(leads):
        if lead.id == lead_id:
            now = datetime.now()
            
            # Track what changed
            activities = list(lead.activity_history)
            
            # Check for status change
            if lead_data.status != lead.status:
                activities.append(Activity(
                    timestamp=now,
                    type=ActivityType.STATUS_CHANGED,
                    description=f"Status changed from {lead.status.value} to {lead_data.status.value}",
                    details=None
                ))
                
                # Update last_contacted if status changed to contacted or responded
                if lead_data.status.value in ['contacted', 'responded']:
                    last_contacted = now
                else:
                    last_contacted = lead.last_contacted
            else:
                last_contacted = lead.last_contacted
            
            # Check for notes change
            if lead_data.notes and lead_data.notes != lead.notes:
                activities.append(Activity(
                    timestamp=now,
                    type=ActivityType.NOTE_ADDED,
                    description="Note updated",
                    details=lead_data.notes[:100]
                ))
            
            # Check for tag changes
            old_tags = set(lead.tags)
            new_tags = set(lead_data.tags)
            
            added_tags = new_tags - old_tags
            removed_tags = old_tags - new_tags
            
            for tag in added_tags:
                activities.append(Activity(
                    timestamp=now,
                    type=ActivityType.TAG_ADDED,
                    description=f"Tag added: {tag}",
                    details=None
                ))
            
            for tag in removed_tags:
                activities.append(Activity(
                    timestamp=now,
                    type=ActivityType.TAG_REMOVED,
                    description=f"Tag removed: {tag}",
                    details=None
                ))
            
            # General update activity if something changed
            if not (activities[-1:] and activities[-1].type in [ActivityType.STATUS_CHANGED, ActivityType.NOTE_ADDED, ActivityType.TAG_ADDED, ActivityType.TAG_REMOVED]):
                activities.append(Activity(
                    timestamp=now,
                    type=ActivityType.UPDATED,
                    description="Lead information updated",
                    details=None
                ))
            
            # Preserve original ID and date_added
            updated_lead = Lead(
                id=lead.id,
                date_added=lead.date_added,
                last_contacted=last_contacted,
                activity_history=activities,
                **lead_data.model_dump()
            )
            leads[i] = updated_lead
            save_leads(leads)
            return updated_lead

    return None


def delete_lead(lead_id: str) -> bool:
    """
    Delete a lead by ID.

    Parameters:
        lead_id: ID of the lead to delete

    Returns:
        bool: True if lead was deleted, False if not found

    Side Effects:
        Removes lead from JSON file
    """
    leads = load_leads()
    initial_count = len(leads)

    leads = [lead for lead in leads if lead.id != lead_id]

    if len(leads) < initial_count:
        save_leads(leads)
        return True

    return False


def get_stats() -> Dict:
    """
    Get statistics about leads.

    Returns:
        Dict: Statistics including total count, status breakdown, and company counts
    """
    leads = load_leads()

    # Count by status
    status_counts = {
        "not_contacted": 0,
        "contacted": 0,
        "responded": 0
    }

    # Count by company
    company_counts = {}

    for lead in leads:
        status_counts[lead.status.value] += 1
        company_counts[lead.company_name] = company_counts.get(
            lead.company_name, 0
        ) + 1

    # Get top 5 companies
    top_companies = sorted(
        company_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return {
        "total": len(leads),
        "by_status": status_counts,
        "top_companies": [
            {"company": company, "count": count}
            for company, count in top_companies
        ]
    }
