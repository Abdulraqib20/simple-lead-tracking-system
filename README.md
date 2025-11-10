# Lead Tracking System

A simple, lightweight lead management system built with FastAPI and vanilla JavaScript. Perfect for tracking sales leads, networking contacts, or customer prospects locally without requiring a database setup.

## Features

- **Complete CRUD Operations**: Create, read, update, and delete leads
- **Tags & Labels System**: Categorize leads with custom tags for better organization
- **Activity Timeline**: Track complete history of all lead interactions and changes
- **Smart Search**: Real-time search across company names, contact names, and emails
- **Duplicate Detection**: Warns when adding leads with existing email addresses
- **Sortable Data**: Sort leads by company name or date added
- **Quick Statistics**: View total leads and breakdown by status
- **CSV Export**: Export all leads to CSV format
- **Email Validation**: Strict email format validation (name@company.com)
- **Quick Copy**: Click any email to copy it to clipboard
- **Keyboard Shortcuts**: Press Ctrl+N (Cmd+N on Mac) to add a new lead
- **Dark Mode Support**: Seamless dark/light theme integration
- **Clean UI**: Modern, responsive design with Tailwind CSS
- **JSON Storage**: Simple file-based storage - no database required

## Project Structure

```
lead-tracking-system/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── models.py            # Pydantic models for data validation
│   ├── database.py          # JSON file operations and CRUD functions
│   └── utils.py             # Helper functions (CSV export, etc.)
├── frontend/
│   └── index.html           # Single-page application with Tailwind CSS
├── data/
│   └── leads.json           # Lead storage (auto-created with sample data)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd lead-tracking-system
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI server**
   ```bash
   python backend/main.py
   ```

   Or alternatively:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

2. **Open your browser**
   Navigate to: `http://localhost:8000`

3. **Start managing leads!**

## Usage Guide

### Adding a New Lead

1. Click the **"+ Add Lead"** button in the top right, or press **Ctrl+N** (Cmd+N on Mac)
2. Fill in the required fields:
   - Company Name
   - Contact Name
   - Title
   - Email (must be in format: name@company.com)
3. Optionally add:
   - LinkedIn URL
   - Status (Not Contacted, Contacted, or Responded)
   - Tags (click "Add Tag" or press Enter to add multiple tags)
   - Notes
4. Click **"Save Lead"**

If the email already exists, you'll see a warning but the lead will still be added.

### Managing Tags

Tags help you categorize and organize your leads:
- Add tags when creating or editing a lead
- Type a tag name and press Enter or click "Add Tag"
- Remove tags by clicking the X button on any tag
- Common tag examples: "Hot Lead", "Follow-up", "Technical", "Conference"

### Viewing Activity Timeline

Each lead maintains a complete history of all interactions:
- Click **"View Activity Timeline"** button on any lead card
- See chronological list of all activities:
  - Lead creation
  - Status changes
  - Notes added
  - Tags added/removed
  - General updates
- Each activity shows timestamp and description

### Searching for Leads

Simply type in the search bar to filter leads by:
- Company name
- Contact name
- Email address

Results update in real-time as you type.

### Editing a Lead

1. Click the **"Edit"** button next to any lead
2. Modify the fields as needed
3. Click **"Save Lead"**

### Deleting a Lead

1. Click the **"Delete"** button next to any lead
2. Confirm the deletion in the popup dialog

### Copying Email Addresses

Click on any email address in the table to copy it to your clipboard. A confirmation message will appear briefly.

### Sorting Leads

Click on the **"Company"** or **"Date Added"** column headers to sort:
- First click: Sort ascending
- Second click: Sort descending
- Third click: Return to original order

### Exporting to CSV

Click the **"Export to CSV"** button to download all leads as a CSV file. The file will be named with the current date (e.g., `leads_export_2025-11-10.csv`).

### Understanding Lead Status

- **Not Contacted** (Gray badge): Lead has not been reached out to yet
- **Contacted** (Blue badge): Initial contact has been made, awaiting response
- **Responded** (Green badge): Lead has responded to outreach

## API Documentation

The backend provides a RESTful API at `http://localhost:8000/api`:

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leads` | Get all leads (optional `?search=` param) |
| GET | `/api/leads/{id}` | Get a specific lead by ID |
| POST | `/api/leads` | Create a new lead |
| PUT | `/api/leads/{id}` | Update an existing lead |
| DELETE | `/api/leads/{id}` | Delete a lead |
| GET | `/api/export` | Export all leads as CSV |
| GET | `/api/stats` | Get lead statistics |
| GET | `/api/tags` | Get all unique tags with usage counts |

### Example API Calls

**Get all leads:**
```bash
curl http://localhost:8000/api/leads
```

**Search for leads:**
```bash
curl "http://localhost:8000/api/leads?search=TechCorp"
```

**Add a new lead:**
```bash
curl -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "NewCorp",
    "contact_name": "Jane Doe",
    "title": "CEO",
    "email": "jane.doe@newcorp.com",
    "status": "not_contacted",
    "notes": "Met at tech conference"
  }'
```

**Update a lead:**
```bash
curl -X PUT http://localhost:8000/api/leads/{lead_id} \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "NewCorp",
    "contact_name": "Jane Doe",
    "title": "CEO",
    "email": "jane.doe@newcorp.com",
    "status": "contacted",
    "notes": "Follow-up scheduled"
  }'
```

**Delete a lead:**
```bash
curl -X DELETE http://localhost:8000/api/leads/{lead_id}
```

## Data Structure

Each lead contains the following fields:

```json
{
  "id": "unique-uuid",
  "company_name": "TechCorp",
  "contact_name": "John Smith",
  "title": "CTO",
  "email": "john.smith@techcorp.com",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "date_added": "2025-11-01T10:00:00",
  "last_contacted": "2025-11-10T14:30:00",
  "status": "responded",
  "notes": "Interested in Q1 2026 partnership",
  "tags": ["Hot Lead", "Technical", "Follow-up"],
  "activity_history": [
    {
      "timestamp": "2025-11-01T10:00:00",
      "type": "created",
      "description": "Lead created for John Smith",
      "details": null
    },
    {
      "timestamp": "2025-11-10T14:30:00",
      "type": "status_changed",
      "description": "Status changed from not_contacted to contacted",
      "details": null
    }
  ]
}
```

### Field Descriptions

- **id**: Auto-generated UUID
- **company_name**: Name of the company (required)
- **contact_name**: Name of the contact person (required)
- **title**: Job title of the contact (required)
- **email**: Email address in name@company.com format (required)
- **linkedin_url**: LinkedIn profile URL (optional)
- **date_added**: Timestamp when lead was added (auto-generated)
- **last_contacted**: Timestamp of last contact (auto-updated)
- **status**: One of: `not_contacted`, `contacted`, `responded`
- **notes**: Free-form notes about the lead (optional)
- **tags**: Array of tag strings for categorization
- **activity_history**: Array of activity objects tracking all changes

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N (Cmd+N on Mac) | Open "Add New Lead" modal |
| Esc | Close modal (when modal is open) |

## Customization

### Changing the Port

Edit `backend/main.py`, line 228:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to your desired port
```

### Modifying Sample Data

Edit `data/leads.json` to add, modify, or remove sample leads.

### Styling Changes

The frontend uses Tailwind CSS via CDN. To customize styles, edit the classes in `frontend/index.html` or add custom CSS in the `<style>` tag.

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or run on a different port
uvicorn backend.main:app --reload --port 8001
```

### Dependencies Not Installing

Make sure you're using Python 3.8+:
```bash
python --version
```

Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Leads Not Saving

Check that the `data` directory exists and `leads.json` is writable:
```bash
ls -la data/leads.json
```

The application will auto-create the file if it doesn't exist.

## Development

### Running in Development Mode

```bash
uvicorn backend.main:app --reload --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### API Documentation

When the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security Notes

This application is designed for **local, single-user use only**. It does not include:
- User authentication
- API rate limiting
- CSRF protection
- Input sanitization beyond basic validation

**Do not expose this application to the internet without adding proper security measures.**

## License

This project is provided as-is for personal and educational use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the API documentation at `/docs`
3. Ensure all dependencies are correctly installed

## Future Enhancements

Potential features to add:
- User authentication
- Multiple status workflows
- Custom fields
- Email templates
- Integration with CRM systems
- Advanced filtering and reporting
- Mobile app
- Tag-based filtering
- Export with activity history

---

**Built with FastAPI, Tailwind CSS, and vanilla JavaScript.**

## Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically detect the `vercel.json` configuration
4. Deploy with a single click

Note: For production use, consider migrating from JSON file storage to a proper database (PostgreSQL, MongoDB, etc.).
