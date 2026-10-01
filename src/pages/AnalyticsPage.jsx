import React from 'react';
import { BarChart3, PieChart, Layers, Flame, Trophy } from 'lucide-react';
import ProgressBar from '../components/ProgressBar';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function AnalyticsPage({
  questions,
  streak
}) {
  const total = questions.length;
  const completed = questions.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;
  const attempted = questions.filter(q => q.status === DEFAULT_STATUSES.ATTEMPTED).length;
  const remaining = total - completed;
  const overallPct = ((completed / total) * 100).toFixed(1);

  // Difficulty breakdown (LeetCode colors: Easy Green, Medium Orange, Hard Red)
  const diffStats = {
    Easy: { total: 0, completed: 0 },
    Medium: { total: 0, completed: 0 },
    Hard: { total: 0, completed: 0 }
  };

  questions.forEach(q => {
    const d = q.difficulty || 'Medium';
    if (!diffStats[d]) diffStats[d] = { total: 0, completed: 0 };
    diffStats[d].total++;
    if (q.status === DEFAULT_STATUSES.SOLVED) {
      diffStats[d].completed++;
    }
  });

  // Topic breakdown
  const topicMap = {};
  questions.forEach(q => {
    const t = q.topic;
    if (!topicMap[t]) topicMap[t] = { total: 0, completed: 0 };
    topicMap[t].total++;
    if (q.status === DEFAULT_STATUSES.SOLVED) {
      topicMap[t].completed++;
    }
  });

  const topicList = Object.entries(topicMap).map(([topic, data]) => ({
    topic,
    total: data.total,
    completed: data.completed,
    remaining: data.total - data.completed,
    percentage: ((data.completed / data.total) * 100).toFixed(1)
  })).sort((a, b) => b.total - a.total);

  // Pattern breakdown
  const patternMap = {};
  questions.forEach(q => {
    const p = q.pattern;
    if (!patternMap[p]) patternMap[p] = { total: 0, completed: 0 };
    patternMap[p].total++;
    if (q.status === DEFAULT_STATUSES.SOLVED) {
      patternMap[p].completed++;
    }
  });

  const patternList = Object.entries(patternMap).map(([pattern, data]) => ({
    pattern,
    total: data.total,
    completed: data.completed,
    percentage: ((data.completed / data.total) * 100).toFixed(1)
  })).sort((a, b) => b.total - a.total);

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Header */}
      <div style={{ marginBottom: '22px' }}>
        <h1 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>
          Preparation Analytics
        </h1>
        <p style={{ color: '#B3B3B3', fontSize: '0.85rem' }}>
          Progress metrics calculated from recorded problem status.
        </p>
      </div>

      {/* Overview Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '14px',
        marginBottom: '20px'
      }}>
        {/* Questions Solved Card */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#777777', fontWeight: 600, marginBottom: '6px' }}>
            Questions Solved
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#F5F5F5', marginBottom: '6px' }}>
            {completed} <span style={{ fontSize: '1rem', color: '#777777', fontWeight: 400 }}>/ {total}</span>
          </div>
          <ProgressBar value={completed} max={total} color="#FFA116" height={6} />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#777777', marginTop: '6px' }}>
            <span>Remaining: {remaining}</span>
            <span>Attempted: {attempted}</span>
          </div>
        </div>

        {/* Practice Streak Card */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#777777', fontWeight: 600, marginBottom: '6px' }}>
            Practice Streak
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '1.8rem', fontWeight: 700, color: '#FFA116', marginBottom: '6px' }}>
            <Flame size={24} fill="#FFA116" />
            {streak.current} <span style={{ fontSize: '1rem', color: '#777777', fontWeight: 400 }}>Days</span>
          </div>
          <div style={{ fontSize: '0.78rem', color: '#B3B3B3' }}>
            Longest Streak: <strong style={{ color: '#F5F5F5' }}>{streak.longest} Days</strong>
          </div>
        </div>

        {/* Completion Percentage */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#777777', fontWeight: 600, marginBottom: '6px' }}>
            Overall Coverage
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#2CBB5D', marginBottom: '6px' }}>
            {overallPct}%
          </div>
          <div style={{ fontSize: '0.78rem', color: '#B3B3B3' }}>
            {completed >= 100 ? 'Advanced interview readiness' :
             completed >= 50 ? 'Steady progress' :
             'Foundations underway'}
          </div>
        </div>
      </div>

      {/* Difficulty Breakdown (LeetCode Colors) */}
      <div className="glass-card" style={{ padding: '20px', marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.05rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px', color: '#F5F5F5' }}>
          <Layers size={16} color="#FFA116" />
          Difficulty Breakdown
        </h3>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '14px'
        }}>
          {/* Easy */}
          <div style={{
            padding: '12px 14px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #333333',
            borderLeft: '3px solid #2CBB5D'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontWeight: 600, color: '#2CBB5D', fontSize: '0.84rem' }}>Easy</span>
              <span style={{ fontSize: '0.75rem', color: '#B3B3B3' }}>
                {diffStats.Easy.completed} / {diffStats.Easy.total}
              </span>
            </div>
            <ProgressBar
              value={diffStats.Easy.completed}
              max={diffStats.Easy.total}
              color="#2CBB5D"
              height={5}
            />
          </div>

          {/* Medium */}
          <div style={{
            padding: '12px 14px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #333333',
            borderLeft: '3px solid #FFA116'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontWeight: 600, color: '#FFA116', fontSize: '0.84rem' }}>Medium</span>
              <span style={{ fontSize: '0.75rem', color: '#B3B3B3' }}>
                {diffStats.Medium.completed} / {diffStats.Medium.total}
              </span>
            </div>
            <ProgressBar
              value={diffStats.Medium.completed}
              max={diffStats.Medium.total}
              color="#FFA116"
              height={5}
            />
          </div>

          {/* Hard */}
          <div style={{
            padding: '12px 14px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #333333',
            borderLeft: '3px solid #EF4743'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontWeight: 600, color: '#EF4743', fontSize: '0.84rem' }}>Hard</span>
              <span style={{ fontSize: '0.75rem', color: '#B3B3B3' }}>
                {diffStats.Hard.completed} / {diffStats.Hard.total}
              </span>
            </div>
            <ProgressBar
              value={diffStats.Hard.completed}
              max={diffStats.Hard.total}
              color="#EF4743"
              height={5}
            />
          </div>
        </div>
      </div>

      {/* Two Columns: Topic-Wise Progress & Pattern Tracking */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))',
        gap: '18px'
      }}>
        {/* Topic-Wise Progress */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <h3 style={{ fontSize: '1.05rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px', color: '#F5F5F5' }}>
            <BarChart3 size={16} color="#FFA116" />
            Topic Coverage
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '420px', overflowY: 'auto', paddingRight: '4px' }}>
            {topicList.map(t => (
              <div key={t.topic}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3px', fontSize: '0.8125rem' }}>
                  <span style={{ fontWeight: 500, color: '#F5F5F5' }}>{t.topic}</span>
                  <div style={{ display: 'flex', gap: '8px', fontSize: '0.75rem' }}>
                    <span style={{ color: '#777777' }}>{t.completed}/{t.total}</span>
                    <span style={{ fontWeight: 600, color: t.completed === t.total ? '#2CBB5D' : '#FFA116' }}>
                      {t.percentage}%
                    </span>
                  </div>
                </div>
                <ProgressBar
                  value={t.completed}
                  max={t.total}
                  showPercentage={false}
                  color={t.completed === t.total ? '#2CBB5D' : '#FFA116'}
                  height={5}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Pattern Tracking */}
        <div className="glass-card" style={{ padding: '18px' }}>
          <h3 style={{ fontSize: '1.05rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px', color: '#F5F5F5' }}>
            <PieChart size={16} color="#FFA116" />
            Patterns Tracked
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '420px', overflowY: 'auto', paddingRight: '4px' }}>
            {patternList.slice(0, 16).map(p => (
              <div key={p.pattern} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '8px 10px',
                borderRadius: 'var(--radius-md)',
                background: '#202020',
                border: '1px solid #333333',
                fontSize: '0.8rem'
              }}>
                <span style={{ fontFamily: 'var(--font-mono)', color: '#D4D4D4' }}>
                  {p.pattern}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ color: '#777777', fontSize: '0.75rem' }}>
                    {p.completed} / {p.total}
                  </span>
                  <span style={{
                    fontSize: '0.7rem',
                    fontWeight: 600,
                    padding: '1px 5px',
                    borderRadius: 'var(--radius-sm)',
                    background: p.completed === p.total && p.total > 0 ? 'rgba(44, 187, 93, 0.15)' : '#2A2A2A',
                    color: p.completed === p.total && p.total > 0 ? '#2CBB5D' : '#A0A0A0'
                  }}>
                    {p.percentage}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
