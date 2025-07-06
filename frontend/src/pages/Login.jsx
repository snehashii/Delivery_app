import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
  if (!userId) {
    alert('Please enter your User ID');
    return;
  }

  try {
    const response = await fetch(`http://localhost:5000/users/${userId}`);
    if (!response.ok) {
      throw new Error('User not found');
    }

    const data = await response.json();

    // Save both user ID and role name in localStorage
    localStorage.setItem('X-User-ID', userId);
    localStorage.setItem('Role', data.role_name); // we will expose this in the backend

    alert(`Logged in as ${data.name} (${data.role_name})`);
    navigate('/roles');
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
};


  return (
    <div className="max-w-md mx-auto p-4 bg-gray-100 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Login</h2>
      <input
        type="number"
        placeholder="Enter your User ID (e.g., 4)"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="border p-2 w-full mb-4"
      />
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Login
      </button>
    </div>
  );
};

export default Login;
