import React from 'react';

export default function TopicBadge({ topic, subtopic }) {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
      <span className="badge badge-topic">
        {topic}
      </span>
      {subtopic && (
        <span style={{
          fontSize: '0.72rem',
          color: 'var(--text-muted)',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          • {subtopic}
        </span>
      )}
    </div>
  );
}
