from datetime import datetime, timezone
from itertools import count

lesson_id = count(1)

def create_course(course_id, title, description):
    title = title.strip()

    if title == "":
        return None
    
    return {
        "id": course_id,
        "title": title,
        "description": description.strip(),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "lessons": []
    }



def add_lesson(course, title):]
    title = title.strip()
    if title == "":
        return None
    
    lesson = {
        "id": next(lesson_id),
        "courseId": course["id"],
        "title": title,
        "isCompleted": False,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    
    course["lessons"].append(lesson)
    return lesson

def set_lesson_completed(course, lesson_id, is_completed):
    for lesson in course["lessons"]:
        if lesson["id"] == lesson_id:
            lesson["isCompleted"] = is_completed
            return lesson
    return None

def delete_lesson(course, lesson_id):
    for lesson in course["lessons"]:
        if lesson["id"] == lesson_id:
            course["lessons"].remove(lesson)
            return lesson
    return None


def calculate_progress(course):
    total_lessons = len(course["lessons"])

    if total_lessons == 0:
        return 0
    
    completed = 0

    for lesson in course ["lessons"]:
        if lesson["isCompleted"]:
            completed += 1

    return completed / total_lessons * 100