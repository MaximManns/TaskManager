from fastapi.testclient import TestClient
from backend.main import app
from http import HTTPStatus

client = TestClient(app)


# User-Route Tests

def test_read_existing_user():
    response = client.get("/users/{user_name}")
    assert response.status_code == HTTPStatus.OK
    expected_user = {
        "id": 1,
        "email": "user123@example.com",
        "name": "user123", "tasks": []
        }
    assert response.json() == expected_user


def test_read_non_existent_user():
    response = client.get("/users/{user_name}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "No User with this name registered"}


def test_create_new_user():
    response = client.post("/users/", json={"email": "test1@example.com", "name": "testi", "password": "1test1"},)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": "test1@example.com",
        "name": "testi",
        "password": "1test1"
    }


def test_create_existing_user():
    response = client.post("/users/", json={"email": "test1@example.com", "name": "testi", "password": "1test1"},)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "User with this name already registered"}


def test_read_user_list():
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    expected_response = [
        {"id": 1, "email": "test1@example.com", "tasks": None},
        {"id": 2, "email": "test2@example.com", "tasks": None}
    ]
    assert response.json() == expected_response


# Task-Route-Tests

def test_read_task_list():
    response = client.get("/tasks/")
    assert response.status_code == HTTPStatus.OK
    expected_response = [
        {"id": 1, "ownwer_id": "3", "title": "TestTask1"},
        {"id": 2, "ownwer_id": "5", "title": "TestTask2"}
    ]
    assert response.json() == expected_response


def test_create_new_task():
    response = client.post("/tasks/", json={"titke": "test1@example.com", "description": "testi", "owner_id": "1test1"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": "test1@example.com",
        "name": "testi",
        "password": "1test1"
    }


def test_create__existing_task():
    response = client.post("/tasks/", json={"titke": "test1@example.com", "description": "testi", "owner_id": "1test1"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail: User not found"}


def test_delete_existing_taks():
    response = client.delete("/tasks/existing_task")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ok": True}


def test_delete_non_existent_task():
    response = client.delete("/tasks/nonexistent_task")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found"}
