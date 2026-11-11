
import json
import os
from datetime import datetime

FILE_NAME = "tasks.txt"

# Load tasks from file
def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError):
            return []
    return []


# Save tasks to file
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# Generate unique task ID
def generate_id():
    if not tasks:
        return "T101"

    numbers = [
        int(task["id"][1:])
        for task in tasks
    ]

    return "T" + str(max(numbers) + 1)


# Add new task
def add_task():
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    priority = input(
        "Enter priority (High/Medium/Low): "
    ).strip().capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("Invalid priority. Enter High, Medium or Low.")
        return

    due_date = input(
        "Enter due date (YYYY-MM-DD): "
    ).strip()

    try:
        date = datetime.strptime(due_date, "%Y-%m-%d")

        if date.strftime("%Y-%m-%d") != due_date:
            raise ValueError

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    task = {
        "id": generate_id(),
        "title": title,
        "priority": priority,
        "due": due_date,
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks()

    print("Task added.")
    print(
        task["id"], "|",
        task["title"], "|",
        task["priority"], "|",
        task["due"], "|",
        task["status"]
    )


# View tasks by priority
def view_by_priority():
    if not tasks:
        print("No tasks available.")
        return

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    sorted_tasks = sorted(
        tasks,
        key=lambda x: priority_order[x["priority"]]
    )

    for task in sorted_tasks:
        print(
            task["id"], "|",
            task["title"], "|",
            task["priority"], "|",
            task["due"], "|",
            task["status"]
        )


# Show pending tasks
def show_pending():
    pending_tasks = [
        task for task in tasks
        if task["status"] == "Pending"
    ]

    if not pending_tasks:
        print("No pending tasks. You are all caught up!")
        return

    for task in pending_tasks:
        print(
            task["id"], "|",
            task["title"], "|",
            task["priority"], "|",
            task["due"], "|",
            task["status"]
        )


# Complete a task
def complete_task():
    task_id = input("Enter Task ID: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:

            if task["status"] == "Done":
                print("Task is already completed.")
                return

            task["status"] = "Done"
            save_tasks()

            pending_count = sum(
                1 for t in tasks
                if t["status"] == "Pending"
            )

            print(
                f"Task {task_id} marked as done. "
                f"Pending tasks: {pending_count}"
            )
            return

    print(f"Task {task_id} not found.")


# Main program
tasks = load_tasks()

while True:
    print("\n===== DAILY TASK MANAGER =====")
    print("1. Add Task")
    print("2. View by Priority")
    print("3. Show Pending")
    print("4. Complete Task")
    print("5. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_task()

    elif choice == "2":
        view_by_priority()

    elif choice == "3":
        show_pending()

    elif choice == "4":
        complete_task()

    elif choice == "5":
        print("Thank you for using Daily Task Manager!")
        break

    else:
        print("Invalid choice. Please select 1 to 5.")
