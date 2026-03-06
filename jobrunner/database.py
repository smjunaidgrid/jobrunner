import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path(".jobrunner/jobs.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        name TEXT,
        status TEXT,
        created_at TEXT,
        completed_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS steps (
        id TEXT PRIMARY KEY,
        job_id TEXT,
        name TEXT,
        command TEXT,
        status TEXT,
        retry_count INTEGER,
        max_retries INTEGER,
        started_at TEXT,
        completed_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_job(name):
    conn = get_connection()
    cursor = conn.cursor()

    job_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO jobs (id, name, status, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (job_id, name, "pending", datetime.utcnow().isoformat()),
    )

    conn.commit()
    conn.close()

    return job_id


def create_steps(job_id, steps):
    conn = get_connection()
    cursor = conn.cursor()

    for step in steps:
        step_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO steps
            (id, job_id, name, command, status, retry_count, max_retries)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                step_id,
                job_id,
                step["name"],
                step["command"],
                "pending",
                0,
                step["retry"],
            ),
        )

    conn.commit()
    conn.close()