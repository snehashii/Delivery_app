import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Roles from './pages/Roles';
import Login from './pages/Login';
import Users from './pages/Users';
import Deliveries from './pages/Deliveries';

function App() {
  return (
    <Router>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Delivery App Admin Panel</h1>
        <nav className="space-x-4 mb-6">
          <Link to="/login" className="text-blue-500 hover:underline">Login</Link>
          <Link to="/roles" className="text-blue-500 hover:underline">Roles</Link>
          <Link to="/users" className="text-blue-500 hover:underline">Users</Link>
           <Link to="/deliveries" className="text-blue-500 hover:underline">deliveries</Link>
        </nav>

        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/roles" element={<Roles />} />
          <Route path="/users" element={<Users />} />
          <Route path="/deliveries" element={<Deliveries />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
