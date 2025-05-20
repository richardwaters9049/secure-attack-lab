"""
schemas.py

This file contains the Pydantic models used for request validation and response formatting.
These are separate from the SQLAlchemy models and allow FastAPI to safely parse and validate
incoming and outgoing data through API endpoints.
"""

from pydantic import BaseModel
from typing import Optional


class CredentialBase(BaseModel):
    """
    This is the base schema shared between create and read models.
    It includes the basic user credential fields.
    """

    username: str
    original_password: str  # Used for simulation purposes only


class CredentialCreate(CredentialBase):
    """
    Used when a new credential entry is submitted via API (e.g., uploading test users).
    Inherits from CredentialBase and adds no new fields for now.
    """

    pass


class CredentialOut(BaseModel):
    """
    Response model for returning a user credential and result status.
    This omits the original password for security unless needed.
    """

    id: int
    username: str
    result: Optional[str] = None

    class Config:
        orm_mode = True  # This allows compatibility with SQLAlchemy ORM objects
