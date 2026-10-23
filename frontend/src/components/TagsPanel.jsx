import { useState } from "react";
import api from "../services/api";

function TagsPanel({ tags, selectedTagId, onSelectTag, onTagsUpdated }) {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const createTag = async (event) => {
    event.preventDefault();
    const trimmedName = name.trim();
    if (!trimmedName) {
      setErrorMessage("Enter a tag name first.");
      return;
    }

    setBusy(true);
    setErrorMessage("");
    try {
      await api.post("/tags", { name: trimmedName });
      setName("");
      await onTagsUpdated();
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || "Could not create tag.");
    } finally {
      setBusy(false);
    }
  };

  const deleteTag = async (tag) => {
    if (!window.confirm(`Delete tag "${tag.name}"? Notes will not be deleted.`)) return;

    setBusy(true);
    setErrorMessage("");
    try {
      await api.delete(`/tags/${tag.tag_id}`);
      await onTagsUpdated(tag.tag_id);
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || "Could not delete tag.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <section
      aria-label="Manage tags"
      style={{ background: "white", padding: "20px", borderRadius: "10px", marginBottom: "25px", boxShadow: "0 2px 10px rgba(0,0,0,.1)" }}
    >
      <h2>Tags & Categories</h2>
      <form onSubmit={createTag} style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
        <input
          aria-label="New tag name"
          maxLength={40}
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="New tag, e.g. study"
          style={{ flex: "1 1 200px", width: "auto", marginBottom: 0 }}
        />
        <button type="submit" disabled={busy}>Create tag</button>
      </form>
      {errorMessage && <p role="alert" style={{ color: "#b91c1c" }}>{errorMessage}</p>}

      <label htmlFor="tag-filter" style={{ display: "block", marginTop: "16px" }}>
        <strong>Filter notes by tag</strong>
      </label>
      <select
        id="tag-filter"
        value={selectedTagId === null ? "" : String(selectedTagId)}
        onChange={(event) => onSelectTag(event.target.value ? Number(event.target.value) : null)}
        style={{ width: "100%", padding: "10px", marginTop: "6px", marginBottom: "12px" }}
      >
        <option value="">All notes</option>
        {tags.map((tag) => <option value={tag.tag_id} key={tag.tag_id}>{tag.name}</option>)}
      </select>

      {tags.length > 0 ? (
        <div aria-label="Existing tags" style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
          {tags.map((tag) => (
            <span key={tag.tag_id} style={{ display: "inline-flex", alignItems: "center", border: "1px solid #d1d5db", borderRadius: "8px", padding: "2px 6px", gap: "4px" }}>
              <span>#{tag.name}</span>
              <button
                type="button"
                aria-label={`Delete ${tag.name} tag`}
                title={`Delete ${tag.name} tag`}
                disabled={busy}
                onClick={() => deleteTag(tag)}
                style={{ padding: "3px 8px", background: "#64748b" }}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      ) : <p>No tags yet. Create one to organize your notes.</p>}
    </section>
  );
}

export default TagsPanel;
