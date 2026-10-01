import React from 'react';
import { BookmarkCheck, Check } from 'lucide-react';
import QuestionCard from '../components/QuestionCard';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function ReviewQueuePage({
  questions,
  onStatusChange,
  onSaveNote,
  onOpenReplaceModal,
  onNavigateTab
}) {
  const reviewQuestions = questions.filter(q => q.status === DEFAULT_STATUSES.NEED_REVIEW);

  return (
    <div className="page-wrapper animate-fade-in">
      {/* Header */}
      <div className="glass-card" style={{
        padding: '18px 22px',
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '14px',
        border: '1px solid #3A3A3A',
        background: '#262626'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: 36,
            height: 36,
            borderRadius: 'var(--radius-md)',
            background: 'rgba(239, 71, 67, 0.12)',
            border: '1px solid rgba(239, 71, 67, 0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#EF4743'
          }}>
            <BookmarkCheck size={20} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.4rem', marginBottom: '2px', color: '#F5F5F5' }}>
              Review Queue
            </h1>
            <p style={{ color: '#B3B3B3', fontSize: '0.84rem' }}>
              Questions flagged as requiring revision or tricky edge cases.
            </p>
          </div>
        </div>

        <div style={{
          padding: '4px 12px',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(239, 71, 67, 0.12)',
          border: '1px solid rgba(239, 71, 67, 0.3)',
          color: '#EF4743',
          fontWeight: 600,
          fontSize: '0.8125rem'
        }}>
          {reviewQuestions.length} Problems
        </div>
      </div>

      {/* Empty State */}
      {reviewQuestions.length === 0 ? (
        <div className="glass-card" style={{
          padding: '40px 20px',
          textAlign: 'center',
          maxWidth: '500px',
          margin: '30px auto'
        }}>
          <div style={{
            width: 44,
            height: 44,
            borderRadius: '50%',
            background: 'rgba(44, 187, 93, 0.12)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '12px',
            color: '#2CBB5D'
          }}>
            <Check size={22} />
          </div>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', color: '#F5F5F5' }}>
            Queue is Empty
          </h3>
          <p style={{ color: '#777777', fontSize: '0.84rem', marginBottom: '16px', lineHeight: '1.5' }}>
            Select <strong>"🔴 Need Review"</strong> on any question card during your daily practice to save it here for revision.
          </p>
          <button
            onClick={() => onNavigateTab('today')}
            className="btn btn-primary btn-sm"
          >
            Continue Practice
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {reviewQuestions.map((q) => (
            <div key={q.id} style={{ position: 'relative' }}>
              <div style={{
                display: 'flex',
                justifyContent: 'flex-end',
                marginBottom: '-8px',
                position: 'relative',
                zIndex: 10,
                paddingRight: '14px'
              }}>
                <button
                  onClick={() => onStatusChange(q.id, DEFAULT_STATUSES.SOLVED)}
                  className="btn btn-success btn-sm"
                >
                  <Check size={12} /> Mark Reviewed
                </button>
              </div>
              <QuestionCard
                question={q}
                onStatusChange={onStatusChange}
                onSaveNote={onSaveNote}
                onOpenReplaceModal={onOpenReplaceModal}
                showDayBadge={true}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
