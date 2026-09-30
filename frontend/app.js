const courseList = document.getElementById("course-list");
const message = document.getElementById("message");
const courseForm = document.getElementById("course-form");
const refreshButton = document.getElementById("refresh-button");

function showMessage(text, isError = false) {
    message.textContent = text;
    message.classList.toggle("error", isError);
}

async function request(url, options) {
    const response = await fetch(url, options);
    if (response.ok) {
        return response.status === 204 ? null : response.json();
    }
    let detail;
    try {
        const body = await response.json();
        detail = typeof body.detail === "string" ? body.detail : null;
    } catch {
        // An error response may not contain JSON.
    }
    throw new Error(detail || `Request failed (${response.status})`);
}

function makeButton(label, className, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.className = className;
    button.addEventListener("click", onClick);
    return button;
}

async function runAction(action, successText) {
    showMessage("Working...");
    try {
        await action();
        await loadCourses();
        showMessage(successText);
        return true;
    } catch (error) {
        showMessage(error.message || "Something went wrong", true);
        return false;
    }
}

function renderLesson(lesson) {
    const row = document.createElement("li");
    row.className = "lesson";
    const label = document.createElement("label");
    label.className = "lesson-label";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = lesson.isCompleted;
    checkbox.setAttribute("aria-label", `Mark ${lesson.title} as completed`);
    const title = document.createElement("span");
    title.textContent = lesson.title;
    label.append(checkbox, title);

    checkbox.addEventListener("change", async () => {
        checkbox.disabled = true;
        const completed = checkbox.checked;
        const success = await runAction(
            () => request(`/lessons/${lesson.id}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ isCompleted: completed })
            }),
            "Lesson updated"
        );
        if (!success) checkbox.checked = !completed;
        checkbox.disabled = false;
    });

    const remove = makeButton("Delete", "danger small", async () => {
        remove.disabled = true;
        await runAction(
            () => request(`/lessons/${lesson.id}`, { method: "DELETE" }),
            "Lesson deleted"
        );
        remove.disabled = false;
    });
    row.append(label, remove);
    return row;
}

function renderCourse(course) {
    const card = document.createElement("article");
    card.className = "course-card";
    const heading = document.createElement("div");
    heading.className = "course-heading";
    const title = document.createElement("h3");
    title.textContent = course.title;
    const remove = makeButton("Delete course", "danger small", async () => {
        if (!window.confirm(`Delete "${course.title}" and all its lessons?`)) return;
        remove.disabled = true;
        await runAction(
            () => request(`/courses/${course.id}`, { method: "DELETE" }),
            "Course deleted"
        );
        remove.disabled = false;
    });
    heading.append(title, remove);
    card.append(heading);

    if (course.description) {
        const description = document.createElement("p");
        description.className = "description";
        description.textContent = course.description;
        card.append(description);
    }

    const progressText = document.createElement("p");
    progressText.className = "progress-text";
    progressText.textContent = `Progress: ${course.progress.toFixed(1)}%`;
    const progress = document.createElement("progress");
    progress.max = 100;
    progress.value = course.progress;
    progress.setAttribute("aria-label", `${course.title} progress`);
    card.append(progressText, progress);

    const lessonHeading = document.createElement("h4");
    lessonHeading.textContent = "Lessons";
    card.append(lessonHeading);
    if (course.lessons.length === 0) {
        const empty = document.createElement("p");
        empty.className = "description";
        empty.textContent = "No lessons yet";
        card.append(empty);
    } else {
        const list = document.createElement("ul");
        list.className = "lesson-list";
        for (const lesson of course.lessons) list.append(renderLesson(lesson));
        card.append(list);
    }

    const form = document.createElement("form");
    form.className = "lesson-form";
    const input = document.createElement("input");
    input.type = "text";
    input.required = true;
    input.maxLength = 200;
    input.placeholder = "New lesson title";
    input.setAttribute("aria-label", `New lesson for ${course.title}`);
    const submit = document.createElement("button");
    submit.type = "submit";
    submit.textContent = "Add lesson";
    form.append(input, submit);
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        submit.disabled = true;
        await runAction(
            () => request(`/courses/${course.id}/lessons`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: input.value.trim() })
            }),
            "Lesson added"
        );
        submit.disabled = false;
    });
    card.append(form);
    return card;
}

async function loadCourses() {
    showMessage("Loading courses...");
    try {
        const courses = await request("/courses");
        courseList.replaceChildren();
        for (const course of courses) courseList.append(renderCourse(course));
        showMessage(courses.length === 0 ? "No courses yet" : "");
    } catch (error) {
        showMessage(error.message || "Failed to load courses", true);
        throw error;
    }
}

courseForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = courseForm.querySelector('button[type="submit"]');
    submit.disabled = true;
    const success = await runAction(
        () => request("/courses", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: document.getElementById("course-title").value.trim(),
                description: document.getElementById("course-description").value.trim()
            })
        }),
        "Course created"
    );
    submit.disabled = false;
    if (success) courseForm.reset();
});

refreshButton.addEventListener("click", () => {
    loadCourses().catch(() => {});
});

loadCourses().catch(() => {});
