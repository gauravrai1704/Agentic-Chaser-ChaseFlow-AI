import React, { useEffect, useState } from 'react';
import { Bot, Activity, CheckCircle, AlertCircle } from 'lucide-react';
import { getAgentStatuses, getActivities } from '../utils/api';
import { formatRelativeTime } from '../utils/formatters';

export default function AgentMonitor() {
  const [agents, setAgents] = useState([]);
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const statuses = await getAgentStatuses();
      const acts = await getActivities(50);
      setAgents(statuses);
      setActivities(acts);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <div className="card">
        <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Bot size={24} />
          Active Agents
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
          {agents.map(agent => (
            <div key={agent.agent_id} style={{
              padding: '20px',
              border: '2px solid #e5e7eb',
              borderRadius: '8px',
              background: agent.status === 'active' ? '#f0fdf4' : 'white'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                <strong>{agent.agent_type.replace('_', ' ').toUpperCase()}</strong>
                <span className={`badge ${agent.status === 'active' ? 'badge-received' : 'badge-pending'}`}>
                  {agent.status}
                </span>
              </div>
              <div style={{ fontSize: '14px', color: '#6b7280' }}>
                <div>Last Action: {agent.last_action || 'None'}</div>
                <div>Items Processed: {agent.items_processed}</div>
                {agent.last_action_time && (
                  <div style={{ marginTop: '8px', fontSize: '12px' }}>
                    {formatRelativeTime(agent.last_action_time)}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={24} />
          Live Activity Stream
        </h2>
        <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
          {activities.map(activity => (
            <div key={activity.id} style={{
              padding: '16px',
              borderBottom: '1px solid #e5e7eb',
              display: 'flex',
              gap: '12px',
              alignItems: 'start'
            }}>
              {activity.status === 'success' ? 
                <CheckCircle size={20} color="#10b981" /> : 
                <AlertCircle size={20} color="#ef4444" />
              }
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: '600', marginBottom: '4px' }}>
                  {activity.agent_type} • {activity.action}
                </div>
                <div style={{ fontSize: '14px', color: '#6b7280' }}>
                  Target: {activity.target}
                </div>
                <div style={{ fontSize: '12px', color: '#9ca3af', marginTop: '4px' }}>
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
