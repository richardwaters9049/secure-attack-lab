"""
password_cracker.py

This module contains simulated password cracking logic.
For now, it uses naive brute-force logic to attempt matches with SHA-256 hashed passwords.
Later, we will upgrade this to include AI-based mutation and learning.
"""

import hashlib
from sqlalchemy.orm import Session
from .. import crud, models

# A small dictionary of common passwords for testing purposes.
COMMON_PASSWORDS = [
    "password",
    "123456",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
    "iloveyou",
    "football",
]


def hash_password_sha256(password: str) -> str:
    """
    Hashes a given string using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def run_cracking_simulation(db: Session):
    """
    Attempts to 'crack' each credential in the database using a common dictionary list.
    Compares the hash of each dictionary password against the stored hashed password.
    If a match is found, it marks the result as 'cracked', otherwise 'failed'.
    """
    credentials = crud.get_all_credentials(db)

    for user in credentials:
        cracked = False

        for guess in COMMON_PASSWORDS:
            if hash_password_sha256(guess) == user.hashed_password:
                crud.update_result(db, user.id, "cracked")
                cracked = True
                print(f"[+] Cracked user {user.username} with password: {guess}")
                break  # Stop once we've cracked it

        if not cracked:
            crud.update_result(db, user.id, "failed")
            print(f"[-] Failed to crack user {user.username}")
