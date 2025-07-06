import React, { useEffect, useState } from 'react';

const Roles = () => {
  const [roles, setRoles] = useState([]);
  const [newRole, setNewRole] = useState({ name: '', description: '' });
  const [role, setRole] = useState('');
  const [editRoleId, setEditRoleId] = useState(null);
  const [editRoleData, setEditRoleData] = useState({ name: '', description: '' });

  const fetchRoles = async () => {
    try {
      const userId = localStorage.getItem('X-User-ID');
      const roleName = localStorage.getItem('Role');
      setRole(roleName);

      const response = await fetch('http://localhost:5000/roles/', {
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        }
      });

      const data = await response.json();
      setRoles(data);
    } catch (error) {
      console.error('Error fetching roles:', error);
    }
  };

  useEffect(() => {
    fetchRoles();
  }, []);

  const handleCreateRole = async () => {
    const userId = localStorage.getItem('X-User-ID');

    if (!newRole.name) {
      alert('Name is required');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/roles/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(newRole)
      });

      if (response.status === 201) {
        alert('Role created successfully');
        setNewRole({ name: '', description: '' });
        fetchRoles();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error('Error creating role:', err);
    }
  };

  const handleDeleteRole = async (roleId) => {
    const userId = localStorage.getItem('X-User-ID');

    try {
      const response = await fetch(`http://localhost:5000/roles/${roleId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        }
      });

      if (response.status === 204) {
        alert('Role deleted successfully');
        fetchRoles();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error('Error deleting role:', err);
    }
  };

  const handleEditRole = (roleItem) => {
    setEditRoleId(roleItem.id);
    setEditRoleData({ name: roleItem.name, description: roleItem.description });
  };

  const handleUpdateRole = async () => {
    const userId = localStorage.getItem('X-User-ID');

    try {
      const response = await fetch(`http://localhost:5000/roles/${editRoleId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(editRoleData)
      });

      if (response.ok) {
        alert('Role updated successfully');
        setEditRoleId(null);
        setEditRoleData({ name: '', description: '' });
        fetchRoles();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error('Error updating role:', err);
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Roles</h2>

      {role === 'Admin' && (
        <div className="mb-6 p-4 border rounded bg-gray-50">
          <h3 className="font-semibold mb-2">Create New Role</h3>
          <input
            type="text"
            placeholder="Role Name"
            value={newRole.name}
            onChange={(e) => setNewRole({ ...newRole, name: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="text"
            placeholder="Description"
            value={newRole.description}
            onChange={(e) => setNewRole({ ...newRole, description: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <button
            onClick={handleCreateRole}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Create Role
          </button>
        </div>
      )}

      <ul className="space-y-2">
        {roles.map((roleItem) => (
          <li key={roleItem.id} className="border p-2 rounded flex justify-between items-center">
            <div>
              <strong>{roleItem.name}</strong> — {roleItem.description}
            </div>
            {role === 'Admin' && (
              <div className="flex space-x-2">
                <button
                  onClick={() => handleEditRole(roleItem)}
                  className="bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteRole(roleItem.id)}
                  className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>

      {role === 'Admin' && editRoleId && (
        <div className="mt-6 p-4 border rounded bg-yellow-50">
          <h3 className="font-semibold mb-2">Edit Role</h3>
          <input
            type="text"
            placeholder="Role Name"
            value={editRoleData.name}
            onChange={(e) => setEditRoleData({ ...editRoleData, name: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <input
            type="text"
            placeholder="Description"
            value={editRoleData.description}
            onChange={(e) => setEditRoleData({ ...editRoleData, description: e.target.value })}
            className="border p-2 w-full mb-2"
          />
          <div className="flex space-x-2">
            <button
              onClick={handleUpdateRole}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Update
            </button>
            <button
              onClick={() => setEditRoleId(null)}
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

export default Roles;
