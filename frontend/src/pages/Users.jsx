import React, { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ name: '', email: '', password: '', role_id: '' });
  const [editUserId, setEditUserId] = useState(null);
  const [editUserData, setEditUserData] = useState({ name: '', email: '', password: '', role_id: '' });
  const [role, setRole] = useState('');

  const fetchUsers = async () => {
  try {
    const userId = localStorage.getItem('X-User-ID');
    const roleName = localStorage.getItem('Role');
    setRole(roleName);

    const res = await fetch('http://localhost:5000/users/', {
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId
      }
    });

    const data = await res.json();

    if (!Array.isArray(data)) {
      console.warn('Non-array response:', data);
      setUsers([]); // or null if you want to show a message
    } else {
      setUsers(data);
    }
  } catch (err) {
    console.error('Error fetching users:', err);
    setUsers([]); // fallback in case of error
  }
};


  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async () => {
    const userId = localStorage.getItem('X-User-ID');

    if (!newUser.name || !newUser.email || !newUser.password || !newUser.role_id) {
      alert('All fields are required');
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(newUser)
      });

      const result = await res.json();
      if (res.status === 201) {
        alert('User created');
        setNewUser({ name: '', email: '', password: '', role_id: '' });
        fetchUsers();
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (err) {
      console.error('Error creating user:', err);
    }
  };

  const handleEditUser = (user) => {
    setEditUserId(user.id);
    setEditUserData({
      name: user.name,
      email: user.email,
      password: '',
      role_id: user.role_id
    });
  };

  const handleUpdateUser = async () => {
    const userId = localStorage.getItem('X-User-ID');

    try {
      const res = await fetch(`http://localhost:5000/users/${editUserId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(editUserData)
      });

      if (res.ok) {
        alert('User updated');
        setEditUserId(null);
        setEditUserData({ name: '', email: '', password: '', role_id: '' });
        fetchUsers();
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error('Error updating user:', err);
    }
  };

  const handleDeleteUser = async (id) => {
    const userId = localStorage.getItem('X-User-ID');

    try {
      const res = await fetch(`http://localhost:5000/users/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        }
      });

      if (res.status === 204) {
        alert('User deleted');
        fetchUsers();
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error('Error deleting user:', err);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Users</h2>

      {role === 'Admin' && (
        <div className="mb-6 p-4 border rounded bg-gray-100">
          <h3 className="font-semibold mb-2">Create New User</h3>
          <input
            type="text"
            placeholder="Name"
            value={newUser.name}
            onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="email"
            placeholder="Email"
            value={newUser.email}
            onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="password"
            placeholder="Password"
            value={newUser.password}
            onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="number"
            placeholder="Role ID"
            value={newUser.role_id}
            onChange={(e) => setNewUser({ ...newUser, role_id: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <button
            onClick={handleCreateUser}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Create User
          </button>
        </div>
      )}

      <ul className="space-y-2">
        {users.map((user) => (
          <li key={user.id} className="border p-2 rounded flex justify-between items-center">
            <div>
              <strong>{user.name}</strong> — {user.email} (Role ID: {user.role_id})
            </div>
            {role === 'Admin' && (
              <div className="flex space-x-2">
                <button
                  onClick={() => handleEditUser(user)}
                  className="bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteUser(user.id)}
                  className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>

      {role === 'Admin' && editUserId && (
        <div className="mt-6 p-4 border rounded bg-yellow-50">
          <h3 className="font-semibold mb-2">Edit User</h3>
          <input
            type="text"
            placeholder="Name"
            value={editUserData.name}
            onChange={(e) => setEditUserData({ ...editUserData, name: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="email"
            placeholder="Email"
            value={editUserData.email}
            onChange={(e) => setEditUserData({ ...editUserData, email: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="password"
            placeholder="New Password (leave blank to keep current)"
            value={editUserData.password}
            onChange={(e) => setEditUserData({ ...editUserData, password: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="number"
            placeholder="Role ID"
            value={editUserData.role_id}
            onChange={(e) => setEditUserData({ ...editUserData, role_id: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <div className="flex space-x-2">
            <button
              onClick={handleUpdateUser}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Update
            </button>
            <button
              onClick={() => setEditUserId(null)}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Users;
