from fastapi.testclient import TestClient
from backend.app import app
from http import HTTPStatus
import uuid

client = TestClient(app)


# User-Route Tests

def test_read_existing_user():
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    expected_user = {
        "id": 1,
        "email": "user123@example.com",
        "name": "user123", "tasks": []
        }
    assert response.json() == expected_user


def test_read_non_existent_user():
    non_existent_id = uuid.uuid4()
    response = client.get(f"/users/{non_existent_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "title": "Couldn't find user",
        "detail": "No User with this name registered"
    }


def test_create_new_user():
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post(
        "/users/",
        json={"email": unique_email, "name": "TestUser", "password": "MyTestPW"},
    )

    assert response.status_code == HTTPStatus.CREATED
    created_user = response.json()
    assert "id" in created_user
    assert created_user["email"] == unique_email
    assert created_user["name"] == "TestUser"
    assert "password" not in created_user

    delete_response = client.delete(f"/users/{created_user['id']}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT


def test_create_existing_user():
    response = client.post("/users/", json={"email": "test1@example.com", "name": "testi", "password": "1test1"},)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "title": "Task creation failed",
        "detail": "Belonging user not found"
        }


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
    response = client.post("/tasks/", json={"title": "test1@example.com", "description": "ThisIsATestTask", "owner_id": "1"})
    assert response.status_code == HTTPStatus.OK
    created_task = response.json()
    assert created_task == {
        "email": "test1@example.com",
        "name": "ThisIsATestTask",
        "password": "1"
    }
    delete_response = client.delete(f"/tasks/{created_task['id']}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT


def test_create_existing_task():
    response = client.post("/tasks/", json={"title": "test1@example.com", "description": "testi", "owner_id": "1test1"})
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
