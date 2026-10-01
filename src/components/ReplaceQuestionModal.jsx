import React, { useState } from 'react';
import { RefreshCw, X, Check, AlertCircle } from 'lucide-react';
import DifficultyBadge from './DifficultyBadge';
import TopicBadge from './TopicBadge';

export default function ReplaceQuestionModal({
  currentQuestion,
  candidates = [],
  onClose,
  onConfirmReplace
}) {
  const [selectedCandidateId, setSelectedCandidateId] = useState(
    candidates.length > 0 ? candidates[0].id : null
  );

  if (!currentQuestion) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(3px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '16px'
    }}>
      <div style={{
        maxWidth: '540px',
        width: '100%',
        backgroundColor: '#202020',
        border: '1px solid #3A3A3A',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        boxShadow: '0 12px 30px rgba(0, 0, 0, 0.7)'
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '14px 20px',
          borderBottom: '1px solid #333333',
          background: '#1A1A1A'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <RefreshCw size={16} color="#FFA116" />
            <h3 style={{ fontSize: '0.95rem', color: '#F5F5F5' }}>Replace Question</h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: '#888888', cursor: 'pointer', padding: '4px' }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Current Question Info */}
        <div style={{ padding: '16px 20px' }}>
          <div style={{
            padding: '12px 14px',
            borderRadius: 'var(--radius-md)',
            background: '#262626',
            border: '1px solid #3A3A3A',
            borderLeft: '3px solid #EF4743',
            marginBottom: '16px'
          }}>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: '#EF4743', fontWeight: 600, marginBottom: '3px' }}>
              Current Problem:
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#F5F5F5', marginBottom: '6px' }}>
              {currentQuestion.title}
            </div>
            <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
              <DifficultyBadge difficulty={currentQuestion.difficulty} />
              <TopicBadge topic={currentQuestion.topic} subtopic={currentQuestion.subtopic} />
            </div>
          </div>

          {/* Replacement candidates */}
          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, marginBottom: '8px', color: '#D4D4D4' }}>
              Select Replacement Candidate:
            </div>

            {candidates.length === 0 ? (
              <div style={{
                padding: '14px',
                textAlign: 'center',
                color: '#777777',
                borderRadius: 'var(--radius-md)',
                background: '#1E1E1E',
                border: '1px dashed #3A3A3A',
                fontSize: '0.825rem'
              }}>
                <AlertCircle size={20} style={{ margin: '0 auto 6px', color: '#FFA116' }} />
                No remaining candidates for this topic and difficulty.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '250px', overflowY: 'auto' }}>
                {candidates.map((cand) => {
                  const isSelected = selectedCandidateId === cand.id;
                  return (
                    <div
                      key={cand.id}
                      onClick={() => setSelectedCandidateId(cand.id)}
                      style={{
                        padding: '10px 14px',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid',
                        borderColor: isSelected ? '#FFA116' : '#333333',
                        background: isSelected ? 'rgba(255, 161, 22, 0.08)' : '#262626',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        transition: 'border-color var(--transition-fast)'
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: 600, color: '#F5F5F5', fontSize: '0.875rem', marginBottom: '3px' }}>
                          {cand.title}
                        </div>
                        <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                          <DifficultyBadge difficulty={cand.difficulty} />
                          <TopicBadge topic={cand.topic} subtopic={cand.subtopic} />
                          <span className="badge badge-pattern">{cand.pattern}</span>
                        </div>
                      </div>
                      <div style={{
                        width: 16,
                        height: 16,
                        borderRadius: '50%',
                        border: '1px solid',
                        borderColor: isSelected ? '#FFA116' : '#777777',
                        backgroundColor: isSelected ? '#FFA116' : 'transparent',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        {isSelected && <Check size={10} color="#1A1A1A" strokeWidth={3} />}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Footer actions */}
        <div style={{
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '10px',
          padding: '12px 20px',
          borderTop: '1px solid #333333',
          background: '#1A1A1A'
        }}>
          <button onClick={onClose} className="btn btn-secondary btn-sm">
            Cancel
          </button>
          <button
            onClick={() => {
              if (selectedCandidateId) {
                onConfirmReplace(currentQuestion.id, selectedCandidateId);
              }
            }}
            disabled={!selectedCandidateId || candidates.length === 0}
            className="btn btn-primary btn-sm"
          >
            <RefreshCw size={12} />
            Replace Problem
          </button>
        </div>
      </div>
    </div>
  );
}
