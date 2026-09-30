from psycopg.rows import dict_row
from database import get_connection

def select_lessons(course_id):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    course_id as "courseId",
                    title,
                    is_completed as "isCompleted",
                    created_at AS "createdAt"
                FROM lessons
                WHERE course_id = %s
                ORDER BY id
                """,
                (course_id,)
            )

            return cursor.fetchall()

def insert_lesson(course_id, title):
    title = title.strip()

    if title == "":
        return None

    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO lessons (course_id, title)
                VALUES (%s, %s)
                RETURNING
                    id, 
                    course_id AS "courseId",
                    title,
                    is_completed AS "isCompleted",
                    created_at AS "createdAt"
                """,
                (course_id, title)
            )

            return cursor.fetchone()

def update_lesson_status(lesson_id, is_completed):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                UPDATE lessons
                SET is_completed = %s
                WHERE id = %s
                RETURNING
                    id,
                    course_id AS "courseId",
                    title,
                    is_completed AS "isCompleted",
                    created_at AS "createdAt"
                """,
                (is_completed, lesson_id)
            )

            return cursor.fetchone()

def delete_lesson_by_id(lesson_id):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                DELETE FROM lessons
                WHERE id = %s
                RETURNING id
                """,
                (lesson_id,)
            )

            return cursor.fetchone()