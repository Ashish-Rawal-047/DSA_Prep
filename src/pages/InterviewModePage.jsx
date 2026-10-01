import React, { useState, useEffect } from 'react';
import { Timer, Play, Pause, RotateCcw, ExternalLink, CheckCircle2, Lock, Unlock, Eye } from 'lucide-react';
import DifficultyBadge from '../components/DifficultyBadge';
import TopicBadge from '../components/TopicBadge';
import HintPanel from '../components/HintPanel';
import SolutionPanel from '../components/SolutionPanel';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function InterviewModePage({
  questions,
  currentDay,
  onStatusChange,
  onSaveNote
}) {
  // Filter interview-mode eligible questions (Days 39-45 by default, or all hard/medium problems)
  const interviewQuestions = questions.filter(q => q.day >= 39);
  const [selectedQuestionId, setSelectedQuestionId] = useState(interviewQuestions[0]?.id || questions[0]?.id);

  const activeQuestion = questions.find(q => q.id === selectedQuestionId) || interviewQuestions[0];

  // Timer states
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [hasUnlockedSpoilers, setHasUnlockedSpoilers] = useState(false);
  const [interviewResult, setInterviewResult] = useState(null); // 'solved', 'attempted', null

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds(s => s + 1);
      }, 1000);
    } else if (!isActive && seconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, seconds]);

  const handleStartTimer = () => setIsActive(true);
  const handlePauseTimer = () => setIsActive(false);
  const handleResetTimer = () => {
    setIsActive(false);
    setSeconds(0);
    setHasUnlockedSpoilers(false);
    setInterviewResult(null);
  };

  const handleMarkSolved = () => {
    setIsActive(false);
    setHasUnlockedSpoilers(true);
    setInterviewResult('solved');
    onStatusChange(activeQuestion.id, DEFAULT_STATUSES.SOLVED);
  };

  const handleMarkAttempted = () => {
    setIsActive(false);
    setHasUnlockedSpoilers(true);
    setInterviewResult('attempted');
    onStatusChange(activeQuestion.id, DEFAULT_STATUSES.ATTEMPTED);
  };

  const formatTime = (totalSec) => {
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Header */}
      <div className="glass-card" style={{
        padding: '24px 28px',
        marginBottom: '24px',
        border: '1px solid var(--border-primary)',
        background: 'var(--card-bg)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-orange)', fontWeight: 700, fontSize: '0.8rem', textTransform: 'uppercase', marginBottom: '6px' }}>
              <Timer size={16} />
              <span>Realistic Interview Simulation Mode (Days 39 — 45)</span>
            </div>
            <h1 style={{ fontSize: '1.75rem', marginBottom: '4px' }}>
              Mock Technical Interview
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Timed problem solving with hidden hints and solutions. Simulate real 45-minute live coding conditions.
            </p>
          </div>

          {/* Quick problem select dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Select Challenge:</span>
            <select
              value={selectedQuestionId}
              onChange={(e) => {
                setSelectedQuestionId(Number(e.target.value));
                handleResetTimer();
              }}
              className="input-control"
              style={{ minWidth: '220px', fontSize: '0.85rem' }}
            >
              {interviewQuestions.map(q => (
                <option key={q.id} value={q.id}>
                  Day {q.day}: {q.title} ({q.difficulty})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Interview Workspace */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
        {/* Top: Timer Display & Controls */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          borderRadius: 'var(--radius-lg)',
          background: 'var(--bg-editor)',
          border: '1px solid var(--border-primary)',
          marginBottom: '24px'
        }}>
          <div style={{ fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700, letterSpacing: '0.06em', marginBottom: '6px' }}>
            Elapsed Interview Clock
          </div>
          <div style={{
            fontSize: '3.6rem',
            fontWeight: 800,
            fontFamily: 'var(--font-mono)',
            color: isActive ? 'var(--accent-orange)' : 'var(--text-primary)',
            letterSpacing: '0.05em',
            marginBottom: '16px'
          }}>
            {formatTime(seconds)}
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            {!isActive ? (
              <button onClick={handleStartTimer} className="btn btn-leetcode" style={{ padding: '9px 20px', fontWeight: 600 }}>
                <Play size={16} fill="currentColor" /> Start Timer
              </button>
            ) : (
              <button onClick={handlePauseTimer} className="btn btn-secondary" style={{ padding: '9px 20px' }}>
                <Pause size={16} fill="currentColor" /> Pause Timer
              </button>
            )}
            <button onClick={handleResetTimer} className="btn btn-secondary" style={{ padding: '9px 16px' }}>
              <RotateCcw size={16} /> Reset
            </button>
          </div>
        </div>

        {/* Problem Card Content */}
        {activeQuestion && (
          <div>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '12px' }}>
              <span className="badge badge-topic">Day {activeQuestion.day}</span>
              <DifficultyBadge difficulty={activeQuestion.difficulty} />
              <TopicBadge topic={activeQuestion.topic} subtopic={activeQuestion.subtopic} />
            </div>

            <h2 style={{ fontSize: '1.45rem', marginBottom: '16px', color: 'var(--text-primary)' }}>
              {activeQuestion.title}
            </h2>

            {/* Pattern Card */}
            <div style={{
              padding: '16px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-primary)',
              marginBottom: '24px'
            }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--accent-orange)', fontWeight: 600, marginBottom: '6px' }}>
                Target Pattern: {activeQuestion.pattern}
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                {activeQuestion.whyItMatters}
              </p>
            </div>

            {/* Actions for Candidates */}
            <div style={{
              display: 'flex',
              gap: '12px',
              flexWrap: 'wrap',
              marginBottom: '28px',
              padding: '16px 0',
              borderTop: '1px solid var(--border-primary)',
              borderBottom: '1px solid var(--border-primary)'
            }}>
              <a
                href={activeQuestion.leetcodeUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-leetcode btn-lg"
              >
                Solve on LeetCode <ExternalLink size={16} />
              </a>

              <button
                onClick={handleMarkSolved}
                className="btn btn-solved btn-lg"
              >
                <CheckCircle2 size={18} /> I Solved It
              </button>

              <button
                onClick={handleMarkAttempted}
                className="btn btn-secondary btn-lg"
              >
                Finished Attempt
              </button>

              {!hasUnlockedSpoilers && (
                <button
                  onClick={() => setHasUnlockedSpoilers(true)}
                  className="btn btn-secondary btn-lg"
                  style={{ marginLeft: 'auto' }}
                >
                  <Unlock size={16} /> Reveal Hint / Solution
                </button>
              )}
            </div>

            {/* Interview Result Feedback */}
            {interviewResult === 'solved' && (
              <div className="animate-fade-in" style={{
                padding: '16px 20px',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(44, 187, 93, 0.12)',
                border: '1px solid rgba(44, 187, 93, 0.3)',
                color: 'var(--success)',
                fontWeight: 600,
                marginBottom: '24px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
              }}>
                <CheckCircle2 size={20} />
                Great job! Challenge marked solved in {formatTime(seconds)}. Full solution and explanation unlocked below.
              </div>
            )}

            {/* Hint & Solution Panels (locked until finished or explicitly revealed) */}
            {hasUnlockedSpoilers ? (
              <div className="animate-fade-in">
                <HintPanel hint={activeQuestion.hint} />
                <SolutionPanel
                  approach={activeQuestion.approach}
                  complexity={activeQuestion.complexity}
                  solution={activeQuestion.solution}
                />
              </div>
            ) : (
              <div style={{
                padding: '24px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-secondary)',
                border: '1px dashed var(--border-primary)',
                textAlign: 'center',
                color: 'var(--text-muted)'
              }}>
                <Lock size={28} style={{ margin: '0 auto 8px', color: 'var(--text-muted)' }} />
                <div style={{ fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '4px' }}>
                  Hints & Solutions are Locked
                </div>
                <div style={{ fontSize: '0.825rem' }}>
                  Click "I Solved It" or "Reveal Hint / Solution" above when you are ready to review the official editorial.
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
