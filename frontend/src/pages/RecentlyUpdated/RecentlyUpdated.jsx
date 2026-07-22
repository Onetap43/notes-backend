import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../services/api";
import NoteCard from "../../components/NoteCard";

function RecentlyUpdated() {
  const navigate = useNavigate();

  const [notes, setNotes] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchRecentlyUpdated();
  }, [navigate]);

  const fetchRecentlyUpdated = async () => {
    try {
      const response = await api.get("/recently_updated");
      setNotes(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>Recently Updated Notes</h1>

      <button onClick={() => navigate("/dashboard")}>
        Back to Dashboard
      </button>

      <hr />

      {notes.length === 0 ? (
        <p>No recently updated notes found.</p>
      ) : (notes.map((note) => (
          <NoteCard
            key={note.note_id}
            note={note}
            fetchNotes={fetchRecentlyUpdated}
          />
        ))
      )}
    </div>
  );
}

export default RecentlyUpdated;