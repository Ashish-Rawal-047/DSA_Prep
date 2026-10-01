import React, { useState } from 'react';
import { Code2, ChevronDown, ChevronUp, Copy, Check, Clock, Cpu } from 'lucide-react';

export default function SolutionPanel({ approach, complexity, solution }) {
  const [isRevealed, setIsRevealed] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(solution);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{
      marginTop: '8px',
      borderRadius: 'var(--radius-md)',
      border: '1px solid #3A3A3A',
      background: isRevealed ? '#1E1E1E' : '#282828',
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
          <Code2 size={15} color={isRevealed || isHovered ? '#FFA116' : '#888888'} />
          {isRevealed ? '💻 Solution (C++)' : '💻 Show Solution (C++)'}
        </span>
        {isRevealed ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
      </button>

      {isRevealed && (
        <div className="animate-fade-in" style={{
          padding: '14px',
          borderTop: '1px solid #2D2D2D',
          backgroundColor: '#1E1E1E'
        }}>
          {/* Approach & Intuition */}
          {approach && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{
                fontSize: '0.75rem',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
                color: '#FFA116',
                fontWeight: 600,
                marginBottom: '4px'
              }}>
                Approach & Key Idea
              </div>
              <p style={{ fontSize: '0.84rem', color: '#B3B3B3', lineHeight: '1.55' }}>
                {approach}
              </p>
            </div>
          )}

          {/* Complexity */}
          {complexity && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '6px 10px',
              background: '#262626',
              borderRadius: 'var(--radius-sm)',
              marginBottom: '12px',
              border: '1px solid #333333',
              fontSize: '0.78rem'
            }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#FFA116' }}>
                <Clock size={13} />
                <span style={{ fontFamily: 'var(--font-mono)' }}>{complexity}</span>
              </span>
            </div>
          )}

          {/* C++ Code Box */}
          <div className="code-block" style={{ background: '#181818', border: '1px solid #2D2D2D' }}>
            <div className="code-header">
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#888888' }}>
                <Cpu size={13} /> C++20 Solution
              </span>
              <button
                onClick={handleCopy}
                className="btn btn-secondary btn-sm"
                style={{
                  padding: '3px 8px',
                  fontSize: '0.72rem',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  background: '#282828',
                  border: '1px solid #3A3A3A'
                }}
              >
                {copied ? <Check size={12} color="#2CBB5D" /> : <Copy size={12} />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <pre style={{ margin: 0, fontFamily: 'var(--font-mono)', fontSize: '0.8125rem' }}>
              <code>{solution}</code>
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
