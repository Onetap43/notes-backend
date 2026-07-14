import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [notes, setNotes] = useState([]);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    const fetchData = async () => {
      try {
        const userResponse = await api.get("/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setUser(userResponse.data);

        const notesResponse = await api.get("/notes", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setNotes(notesResponse.data);
      } catch (error) {
        console.error(error);

        localStorage.removeItem("access_token");
        navigate("/login");
      }
    };

    fetchData();
  }, [navigate]);

  const createNote = async () => {
    const token = localStorage.getItem("access_token");

    if (!title.trim() || !content.trim()) {
      alert("Please fill all fields");
      return;
    }

    try {
      await api.post(
        "/notes",
        {
          title: title,
          content: content,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const notesResponse = await api.get("/notes", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setNotes(notesResponse.data);

      setTitle("");
      setContent("");

      alert("Note created successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to create note");
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
      ) : (
        notes.map((note) => (
          <div
            key={note.note_id}
            style={{
              border: "1px solid black",
              padding: "10px",
              marginBottom: "15px",
            }}
          >
            <h3>{note.title}</h3>

            <p>{note.content}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default Dashboard;