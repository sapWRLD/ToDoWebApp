from flask import Flask, render_template, request, redirect, url_for
import json
from time import gmtime,strftime
from datetime import datetime

app = Flask(__name__)
TASK_FILE = "task.json"
TODAY = datetime.now().strftime("%Y-%m-%d")

tags = ["Work", "Personal", "Study", "Home"]

def load_task():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"HIGH":[], "MEDIUM": [], "LOW": []}

def save_task(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def dashboard():
    tasks = load_task()
    return render_template("ToDoPage.html", task_data=tasks, tags=tags)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task", "").strip()
    priority = request.form.get("priority", "").upper()
    tag = request.form.get("tag", "")
    due_date = request.form.get("due_date", "")

    if not task_text or priority not in ["HIGH", "MEDIUM", "LOW"] or tag not in tags or due_date <= TODAY:
        return redirect(url_for("dashboard"))
    
    timestamp = strftime("%d %b %Y %H:%M", gmtime())
    task_entry = f"[{tag}] {task_text} Due By: {due_date} | {timestamp}"

    tasks = load_task()
    tasks[priority].append(task_entry)
    save_task(tasks)
    return redirect(url_for("dashboard"))

@app.route("/remove", methods=["POST"])
def remove_taks():
    priority = request.form.get("priority", "").upper()
    index = int(request.form.get("index", -1))

    tasks = load_task()
    if priority in tasks and 0 <= index < len(tasks[priority]):
        tasks[priority].pop(index)
        save_task(tasks)
    
    return(redirect(url_for("dashboard")))
if __name__ == "__main__":
    app.run(debug=True)