from app.routes.auth import create_access_token


def make_user(client, username):
    response = client.post("/signup", json={"username": username, "password": "password123"})
    assert response.status_code == 200
    token = create_access_token(response.json()["user_id"])
    return {"Authorization": f"Bearer {token}"}


def make_note(client, headers, title):
    response = client.post("/notes", headers=headers, json={"title": title, "content": "Test"})
    assert response.status_code == 200
    return response.json()["note_id"]


def test_create_tag_and_filter_notes(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers, "Exam preparation")

    created = client.post("/tags", headers=headers, json={"name": " Study "})
    assert created.status_code == 201
    tag_id = created.json()["tag_id"]
    assert created.json()["name"] == "study"

    assert client.put(f"/notes/{note_id}/tags/{tag_id}", headers=headers).status_code == 200
    assert client.put(f"/notes/{note_id}/tags/{tag_id}", headers=headers).status_code == 200

    tags = client.get(f"/notes/{note_id}/tags", headers=headers)
    assert tags.json() == [{"tag_id": tag_id, "name": "study"}]

    filtered = client.get(f"/tags/{tag_id}/notes", headers=headers)
    assert filtered.status_code == 200
    assert [note["note_id"] for note in filtered.json()["items"]] == [note_id]
    assert filtered.json()["has_next"] is False

    assert client.delete(f"/notes/{note_id}/tags/{tag_id}", headers=headers).status_code == 200
    assert client.get(f"/tags/{tag_id}/notes", headers=headers).json()["items"] == []


def test_tag_names_must_be_unique_per_user(client):
    headers = make_user(client, "alice")
    assert client.post("/tags", headers=headers, json={"name": "work"}).status_code == 201
    assert client.post("/tags", headers=headers, json={"name": "Work"}).status_code == 409
    assert client.post("/tags", headers=headers, json={"name": "   "}).status_code == 422


def test_users_cannot_access_others_tags(client):
    alice = make_user(client, "alice")
    bob = make_user(client, "bob")
    note_id = make_note(client, alice, "Private")
    tag_id = client.post("/tags", headers=alice, json={"name": "private"}).json()["tag_id"]

    assert client.get("/tags", headers=bob).json() == []
    assert client.put(f"/notes/{note_id}/tags/{tag_id}", headers=bob).status_code == 404
    assert client.get(f"/tags/{tag_id}/notes", headers=bob).status_code == 404
    assert client.delete(f"/tags/{tag_id}", headers=bob).status_code == 404


def test_delete_tag_preserves_note(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers, "Keep this note")
    tag_id = client.post("/tags", headers=headers, json={"name": "temp"}).json()["tag_id"]

    client.put(f"/notes/{note_id}/tags/{tag_id}", headers=headers)
    assert client.delete(f"/tags/{tag_id}", headers=headers).status_code == 200
    assert client.get(f"/notes/{note_id}", headers=headers).status_code == 200
    assert client.get(f"/notes/{note_id}/tags", headers=headers).json() == []
