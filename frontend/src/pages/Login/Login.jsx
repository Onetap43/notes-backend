import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/login", {
        username: username,
        password: password,
      });

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      alert("Login Successful!");

      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      alert("Invalid username or password");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Notes App</h1>

      <h2>Login</h2>

      <form onSubmit={handleLogin}>

        <div>
          <label>Username</label>

          <br />

          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <br />

        <div>
          <label>Password</label>

          <br />

          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <br />

        <button type="submit">
          Login
        </button>

      </form>

      <br />

      <button
        onClick={() => navigate("/signup")}
      >
        Create Account
      </button>

    </div>
  );
}

export default Login;