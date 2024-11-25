from flask import Flask, render_template, request
from config import API_URL
import requests
import argparse
import request_helper

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def show_tasks():
    request_helper.get_request(resource="tasks", template="tasks.html")


@app.route('/users')
def show_users():
    request_helper.get_request(resource="users", template="users.html")


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
    response = requests.post(f"{API_URL}/tasks/", json=data)
    if response.status_code == 200:
        return f"Task {title} has been created!"
    else:
        return f"Failed to create task. Error: {response.text}", response.status_code


@app.route('/create-user', methods=['POST'])
def create_user():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    data = {
        'email': email,
        'name': name,
        'password': password
    }
    response = requests.post(f"{API_URL}/users/", json=data)
    if response.status_code == 200:
        return f"User {name} has been created!"
    else:
        return f"Failed to create user. Error: {response.text}", response.status_code


@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    request_helper.delete_request(resource="tasks", template="tasks.html", parameter={task_id})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true'
    )
    args = parser.parse_args()
    app.run(debug=args.debug)
