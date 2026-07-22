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

      onNoteCreated();

      alert("Note created successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to create note");
    }
  };

  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        marginBottom: "25px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h2>Create Note</h2>

      <input
        type="text"
        placeholder="Enter title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "15px",
        }}
      />

      <textarea
        rows="5"
        placeholder="Enter content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "15px",
          resize: "vertical",
        }}
      />

      <button onClick={createNote}>
        Create Note
      </button>
    </div>
  );
}

export default CreateNote;