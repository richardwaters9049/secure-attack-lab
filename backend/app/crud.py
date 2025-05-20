"""
crud.py

This file defines functions to create and query credentials in the PostgreSQL database
using SQLAlchemy ORM. Each function handles a specific piece of logic that will be used
by our FastAPI routes to interact with the database safely and predictably.
"""

from sqlalchemy.orm import Session
from . import models, schemas
import hashlib


def hash_password_sha256(password: str) -> str:
    """
    Hash a plaintext password using SHA-256.
    NOTE: This is for educational use only. In production, use bcrypt or Argon2.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def create_credential(db: Session, credential: schemas.CredentialCreate):
    """
    Adds a new credential (test user) to the database. This includes both the original password
    and its SHA-256 hashed form, which simulates what a real system might store.
    """
    hashed = hash_password_sha256(credential.original_password)
    db_credential = models.UserCredential(
        username=credential.username,
        original_password=credential.original_password,
        hashed_password=hashed,
        result="pending",  # Initial attack result status
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


def get_credential(db: Session, credential_id: int):
    """
    Retrieve a single credential record by its ID. Useful for checking attack results.
    """
    return (
        db.query(models.UserCredential)
        .filter(models.UserCredential.id == credential_id)
        .first()
    )


def get_all_credentials(db: Session):
    """
    Return all credentials in the database. This is useful for showing results in the dashboard.
    """
    return db.query(models.UserCredential).all()


def update_result(db: Session, credential_id: int, new_result: str):
    """
    Update the attack result (e.g., 'cracked' or 'failed') for a credential after an attack run.
    """
    credential = (
        db.query(models.UserCredential)
        .filter(models.UserCredential.id == credential_id)
        .first()
    )
    if credential:
        credential.result = new_result
        db.commit()
        db.refresh(credential)
    return credential
