import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Trophy, CheckCircle2, ArrowRight, X } from 'lucide-react';

export default function DailyCompleteModal({
  day,
  todayQuestions = [],
  tomorrowQuestions = [],
  onClose,
  onContinueToNextDay
}) {
  useEffect(() => {
    try {
      confetti({
        particleCount: 60,
        spread: 60,
        origin: { y: 0.6 }
      });
    } catch (e) {
      console.warn('Confetti error:', e);
    }
  }, []);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.78)',
      backdropFilter: 'blur(3px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '16px'
    }}>
      <div style={{
        maxWidth: '480px',
        width: '100%',
        backgroundColor: '#202020',
        border: '1px solid #3A3A3A',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.8)',
        textAlign: 'center'
      }}>
        {/* Top Celebration Banner */}
        <div style={{
          padding: '24px 20px 16px',
          background: '#1A1A1A',
          borderBottom: '1px solid #333333',
          position: 'relative'
        }}>
          <button
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '14px',
              right: '14px',
              background: 'none',
              border: 'none',
              color: '#888888',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>

          <div style={{
            width: 48,
            height: 48,
            borderRadius: '50%',
            background: 'rgba(44, 187, 93, 0.15)',
            border: '1px solid rgba(44, 187, 93, 0.3)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '12px',
            color: '#2CBB5D'
          }}>
            <Trophy size={24} />
          </div>

          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#F5F5F5', marginBottom: '4px' }}>
            DAY {day} COMPLETE 🎯
          </h2>
          <p style={{ color: '#2CBB5D', fontWeight: 600, fontSize: '0.85rem' }}>
            3 / 3 Questions Completed
          </p>
        </div>

        {/* Solved Topics List */}
        <div style={{ padding: '16px 22px', textAlign: 'left' }}>
          <div style={{
            fontSize: '0.72rem',
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: '#777777',
            marginBottom: '8px'
          }}>
            Questions Finished Today:
          </div>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '6px',
            marginBottom: '16px'
          }}>
            {todayQuestions.map((q) => (
              <div
                key={q.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-md)',
                  background: '#262626',
                  border: '1px solid #333333'
                }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.84rem', fontWeight: 500, color: '#F5F5F5' }}>
                  <CheckCircle2 size={15} color="#2CBB5D" />
                  {q.title}
                </span>
                <span style={{ fontSize: '0.72rem', color: '#B3B3B3', fontFamily: 'var(--font-mono)' }}>
                  {q.topic}
                </span>
              </div>
            ))}
          </div>

          {/* Tomorrow Preview */}
          {tomorrowQuestions.length > 0 && (
            <div style={{
              padding: '12px 14px',
              borderRadius: 'var(--radius-md)',
              background: '#262626',
              border: '1px solid #333333'
            }}>
              <div style={{
                fontSize: '0.72rem',
                textTransform: 'uppercase',
                color: '#FFA116',
                fontWeight: 600,
                marginBottom: '6px'
              }}>
                Tomorrow's Focus (Day {day + 1}):
              </div>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {tomorrowQuestions.map((tq) => (
                  <span
                    key={tq.id}
                    style={{
                      padding: '2px 8px',
                      borderRadius: 'var(--radius-sm)',
                      background: '#333333',
                      border: '1px solid #3A3A3A',
                      color: '#D4D4D4',
                      fontSize: '0.75rem',
                      fontWeight: 500
                    }}
                  >
                    {tq.topic}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div style={{
          padding: '12px 22px 20px',
          display: 'flex',
          justifyContent: 'center'
        }}>
          {day < 45 ? (
            <button
              onClick={onContinueToNextDay}
              className="btn btn-primary btn-lg"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              Continue to Day {day + 1}
              <ArrowRight size={16} />
            </button>
          ) : (
            <button
              onClick={onClose}
              className="btn btn-primary btn-lg"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              All 45 Days Finished! 🎉
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
