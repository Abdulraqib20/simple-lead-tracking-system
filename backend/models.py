"""
Lead data models with validation.

This module defines the Pydantic models for lead management,
including validation rules and data structures.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re


class ActivityType(str, Enum):
    """
    Enumeration of activity types for lead history.

    Attributes:
        CREATED: Lead was created
        UPDATED: Lead information was updated
        STATUS_CHANGED: Lead status was changed
        NOTE_ADDED: Note was added
        TAG_ADDED: Tag was added
        TAG_REMOVED: Tag was removed
    """
    CREATED = "created"
    UPDATED = "updated"
    STATUS_CHANGED = "status_changed"
    NOTE_ADDED = "note_added"
    TAG_ADDED = "tag_added"
    TAG_REMOVED = "tag_removed"


class Activity(BaseModel):
    """
    Activity log entry for lead history.

    Attributes:
        timestamp: When the activity occurred
        type: Type of activity
        description: Human-readable description
        details: Optional additional details
    """
    timestamp: datetime
    type: ActivityType
    description: str
    details: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LeadStatus(str, Enum):
    """
    Enumeration of possible lead statuses.

    Attributes:
        NOT_CONTACTED: Lead has not been contacted yet
        CONTACTED: Lead has been contacted but not responded
        RESPONDED: Lead has responded to contact
    """
    NOT_CONTACTED = "not_contacted"
    CONTACTED = "contacted"
    RESPONDED = "responded"


class LeadBase(BaseModel):
    """
    Base model for lead data with validation.

    Attributes:
        company_name: Name of the company
        contact_name: Name of the contact person
        title: Job title of the contact
        email: Email address (must match name@company.com format)
        linkedin_url: Optional LinkedIn profile URL
        status: Current status of the lead
        notes: Optional notes about the lead
        tags: List of tags/labels for categorization
    """
    company_name: str = Field(..., min_length=1, max_length=200)
    contact_name: str = Field(..., min_length=1, max_length=200)
    title: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., min_length=5, max_length=200)
    linkedin_url: Optional[str] = Field(default="", max_length=500)
    status: LeadStatus = Field(default=LeadStatus.NOT_CONTACTED)
    notes: Optional[str] = Field(default="", max_length=2000)
    tags: List[str] = Field(default_factory=list)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """
        Validate email format to match name@company.com pattern.

        Parameters:
            v: Email string to validate

        Returns:
            str: Validated email string

        Raises:
            ValueError: If email format is invalid
        """
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError(
                'Email must be in format name@company.com'
            )
        return v.lower()

    @field_validator('linkedin_url')
    @classmethod
    def validate_linkedin_url(cls, v: Optional[str]) -> str:
        """
        Validate LinkedIn URL format if provided.

        Parameters:
            v: LinkedIn URL to validate

        Returns:
            str: Validated URL or empty string
        """
        if v and v.strip():
            v = v.strip()
            if not (v.startswith('http://') or v.startswith('https://')):
                v = 'https://' + v
            return v
        return ""


class LeadCreate(LeadBase):
    """Model for creating a new lead."""
    pass


class LeadUpdate(LeadBase):
    """Model for updating an existing lead."""
    pass


class Lead(LeadBase):
    """
    Complete lead model with system-generated fields.

    Attributes:
        id: Unique identifier for the lead
        date_added: Timestamp when the lead was added
        last_contacted: Timestamp of last contact
        activity_history: List of all activities for this lead
    """
    id: str
    date_added: datetime
    last_contacted: Optional[datetime] = None
    activity_history: List[Activity] = Field(default_factory=list)

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LeadResponse(BaseModel):
    """
    Response model for lead operations with optional warnings.

    Attributes:
        lead: The lead data
        warning: Optional warning message (e.g., duplicate email)
    """
    lead: Lead
    warning: Optional[str] = None
