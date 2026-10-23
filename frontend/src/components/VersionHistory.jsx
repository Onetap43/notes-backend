import { useEffect, useState } from "react";
import api from "../services/api";

function VersionHistory({ noteId, onRestored }) {
  const [expanded, setExpanded] = useState(false);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!expanded) return;
    let active = true;
    api.get(`/notes/${noteId}/history`)
      .then((response) => {
        if (active) { setVersions(response.data); setError(""); }
      })
      .catch(() => { if (active) setError("Could not load version history."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [expanded, noteId]);

  const toggle = () => {
    if (!expanded) setLoading(true);
    setExpanded((value) => !value);
  };

  const restore = async (version) => {
    if (!window.confirm(`Restore the version titled "${version.title}"? The current text will be saved in history.`)) return;
    setBusy(true);
    setError("");
    try {
      await api.post(`/notes/${noteId}/history/${version.version_id}/restore`);
      setExpanded(false);
      onRestored();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not restore this version.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <section style={{ borderTop: "1px solid #e5e7eb", paddingTop: "12px", marginTop: "12px", marginBottom: "14px" }}>
      <button type="button" onClick={toggle} aria-expanded={expanded}>
        {expanded ? "Hide version history" : "Show version history"}
      </button>
      {expanded && (
        <div style={{ marginTop: "10px" }}>
          {loading && <p>Loading previous versions...</p>}
          {error && <p role="alert" style={{ color: "#b91c1c" }}>{error}</p>}
          {!loading && versions.length === 0 && <p>No saved versions yet. Editing the note will create one.</p>}
          <ul style={{ paddingLeft: "20px" }}>
            {versions.map((version) => (
              <li key={version.version_id} style={{ marginBottom: "12px" }}>
                <strong>{version.title}</strong>
                <div style={{ fontSize: "0.85rem", color: "#64748b" }}>
                  {new Date(version.created_at).toLocaleString()}
                </div>
                <p style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>{version.content}</p>
                <button type="button" onClick={() => restore(version)} disabled={busy}>
                  Restore this version
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

export default VersionHistory;
