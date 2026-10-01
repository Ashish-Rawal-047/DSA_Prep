import React, { useState } from 'react';
import { CheckCircle2, Circle, Filter } from 'lucide-react';
import DifficultyBadge from '../components/DifficultyBadge';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function PlanPage({
  questions,
  currentDay,
  onSelectDay,
  onNavigateTab
}) {
  const [filterMode, setFilterMode] = useState('all');

  const daysData = Array.from({ length: 45 }, (_, i) => {
    const dayNum = i + 1;
    const dayQs = questions.filter(q => q.day === dayNum);
    const solvedCount = dayQs.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;
    const isComplete = dayQs.length === 3 && solvedCount === 3;
    const topics = Array.from(new Set(dayQs.map(q => q.topic)));
    
    const hasHard = dayQs.some(q => q.difficulty === 'Hard');
    const allEasy = dayQs.every(q => q.difficulty === 'Easy');
    const dayDifficulty = hasHard ? 'Hard' : allEasy ? 'Easy' : 'Medium';

    return {
      day: dayNum,
      questions: dayQs,
      solvedCount,
      isComplete,
      topics,
      dayDifficulty,
      isCurrent: dayNum === currentDay
    };
  });

  const filteredDays = daysData.filter(d => {
    if (filterMode === 'completed') return d.isComplete;
    if (filterMode === 'pending') return !d.isComplete;
    return true;
  });

  const completedDaysCount = daysData.filter(d => d.isComplete).length;

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>
            45-Day Preparation Schedule
          </h1>
          <p style={{ color: '#B3B3B3', fontSize: '0.85rem' }}>
            135 curated interview problems rotating topics across 45 structured days.
          </p>
        </div>

        {/* Filter buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ fontSize: '0.75rem', color: '#777777', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Filter size={13} /> Filter:
          </span>
          <button
            onClick={() => setFilterMode('all')}
            className={`btn btn-sm ${filterMode === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          >
            All (45)
          </button>
          <button
            onClick={() => setFilterMode('completed')}
            className={`btn btn-sm ${filterMode === 'completed' ? 'btn-primary' : 'btn-secondary'}`}
          >
            Completed ({completedDaysCount})
          </button>
          <button
            onClick={() => setFilterMode('pending')}
            className={`btn btn-sm ${filterMode === 'pending' ? 'btn-primary' : 'btn-secondary'}`}
          >
            Pending ({45 - completedDaysCount})
          </button>
        </div>
      </div>

      {/* Grid of Days (LeetCode Style) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '14px'
      }}>
        {filteredDays.map((d) => {
          return (
            <div
              key={d.day}
              onClick={() => {
                onSelectDay(d.day);
                onNavigateTab('today');
              }}
              style={{
                padding: '14px 16px',
                cursor: 'pointer',
                borderRadius: 'var(--radius-md)',
                border: d.isCurrent
                  ? '1px solid #FFA116'
                  : d.isComplete
                  ? '1px solid rgba(44, 187, 93, 0.3)'
                  : '1px solid #3A3A3A',
                background: d.isCurrent
                  ? 'rgba(255, 161, 22, 0.06)'
                  : '#262626',
                transition: 'background var(--transition-fast), border-color var(--transition-fast)'
              }}
              onMouseEnter={(e) => {
                if (!d.isCurrent) {
                  e.currentTarget.style.backgroundColor = '#2F2F2F';
                  e.currentTarget.style.borderColor = '#555555';
                }
              }}
              onMouseLeave={(e) => {
                if (!d.isCurrent) {
                  e.currentTarget.style.backgroundColor = '#262626';
                  e.currentTarget.style.borderColor = d.isComplete ? 'rgba(44, 187, 93, 0.3)' : '#3A3A3A';
                }
              }}
            >
              {/* Day Header */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '8px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{
                    fontSize: '0.9rem',
                    fontWeight: 700,
                    color: d.isCurrent ? '#FFA116' : '#F5F5F5',
                    fontFamily: 'var(--font-mono)'
                  }}>
                    Day {d.day}
                  </span>
                  {d.isCurrent && (
                    <span style={{
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      padding: '1px 5px',
                      borderRadius: 'var(--radius-sm)',
                      background: '#FFA116',
                      color: '#1A1A1A'
                    }}>
                      ACTIVE
                    </span>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <DifficultyBadge difficulty={d.dayDifficulty} />
                  {d.isComplete ? (
                    <span style={{ color: '#2CBB5D', display: 'flex', alignItems: 'center', gap: '3px', fontSize: '0.78rem', fontWeight: 600 }}>
                      <CheckCircle2 size={14} /> 3/3
                    </span>
                  ) : (
                    <span style={{ color: '#777777', fontSize: '0.78rem', fontWeight: 500 }}>
                      {d.solvedCount}/3
                    </span>
                  )}
                </div>
              </div>

              {/* Topics chips (Neutral LeetCode) */}
              <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginBottom: '10px' }}>
                {d.topics.map((t) => (
                  <span
                    key={t}
                    style={{
                      fontSize: '0.7rem',
                      fontWeight: 500,
                      padding: '1px 6px',
                      borderRadius: 'var(--radius-sm)',
                      background: '#333333',
                      border: '1px solid #3A3A3A',
                      color: '#B3B3B3'
                    }}
                  >
                    {t}
                  </span>
                ))}
              </div>

              {/* 3 Questions preview */}
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '4px',
                borderTop: '1px solid #333333',
                paddingTop: '8px'
              }}>
                {d.questions.map((q) => {
                  const isQSolved = q.status === DEFAULT_STATUSES.SOLVED;
                  return (
                    <div
                      key={q.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        fontSize: '0.78rem',
                        color: isQSolved ? '#777777' : '#B3B3B3'
                      }}
                    >
                      <span style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        maxWidth: '220px'
                      }}>
                        {isQSolved ? (
                          <CheckCircle2 size={12} color="#2CBB5D" />
                        ) : (
                          <Circle size={12} color="#555555" />
                        )}
                        <span style={{ textDecoration: isQSolved ? 'line-through' : 'none' }}>
                          {q.title}
                        </span>
                      </span>
                      <span style={{
                        fontSize: '0.68rem',
                        color: q.difficulty === 'Hard' ? '#EF4743' : q.difficulty === 'Medium' ? '#FFA116' : '#2CBB5D',
                        fontWeight: 600
                      }}>
                        {q.difficulty[0]}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Progress bar */}
              <div style={{ marginTop: '8px' }}>
                <div style={{
                  height: 3,
                  width: '100%',
                  background: '#3A3A3A',
                  borderRadius: 'var(--radius-full)',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(d.solvedCount / 3) * 100}%`,
                    height: '100%',
                    background: d.isComplete ? '#2CBB5D' : '#FFA116'
                  }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
