import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [notes, setNotes] = useState([]);

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

      <h2>My Notes</h2>

      {notes.length === 0 ? (
        <p>No notes found.</p>
      ) : (
        notes.map((note) => (
          <div
            key={note.note_id}
            style={{
              border: "1px solid black",
              marginBottom: "15px",
              padding: "10px",
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