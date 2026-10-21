from app.routes.auth import create_access_token


def create_user(client, username):
    response = client.post(
        "/signup",
        json={"username": username, "password": "password123"},
    )

    assert response.status_code == 200

    token = create_access_token(response.json()["user_id"])
    return {"Authorization": f"Bearer {token}"}


def create_note(client, headers, title):
    response = client.post(
        "/notes",
        headers=headers,
        json={"title": title, "content": "Test content"},
    )

    assert response.status_code == 200
    return response.json()["note_id"]


def test_signup_login_and_profile(client):
    client.post(
        "/signup",
        json={"username": "testuser", "password": "password123"},
    )

    response = client.post(
        "/login",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    profile = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert profile.status_code == 200
    assert profile.json()["username"] == "testuser"


def test_create_update_delete_note(client):
    headers = create_user(client, "alice")

    note_id = create_note(client, headers, "First note")

    response = client.put(
        f"/update_notes/{note_id}",
        headers=headers,
        json={"title": "Updated note", "content": "New content"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated note"

    response = client.delete(
        f"/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_pagination(client):
    headers = create_user(client, "alice")

    create_note(client, headers, "Note 1")
    create_note(client, headers, "Note 2")

    first_page = client.get(
        "/notes?page=1&limit=1",
        headers=headers,
    )

    assert first_page.status_code == 200
    assert len(first_page.json()["items"]) == 1
    assert first_page.json()["has_next"] is True

    second_page = client.get(
        "/notes?page=2&limit=1",
        headers=headers,
    )

    assert second_page.status_code == 200
    assert len(second_page.json()["items"]) == 1
    assert second_page.json()["has_next"] is False

    third_page = client.get(
        "/notes?page=3&limit=1",
        headers=headers,
    )

    assert third_page.json()["items"] == []
    assert third_page.json()["has_next"] is False


def test_user_cannot_access_another_users_notes(client):
    alice = create_user(client, "alice")
    bob = create_user(client, "bob")

    note_id = create_note(client, alice, "Private note")

    response = client.get(
        f"/notes/{note_id}",
        headers=bob,
    )

    assert response.status_code == 404

    response = client.delete(
        f"/notes/{note_id}",
        headers=bob,
    )

    assert response.status_code == 404
