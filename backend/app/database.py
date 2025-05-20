import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env variables
load_dotenv()

# Pull in environment values
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST = os.getenv("PGHOST")
PGDATABASE = os.getenv("PGDATABASE")
PGPORT = os.getenv("PGPORT")

# ✅ Validate that port is a valid integer, fallback to 5432 if needed
try:
    PGPORT = int(PGPORT)
except (ValueError, TypeError):
    raise ValueError("PGPORT environment variable must be a valid integer.")

# Build database URL
DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

# Connect to DB
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
