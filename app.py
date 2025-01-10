import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Task structure
class Task:
    def __init__(self, title, deadline, category, priority, completed=False):
        self.title = title
        self.deadline = deadline
        self.category = category
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now()
        self.time_taken = None  # Time will be set when the task is completed

    def mark_completed(self):
        self.completed = True
        self.time_taken = datetime.now() - self.created_at

    def time_taken_str(self):
        """Return the time taken as a formatted string ('2h 5m 30s')."""
        if isinstance(self.time_taken, timedelta):  # Check if time_taken is a timedelta object
            total_seconds = self.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            return f"{hours}h {minutes}m {seconds}s"
        return None  # Return None if time_taken is not set or if it's a string

    def to_dict(self):
        return {
            'title': self.title,
            'deadline': self.deadline,
            'category': self.category,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'time_taken': self.time_taken_str()  # Store the string representation of time_taken
        }

    @staticmethod
    def from_dict(data):
        task = Task(
            title=data['title'],
            deadline=data['deadline'],
            category=data['category'],
            priority=data['priority'],
            completed=data['completed']
        )
        # If time_taken exists, it's already a string in tasks.json, so we leave it as it is
        task.time_taken = data.get('time_taken', None)
        task.created_at = datetime.fromisoformat(data['created_at'])
        return task

# Load categories from a JSON file
def load_categories():
    try:
        with open('categories.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save categories to a JSON file
def save_categories(categories):
    with open('categories.json', 'w') as file:
        json.dump(categories, file, indent=4)

# Load tasks from a JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            data = json.load(file)
            tasks = [Task.from_dict(task_data) for task_data in data]
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to a JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

# Initialize tasks list
tasks = load_tasks()

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = load_tasks()  # Reload tasks from file to make sure it reflects any changes
    categories = load_categories()
    
    # Get filters from URL parameters
    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')
    priority_filter = request.args.get('priority', 'all')  # Default to 'all'

    # Filter tasks based on the status
    filtered_tasks = tasks
    if status_filter == 'completed':
        filtered_tasks = [task for task in tasks if task.completed]
    elif status_filter == 'pending':
        filtered_tasks = [task for task in tasks if not task.completed]

    # Filter tasks based on category
    if category_filter != 'all':
        filtered_tasks = [task for task in filtered_tasks if task.category == category_filter]
    
    # Filter tasks based on priority
    if priority_filter != 'all':
        filtered_tasks = [task for task in filtered_tasks if task.priority == priority_filter]

    return render_template(
        'index.html',
        tasks=filtered_tasks,
        status_filter=status_filter,
        category_filter=category_filter,
        priority_filter=priority_filter,  # Pass priority filter to template
	categories=categories
    )

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        categories = load_categories()
        if category_name not in categories:
            categories.append(category_name)  # Add the new category
            save_categories(categories)  # Save updated list of categories
    return redirect(url_for('index'))  # Redirect back to task list page

@app.route('/delete_category/<string:category_name>', methods=['POST'])
def delete_category(category_name):
    categories = load_categories()
    if category_name in categories:
        categories.remove(category_name)  # Remove category
        save_categories(categories)  # Save updated list
    return redirect(url_for('index'))  # Redirect back to task list page


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    deadline = request.form['deadline']
    category = request.form['category']
    priority = request.form['priority']
    
    task = Task(title, deadline, category, priority)
    tasks = load_tasks()  # Reload tasks to get the current list
    tasks.append(task)
    save_tasks(tasks)  # Save updated tasks to file
    
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id].mark_completed()
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

