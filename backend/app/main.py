"""
main.py

This is the entry point of the FastAPI backend for our credential attack simulator.
It includes:
- Application startup
- API endpoints to add credentials
- List all credentials and their status
- Trigger a password cracking simulation
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Import internal modules
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .utils.password_cracker import run_cracking_simulation

# Load environment variables from .env file
load_dotenv()

# Create database tables (only runs if they don't already exist)
Base.metadata.create_all(bind=engine)

# Initialise the FastAPI app
app = FastAPI(
    title="Credential Attack Lab API",
    description="Backend for ethical password attack simulation platform",
    version="1.0.0",
)

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency function to get database session
def get_db():
    """
    FastAPI dependency that yields a DB session per request.
    Ensures the session is properly closed after the request is handled.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    Root route — used to verify the backend is live.
    """
    return {"message": "Credential Attack Simulator API is running."}


@app.post("/credentials/", response_model=schemas.CredentialOut)
def create_credential(cred: schemas.CredentialCreate, db: Session = Depends(get_db)):
    """
    Add a new test credential to the database.
    Requires a username and original (plaintext) password.
    """
    return crud.create_credential(db=db, credential=cred)


@app.get("/credentials/", response_model=list[schemas.CredentialOut])
def get_all_credentials(db: Session = Depends(get_db)):
    """
    Retrieve all stored credentials and their attack result status.
    Useful for showing in the dashboard.
    """
    return crud.get_all_credentials(db)


@app.post("/simulate/")
def simulate_attack(db: Session = Depends(get_db)):
    """
    Trigger the password cracking simulation.
    Runs through all stored credentials using the naive brute-force method.
    """
    run_cracking_simulation(db)
    return {"message": "Simulation complete. Check results."}
