import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
                """
            )

            cur.execute("SELECT COUNT(*) FROM tasks")
            count = cur.fetchone()[0]

            if count == 0:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn FastAPI with PostgreSQL", False),
                        ("Build the FlyRank A3 API", False),
                        ("Containerize the application", False),
                    ],
                )

        conn.commit()


def list_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            )
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2],
        }
        for row in rows
    ]


def get_task(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            )
            row = cur.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2],
    }


def create_task(title, done=False):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (title, done),
            )
            row = cur.fetchone()

        conn.commit()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2],
    }