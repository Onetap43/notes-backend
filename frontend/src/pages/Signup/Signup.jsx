/*
  This file was generated with the assistance of OpenAI ChatGPT.
  It was reviewed, modified, and tested by the author.
*/

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function Signup() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (event) => {
    event.preventDefault();
    setErrorMessage("");

    const cleanedUsername = username.trim();

    if (!cleanedUsername || !password || !confirmPassword) {
      setErrorMessage("Please complete all fields.");
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      await api.post("/signup", {
        username: cleanedUsername,
        password: password,
      });

      alert("Account created successfully. Please log in.");

      navigate("/login", { replace: true });
    } catch (error) {
      console.error("Signup failed:", error);

      const backendMessage = error.response?.data?.detail;

      if (typeof backendMessage === "string") {
        setErrorMessage(backendMessage);
      } else if (!error.response) {
        setErrorMessage(
          "Could not connect to the server. Please try again."
        );
      } else {
        setErrorMessage(
          "Account creation failed. Please try another username."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "420px",
        margin: "80px auto",
        padding: "24px",
        textAlign: "center",
      }}
    >
      <h1>Notes App</h1>
      <h2>Create Account</h2>

      <form onSubmit={handleSignup}>
        <div>
          <label htmlFor="username">Username</label>

          <br />

          <input
            id="username"
            type="text"
            placeholder="Choose a username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            required
          />
        </div>

        <br />

        <div>
          <label htmlFor="password">Password</label>

          <br />

          <input
            id="password"
            type="password"
            placeholder="Choose a password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="new-password"
            required
          />
        </div>

        <br />

        <div>
          <label htmlFor="confirm-password">Confirm Password</label>

          <br />

          <input
            id="confirm-password"
            type="password"
            placeholder="Enter password again"
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(event.target.value)
            }
            autoComplete="new-password"
            required
          />
        </div>

        {errorMessage && (
          <p style={{ marginTop: "18px" }}>
            {errorMessage}
          </p>
        )}

        <br />

        <button type="submit" disabled={loading}>
          {loading ? "Creating account..." : "Create Account"}
        </button>
      </form>

      <br />

      <button
        type="button"
        onClick={() => navigate("/login")}
        disabled={loading}
      >
        Back to Login
      </button>
    </div>
  );
}

export default Signup;