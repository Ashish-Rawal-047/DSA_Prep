import React from 'react';
import { Map, ArrowDown, CheckCircle2, ChevronRight } from 'lucide-react';
import ProgressBar from '../components/ProgressBar';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function RoadmapPage({
  questions,
  currentDay,
  onSelectDay,
  onNavigateTab
}) {
  const phases = [
    {
      id: 1,
      title: 'FOUNDATIONS & PATTERN RECOGNITION',
      days: 'Day 1 — Day 10',
      startDay: 1,
      endDay: 10,
      description: 'Pattern recognition, Medium problems, reinforcing core mechanics: Two Pointers, Sliding Window, Monotonic Stack, BFS/DFS Flood Fill, Binary Search on Answer, Prefix Sum with Hashing.',
      tag: 'Core Patterns'
    },
    {
      id: 2,
      title: 'PATTERN BUILDING & COMBINATIONS',
      days: 'Day 11 — Day 20',
      startDay: 11,
      endDay: 20,
      description: 'Medium to Medium-Hard problems combining multiple patterns: Graph BFS with Queues, LIS Binary Search, Matrix Elimination, Backtracking with Pruning, Dijkstra Shortest Path, State Machine DP.',
      tag: 'Multi-Pattern'
    },
    {
      id: 3,
      title: 'INTERMEDIATE MASTERY',
      days: 'Day 21 — Day 30',
      startDay: 21,
      endDay: 30,
      description: 'Union Find (DSU), Trie prefix trees with wildcards, Boundary Connected Components, 2D Grid DP with Obstacles, Greedy Interval Scheduling, LRU Cache system design.',
      tag: 'Complex Structures'
    },
    {
      id: 4,
      title: 'ADVANCED ALGORITHMIC ARCHITECTURE',
      days: 'Day 31 — Day 38',
      startDay: 31,
      endDay: 38,
      description: 'Cheapest Flights (Bellman-Ford / K-step), Tarjan’s Bridges, Tree DP & Binary Tree Cameras, Burst Balloons (Interval DP), Median of Two Sorted Arrays, Word Ladder.',
      tag: 'Advanced Algorithms'
    },
    {
      id: 5,
      title: 'INTERVIEW SIMULATION & CAPSTONES',
      days: 'Day 39 — Day 45',
      startDay: 39,
      endDay: 45,
      description: 'Full mock interview simulation: 45-minute timed challenges, multi-concept problems (Word Search II, Course Schedule III, Smallest Range from K Lists, Day 45 Grand Finale: Graph + DP + Tree).',
      tag: 'Interview Simulation'
    },
  ];

  return (
    <div className="page-wrapper animate-fade-in">
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', marginBottom: '4px' }}>
          45-Day Technical Roadmap
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Visual progression path navigating from pattern recognition to full interview mastery.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '900px', margin: '0 auto' }}>
        {phases.map((phase, idx) => {
          const phaseQuestions = questions.filter(q => q.day >= phase.startDay && q.day <= phase.endDay);
          const solvedInPhase = phaseQuestions.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;
          const isPhaseComplete = phaseQuestions.length > 0 && solvedInPhase === phaseQuestions.length;
          const isCurrentPhase = currentDay >= phase.startDay && currentDay <= phase.endDay;

          return (
            <React.Fragment key={phase.id}>
              <div className="glass-card" style={{
                padding: '24px',
                border: isCurrentPhase
                  ? '2px solid var(--accent-orange)'
                  : isPhaseComplete
                  ? '1px solid rgba(44, 187, 93, 0.4)'
                  : '1px solid var(--border-primary)',
                background: isCurrentPhase
                  ? 'rgba(255, 161, 22, 0.04)'
                  : isPhaseComplete
                  ? 'rgba(44, 187, 93, 0.03)'
                  : 'var(--card-bg)',
                borderRadius: 'var(--radius-lg)',
                position: 'relative'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '14px', marginBottom: '14px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <span style={{
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        padding: '3px 10px',
                        borderRadius: 'var(--radius-sm)',
                        background: isCurrentPhase
                          ? 'rgba(255, 161, 22, 0.15)'
                          : isPhaseComplete
                          ? 'rgba(44, 187, 93, 0.15)'
                          : 'var(--bg-tertiary)',
                        color: isCurrentPhase
                          ? 'var(--accent-orange)'
                          : isPhaseComplete
                          ? 'var(--success)'
                          : 'var(--text-secondary)',
                        border: isCurrentPhase
                          ? '1px solid rgba(255, 161, 22, 0.3)'
                          : isPhaseComplete
                          ? '1px solid rgba(44, 187, 93, 0.3)'
                          : '1px solid var(--border-primary)'
                      }}>
                        PHASE {phase.id} • {phase.days}
                      </span>
                      {isCurrentPhase && (
                        <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#1A1A1A', background: 'var(--accent-orange)', padding: '2px 8px', borderRadius: 'var(--radius-sm)' }}>
                          CURRENT PHASE
                        </span>
                      )}
                      {isPhaseComplete && (
                        <span style={{ color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem', fontWeight: 700 }}>
                          <CheckCircle2 size={16} /> Completed
                        </span>
                      )}
                    </div>

                    <h2 style={{ fontSize: '1.25rem', color: 'var(--text-primary)' }}>
                      {phase.title}
                    </h2>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>
                      {solvedInPhase} / {phaseQuestions.length}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Questions Solved</div>
                  </div>
                </div>

                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: '1.6', marginBottom: '18px' }}>
                  {phase.description}
                </p>

                {/* Progress bar */}
                <div style={{ marginBottom: '16px' }}>
                  <ProgressBar
                    value={solvedInPhase}
                    max={phaseQuestions.length}
                    color={isPhaseComplete ? 'var(--success)' : 'var(--accent-orange)'}
                    showPercentage={true}
                    height={6}
                  />
                </div>

                {/* Day pills */}
                <div style={{
                  display: 'flex',
                  gap: '8px',
                  flexWrap: 'wrap',
                  paddingTop: '14px',
                  borderTop: '1px solid var(--border-primary)'
                }}>
                  {Array.from({ length: phase.endDay - phase.startDay + 1 }, (_, i) => {
                    const dayNum = phase.startDay + i;
                    const dayQs = questions.filter(q => q.day === dayNum);
                    const isDayDone = dayQs.length === 3 && dayQs.every(q => q.status === DEFAULT_STATUSES.SOLVED);
                    const isDayCurrent = dayNum === currentDay;

                    return (
                      <button
                        key={dayNum}
                        onClick={() => {
                          onSelectDay(dayNum);
                          onNavigateTab('today');
                        }}
                        style={{
                          padding: '6px 12px',
                          borderRadius: 'var(--radius-sm)',
                          border: isDayCurrent
                            ? '1px solid var(--accent-orange)'
                            : isDayDone
                            ? '1px solid rgba(44, 187, 93, 0.4)'
                            : '1px solid var(--border-primary)',
                          background: isDayCurrent
                            ? 'var(--accent-orange)'
                            : isDayDone
                            ? 'rgba(44, 187, 93, 0.12)'
                            : 'var(--bg-secondary)',
                          color: isDayCurrent ? '#1A1A1A' : isDayDone ? 'var(--success)' : 'var(--text-secondary)',
                          fontSize: '0.8rem',
                          fontWeight: 600,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '5px'
                        }}
                      >
                        {isDayDone && <CheckCircle2 size={12} />}
                        Day {dayNum}
                      </button>
                    );
                  })}
                </div>
              </div>

              {idx < phases.length - 1 && (
                <div style={{ display: 'flex', justifyContent: 'center', color: 'var(--text-muted)' }}>
                  <div style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: 'var(--bg-secondary)',
                    border: '1px solid var(--border-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text-muted)'
                  }}>
                    <ArrowDown size={16} />
                  </div>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
