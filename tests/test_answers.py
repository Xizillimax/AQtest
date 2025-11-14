import pytest
from fastapi import status


def test_create_answer(client):
    """Тест создания ответа"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос для ответа"}
    )
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-123",
            "text": "Это ответ на вопрос"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["text"] == "Это ответ на вопрос"
    assert data["user_id"] == "user-123"
    assert data["question_id"] == question_id
    assert "id" in data
    assert "created_at" in data


def test_create_answer_nonexistent_question(client):
    """Тест: нельзя создать ответ к несуществующему вопросу"""
    response = client.post(
        "/api/v1/questions/99999/answers/",
        json={
            "user_id": "user-123",
            "text": "Ответ"
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_answer_by_id(client):
    """Тест получения ответа по ID"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-456",
            "text": "Ответ на вопрос"
        }
    )
    answer_id = answer_response.json()["id"]

    response = client.get(f"/api/v1/answers/{answer_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == answer_id
    assert data["text"] == "Ответ на вопрос"


def test_delete_answer(client):
    """Тест удаления ответа"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-789",
            "text": "Ответ для удаления"
        }
    )
    answer_id = answer_response.json()["id"]

    response = client.delete(f"/api/v1/answers/{answer_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/api/v1/answers/{answer_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_cascade_delete_answers(client):
    """Тест каскадного удаления ответов при удалении вопроса"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос с ответами"}
    )
    question_id = question_response.json()["id"]

    answer1_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-1",
            "text": "Ответ 1"
        }
    )
    answer1_id = answer1_response.json()["id"]

    answer2_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-2",
            "text": "Ответ 2"
        }
    )
    answer2_id = answer2_response.json()["id"]

    client.delete(f"/api/v1/questions/{question_id}")

    assert client.get(f"/api/v1/answers/{answer1_id}").status_code == status.HTTP_404_NOT_FOUND
    assert client.get(f"/api/v1/answers/{answer2_id}").status_code == status.HTTP_404_NOT_FOUND


def test_multiple_answers_same_user(client):
    """Тест: один пользователь может оставить несколько ответов на один вопрос"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    user_id = "same-user"

    response1 = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": user_id,
            "text": "Первый ответ"
        }
    )
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": user_id,
            "text": "Второй ответ"
        }
    )
    assert response2.status_code == status.HTTP_201_CREATED

    question_data = client.get(f"/api/v1/questions/{question_id}").json()
    assert len(question_data["answers"]) == 2


def test_create_answer_empty_text(client):
    """Тест валидации: нельзя создать ответ с пустым текстом"""
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "user_id": "user-123",
            "text": ""
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
