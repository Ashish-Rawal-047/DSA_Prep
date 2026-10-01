import React, { useState } from 'react';
import { ExternalLink, Check, MoreVertical, Sparkles, Edit3, Save } from 'lucide-react';
import DifficultyBadge from './DifficultyBadge';
import TopicBadge from './TopicBadge';
import HintPanel from './HintPanel';
import SolutionPanel from './SolutionPanel';
import { DEFAULT_STATUSES } from '../services/storageService';

export default function QuestionCard({
  question,
  onStatusChange,
  onSaveNote,
  onOpenReplaceModal,
  showDayBadge = false
}) {
  const [noteText, setNoteText] = useState(question.notes || '');
  const [isEditingNote, setIsEditingNote] = useState(false);
  const [noteSavedFeedback, setNoteSavedFeedback] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  const handleSaveNote = () => {
    onSaveNote(question.id, noteText);
    setNoteSavedFeedback(true);
    setIsEditingNote(false);
    setTimeout(() => setNoteSavedFeedback(false), 2000);
  };

  const isSolved = question.status === DEFAULT_STATUSES.SOLVED;

  // Status color mapper
  const getStatusColor = (status) => {
    if (status === DEFAULT_STATUSES.SOLVED) return '#2CBB5D';
    if (status === DEFAULT_STATUSES.ATTEMPTED) return '#FFA116';
    if (status === DEFAULT_STATUSES.NEED_REVIEW) return '#EF4743';
    return '#777777';
  };

  return (
    <div className="glass-card animate-fade-in" style={{
      padding: '18px 20px',
      marginBottom: '14px',
      border: isSolved ? '1px solid rgba(44, 187, 93, 0.28)' : '1px solid #3A3A3A',
      background: '#262626',
      borderRadius: 'var(--radius-lg)',
      position: 'relative'
    }}>
      {/* Top Meta Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '10px',
        gap: '10px',
        flexWrap: 'wrap'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {showDayBadge && (
            <span style={{
              fontSize: '0.72rem',
              fontWeight: 700,
              padding: '2px 7px',
              borderRadius: 'var(--radius-sm)',
              background: '#333333',
              color: '#FFA116',
              fontFamily: 'var(--font-mono)'
            }}>
              DAY {question.day}
            </span>
          )}
          <DifficultyBadge difficulty={question.difficulty} />
          <TopicBadge topic={question.topic} subtopic={question.subtopic} />
        </div>

        {/* Top Right Actions & Status Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Status Dropdown (LeetCode Colors) */}
          <select
            value={question.status}
            onChange={(e) => onStatusChange(question.id, e.target.value)}
            style={{
              padding: '4px 8px',
              fontSize: '0.78rem',
              fontWeight: 600,
              borderRadius: 'var(--radius-sm)',
              background: '#282828',
              color: getStatusColor(question.status),
              border: '1px solid #3A3A3A',
              cursor: 'pointer',
              outline: 'none'
            }}
          >
            <option value={DEFAULT_STATUSES.NOT_STARTED}>⚪ Not Started</option>
            <option value={DEFAULT_STATUSES.ATTEMPTED}>🟡 Attempted</option>
            <option value={DEFAULT_STATUSES.SOLVED}>🟢 Solved</option>
            <option value={DEFAULT_STATUSES.NEED_REVIEW}>🔴 Need Review</option>
          </select>

          {/* Options Menu (Replace Question) */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="btn btn-secondary btn-icon"
              title="Question Options"
              style={{ padding: '5px', background: '#282828', border: '1px solid #3A3A3A' }}
            >
              <MoreVertical size={14} color="#A0A0A0" />
            </button>

            {showMenu && (
              <div style={{
                position: 'absolute',
                right: 0,
                top: '110%',
                background: '#282828',
                border: '1px solid #444444',
                borderRadius: 'var(--radius-md)',
                boxShadow: '0 8px 20px rgba(0,0,0,0.6)',
                zIndex: 50,
                minWidth: '170px',
                overflow: 'hidden'
              }}>
                <button
                  onClick={() => {
                    setShowMenu(false);
                    onOpenReplaceModal(question);
                  }}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    textAlign: 'left',
                    background: 'none',
                    border: 'none',
                    color: '#F5F5F5',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#333333'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                >
                  🔄 Replace Question
                </button>
                <button
                  onClick={() => {
                    setShowMenu(false);
                    onStatusChange(question.id, DEFAULT_STATUSES.NEED_REVIEW);
                  }}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    textAlign: 'left',
                    background: 'none',
                    border: 'none',
                    color: '#EF4743',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    borderTop: '1px solid #333333'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#333333'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                >
                  🚩 Mark Need Review
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Question Title & Actions */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '12px',
        marginBottom: '12px'
      }}>
        <h3 style={{
          fontSize: '1.15rem',
          fontWeight: 600,
          color: isSolved ? '#F5F5F5' : '#F5F5F5',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          {question.title}
          {isSolved && (
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 18,
              height: 18,
              borderRadius: '50%',
              backgroundColor: '#2CBB5D',
              color: '#fff'
            }}>
              <Check size={12} strokeWidth={3} />
            </span>
          )}
        </h3>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Solve on LeetCode button (LeetCode Orange) */}
          <a
            href={question.leetcodeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-leetcode btn-sm"
          >
            Solve on LeetCode
            <ExternalLink size={12} />
          </a>

          {/* Mark Solved Button (LeetCode Green) */}
          <button
            onClick={() => onStatusChange(
              question.id,
              isSolved ? DEFAULT_STATUSES.NOT_STARTED : DEFAULT_STATUSES.SOLVED
            )}
            className={`btn btn-sm ${isSolved ? 'btn-solved-subtle' : 'btn-success'}`}
          >
            {isSolved ? '✓ Solved' : 'Mark Solved'}
          </button>
        </div>
      </div>

      {/* Pattern Recognition Card */}
      <div style={{
        padding: '10px 14px',
        borderRadius: 'var(--radius-md)',
        background: '#202020',
        border: '1px solid #333333',
        marginBottom: '10px'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          marginBottom: '6px',
          color: '#FFA116',
          fontWeight: 600,
          fontSize: '0.8rem'
        }}>
          <Sparkles size={14} />
          <span>Pattern: {question.pattern}</span>
        </div>

        <div style={{ fontSize: '0.8125rem', color: '#B3B3B3', lineHeight: '1.45', marginBottom: '6px' }}>
          <strong style={{ color: '#E0E0E0' }}>Why this matters: </strong>
          {question.whyItMatters}
        </div>

        <div style={{ fontSize: '0.78rem', color: '#888888', fontFamily: 'var(--font-mono)' }}>
          <strong style={{ color: '#B3B3B3' }}>Key Signal: </strong>
          "{question.interviewSignal}"
        </div>
      </div>

      {/* Expandable Hint & Solution Panels */}
      <HintPanel hint={question.hint} />
      <SolutionPanel
        approach={question.approach}
        complexity={question.complexity}
        solution={question.solution}
      />

      {/* Personal Notes Section */}
      <div style={{ marginTop: '10px' }}>
        {!isEditingNote && !question.notes ? (
          <button
            onClick={() => setIsEditingNote(true)}
            style={{
              background: 'none',
              border: 'none',
              color: '#777777',
              fontSize: '0.75rem',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              cursor: 'pointer',
              padding: '3px 0'
            }}
            onMouseEnter={(e) => e.target.style.color = '#FFA116'}
            onMouseLeave={(e) => e.target.style.color = '#777777'}
          >
            <Edit3 size={12} />
            Add personal interview notes / edge cases
          </button>
        ) : isEditingNote ? (
          <div className="animate-fade-in" style={{
            padding: '10px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #3A3A3A'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '6px',
              fontSize: '0.75rem',
              fontWeight: 600,
              color: '#B3B3B3'
            }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <Edit3 size={13} /> My Notes
              </span>
              <button
                onClick={() => setIsEditingNote(false)}
                style={{ background: 'none', border: 'none', color: '#777777', cursor: 'pointer', fontSize: '0.72rem' }}
              >
                Cancel
              </button>
            </div>
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Record observations, edge cases, or interview tricks..."
              rows={3}
              className="input-control"
              style={{ resize: 'vertical', fontSize: '0.8rem', marginBottom: '6px', background: '#1E1E1E' }}
            />
            <button
              onClick={handleSaveNote}
              className="btn btn-primary btn-sm"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}
            >
              <Save size={12} />
              Save Note
            </button>
          </div>
        ) : (
          <div style={{
            padding: '8px 12px',
            borderRadius: 'var(--radius-md)',
            background: '#202020',
            border: '1px solid #333333',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            fontSize: '0.8rem'
          }}>
            <div>
              <span style={{ fontWeight: 600, color: '#FFA116', display: 'block', marginBottom: '3px', fontSize: '0.75rem' }}>
                📝 My Notes:
              </span>
              <p style={{ color: '#B3B3B3', whiteSpace: 'pre-wrap' }}>
                {question.notes}
              </p>
            </div>
            <button
              onClick={() => setIsEditingNote(true)}
              className="btn btn-secondary btn-sm"
              style={{ padding: '2px 6px', fontSize: '0.72rem' }}
            >
              Edit
            </button>
          </div>
        )}

        {noteSavedFeedback && (
          <span style={{ fontSize: '0.72rem', color: '#2CBB5D', display: 'block', marginTop: '3px' }}>
            ✓ Note saved!
          </span>
        )}
      </div>
    </div>
  );
}
