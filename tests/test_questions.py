import pytest
from fastapi import status


def test_create_question(client):
    """Тест создания вопроса"""
    response = client.post(
        "/api/v1/questions/",
        json={"text": "Как работает Python?"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["text"] == "Как работает Python?"
    assert "id" in data
    assert "created_at" in data


def test_get_all_questions(client):
    """Тест получения списка всех вопросов"""
    client.post("/api/v1/questions/", json={"text": "Вопрос 1"})
    client.post("/api/v1/questions/", json={"text": "Вопрос 2"})

    response = client.get("/api/v1/questions/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2


def test_get_question_by_id(client):
    """Тест получения вопроса по ID"""
    create_response = client.post(
        "/api/v1/questions/",
        json={"text": "Тестовый вопрос"}
    )
    question_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/questions/{question_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == question_id
    assert data["text"] == "Тестовый вопрос"
    assert "answers" in data


def test_get_nonexistent_question(client):
    """Тест получения несуществующего вопроса"""
    response = client.get("/api/v1/questions/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_question(client):
    """Тест удаления вопроса"""

    create_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос для удаления"}
    )
    question_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/questions/{question_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_create_question_empty_text(client):
    """Тест валидации: нельзя создать вопрос с пустым текстом"""
    response = client.post(
        "/api/v1/questions/",
        json={"text": ""}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_question_whitespace_text(client):
    """Тест валидации: нельзя создать вопрос только из пробелов"""
    response = client.post(
        "/api/v1/questions/",
        json={"text": "   "}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
