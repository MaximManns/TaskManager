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
    """Attempt to create an existing user"""
    unique_email = f"test_{uuid.uuid4()}@example.com"
    create_response = client.post(
        "/users/",
        json={"email": unique_email, "name": "TestUser", "password": "MyTestPW"},
    )

    assert create_response.status_code == HTTPStatus.CREATED
    created_user = create_response.json()
    user_id = created_user["id"]

    duplicate_response = client.post(
        "/users/",
        json={"email": unique_email, "name": "TestUser", "password": "MyTestPW"},
    )

    assert duplicate_response.status_code == HTTPStatus.BAD_REQUEST
    assert duplicate_response.json() == {
        "title": "User creation failed",
        "detail": "Belonging user already exists",
    }

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT


def test_read_user_list():
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 1


# Task-Route-Tests

def test_read_task_list():
    response = client.get("/tasks/")
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 1


def test_create_new_task():
    unique_owner_id = uuid.uuid4()
    response = client.post(
        "/tasks/",
        json={"owner_id": unique_owner_id, "title": "TestTask", "description": "It's a test task"},
    )

    assert response.status_code == HTTPStatus.CREATED
    created_task = response.json()
    assert "id" in created_task
    assert created_task["owner_id"] == unique_owner_id
    assert created_task["title"] == "TestTask"
    assert created_task["description"] == "It's a test task."

    delete_response = client.delete(f"/users/{created_task['id']}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT


def test_create_existing_task():
    """Attempt to create an existing user"""
    unique_owner_id = uuid.uuid4()
    create_response = client.post(
        "/tasks/",
        json={"owner_id": unique_owner_id, "title": "TestTask", "description": "It's a test task"},
    )

    assert create_response.status_code == HTTPStatus.CREATED
    created_task = create_response.json()
    task_id = created_task["id"]

    duplicate_response = client.post(
        "/tasks/",
        json={"owner_id": unique_owner_id, "title": "TestTask", "description": "It's a test task"},
    )

    assert duplicate_response.status_code == HTTPStatus.BAD_REQUEST
    assert duplicate_response.json() == {
        "title": "Task creation failed",
        "detail": "Belonging task already exists",
    }
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT


def test_delete_existing_task():
    create_response = client.post("/tasks/", json={"name": "existing_task"})
    assert create_response.status_code == HTTPStatus.CREATED

    delete_response = client.delete("/tasks/existing_task")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json() == {
        "title": "Deletion was successful",
        "detail": "The task has been deleted",
    }

    get_response = client.get("/tasks/existing_task")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_delete_non_existent_task():
    get_response = client.get("/tasks/nonexistent_task")
    assert get_response.status_code == HTTPStatus.NOT_FOUND

    delete_response = client.delete("/tasks/nonexistent_task")
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_response.json() == {
        "title": "Deletion failed",
        "detail": "Task couldn't be found",
    }
