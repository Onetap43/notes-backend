import { useCallback, useEffect, useState } from "react";
import api from "../services/api";
import Checklist from "./Checklist";
import VersionHistory from "./VersionHistory";

function NoteCard({ note, fetchNotes, allTags = null, onTagChanged }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(note.title);
  const [content, setContent] = useState(note.content);
  const [noteTags, setNoteTags] = useState([]);
  const [tagToAdd, setTagToAdd] = useState("");
  const [tagBusy, setTagBusy] = useState(false);
  const [tagError, setTagError] = useState("");

  // Keep edit form synced after a restored version refreshes this note.
  useEffect(() => {
    setTitle(note.title);
    setContent(note.content);
  }, [note.title, note.content]);

  const fetchNoteTags = useCallback(async () => {
    const response = await api.get(`/notes/${note.note_id}/tags`);
    setNoteTags(response.data);
  }, [note.note_id]);

  useEffect(() => {
    if (allTags === null) return;
    let active = true;
    api.get(`/notes/${note.note_id}/tags`)
      .then((response) => {
        if (active) {
          setNoteTags(response.data);
          setTagError("");
        }
      })
      .catch(() => {
        if (active) setTagError("Could not load note tags.");
      });
    return () => { active = false; };
  }, [allTags, note.note_id]);

  const deleteNote = async () => {
    try {
      await api.delete(`/notes/${note.note_id}`);
      alert("Note deleted successfully!");
      fetchNotes();
    } catch (error) {
      console.error(error);
      alert("Failed to delete note");
    }
  };

  const updateNote = async () => {
    try {
      await api.put(`/update_notes/${note.note_id}`, { title, content });
      alert("Note updated successfully!");
      setEditing(false);
      fetchNotes();
    } catch (error) {
      console.error(error);
      alert("Failed to update note");
    }
  };

  const togglePin = async () => {
    try {
      await api.patch(`/notes/${note.note_id}/pin`);
      fetchNotes();
    } catch (error) { console.error(error); }
  };

  const toggleArchive = async () => {
    try {
      await api.patch(`/notes/${note.note_id}/archive`);
      fetchNotes();
    } catch (error) { console.error(error); }
  };

  const addTag = async () => {
    if (!tagToAdd) return;
    setTagBusy(true);
    setTagError("");
    try {
      await api.put(`/notes/${note.note_id}/tags/${tagToAdd}`);
      await fetchNoteTags();
      setTagToAdd("");
      onTagChanged?.();
    } catch (error) {
      setTagError(error.response?.data?.detail || "Could not add tag.");
    } finally {
      setTagBusy(false);
    }
  };

  const removeTag = async (tagId) => {
    setTagBusy(true);
    setTagError("");
    try {
      await api.delete(`/notes/${note.note_id}/tags/${tagId}`);
      await fetchNoteTags();
      onTagChanged?.();
    } catch (error) {
      setTagError(error.response?.data?.detail || "Could not remove tag.");
    } finally {
      setTagBusy(false);
    }
  };

  const availableTags = allTags === null
    ? []
    : allTags.filter((tag) => !noteTags.some((assigned) => assigned.tag_id === tag.tag_id));

  if (editing) {
    return (
      <div style={{ background: "white", padding: "20px", marginBottom: "20px", borderRadius: "10px", boxShadow: "0 2px 10px rgba(0,0,0,.1)" }}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        />
        <textarea
          rows="5"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "15px", resize: "vertical" }}
        />
        <button onClick={updateNote} style={{ marginRight: "10px" }}>Save</button>
        <button onClick={() => setEditing(false)}>Cancel</button>
      </div>
    );
  }

  return (
    <div style={{ background: "white", padding: "20px", marginBottom: "20px", borderRadius: "10px", boxShadow: "0 2px 10px rgba(0,0,0,.1)" }}>
      <h3>{note.pinned ? "📌 " : ""}{note.title}</h3>
      <p>{note.content}</p>

      {allTags !== null && (
        <div style={{ borderTop: "1px solid #e5e7eb", paddingTop: "12px", marginBottom: "16px" }}>
          <strong>Tags:</strong>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "8px", marginBottom: "8px" }}>
            {noteTags.length === 0 && <span style={{ color: "#64748b" }}>None</span>}
            {noteTags.map((tag) => (
              <span key={tag.tag_id} style={{ border: "1px solid #d1d5db", borderRadius: "6px", padding: "4px 8px" }}>
                #{tag.name}{" "}
                <button
                  type="button"
                  title={`Remove ${tag.name} from note`}
                  aria-label={`Remove ${tag.name} from ${note.title}`}
                  onClick={() => removeTag(tag.tag_id)}
                  disabled={tagBusy}
                  style={{ background: "#64748b", padding: "2px 7px" }}
                >×</button>
              </span>
            ))}
          </div>
          {availableTags.length > 0 && (
            <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
              <select
                aria-label={`Tag to add to ${note.title}`}
                value={tagToAdd}
                onChange={(event) => setTagToAdd(event.target.value)}
                style={{ padding: "8px", minWidth: "130px" }}
              >
                <option value="">Choose a tag</option>
                {availableTags.map((tag) => <option key={tag.tag_id} value={tag.tag_id}>{tag.name}</option>)}
              </select>
              <button type="button" disabled={tagBusy || !tagToAdd} onClick={addTag}>
                Add tag
              </button>
            </div>
          )}
          {tagError && <p role="alert" style={{ color: "#b91c1c" }}>{tagError}</p>}
        </div>
      )}

      <Checklist noteId={note.note_id} />
      <VersionHistory noteId={note.note_id} onRestored={fetchNotes} />

      <button onClick={() => setEditing(true)} style={{ marginRight: "10px" }}>Edit</button>
      <button onClick={deleteNote} style={{ marginRight: "10px" }}>Delete</button>
      <button onClick={togglePin} style={{ marginRight: "10px" }}>
        {note.pinned ? "Unpin" : "Pin"}
      </button>
      <button onClick={toggleArchive}>{note.archived ? "Unarchive" : "Archive"}</button>
    </div>
  );
}

export default NoteCard;
