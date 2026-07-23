import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../services/api";
import NoteCard from "../../components/NoteCard";

function Archived() {

  const navigate = useNavigate();

  const [notes, setNotes] = useState([]);

  useEffect(() => {

    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchArchivedNotes();

  }, [navigate]);

  const fetchArchivedNotes = async () => {

    try {

      const response = await api.get("/archived_notes");

      setNotes(response.data);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div
      style={{
        padding: "40px",
      }}
    >

      <h1>Archived Notes</h1>

      <hr />

      {notes.length === 0 ? (
        <p>No archived notes found.</p>
      ) : (notes.map((note) => (
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