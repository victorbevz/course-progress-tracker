from psycopg.rows import dict_row
from database import get_connection


def  insert_course(title, description):
    title = title.strip()

    if title == "":
        return None


    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO courses (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, created_at AS "createdAt"
                """,
                (title, description.strip())
            )
            return cursor.fetchone()


def select_courses():
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, title, description, created_at AS "createdAt"
                FROM courses
                ORDER BY id
                """
            )
            return cursor.fetchall()


def select_course(course_id):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, title, description, created_at AS "createdAt"
                FROM courses
                WHERE id = %s
                """,
                (course_id,)
            )
            return cursor.fetchone()

def delete_course_by_id(course_id):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                DELETE FROM courses
                WHERE id = %s
                RETURNING id
                """,
                (course_id,)
            )

            return cursor.fetchone()