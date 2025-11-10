"""
Utility functions for lead tracking system.

This module provides helper functions for email validation,
CSV export, and other utility operations.
"""

import csv
import io
from typing import List
from models import Lead


def export_leads_to_csv(leads: List[Lead]) -> str:
    """
    Export leads to CSV format.

    Parameters:
        leads: List of leads to export

    Returns:
        str: CSV-formatted string of all leads
    """
    output = io.StringIO()

    # Define CSV headers
    fieldnames = [
        'ID',
        'Company Name',
        'Contact Name',
        'Title',
        'Email',
        'LinkedIn URL',
        'Date Added',
        'Status',
        'Notes'
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for lead in leads:
        writer.writerow({
            'ID': lead.id,
            'Company Name': lead.company_name,
            'Contact Name': lead.contact_name,
            'Title': lead.title,
            'Email': lead.email,
            'LinkedIn URL': lead.linkedin_url,
            'Date Added': lead.date_added.strftime('%Y-%m-%d %H:%M:%S'),
            'Status': lead.status.value,
            'Notes': lead.notes
        })

    return output.getvalue()


def format_status_display(status: str) -> str:
    """
    Format status string for display.

    Parameters:
        status: Status value (e.g., 'not_contacted')

    Returns:
        str: Formatted status (e.g., 'Not Contacted')
    """
    return status.replace('_', ' ').title()
