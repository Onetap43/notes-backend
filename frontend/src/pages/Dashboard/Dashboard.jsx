import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [notes, setNotes] = useState([]);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchUser();
    fetchNotes();
  }, [navigate]);

  const fetchUser = async () => {
    try {
      const response = await api.get("/me");
      setUser(response.data);
    } catch (error) {
      console.error(error);
      localStorage.removeItem("access_token");
      navigate("/login");
    }
  };

  const fetchNotes = async () => {
    try {
      const response = await api.get("/notes");
      setNotes(response.data);
    } catch (error) {
      console.error(error);
    }
  };

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

      await fetchNotes();

      alert("Note created successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to create note");
    }
  };

  const deleteNote = async (noteId) => {
    try {
      await api.delete(`/notes/${noteId}`);

      setNotes(notes.filter((note) => note.note_id !== noteId));

      alert("Note deleted successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to delete note");
    }
  };

  const startEditing = (note) => {
    setEditingId(note.note_id);
    setEditTitle(note.title);
    setEditContent(note.content);
  };

  const updateNote = async (noteId) => {
    try {
      await api.put(`/update_notes/${noteId}`, {
        title: editTitle,
        content: editContent,
      });

      await fetchNotes();

      setEditingId(null);
      setEditTitle("");
      setEditContent("");

      alert("Note updated successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to update note");
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  if (!user) {
    return <h2>Loading...</h2>;
  }

  return (
    <div style={{ padding: "40px" }}>
      <h1>Dashboard</h1>

      <h2>Welcome, {user.username}</h2>

      <p>User ID: {user.user_id}</p>

      <button onClick={logout}>Logout</button>

      <hr />

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

      <button onClick={createNote}>Create Note</button>

      <hr />

      <h2>My Notes</h2>

      {notes.length === 0 ? (
        <p>No notes found.</p>
      ) : (notes.map((note) => (
          <div
            key={note.note_id}
            style={{
              border: "1px solid black",
              padding: "15px",
              marginBottom: "15px",
              borderRadius: "10px",
            }}
          >
            {editingId === note.note_id ? (
              <>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  style={{
                    width: "100%",
                    marginBottom: "10px",
                  }}
                />

                <textarea
                  rows="5"
                  cols="40"
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  style={{
                    width: "100%",
                    marginBottom: "10px",
                  }}
                />

                <button
                  onClick={() => updateNote(note.note_id)}
                  style={{ marginRight: "10px" }}
                >
                  Save
                </button>

                <button onClick={() => setEditingId(null)}>
                  Cancel
                </button>
              </>
            ) : (
              <>
                <h3>{note.title}</h3>

                <p>{note.content}</p>

                <button
                  onClick={() => startEditing(note)}
                  style={{ marginRight: "10px" }}
                >
                  Edit
                </button>

                <button
                  onClick={() => deleteNote(note.note_id)}
                >
                  Delete
                </button>
              </>
            )}
          </div>
        ))
      )}</div>
  );
}

export default Dashboard;