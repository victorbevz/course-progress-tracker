from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StrictBool
from fastapi.staticfiles import StaticFiles
from course_repository import (
    select_course,
    insert_course,
    select_courses,
    delete_course_by_id,
)
from lesson_repository import (
    select_lessons, 
    insert_lesson, 
    update_lesson_status, 
    delete_lesson_by_id,
)
from course_service import calculate_progress
class CourseCreate(BaseModel):
    title: str
    description: str = ""

class LessonCreate(BaseModel):
    title: str
class LessonUpdate(BaseModel):
    isCompleted: StrictBool

app = FastAPI()

app.mount(
    "/app",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)

@app.get("/")
def home():
    return {"message": "Course Tracker API"}

@app.get("/courses")
def get_courses():
    courses_data = select_courses()

    for course in courses_data:
        course["lessons"] = select_lessons(course["id"])
        course["progress"] = calculate_progress(course)

    return courses_data

@app.post("/courses", status_code=201)
def add_course(data: CourseCreate):
    course = insert_course(data.title, data.description)

    if course is None:
        raise HTTPException(
            status_code=400,
            detail="Course title is required"
        )

    return course

@app.post("/courses/{course_id}/lessons", status_code=201)
def create_lesson(course_id: int, data: LessonCreate):
    course = select_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    lesson = insert_lesson(course_id, data.title)

    if lesson is None:
        raise HTTPException(
            status_code=400,
            detail="Lesson title is required"
        )

    return lesson

@app.patch("/lessons/{lesson_id}")
def update_lesson(lesson_id: int, data: LessonUpdate):
    lesson = update_lesson_status(lesson_id, data.isCompleted)

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson

@app.delete("/lessons/{lesson_id}")
def remove_lesson(lesson_id: int):
    lesson = delete_lesson_by_id(lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {"message": "Lesson deleted"}

@app.delete("/courses/{course_id}")
def remove_course(course_id: int):
    course = delete_course_by_id(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {"message": "Course deleted"}

@app.get("/courses/{course_id}/lessons")
def get_lessons(course_id: int):
    course = select_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return select_lessons(course_id)

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    course = select_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course
