"use client"; // <--- Required for Next.js App Router interactivity

import { useState } from "react";

export default function App() { // Use 'export default' for the main page
  const [isSignup, setIsSignup] = useState(false);
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    // Note: In Next.js, you usually need the full URL if connecting to a separate 
    // Python backend (e.g., http://localhost:8000/signup)
    const baseUrl = process.env.NEXT_PUBLIC_API_URL; 
    const endpoint = isSignup ? "/signup" : "/login";

    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage("Error connecting to server");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h2>{isSignup ? "Signup" : "Login"}</h2>

      {isSignup && (
        <>
          <input name="first_name" placeholder="First Name" style={inputStyle} onChange={handleChange} /><br/>
          <input name="last_name" placeholder="Last Name" style={inputStyle} onChange={handleChange} /><br/>
        </>
      )}

      <input name="phone" placeholder="Phone" style={inputStyle} onChange={handleChange} /><br/>
      <input type="password" name="password" placeholder="Password" style={inputStyle} onChange={handleChange} /><br/>

      <button onClick={handleSubmit} style={btnStyle}>
        {isSignup ? "Signup" : "Login"}
      </button>

      <br/><br/>
      <button onClick={() => setIsSignup(!isSignup)} style={{ ...btnStyle, backgroundColor: "#ccc", color: "#000" }}>
        Switch to {isSignup ? "Login" : "Signup"}
      </button>

      <h3>{message}</h3>
    </div>
  );
}

// Simple styles to make it look decent in Next.js
const inputStyle = { padding: "8px", margin: "5px 0", width: "250px" };
const btnStyle = { padding: "10px 20px", cursor: "pointer", backgroundColor: "#0070f3", color: "white", border: "none", borderRadius: "5px" };