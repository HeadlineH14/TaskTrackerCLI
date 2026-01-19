import json
import os
from datetime import datetime

# Valid status options (choose tokens without spaces to make input simpler)
VALID_STATUSES = ["todo", "inprogress", "done"]

# File where tasks are stored
TASKS_FILE = "Task_List.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        # create empty file
        save_tasks([])
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def list_tasks():
    return load_tasks()


def add(task_description, task_status):
    if task_status not in VALID_STATUSES:
        print(f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}")
        return
    tasks = load_tasks()
    new_id = 1 if not tasks else max(t.get("ID", 0) for t in tasks) + 1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task = {
        "ID": new_id,
        "Description": task_description,
        "Status": task_status,
        "Created At": now,
        "Updated At": ""
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added:", task)


def update(task_id, new_description=None, new_status=None):
    tasks = load_tasks()
    for task in tasks:
        if task.get("ID") == task_id:
            if new_status and new_status not in VALID_STATUSES:
                print(f"Invalid status. Allowed values: {', '.join(VALID_STATUSES)}")
                return
            if new_description:
                task["Description"] = new_description
            if new_status:
                task["Status"] = new_status
            task["Updated At"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_tasks(tasks)
            print("Task updated:", task)
            return
    print(f"Task with ID {task_id} not found.")


def delete(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task.get("ID") != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found.")
    
    save_tasks(new_tasks)
    print(f"Task with ID {task_id} deleted.")
    


def print_task(task):
    print("-" * 40)
    for k, v in task.items():
        print(f"{k}: {v}")


def main_loop():
    while True:
        userInput = input("Enter command (list, add, update, delete, exit): ")
        if userInput == "exit":
            break

        elif userInput == "list":
            tasks = list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    print_task(task)

        elif userInput == "add":
            task_description = input("Enter task description: ")
            while True:
                task_status = input(f"Enter task status ({', '.join(VALID_STATUSES)}): ")
                if task_status in VALID_STATUSES:
                    break
                print(f"Invalid status. Please enter one of: {', '.join(VALID_STATUSES)}")
            add(task_description, task_status)

        elif userInput == "update":
            try:
                task_id = int(input("Enter task ID to update: "))
            except ValueError:
                print("Invalid ID")
                continue
            new_description = input("Enter new description (leave blank to keep current): ")
            while True:
                new_status = input(f"Enter new status (leave blank to keep current, or {', '.join(VALID_STATUSES)}): ")
                if new_status == "" or new_status in VALID_STATUSES:
                    break
                print(f"Invalid status. Please enter one of: {', '.join(VALID_STATUSES)}")
            update(task_id, new_description if new_description else None, new_status if new_status else None)

        elif userInput == "delete":
            try:
                task_id = int(input("Enter task ID to delete: "))
            except ValueError:
                print("Invalid ID")
                continue
            delete(task_id)

        else:
            print("Invalid command. Please enter 'list', 'add', 'update', or 'exit'.")


if __name__ == "__main__":
    main_loop()

