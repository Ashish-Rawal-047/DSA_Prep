import React from 'react';

export default function ProgressBar({
  value = 0,
  max = 100,
  label = '',
  sublabel = '',
  color = '#FFA116',
  height = 6,
  showPercentage = true,
}) {
  const percentage = max > 0 ? Math.min(100, Math.max(0, (value / max) * 100)) : 0;
  const formattedPct = percentage.toFixed(1);

  return (
    <div style={{ width: '100%' }}>
      {(label || showPercentage || sublabel) && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
          marginBottom: '5px',
          fontSize: '0.8125rem'
        }}>
          <div>
            {label && <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{label}</span>}
            {sublabel && (
              <span style={{ marginLeft: '8px', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                {sublabel}
              </span>
            )}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
              {value} / {max}
            </span>
            {showPercentage && (
              <span style={{ fontWeight: 600, color: 'var(--text-primary)', minWidth: '40px', textAlign: 'right', fontSize: '0.8rem' }}>
                {formattedPct}%
              </span>
            )}
          </div>
        </div>
      )}
      <div style={{
        width: '100%',
        height: `${height}px`,
        backgroundColor: '#3A3A3A',
        borderRadius: 'var(--radius-full)',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          background: color,
          borderRadius: 'var(--radius-full)',
          transition: 'width 0.3s ease'
        }} />
      </div>
    </div>
  );
}
