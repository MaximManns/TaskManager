from flask import Flask, render_template, request
import argparse
import request_helper

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def show_tasks():
    return request_helper.get_request(resource="tasks", template="tasks.html")


@app.route('/users')
def show_users():
    return request_helper.get_request(resource="users", template="users.html")


@app.route('/create-task', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    owner_id = request.form['owner_id']
    json = {
        'title': title,
        'description': description,
        'owner_id': owner_id
    }
    return request_helper.post_request(resource="tasks", template="tasks.html", json=json)


@app.route('/create-user', methods=['POST'])
def create_user():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    json = {
        'email': email,
        'name': name,
        'password': password
    }
    return request_helper.post_request(resource="users", template="users.html", json=json)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    return request_helper.delete_request(template="tasks.html", resource="tasks", parameter=task_id)


@app.route('/tasks/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return request_helper.delete_request(template="users.html", resource="users", parameter=user_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true'
    )
    args = parser.parse_args()
    app.run(debug=args.debug)
