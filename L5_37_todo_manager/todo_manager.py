"""Manage tasks, persist them as JSON, and demonstrate common operations."""

import json
import secrets
import smtplib
from datetime import datetime
from email.message import EmailMessage

TASKS = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(title, priority="medium", labels=None):
    """Add a task with independent labels and return its unique integer ID."""
    if priority not in PRIORITY_ORDER:
        raise ValueError("Priority must be high, medium, or low")
    task_id = max(TASKS, default=0) + 1
    task_labels = list(labels) if labels is not None else []
    task_labels.append(priority)
    TASKS[task_id] = {
        "title": title, "priority": priority, "done": False,
        "created": datetime.now().isoformat(), "labels": task_labels,
    }
    return task_id


def complete_task(task_id):
    """Mark an existing task complete and report whether it was found."""
    if task_id in TASKS:
        TASKS[task_id]["done"] = True
        return True
    print("No task with id", task_id)
    return False


def pending_tasks():
    """Return pending task titles ordered from high to low priority."""
    pending = [task for task in TASKS.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword):
    """Return the first matching task ID, or None when no title matches."""
    for task_id, task in TASKS.items():
        if keyword.lower() in task["title"].lower():
            return task_id
    return None


def save_tasks(file_name="tasks.json"):
    """Save tasks as UTF-8 JSON without executable serialization."""
    with open(file_name, "w", encoding="utf-8") as task_file:
        json.dump(TASKS, task_file, indent=2)


def load_tasks(file_name="tasks.json"):
    """Read saved tasks and restore integer keys in the returned mapping."""
    with open(file_name, encoding="utf-8") as task_file:
        saved_tasks = json.load(task_file)
    return {int(task_id): task for task_id, task in saved_tasks.items()}


def export_json(file_name="tasks.json"):
    """Export the current tasks to a JSON file."""
    save_tasks(file_name)


def remind_by_email(address, host="localhost", port=25):
    """Send tasks through a configured local SMTP relay without a shell."""
    message = EmailMessage()
    message["Subject"] = "Pending tasks"
    message["From"] = "todo-manager@localhost"
    message["To"] = address
    message.set_content(json.dumps(TASKS, indent=2))
    with smtplib.SMTP(host, port, timeout=10) as server:
        server.send_message(message)


def main():
    """Run a short task-manager demonstration."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)
    pending = pending_tasks()
    print("Pending tasks:", pending)
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))
    suggestion = secrets.choice(pending) if pending else "No pending tasks"
    print("Try this next:", suggestion)
    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))
    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
