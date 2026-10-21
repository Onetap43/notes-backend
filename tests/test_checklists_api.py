from app.routes.auth import create_access_token


def make_user(client, username):
    response = client.post("/signup", json={"username": username, "password": "password123"})
    assert response.status_code == 200
    token = create_access_token(response.json()["user_id"])
    return {"Authorization": f"Bearer {token}"}


def make_note(client, headers):
    response = client.post(
        "/notes", headers=headers, json={"title": "Tasks", "content": "Before exam"}
    )
    assert response.status_code == 200
    return response.json()["note_id"]


def add_item(client, headers, note_id, label):
    return client.post(
        f"/notes/{note_id}/checklist", headers=headers, json={"text": label}
    )


def test_create_items_and_progress(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers)
    first = add_item(client, headers, note_id, "Learn SQL")
    second = add_item(client, headers, note_id, "Review React")
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["position"] == 0
    assert second.json()["position"] == 1

    checklist = client.get(f"/notes/{note_id}/checklist", headers=headers)
    assert checklist.status_code == 200
    assert checklist.json()["completed"] == 0
    assert checklist.json()["total"] == 2
    assert [row["text"] for row in checklist.json()["items"]] == ["Learn SQL", "Review React"]


def test_toggle_and_rename_items(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers)
    item_id = add_item(client, headers, note_id, "Old name").json()["item_id"]
    url = f"/notes/{note_id}/checklist/{item_id}"
    edited = client.patch(url, headers=headers, json={"text": "New name", "completed": True})
    assert edited.status_code == 200
    assert edited.json()["text"] == "New name"
    assert edited.json()["completed"] is True
    assert client.get(f"/notes/{note_id}/checklist", headers=headers).json()["completed"] == 1

    unchecked = client.patch(url, headers=headers, json={"completed": False})
    assert unchecked.status_code == 200
    assert unchecked.json()["completed"] is False


def test_users_cannot_access_other_users_checklists(client):
    alice = make_user(client, "alice")
    bob = make_user(client, "bob")
    note_id = make_note(client, alice)
    item_id = add_item(client, alice, note_id, "Private task").json()["item_id"]
    base = f"/notes/{note_id}/checklist"
    assert client.get(base, headers=bob).status_code == 404
    assert add_item(client, bob, note_id, "Intrusion").status_code == 404
    assert client.patch(f"{base}/{item_id}", headers=bob, json={"completed": True}).status_code == 404
    assert client.delete(f"{base}/{item_id}", headers=bob).status_code == 404
    assert client.get(base, headers=alice).json()["completed"] == 0


def test_deleting_item_or_note_preserves_data_isolation(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers)
    item_id = add_item(client, headers, note_id, "Buy milk").json()["item_id"]
    assert client.delete(f"/notes/{note_id}/checklist/{item_id}", headers=headers).status_code == 200
    assert client.get(f"/notes/{note_id}/checklist", headers=headers).json()["total"] == 0
    add_item(client, headers, note_id, "Retired with note")
    assert client.delete(f"/notes/{note_id}", headers=headers).status_code == 200
    assert client.get(f"/notes/{note_id}/checklist", headers=headers).status_code == 404


def test_reject_blank_or_empty_updates(client):
    headers = make_user(client, "alice")
    note_id = make_note(client, headers)
    assert add_item(client, headers, note_id, "   ").status_code == 422
    item_id = add_item(client, headers, note_id, "Correct").json()["item_id"]
    url = f"/notes/{note_id}/checklist/{item_id}"
    assert client.patch(url, headers=headers, json={}).status_code == 422
    assert client.patch(url, headers=headers, json={"text": "   "}).status_code == 422
    assert client.get(f"/notes/{note_id}/checklist", headers=headers).json()["items"][0]["text"] == "Correct"
