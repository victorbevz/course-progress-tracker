from course_service import (
    create_course,
    add_lesson,
    set_lesson_completed,
    delete_lesson,
    calculate_progress
)


def show_lessons(course):
    if not course["lessons"]:
        print("No lessons yet")
        return

    for lesson in course["lessons"]:
        if lesson["isCompleted"]:
            status = "Completed"
        else:
            status = "Not completed"

        print(f"{lesson['id']}. {lesson['title']} - {status}")

def main():
    course_title = input("Enter course title: ")
    course_description = input("Enter course description: ")

    course = create_course(1, course_title, course_description)
    if course is None:
        print("Course title is required")
        raise SystemExit

    print("Course created: ", course["title"])

    while True:
        title = input("Enter the lesson title (or 'done' to finish): ")

        if title.strip().lower() == "done":
            break

        new_lesson = add_lesson(course, title)

        if new_lesson is None:
            print("Lesson title is required")
        else:
            print("Lesson added: ", new_lesson["id"], new_lesson["title"])

    while True:
        show_lessons(course)

        value = input("Enter lesson ID (or 'done' to finish): ").strip()

        if value.lower() == "done":
            break

        try:
            lesson_id = int(value)
        except ValueError:
            print("Please enter a whole number")
            continue

        action = input("Choose an action (yes/no/delete): ").strip().lower()

        if action == "delete":
            deleted_lesson = delete_lesson(course, lesson_id)

            if deleted_lesson is None:
                print("Lesson not found")
            else:
                print("Lesson deleted: ", deleted_lesson["title"])
        
        elif action in ("yes", "no"):
            updated_lesson = set_lesson_completed(
                course, lesson_id, action == "yes"
            )    

            if updated_lesson is None:
                print("Lesson not found")
            else:
                print("Lesson updated: ", updated_lesson["title"])
        else:
            print("Please enter yes, no or delete")
            continue
        progress = calculate_progress(course)
        print(f"Course progress: {progress:.1f}%")
if __name__ == "__main__":
    main()
