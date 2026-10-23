import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../services/api";
import CreateNote from "../../components/CreateNote";
import NoteCard from "../../components/NoteCard";
import TagsPanel from "../../components/TagsPanel";

const LIMIT = 5;

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [notes, setNotes] = useState([]);
  const [hasNext, setHasNext] = useState(false);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [tags, setTags] = useState([]);
  const [selectedTagId, setSelectedTagId] = useState(null);
  const [tagsError, setTagsError] = useState("");
  const [notesError, setNotesError] = useState("");

  const fetchUser = useCallback(async () => {
    try {
      const response = await api.get("/me");
      setUser(response.data);
    } catch (error) {
      console.error(error);
      localStorage.removeItem("access_token");
      navigate("/login");
    }
  }, [navigate]);

  const fetchTags = useCallback(async () => {
    try {
      const response = await api.get("/tags");
      setTags(response.data);
      setTagsError("");
    } catch (error) {
      console.error(error);
      setTagsError("Could not load tags. Please refresh the page.");
    }
  }, []);

  const fetchNotes = useCallback(async () => {
    try {
      const url = selectedTagId === null
        ? "/notes"
        : `/tags/${selectedTagId}/notes`;
      const params = selectedTagId === null
        ? { search, page, limit: LIMIT }
        : { page, limit: LIMIT };

      const response = await api.get(url, { params });
      const fetchedNotes = response.data.items;

      if (fetchedNotes.length === 0 && page > 1) {
        setPage((currentPage) => currentPage - 1);
        return;
      }

      setNotes(fetchedNotes);
      setHasNext(response.data.has_next);
      setNotesError("");
    } catch (error) {
      console.error(error);
      setNotes([]);
      setHasNext(false);
      setNotesError("Could not load notes. Please try again.");
    }
  }, [page, search, selectedTagId]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    fetchUser();
    fetchTags();
  }, [navigate, fetchUser, fetchTags]);

  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  const selectTag = (tagId) => {
    setSelectedTagId(tagId);
    setPage(1);
    if (tagId !== null) setSearch("");
  };

  const afterTagsUpdated = async (deletedTagId = null) => {
    if (deletedTagId !== null && selectedTagId === deletedTagId) {
      setSelectedTagId(null);
      setPage(1);
    }
    await fetchTags();
  };

  const afterNoteCreated = () => {
    if (selectedTagId !== null || page !== 1 || search !== "") {
      setSelectedTagId(null);
      setSearch("");
      setPage(1);
    } else {
      fetchNotes();
    }
  };

  if (!user) return <h2>Loading...</h2>;

  return (
    <div style={{ padding: "40px" }}>
      <h1>Dashboard</h1>
      <h2>Welcome, {user.username}</h2>
      <p>User ID: {user.user_id}</p>

      <button onClick={logout} style={{ marginRight: "10px" }}>Logout</button>
      <button onClick={() => navigate("/archived")} style={{ marginRight: "10px" }}>
        Archived Notes
      </button>
      <button onClick={() => navigate("/recently-updated")}>Recently Updated</button>

      <hr />
      <CreateNote onNoteCreated={afterNoteCreated} />

      <TagsPanel
        tags={tags}
        selectedTagId={selectedTagId}
        onSelectTag={selectTag}
        onTagsUpdated={afterTagsUpdated}
      />
      {tagsError && <p role="alert" style={{ color: "#b91c1c" }}>{tagsError}</p>}

      <h2>My Notes</h2>
      {selectedTagId !== null && (
        <p>Filtering by tag. Select "All notes" to use title/content search.</p>
      )}
      <input
        type="text"
        placeholder={selectedTagId === null ? "Search notes..." : "Select All notes to search"}
        aria-label="Search notes"
        value={search}
        disabled={selectedTagId !== null}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(1);
        }}
        style={{ width: "100%", padding: "10px", marginBottom: "20px" }}
      />

      {notesError && <p role="alert" style={{ color: "#b91c1c" }}>{notesError}</p>}
      {notes.length === 0 ? (
        <p>No notes found.</p>
      ) : (
        notes.map((note) => (
          <NoteCard
            key={note.note_id}
            note={note}
            fetchNotes={fetchNotes}
            allTags={tags}
            onTagChanged={fetchNotes}
          />
        ))
      )}

      <div style={{ marginTop: "25px" }}>
        <button disabled={page === 1} onClick={() => setPage((currentPage) => currentPage - 1)}>
          Previous
        </button>
        <span style={{ margin: "0 15px" }}>Page {page}</span>
        <button disabled={!hasNext} onClick={() => setPage((currentPage) => currentPage + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
