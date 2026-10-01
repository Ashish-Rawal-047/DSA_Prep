import React, { useState } from 'react';
import { Lightbulb, ChevronDown, ChevronUp } from 'lucide-react';

export default function HintPanel({ hint }) {
  const [isRevealed, setIsRevealed] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div style={{
      marginTop: '10px',
      borderRadius: 'var(--radius-md)',
      border: '1px solid #3A3A3A',
      borderLeft: isRevealed ? '2px solid #FFA116' : '1px solid #3A3A3A',
      background: isRevealed ? '#202020' : '#282828',
      overflow: 'hidden',
      transition: 'background var(--transition-fast)'
    }}>
      <button
        onClick={() => setIsRevealed(!isRevealed)}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 12px',
          background: 'none',
          border: 'none',
          color: (isHovered || isRevealed) ? '#FFA116' : '#D4D4D4',
          cursor: 'pointer',
          fontSize: '0.8125rem',
          fontWeight: 500,
          textAlign: 'left'
        }}
      >
        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Lightbulb size={15} color={isRevealed || isHovered ? '#FFA116' : '#888888'} />
          {isRevealed ? '💡 Hint Revealed' : '💡 Show Hint'}
        </span>
        {isRevealed ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
      </button>

      {isRevealed && (
        <div className="animate-fade-in" style={{
          padding: '10px 14px 12px',
          borderTop: '1px solid #2D2D2D',
          color: '#B3B3B3',
          fontSize: '0.84rem',
          lineHeight: '1.55',
          backgroundColor: '#1C1C1C'
        }}>
          <p style={{ color: '#E0E0E0' }}>
            {hint}
          </p>
        </div>
      )}
    </div>
  );
}
