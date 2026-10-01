import React, { useState } from 'react';
import { ExternalLink, ChevronRight, CheckCircle2 } from 'lucide-react';
import DifficultyBadge from '../components/DifficultyBadge';
import ProgressBar from '../components/ProgressBar';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function TopicsPage({
  questions,
  onSelectDay,
  onNavigateTab
}) {
  const topicsMap = {};
  questions.forEach(q => {
    if (!topicsMap[q.topic]) {
      topicsMap[q.topic] = {
        name: q.topic,
        questions: [],
        completed: 0,
        patterns: new Set()
      };
    }
    topicsMap[q.topic].questions.push(q);
    topicsMap[q.topic].patterns.add(q.pattern);
    if (q.status === DEFAULT_STATUSES.SOLVED) {
      topicsMap[q.topic].completed++;
    }
  });

  const topicList = Object.values(topicsMap).sort((a, b) => b.questions.length - a.questions.length);
  const [selectedTopic, setSelectedTopic] = useState(topicList[0]?.name || 'Dynamic Programming');

  const activeTopicData = topicsMap[selectedTopic] || topicList[0];

  return (
    <div className="page-wrapper animate-fade-in">
      <div style={{ marginBottom: '20px' }}>
        <h1 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>
          DSA Topic Explorer
        </h1>
        <p style={{ color: '#B3B3B3', fontSize: '0.85rem' }}>
          Explore curated interview problems organized by topic domain.
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'minmax(240px, 280px) 1fr',
        gap: '18px',
        alignItems: 'start'
      }}>
        {/* Left: Topic Selector List */}
        <div className="glass-card" style={{ padding: '12px', maxHeight: '680px', overflowY: 'auto' }}>
          <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: '#777777', fontWeight: 600, padding: '4px 8px 8px' }}>
            All Topics ({topicList.length})
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {topicList.map(t => {
              const isSelected = selectedTopic === t.name;
              const pct = ((t.completed / t.questions.length) * 100).toFixed(0);

              return (
                <button
                  key={t.name}
                  onClick={() => setSelectedTopic(t.name)}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    padding: '8px 10px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid',
                    borderColor: isSelected ? '#FFA116' : '#333333',
                    background: isSelected ? 'rgba(255, 161, 22, 0.08)' : '#262626',
                    cursor: 'pointer',
                    transition: 'border-color var(--transition-fast)',
                    textAlign: 'left'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 500, color: isSelected ? '#FFA116' : '#F5F5F5', fontSize: '0.84rem' }}>
                      {t.name}
                    </span>
                    <span style={{
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      color: t.completed === t.questions.length ? '#2CBB5D' : '#777777',
                      fontFamily: 'var(--font-mono)'
                    }}>
                      {t.completed}/{t.questions.length} ({pct}%)
                    </span>
                  </div>
                  <ProgressBar
                    value={t.completed}
                    max={t.questions.length}
                    showPercentage={false}
                    color={t.completed === t.questions.length ? '#2CBB5D' : '#FFA116'}
                    height={3}
                  />
                </button>
              );
            })}
          </div>
        </div>

        {/* Right: Detailed Questions in Selected Topic */}
        {activeTopicData && (
          <div className="glass-card" style={{ padding: '20px' }}>
            {/* Topic Header */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              paddingBottom: '14px',
              borderBottom: '1px solid #333333',
              marginBottom: '16px',
              flexWrap: 'wrap',
              gap: '10px'
            }}>
              <div>
                <span style={{ fontSize: '0.72rem', color: '#FFA116', fontWeight: 600, textTransform: 'uppercase' }}>
                  Topic Domain
                </span>
                <h2 style={{ fontSize: '1.35rem', color: '#F5F5F5' }}>{activeTopicData.name}</h2>
              </div>
              <div style={{
                padding: '4px 10px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(255, 161, 22, 0.1)',
                border: '1px solid rgba(255, 161, 22, 0.25)',
                color: '#FFA116',
                fontWeight: 600,
                fontSize: '0.8125rem'
              }}>
                {activeTopicData.completed} / {activeTopicData.questions.length} Solved
              </div>
            </div>

            {/* Patterns */}
            <div style={{ marginBottom: '16px' }}>
              <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: '#777777', fontWeight: 600, marginBottom: '6px' }}>
                Patterns in {activeTopicData.name}:
              </div>
              <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                {Array.from(activeTopicData.patterns).map(p => (
                  <span key={p} className="badge badge-pattern">
                    {p}
                  </span>
                ))}
              </div>
            </div>

            {/* Questions Table */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {activeTopicData.questions.map(q => {
                const isSolved = q.status === DEFAULT_STATUSES.SOLVED;

                return (
                  <div
                    key={q.id}
                    style={{
                      padding: '10px 14px',
                      borderRadius: 'var(--radius-md)',
                      background: '#202020',
                      border: '1px solid #333333',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      flexWrap: 'wrap',
                      gap: '10px'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '3px' }}>
                        {isSolved ? (
                          <CheckCircle2 size={15} color="#2CBB5D" />
                        ) : (
                          <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#666666' }} />
                        )}
                        <span style={{ fontWeight: 500, color: '#F5F5F5', fontSize: '0.875rem' }}>
                          {q.title}
                        </span>
                        <DifficultyBadge difficulty={q.difficulty} />
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#777777', display: 'flex', gap: '8px' }}>
                        <span>Day {q.day}</span>
                        <span>•</span>
                        <span style={{ color: '#B3B3B3' }}>{q.pattern}</span>
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <a
                        href={q.leetcodeUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-leetcode btn-sm"
                      >
                        Solve <ExternalLink size={11} />
                      </a>
                      <button
                        onClick={() => {
                          onSelectDay(q.day);
                          onNavigateTab('today');
                        }}
                        className="btn btn-secondary btn-sm"
                      >
                        Day {q.day} <ChevronRight size={11} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
