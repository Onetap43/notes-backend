import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../services/api";
import CreateNote from "../../components/CreateNote";
import NoteCard from "../../components/NoteCard";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [notes, setNotes] = useState([]);

  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const limit = 5;

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchUser();
  }, [navigate]);

  useEffect(() => {
    fetchNotes();
  }, [page, search]);

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
      const response = await api.get("/notes", {
        params: {
          search,
          page,
          limit,
        },
      });

      setNotes(response.data);
    } catch (error) {
      console.error(error);
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

      <button onClick={logout} style={{ marginRight: "10px" }}>
        Logout
      </button>

      <button
        onClick={() => navigate("/archived")}
        style={{ marginRight: "10px" }}
      >
        Archived Notes
      </button>

      <button onClick={() => navigate("/recently-updated")}>
        Recently Updated
      </button>

      <hr />

      <CreateNote
        onNoteCreated={fetchNotes}
      />

      <h2>My Notes</h2>

      <input
        type="text"
        placeholder="Search notes..."
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(1);
        }}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "20px",
        }}
      />

      {notes.length === 0 ? (
        <p>No notes found.</p>
      ) : (
        notes.map((note) => (
          <NoteCard
            key={note.note_id}
            note={note}
            fetchNotes={fetchNotes}
          />
        ))
      )}

      <div style={{ marginTop: "25px" }}>
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Previous
        </button>

        <span style={{ margin: "0 15px" }}>
          Page {page}
        </span>

        <button
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default Dashboard;