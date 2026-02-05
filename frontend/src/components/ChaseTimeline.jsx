import React, { useEffect, useState } from 'react';
import { Clock, Filter } from 'lucide-react';
import { getChaseItems } from '../utils/api';
import { formatDate } from '../utils/formatters';

export default function ChaseTimeline() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadItems();
  }, [filter]);

  const loadItems = async () => {
    try {
      const data = await getChaseItems({ status: filter === 'all' ? '' : filter });
      setItems(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={24} />
          Chase Timeline
        </h2>
        <select 
          value={filter} 
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
        >
          <option value="all">All Status</option>
          <option value="pending">Pending</option>
          <option value="sent">Sent</option>
          <option value="overdue">Overdue</option>
          <option value="received">Received</option>
        </select>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Target</th>
            <th>Type</th>
            <th>Description</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Sent Date</th>
            <th>Attempts</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>#{item.id}</td>
              <td>{item.target}</td>
              <td><span className="badge">{item.type}</span></td>
              <td>{item.description}</td>
              <td><span className={`badge badge-${item.status}`}>{item.status}</span></td>
              <td><span className={`badge badge-${item.priority}`}>{item.priority}</span></td>
              <td>{formatDate(item.sent_date)}</td>
              <td>{item.attempts}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
