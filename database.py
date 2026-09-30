import psycopg
import os

def get_connection():
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/courses_db"
    )

    return psycopg.connect(database_url, connect_timeout=5)

def create_tables():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses(
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    description TEXT NOT NULL DEFAULT '',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lessons(
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

if __name__ == "__main__":
    create_tables()
    print("Tables created")