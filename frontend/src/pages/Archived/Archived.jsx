import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../services/api";
import NoteCard from "../../components/NoteCard";

function Archived() {
  const navigate = useNavigate();

  const [notes, setNotes] = useState([]);

  const fetchArchivedNotes = useCallback(async () => {
    try {
      const response = await api.get("/archived_notes");
      setNotes(response.data);
    } catch (error) {
      console.error(error);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchArchivedNotes();
  }, [navigate, fetchArchivedNotes]);

  return (
    <div
      style={{
        padding: "40px",
      }}
    >
      <h1>Archived Notes</h1>

      <button
        onClick={() => navigate("/dashboard")}
        style={{ marginBottom: "20px" }}
      >
        Back to Dashboard
      </button>

      <hr />

      {notes.length === 0 ? (
        <p>No archived notes found.</p>
      ) : (
        notes.map((note) => (
          <NoteCard
            key={note.note_id}
            note={note}
            fetchNotes={fetchArchivedNotes}
          />
        ))
      )}
    </div>
  );
}

export default Archived;