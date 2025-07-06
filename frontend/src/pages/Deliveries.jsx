import React, { useEffect, useState } from 'react';

const Deliveries = () => {
  const [deliveries, setDeliveries] = useState([]);
  const [newDelivery, setNewDelivery] = useState({ order_id: '', rider_id: '', status: '', tracking_id: '' });
  const [editId, setEditId] = useState(null);
  const [editData, setEditData] = useState({ order_id: '', rider_id: '', status: '', tracking_id: '' });
  const [role, setRole] = useState('');
  const [userId, setUserId] = useState('');
  const [riders, setRiders] = useState([]);

  useEffect(() => {
    const uid = localStorage.getItem('X-User-ID');
    const roleName = localStorage.getItem('Role');
    setUserId(uid);
    setRole(roleName);
    fetchDeliveries(uid, roleName);
    fetchRiders();
  }, []);

  const fetchDeliveries = async (uid, roleName) => {
    try {
      const res = await fetch('http://localhost:5000/deliveries/', {
        headers: { 'X-User-ID': uid }
      });
      const data = await res.json();

      if (roleName === 'Manager' || roleName === 'Rider') {
        const filtered = data.filter((d) => d.rider_id?.toString() === uid);
        setDeliveries(filtered);
      } else {
        setDeliveries(data);
      }
    } catch (err) {
      console.error('Error fetching deliveries:', err);
    }
  };

  const fetchRiders = async () => {
    try {
      const res = await fetch('http://localhost:5000/riders/', {
        headers: { 'X-User-ID': userId }
      });
      const data = await res.json();
      setRiders(data);
    } catch (err) {
      console.error('Error fetching riders:', err);
    }
  };

  const handleCreate = async () => {
    if (!newDelivery.order_id || !newDelivery.status || !newDelivery.tracking_id) {
      alert('Please fill all required fields');
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/deliveries/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(newDelivery)
      });

      if (res.status === 201) {
        alert('Delivery created');
        setNewDelivery({ order_id: '', rider_id: '', status: '', tracking_id: '' });
        fetchDeliveries(userId, role);
      } else {
        const err = await res.json();
        alert(`Error: ${err.error}`);
      }
    } catch (err) {
      console.error('Error creating delivery:', err);
    }
  };

  const handleEdit = (delivery) => {
    setEditId(delivery.id);
    setEditData({
      order_id: delivery.order_id,
      rider_id: delivery.rider_id || '',
      status: delivery.status,
      tracking_id: delivery.tracking_id
    });
  };

  const handleUpdate = async () => {
    try {
      const res = await fetch(`http://localhost:5000/deliveries/${editId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId
        },
        body: JSON.stringify(editData)
      });

      if (res.ok) {
        alert('Delivery updated');
        setEditId(null);
        setEditData({ order_id: '', rider_id: '', status: '', tracking_id: '' });
        fetchDeliveries(userId, role);
      } else {
        const err = await res.json();
        alert(`Error: ${err.error}`);
      }
    } catch (err) {
      console.error('Error updating delivery:', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`http://localhost:5000/deliveries/${id}`, {
        method: 'DELETE',
        headers: {
          'X-User-ID': userId
        }
      });

      if (res.status === 204) {
        alert('Deleted');
        fetchDeliveries(userId, role);
      } else {
        const err = await res.json();
        alert(`Error: ${err.error}`);
      }
    } catch (err) {
      console.error('Error deleting delivery:', err);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Deliveries</h2>

      {role === 'Admin' && (
        <div className="mb-6 p-4 border rounded bg-gray-100">
          <h3 className="font-semibold mb-2">Create Delivery</h3>
          <input
            placeholder="Order ID"
            className="border p-2 w-full mb-2"
            value={newDelivery.order_id}
            onChange={(e) => setNewDelivery({ ...newDelivery, order_id: e.target.value })}
          />
          <select
            className="border p-2 w-full mb-2"
            value={newDelivery.rider_id}
            onChange={(e) => setNewDelivery({ ...newDelivery, rider_id: e.target.value })}
          >
            <option value="">Select Rider</option>
            {riders.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
          <select
            className="border p-2 w-full mb-2"
            value={newDelivery.status}
            onChange={(e) => setNewDelivery({ ...newDelivery, status: e.target.value })}
          >
            <option value="">Select Status</option>
            <option value="assigned">Assigned</option>
            <option value="in-progress">In Progress</option>
            <option value="done">Done</option>
            <option value="outsourced">Outsourced</option>
          </select>
          <input
            placeholder="Tracking ID"
            className="border p-2 w-full mb-2"
            value={newDelivery.tracking_id}
            onChange={(e) => setNewDelivery({ ...newDelivery, tracking_id: e.target.value })}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            onClick={handleCreate}
          >
            Create
          </button>
        </div>
      )}

      <ul className="space-y-2">
        {deliveries.map((d) => (
          <li key={d.id} className="border p-3 rounded flex justify-between items-center">
            <div>
              <strong>Order:</strong> {d.order_id} | <strong>Status:</strong> {d.status}{' '}
              | <strong>Tracking:</strong> {d.tracking_id} | <strong>Rider:</strong> {d.rider_name}
            </div>
            {role === 'Admin' && (
              <div className="space-x-2">
                <button
                  onClick={() => handleEdit(d)}
                  className="bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(d.id)}
                  className="bg-red-600 text-white px-2 py-1 rounded hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>

      {editId && (
        <div className="mt-6 p-4 border rounded bg-yellow-50">
          <h3 className="font-semibold mb-2">Edit Delivery</h3>
          <input
            placeholder="Order ID"
            className="border p-2 w-full mb-2"
            value={editData.order_id}
            onChange={(e) => setEditData({ ...editData, order_id: e.target.value })}
          />
          <select
            className="border p-2 w-full mb-2"
            value={editData.rider_id}
            onChange={(e) => setEditData({ ...editData, rider_id: e.target.value })}
          >
            <option value="">Select Rider</option>
            {riders.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
          <select
            className="border p-2 w-full mb-2"
            value={editData.status}
            onChange={(e) => setEditData({ ...editData, status: e.target.value })}
          >
            <option value="">Select Status</option>
            <option value="assigned">Assigned</option>
            <option value="in-progress">In Progress</option>
            <option value="done">Done</option>
            <option value="outsourced">Outsourced</option>
          </select>
          <input
            placeholder="Tracking ID"
            className="border p-2 w-full mb-2"
            value={editData.tracking_id}
            onChange={(e) => setEditData({ ...editData, tracking_id: e.target.value })}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mr-2"
            onClick={handleUpdate}
          >
            Update
          </button>
          <button
            onClick={() => setEditId(null)}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
};

export default Deliveries;
