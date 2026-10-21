from app.routes.auth import create_access_token


def user_headers(client, username):
    response = client.post("/signup", json={"username": username, "password": "password123"})
    assert response.status_code == 200
    token = create_access_token(response.json()["user_id"])
    return {"Authorization": f"Bearer {token}"}


def new_note(client, headers, title="Original", content="First draft"):
    result = client.post("/notes", json={"title": title, "content": content}, headers=headers)
    assert result.status_code == 200
    return result.json()["note_id"]


def change_note(client, headers, note_id, title, content):
    return client.put(f"/update_notes/{note_id}", headers=headers, json={"title": title, "content": content})


def history(client, headers, note_id):
    return client.get(f"/notes/{note_id}/history", headers=headers)


def test_edit_saves_previous_state(client):
    headers = user_headers(client, "alice")
    note_id = new_note(client, headers)
    assert history(client, headers, note_id).json() == []
    response = change_note(client, headers, note_id, "Revised", "Second draft")
    assert response.status_code == 200
    versions = history(client, headers, note_id).json()
    assert len(versions) == 1
    assert versions[0]["title"] == "Original"
    assert versions[0]["content"] == "First draft"
    assert versions[0]["created_at"]


def test_multiple_edits_show_latest_version_first(client):
    headers = user_headers(client, "alice")
    note_id = new_note(client, headers)
    change_note(client, headers, note_id, "Second", "Two")
    change_note(client, headers, note_id, "Third", "Three")
    versions = history(client, headers, note_id).json()
    assert [v["title"] for v in versions] == ["Second", "Original"]
    assert history(client, headers, note_id).status_code == 200


def test_restore_saves_current_state_for_undo(client):
    headers = user_headers(client, "alice")
    note_id = new_note(client, headers)
    change_note(client, headers, note_id, "Revised", "Edited")
    first_version = history(client, headers, note_id).json()[0]["version_id"]
    response = client.post(f"/notes/{note_id}/history/{first_version}/restore", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Original"
    assert client.get(f"/notes/{note_id}", headers=headers).json()["title"] == "Original"
    current_saved = history(client, headers, note_id).json()[0]
    assert current_saved["title"] == "Revised"
    assert current_saved["content"] == "Edited"


def test_no_history_for_unchanged_edits_or_restores(client):
    headers = user_headers(client, "alice")
    note_id = new_note(client, headers)
    change_note(client, headers, note_id, "Original", "First draft")
    assert history(client, headers, note_id).json() == []
    change_note(client, headers, note_id, "Revised", "Edited")
    version_id = history(client, headers, note_id).json()[0]["version_id"]
    client.post(f"/notes/{note_id}/history/{version_id}/restore", headers=headers)
    before = len(history(client, headers, note_id).json())
    assert client.post(f"/notes/{note_id}/history/{version_id}/restore", headers=headers).status_code == 200
    assert len(history(client, headers, note_id).json()) == before


def test_other_user_cannot_read_or_restore_and_deleting_note_removes_history(client):
    alice = user_headers(client, "alice")
    bob = user_headers(client, "bob")
    note_id = new_note(client, alice)
    change_note(client, alice, note_id, "Updated", "Modified")
    version_id = history(client, alice, note_id).json()[0]["version_id"]
    assert history(client, bob, note_id).status_code == 404
    assert client.post(f"/notes/{note_id}/history/{version_id}/restore", headers=bob).status_code == 404
    other_note = new_note(client, alice, "Another note", "safe")
    assert client.post(f"/notes/{other_note}/history/{version_id}/restore", headers=alice).status_code == 404
    assert client.delete(f"/notes/{note_id}", headers=alice).status_code == 200
    assert history(client, alice, note_id).status_code == 404
