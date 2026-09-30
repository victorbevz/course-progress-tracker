# Course Progress Tracker

Track courses and lessons in a simple web app. Add lessons, mark them complete, and see progress update instantly.

**Python · FastAPI · PostgreSQL · JavaScript · Docker Compose**

> A live demo and screenshot will be added after deployment.

## What it does

- Create and delete courses.
- Add and delete lessons within a course.
- Mark lessons complete or incomplete.
- Show each course's completion percentage.
- Keep data across restarts in PostgreSQL.

## Run locally

Install Docker Desktop, then run:

```bash
docker compose up --build
```

Open the [app](http://localhost:4000/app/) or the [API docs](http://localhost:4000/docs). The database uses a Docker volume, so normal container restarts keep your data. `docker compose down -v` removes the volume and its data.

## How it works

```text
Browser (HTML, CSS, JavaScript)
          ↓ HTTP
FastAPI (Python)
          ↓ SQL via psycopg
PostgreSQL (courses, lessons)
```

The browser calls the REST API. The API validates requests and reads or writes the database. Each lesson belongs to a course; deleting a course also deletes its lessons. Docker Compose runs the backend and database together.

## API

| Method | Endpoint | Action |
| --- | --- | --- |
| GET | `/courses` | List courses with lessons and progress |
| POST | `/courses` | Create a course |
| GET | `/courses/{course_id}` | Get one course |
| DELETE | `/courses/{course_id}` | Delete a course |
| GET | `/courses/{course_id}/lessons` | List lessons |
| POST | `/courses/{course_id}/lessons` | Add a lesson |
| PATCH | `/lessons/{lesson_id}` | Set completion status |
| DELETE | `/lessons/{lesson_id}` | Delete a lesson |

