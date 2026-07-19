import { useState } from "react";
import api from "../services/api";

function NoteCard({
  note,
  fetchNotes,
}) {
  const [editing, setEditing] = useState(false);

  const [title, setTitle] = useState(note.title);
  const [content, setContent] = useState(note.content);

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
      await api.put(`/update_notes/${note.note_id}`, {
        title,
        content,
      });

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
    } catch (error) {
      console.error(error);
    }
  };

  const toggleArchive = async () => {
    try {
      await api.patch(`/notes/${note.note_id}/archive`);

      fetchNotes();
    } catch (error) {
      console.error(error);
    }
  };

  if (editing) {
    return (
      <div
        style={{
          border: "1px solid black",
          padding: "15px",
          marginBottom: "15px",
        }}
      ><input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{
            width: "100%",
            marginBottom: "10px",
          }}
        />

        <textarea
          rows="5"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{
            width: "100%",
            marginBottom: "10px",
          }}
        />

        <button
          onClick={updateNote}
          style={{ marginRight: "10px" }}
        >
          Save
        </button>

        <button onClick={() => setEditing(false)}>
          Cancel
        </button>
      </div>
    );
  }

  return (
    <div
      style={{
        border: "1px solid black",
        padding: "15px",
        marginBottom: "15px",
        borderRadius: "10px",
      }}
    >
      <h3>
        {note.pinned ? "📌 " : ""}
        {note.title}
      </h3>

      <p>{note.content}</p>

      <button
        onClick={() => setEditing(true)}
        style={{ marginRight: "10px" }}
      >
        Edit
      </button>

      <button
        onClick={deleteNote}
        style={{ marginRight: "10px" }}
      >
        Delete
      </button>

      <button
        onClick={togglePin}
        style={{ marginRight: "10px" }}
      >
        {note.pinned ? "Unpin" : "Pin"}
      </button>

      <button onClick={toggleArchive}>
        {note.archived ? "Unarchive" : "Archive"}
      </button>
    </div>
  );
}

export default NoteCard;