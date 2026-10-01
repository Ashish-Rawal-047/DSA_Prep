import React from 'react';
import { ChevronLeft, ChevronRight, CheckCircle2, Award } from 'lucide-react';
import QuestionCard from '../components/QuestionCard';
import ProgressBar from '../components/ProgressBar';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function TodayQuestionsPage({
  questions,
  currentDay,
  onSelectDay,
  onStatusChange,
  onSaveNote,
  onOpenReplaceModal,
  onTriggerDailyComplete
}) {
  const todayQuestions = questions.filter(q => q.day === currentDay);
  const solvedCount = todayQuestions.filter(q => q.status === DEFAULT_STATUSES.SOLVED).length;
  const isDayFullyComplete = todayQuestions.length === 3 && solvedCount === 3;

  const handlePrevDay = () => {
    if (currentDay > 1) onSelectDay(currentDay - 1);
  };

  const handleNextDay = () => {
    if (currentDay < 45) onSelectDay(currentDay + 1);
  };

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Day Navigation Header */}
      <div className="glass-card" style={{
        padding: '16px 20px',
        marginBottom: '18px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            onClick={handlePrevDay}
            disabled={currentDay === 1}
            className="btn btn-secondary btn-icon"
            title="Previous Day"
            style={{ opacity: currentDay === 1 ? 0.35 : 1 }}
          >
            <ChevronLeft size={16} />
          </button>

          <div>
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.04em', color: '#FFA116', fontWeight: 600 }}>
              45-DAY CURRICULUM
            </div>
            <h1 style={{ fontSize: '1.4rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              Day {currentDay} Preparation
              {isDayFullyComplete && (
                <span style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  padding: '2px 8px',
                  borderRadius: 'var(--radius-sm)',
                  background: 'rgba(44, 187, 93, 0.12)',
                  color: '#2CBB5D',
                  border: '1px solid rgba(44, 187, 93, 0.25)'
                }}>
                  <CheckCircle2 size={12} /> Completed
                </span>
              )}
            </h1>
          </div>

          <button
            onClick={handleNextDay}
            disabled={currentDay === 45}
            className="btn btn-secondary btn-icon"
            title="Next Day"
            style={{ opacity: currentDay === 45 ? 0.35 : 1 }}
          >
            <ChevronRight size={16} />
          </button>
        </div>

        {/* Day completion trigger button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {isDayFullyComplete && (
            <button
              onClick={onTriggerDailyComplete}
              className="btn btn-success btn-sm"
            >
              <Award size={14} />
              Day {currentDay} Summary
            </button>
          )}
        </div>
      </div>

      {/* Daily Progress Bar */}
      <div className="glass-card" style={{ padding: '12px 16px', marginBottom: '18px' }}>
        <ProgressBar
          value={solvedCount}
          max={3}
          label={`Day ${currentDay} Progress`}
          color={isDayFullyComplete ? '#2CBB5D' : '#FFA116'}
          height={6}
        />
      </div>

      {/* Questions list */}
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {todayQuestions.map((q, idx) => (
          <div key={q.id}>
            <div style={{
              fontSize: '0.75rem',
              fontWeight: 600,
              color: '#777777',
              marginBottom: '5px',
              textTransform: 'uppercase',
              letterSpacing: '0.04em'
            }}>
              Question {idx + 1} of 3 • {q.topic}
            </div>
            <QuestionCard
              question={q}
              onStatusChange={onStatusChange}
              onSaveNote={onSaveNote}
              onOpenReplaceModal={onOpenReplaceModal}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
