import { useState } from "react";
import api from "../services/api";

function CreateNote({ onNoteCreated }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const createNote = async () => {
    if (!title.trim() || !content.trim()) {
      alert("Please fill all fields");
      return;
    }

    try {
      await api.post("/notes", {
        title,
        content,
      });

      setTitle("");
      setContent("");

      alert("Note created successfully!");

      onNoteCreated();
    } catch (error) {
      console.error(error);
      alert("Failed to create note");
    }
  };

  return (
    <div>
      <h2>Create Note</h2>

      <input
        type="text"
        placeholder="Enter title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <br />
      <br />

      <textarea
        rows="5"
        cols="40"
        placeholder="Enter content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <br />
      <br />

      <button onClick={createNote}>
        Create Note
      </button>

      <hr />
    </div>
  );
}

export default CreateNote;