import { useCallback, useEffect, useState } from "react";
import api from "../services/api";

function Checklist({ noteId }) {
  const [expanded, setExpanded] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [newText, setNewText] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const loadChecklist = useCallback(async () => {
    const response = await api.get(`/notes/${noteId}/checklist`);
    setItems(response.data.items);
    setLoaded(true);
    setError("");
  }, [noteId]);

  useEffect(() => {
    if (!expanded) return;
    let active = true;
    api.get(`/notes/${noteId}/checklist`)
      .then((response) => {
        if (!active) return;
        setItems(response.data.items);
        setLoaded(true);
        setError("");
      })
      .catch(() => { if (active) setError("Could not load checklist."); });
    return () => { active = false; };
  }, [expanded, noteId]);

  const apply = async (operation) => {
    setBusy(true);
    setError("");
    try {
      await operation();
      await loadChecklist();
      return true;
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Could not update checklist.");
      return false;
    } finally {
      setBusy(false);
    }
  };

  const add = async (event) => {
    event.preventDefault();
    const text = newText.trim();
    if (!text) return;
    const ok = await apply(() => api.post(`/notes/${noteId}/checklist`, { text }));
    if (ok) setNewText("");
  };

  const toggle = (item) => apply(() => api.patch(
    `/notes/${noteId}/checklist/${item.item_id}`,
    { completed: !item.completed },
  ));

  const saveEdit = async (event) => {
    event.preventDefault();
    const text = editingText.trim();
    if (!text) return;
    const ok = await apply(() => api.patch(
      `/notes/${noteId}/checklist/${editingId}`,
      { text },
    ));
    if (ok) setEditingId(null);
  };

  const remove = (item) => apply(() => api.delete(`/notes/${noteId}/checklist/${item.item_id}`));

  const complete = items.filter((item) => item.completed).length;
  const percent = items.length ? Math.round(100 * complete / items.length) : 0;

  return (
    <section style={{ borderTop: "1px solid #e5e7eb", paddingTop: "12px", marginTop: "12px", marginBottom: "14px" }}>
      <button type="button" onClick={() => setExpanded((value) => !value)} aria-expanded={expanded}>
        {expanded ? "Hide checklist" : "Show checklist"}
      </button>
      {expanded && (
        <div style={{ marginTop: "12px" }}>
          {loaded && (
            <>
              <p style={{ margin: "4px 0 8px" }}>Progress: {complete}/{items.length} ({percent}%)</p>
              <progress value={complete} max={Math.max(items.length, 1)} style={{ width: "100%" }} />
            </>
          )}
          {error && <p role="alert" style={{ color: "#b91c1c" }}>{error}</p>}
          {items.length === 0 && loaded && <p>No checklist items yet.</p>}
          <ul style={{ listStyle: "none", margin: "12px 0", padding: 0 }}>
            {items.map((item) => (
              <li key={item.item_id} style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "8px", marginBottom: "9px" }}>
                {editingId === item.item_id ? (
                  <form onSubmit={saveEdit} style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                    <input aria-label="Edit checklist text" maxLength={300} value={editingText} onChange={(event) => setEditingText(event.target.value)} required />
                    <button type="submit" disabled={busy || !editingText.trim()}>Save</button>
                    <button type="button" disabled={busy} onClick={() => setEditingId(null)}>Cancel</button>
                  </form>
                ) : (
                  <>
                    <label style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <input type="checkbox" checked={item.completed} disabled={busy} onChange={() => toggle(item)} />
                      <span style={{ textDecoration: item.completed ? "line-through" : "none" }}>{item.text}</span>
                    </label>
                    <button type="button" disabled={busy} onClick={() => { setEditingId(item.item_id); setEditingText(item.text); }}>Edit task</button>
                    <button type="button" disabled={busy} onClick={() => remove(item)}>Delete task</button>
                  </>
                )}
              </li>
            ))}
          </ul>
          <form onSubmit={add} style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            <input aria-label="New checklist item" placeholder="Add a task..." value={newText} maxLength={300} onChange={(event) => setNewText(event.target.value)} required />
            <button type="submit" disabled={busy || !newText.trim()}>Add task</button>
          </form>
        </div>
      )}
    </section>
  );
}

export default Checklist;
