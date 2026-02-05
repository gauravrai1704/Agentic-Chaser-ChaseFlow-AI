import React, { useEffect, useState } from 'react';
import { Users } from 'lucide-react';
import { api } from '../utils/api';

export default function ClientList() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      const data = await api.get('/clients');
      setClients(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Users size={24} />
        Clients ({clients.length})
      </h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Risk Profile</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {clients.map(client => (
            <tr key={client.id}>
              <td><strong>{client.name}</strong></td>
              <td>{client.email}</td>
              <td>{client.phone}</td>
              <td><span className="badge">{client.risk_profile}</span></td>
              <td><span className={`badge badge-${client.status}`}>{client.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
