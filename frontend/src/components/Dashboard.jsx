import React, { useEffect, useState } from 'react';
import { TrendingUp, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { getChaseItems, getActivities } from '../utils/api';
import { formatRelativeTime } from '../utils/formatters';

export default function Dashboard({ stats }) {
  const [recentItems, setRecentItems] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const items = await getChaseItems({ limit: 10 });
      const activities = await getActivities(10);
      setRecentItems(items);
      setRecentActivities(activities);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <h3>Total Chase Items</h3>
          <div className="value">{stats?.total_chase_items || 0}</div>
          <div>Across all clients</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
          <h3>Pending Items</h3>
          <div className="value">{stats?.pending_items || 0}</div>
          <div>Awaiting response</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
          <h3>Avg Completion</h3>
          <div className="value">{stats?.avg_completion_days || 0}<span style={{ fontSize: '18px' }}>d</span></div>
          <div>Days to complete</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
          <h3>Automation Rate</h3>
          <div className="value">{stats?.automation_rate || 0}<span style={{ fontSize: '18px' }}>%</span></div>
          <div>Tasks automated</div>
        </div>
      </div>

      {/* Recent Chase Items */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={24} />
          Recent Chase Items
        </h2>
        <table>
          <thead>
            <tr>
              <th>Target</th>
              <th>Type</th>
              <th>Description</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Attempts</th>
            </tr>
          </thead>
          <tbody>
            {recentItems.map(item => (
              <tr key={item.id}>
                <td>{item.target}</td>
                <td>{item.type}</td>
                <td>{item.description}</td>
                <td><span className={`badge badge-${item.status}`}>{item.status}</span></td>
                <td><span className={`badge badge-${item.priority}`}>{item.priority}</span></td>
                <td>{item.attempts}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recent Agent Activities */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <TrendingUp size={24} />
          Recent Agent Activities
        </h2>
        <div>
          {recentActivities.map(activity => (
            <div key={activity.id} style={{
              padding: '12px',
              borderBottom: '1px solid #e5e7eb',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <strong>{activity.agent_type}</strong> - {activity.action}
                <div style={{ fontSize: '14px', color: '#6b7280', marginTop: '4px' }}>
                  {activity.target}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span className={`badge badge-${activity.status}`}>{activity.status}</span>
                <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>
                  {formatRelativeTime(activity.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
