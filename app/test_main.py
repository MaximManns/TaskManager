from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_existing_user():
    response = client.get("/users/{user_name}")
    assert response.status_code == 200
    expected_user = {
        "id": 1,
        "email": "user123@example.com",
        "name": "user123",
        "tasks": []
    }
    assert response.json() == expected_user


def test_read_non_existent_user():
    response = client.get("/users/{user_name}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No User with this name registered"}


def test_delete_non_existent_task():
    response = client.delete("/tasks/nonexistent_task")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
