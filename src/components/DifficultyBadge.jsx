import React from 'react';

export default function DifficultyBadge({ difficulty }) {
  const diffLower = (difficulty || 'medium').toLowerCase();
  
  let label = difficulty;
  let badgeClass = 'badge-medium';

  if (diffLower === 'easy') {
    badgeClass = 'badge-easy';
    label = 'Easy';
  } else if (diffLower === 'hard') {
    badgeClass = 'badge-hard';
    label = 'Hard';
  } else {
    badgeClass = 'badge-medium';
    label = 'Medium';
  }

  return (
    <span className={`badge ${badgeClass}`}>
      <span style={{
        display: 'inline-block',
        width: 6,
        height: 6,
        borderRadius: '50%',
        backgroundColor: 'currentColor'
      }} />
      {label}
    </span>
  );
}
