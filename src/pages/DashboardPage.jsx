import React from 'react';
import { Trophy, Flame, BookmarkCheck, Calendar, ArrowRight, Sparkles } from 'lucide-react';
import QuestionCard from '../components/QuestionCard';
import ProgressBar from '../components/ProgressBar';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function DashboardPage({
  questions,
  currentDay,
  onSelectDay,
  onStatusChange,
  onSaveNote,
  onOpenReplaceModal,
  onNavigateTab,
  streak,
  userProfile
}) {
  const totalQuestions = questions.length;
  const completedCount = questions.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;
  const attemptedCount = questions.filter(q => q.status === DEFAULT_STATUSES.ATTEMPTED).length;
  const reviewCount = questions.filter(q => q.status === DEFAULT_STATUSES.NEED_REVIEW).length;

  // Days completed (all 3 questions solved)
  const completedDaysCount = Array.from({ length: 45 }, (_, i) => i + 1).filter(dayNum => {
    const dayQs = questions.filter(q => q.day === dayNum);
    return dayQs.length === 3 && dayQs.every(q => q.status === DEFAULT_STATUSES.SOLVED);
  }).length;

  const todayQuestions = questions.filter(q => q.day === currentDay);
  const todaySolved = todayQuestions.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;

  // Phase computation
  let currentPhase = 'Foundations & Pattern Recognition';
  let phaseRange = 'Days 1 — 10';
  let phaseDesc = 'Core patterns: Two Pointers, Sliding Window, Monotonic Stack, BFS/DFS.';
  if (currentDay > 10 && currentDay <= 20) {
    currentPhase = 'Pattern Building';
    phaseRange = 'Days 11 — 20';
    phaseDesc = 'Multi-pattern combinations, 2D Grid DP, Prefix Hashing, Shortest Paths.';
  } else if (currentDay > 20 && currentDay <= 30) {
    currentPhase = 'Intermediate Mastery';
    phaseRange = 'Days 21 — 30';
    phaseDesc = 'DSU, Trie searches, State Machine DP, Complex tree traversals.';
  } else if (currentDay > 30 && currentDay <= 38) {
    currentPhase = 'Advanced Problem Solving';
    phaseRange = 'Days 31 — 38';
    phaseDesc = 'Hard Graphs, Bellman-Ford/Tarjan, Tree DP, Interval DP, Hard Greedy.';
  } else if (currentDay > 38) {
    currentPhase = 'Interview Mode & Mixed Simulation';
    phaseRange = 'Days 39 — 45';
    phaseDesc = 'Mock interview conditions, multi-concept problems, timing.';
  }

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Welcome Banner - LeetCode Style */}
      <div className="glass-card" style={{
        padding: '20px 24px',
        marginBottom: '20px',
        background: '#262626',
        border: '1px solid #3A3A3A'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: '#FFA116', fontWeight: 600, marginBottom: '6px' }}>
              <Sparkles size={14} color="#FFA116" />
              <span>45-DAY DSA PLACEMENT PREPARATION</span>
            </div>
            <h1 style={{ fontSize: '1.5rem', marginBottom: '4px', color: '#F5F5F5' }}>
              {userProfile.username ? `Dashboard • @${userProfile.username}` : 'Placement Preparation Dashboard'}
            </h1>
            <p style={{ color: '#B3B3B3', fontSize: '0.875rem', maxWidth: '600px' }}>
              Systematic 3-problem daily topic rotation targeting high-frequency technical interview patterns.
            </p>
          </div>

          <div style={{
            padding: '10px 16px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #333333',
            textAlign: 'right'
          }}>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: '#FFA116', fontWeight: 600 }}>
              Current Phase: {phaseRange}
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#F5F5F5', marginTop: '2px' }}>
              {currentPhase}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#777777', marginTop: '2px' }}>
              {phaseDesc}
            </div>
          </div>
        </div>
      </div>

      {/* 4 Stat Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '14px',
        marginBottom: '24px'
      }}>
        {/* Stat 1: Total Solved */}
        <div className="glass-card" style={{ padding: '16px 18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: '#B3B3B3', fontWeight: 500 }}>Total Solved</span>
            <Trophy size={16} color="#FFA116" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 700, color: '#F5F5F5', marginBottom: '6px' }}>
            {completedCount} <span style={{ fontSize: '0.9rem', color: '#777777', fontWeight: 400 }}>/ {totalQuestions}</span>
          </div>
          <ProgressBar value={completedCount} max={totalQuestions} showPercentage={false} height={5} />
        </div>

        {/* Stat 2: Days Completed */}
        <div className="glass-card" style={{ padding: '16px 18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: '#B3B3B3', fontWeight: 500 }}>Days Completed</span>
            <Calendar size={16} color="#2CBB5D" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 700, color: '#F5F5F5', marginBottom: '6px' }}>
            {completedDaysCount} <span style={{ fontSize: '0.9rem', color: '#777777', fontWeight: 400 }}>/ 45</span>
          </div>
          <ProgressBar value={completedDaysCount} max={45} color="#2CBB5D" showPercentage={false} height={5} />
        </div>

        {/* Stat 3: Streak */}
        <div className="glass-card" style={{ padding: '16px 18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: '#B3B3B3', fontWeight: 500 }}>Active Streak</span>
            <Flame size={16} fill="#FFA116" color="#FFA116" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 700, color: '#FFA116', marginBottom: '6px' }}>
            {streak.current} Days
          </div>
          <div style={{ fontSize: '0.75rem', color: '#777777' }}>
            Longest Streak: <strong style={{ color: '#D4D4D4' }}>{streak.longest} Days</strong>
          </div>
        </div>

        {/* Stat 4: Review Queue */}
        <div
          className="glass-card"
          style={{ padding: '16px 18px', cursor: 'pointer' }}
          onClick={() => onNavigateTab('review')}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: '#B3B3B3', fontWeight: 500 }}>Review Queue</span>
            <BookmarkCheck size={16} color="#EF4743" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 700, color: reviewCount > 0 ? '#EF4743' : '#F5F5F5', marginBottom: '6px' }}>
            {reviewCount} <span style={{ fontSize: '0.9rem', color: '#777777', fontWeight: 400 }}>Problems</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: '#FFA116', display: 'flex', alignItems: 'center', gap: '4px' }}>
            Open Review Queue <ArrowRight size={12} />
          </div>
        </div>
      </div>

      {/* Today's Section Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '14px',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <h2 style={{ fontSize: '1.25rem', color: '#F5F5F5' }}>
            Day {currentDay} Questions
          </h2>
          <span style={{
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '2px 8px',
            borderRadius: 'var(--radius-sm)',
            background: todaySolved === 3 ? 'rgba(44, 187, 93, 0.12)' : 'rgba(255, 161, 22, 0.12)',
            color: todaySolved === 3 ? '#2CBB5D' : '#FFA116',
            border: `1px solid ${todaySolved === 3 ? 'rgba(44, 187, 93, 0.25)' : 'rgba(255, 161, 22, 0.25)'}`
          }}>
            {todaySolved} / 3 Completed
          </span>
        </div>

        <button
          onClick={() => onNavigateTab('today')}
          className="btn btn-secondary btn-sm"
        >
          Open Day View <ArrowRight size={13} />
        </button>
      </div>

      {/* Today's 3 Questions Cards */}
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {todayQuestions.map((q) => (
          <QuestionCard
            key={q.id}
            question={q}
            onStatusChange={onStatusChange}
            onSaveNote={onSaveNote}
            onOpenReplaceModal={onOpenReplaceModal}
          />
        ))}
      </div>
    </div>
  );
}
