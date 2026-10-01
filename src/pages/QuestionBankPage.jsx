import React, { useState, useMemo } from 'react';
import { Search, Filter, RotateCcw } from 'lucide-react';
import QuestionCard from '../components/QuestionCard';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function QuestionBankPage({
  questions,
  onStatusChange,
  onSaveNote,
  onOpenReplaceModal
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('ALL');
  const [selectedDifficulty, setSelectedDifficulty] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [selectedPattern, setSelectedPattern] = useState('ALL');
  const [selectedDay, setSelectedDay] = useState('ALL');

  // Extract filter options dynamically
  const topics = useMemo(() => {
    return ['ALL', ...Array.from(new Set(questions.map(q => q.topic))).sort()];
  }, [questions]);

  const patterns = useMemo(() => {
    return ['ALL', ...Array.from(new Set(questions.map(q => q.pattern))).sort()];
  }, [questions]);

  const filteredQuestions = useMemo(() => {
    return questions.filter(q => {
      // Text search
      if (searchTerm.trim()) {
        const term = searchTerm.toLowerCase();
        const matchTitle = q.title.toLowerCase().includes(term);
        const matchTopic = q.topic.toLowerCase().includes(term);
        const matchSubtopic = (q.subtopic || '').toLowerCase().includes(term);
        const matchPattern = q.pattern.toLowerCase().includes(term);
        const matchNote = (q.notes || '').toLowerCase().includes(term);
        if (!matchTitle && !matchTopic && !matchSubtopic && !matchPattern && !matchNote) {
          return false;
        }
      }

      // Topic filter
      if (selectedTopic !== 'ALL' && q.topic !== selectedTopic) return false;

      // Difficulty filter
      if (selectedDifficulty !== 'ALL' && q.difficulty !== selectedDifficulty) return false;

      // Status filter
      if (selectedStatus !== 'ALL' && q.status !== selectedStatus) return false;

      // Pattern filter
      if (selectedPattern !== 'ALL' && q.pattern !== selectedPattern) return false;

      // Day filter
      if (selectedDay !== 'ALL' && q.day !== Number(selectedDay)) return false;

      return true;
    });
  }, [questions, searchTerm, selectedTopic, selectedDifficulty, selectedStatus, selectedPattern, selectedDay]);

  const handleResetFilters = () => {
    setSearchTerm('');
    setSelectedTopic('ALL');
    setSelectedDifficulty('ALL');
    setSelectedStatus('ALL');
    setSelectedPattern('ALL');
    setSelectedDay('ALL');
  };

  return (
    <div className="page-wrapper animate-fade-in">
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', marginBottom: '4px' }}>
          Question Bank & Filter Engine
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Instantly filter and search through all 135 curated interview problems.
        </p>
      </div>

      {/* Search & Filter Bar */}
      <div className="glass-card" style={{ padding: '20px', marginBottom: '24px' }}>
        {/* Search input */}
        <div style={{ position: 'relative', marginBottom: '16px' }}>
          <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by problem name, topic, pattern, or keyword..."
            className="input-control"
            style={{ paddingLeft: '40px', fontSize: '0.95rem' }}
          />
        </div>

        {/* Filters Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '12px',
          alignItems: 'center'
        }}>
          {/* Topic */}
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Topic:
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.825rem' }}
            >
              {topics.map(t => (
                <option key={t} value={t}>{t === 'ALL' ? 'All Topics' : t}</option>
              ))}
            </select>
          </div>

          {/* Difficulty */}
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Difficulty:
            </label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.825rem' }}
            >
              <option value="ALL">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          {/* Status */}
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Status:
            </label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.825rem' }}
            >
              <option value="ALL">All Statuses</option>
              <option value={DEFAULT_STATUSES.NOT_STARTED}>⚪ Not Started</option>
              <option value={DEFAULT_STATUSES.ATTEMPTED}>🟡 Attempted</option>
              <option value={DEFAULT_STATUSES.SOLVED}>🟢 Solved</option>
              <option value={DEFAULT_STATUSES.NEED_REVIEW}>🔴 Need Review</option>
            </select>
          </div>

          {/* Pattern */}
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Pattern:
            </label>
            <select
              value={selectedPattern}
              onChange={(e) => setSelectedPattern(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.825rem' }}
            >
              {patterns.map(p => (
                <option key={p} value={p}>{p === 'ALL' ? 'All Patterns' : p}</option>
              ))}
            </select>
          </div>

          {/* Day */}
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Day:
            </label>
            <select
              value={selectedDay}
              onChange={(e) => setSelectedDay(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.825rem' }}
            >
              <option value="ALL">All Days (1 - 45)</option>
              {Array.from({ length: 45 }, (_, i) => i + 1).map(d => (
                <option key={d} value={d}>Day {d}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Clear Filters */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px', paddingTop: '12px', borderTop: '1px solid var(--border-primary)' }}>
          <span style={{ fontSize: '0.825rem', color: 'var(--text-secondary)' }}>
            Showing <strong>{filteredQuestions.length}</strong> of {questions.length} questions
          </span>
          <button
            onClick={handleResetFilters}
            className="btn btn-secondary btn-sm"
          >
            <RotateCcw size={13} /> Reset Filters
          </button>
        </div>
      </div>

      {/* Filtered Questions List */}
      <div>
        {filteredQuestions.length === 0 ? (
          <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            No questions match your current search and filter combination.
          </div>
        ) : (
          filteredQuestions.map(q => (
            <QuestionCard
              key={q.id}
              question={q}
              onStatusChange={onStatusChange}
              onSaveNote={onSaveNote}
              onOpenReplaceModal={onOpenReplaceModal}
              showDayBadge={true}
            />
          ))
        )}
      </div>
    </div>
  );
}
