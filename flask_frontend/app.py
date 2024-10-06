from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

FASTAPI_URL = "http://127.0.0.1:8000"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def tasks():
    response = requests.get(f"{FASTAPI_URL}/tasks")
    tasks = response.json()
    return render_template('tasks.html', tasks=tasks)


@app.route('/create-task', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    owner_id = request.form['owner_id']
    data = {
        'title': title,
        'description': description,
        'owner_id': owner_id
    }
    response = requests.post(f"{FASTAPI_URL}/tasks/", json=data)
    if response.status_code == 201:
        return redirect('/tasks')
    else:
        return f"Failed to create task. Error: {response.text}", response.status_code


if __name__ == '__main__':
    app.run(debug=True)
