import React from 'react';
import { Menu, Flame, Trophy, ExternalLink, Sun, Moon, Calendar } from 'lucide-react';

export default function Header({
  currentDay,
  onSelectDay,
  completedCount,
  totalQuestions = 135,
  streak,
  userProfile,
  theme,
  onToggleTheme,
  onOpenMobileMenu,
  onOpenSettings
}) {
  const progressPct = ((completedCount / totalQuestions) * 100).toFixed(1);

  return (
    <header style={{
      height: '56px',
      borderBottom: '1px solid var(--border-secondary)',
      backgroundColor: 'var(--bg-primary)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 80
    }}>
      {/* Left: Mobile Menu & Day Quick Jump */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <button
          onClick={onOpenMobileMenu}
          className="btn btn-secondary btn-icon mobile-menu-trigger"
          style={{ display: 'none', padding: '6px' }}
        >
          <Menu size={18} />
        </button>

        {/* Day Selector dropdown (LeetCode style) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Calendar size={14} /> Active Day:
          </span>
          <select
            value={currentDay}
            onChange={(e) => onSelectDay(Number(e.target.value))}
            style={{
              padding: '5px 10px',
              fontSize: '0.8125rem',
              fontWeight: 600,
              borderRadius: 'var(--radius-md)',
              background: '#282828',
              color: '#F5F5F5',
              border: '1px solid #444444',
              cursor: 'pointer',
              outline: 'none',
              fontFamily: 'var(--font-mono)'
            }}
            onFocus={(e) => e.target.style.borderColor = '#FFA116'}
            onBlur={(e) => e.target.style.borderColor = '#444444'}
          >
            {Array.from({ length: 45 }, (_, i) => i + 1).map((d) => (
              <option key={d} value={d}>
                Day {d} {d <= 10 ? '(Foundations)' : d <= 20 ? '(Patterns)' : d <= 30 ? '(Intermediate)' : d <= 38 ? '(Advanced)' : '(Interview Mode)'}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Right: Stats, Streak, Profile, Theme */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/* Streak counter (LeetCode Orange) */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          borderRadius: 'var(--radius-full)',
          background: 'rgba(255, 161, 22, 0.08)',
          border: '1px solid rgba(255, 161, 22, 0.25)',
          color: '#FFA116',
          fontSize: '0.8rem',
          fontWeight: 600
        }}>
          <Flame size={15} fill="#FFA116" />
          <span>{streak.current}d Streak</span>
          {streak.longest > 0 && (
            <span style={{ color: '#888888', fontSize: '0.72rem', fontWeight: 400 }}>
              (Best {streak.longest}d)
            </span>
          )}
        </div>

        {/* Overall progress pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          borderRadius: 'var(--radius-full)',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-primary)',
          color: 'var(--text-secondary)',
          fontSize: '0.8rem',
          fontWeight: 500
        }} className="hide-on-mobile">
          <Trophy size={13} color="#FFA116" />
          <span>{completedCount}/{totalQuestions}</span>
          <span style={{ color: '#FFA116', fontWeight: 600 }}>({progressPct}%)</span>
        </div>

        {/* LeetCode Profile Badge */}
        {userProfile.username ? (
          <a
            href={userProfile.profileUrl || `https://leetcode.com/${userProfile.username}`}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 10px',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255, 161, 22, 0.1)',
              border: '1px solid rgba(255, 161, 22, 0.25)',
              color: '#FFA116',
              fontSize: '0.78rem',
              fontWeight: 600,
              textDecoration: 'none'
            }}
            title="Open LeetCode Profile"
            className="hide-on-mobile"
          >
            <span>@{userProfile.username}</span>
            <ExternalLink size={12} />
          </a>
        ) : (
          <button
            onClick={onOpenSettings}
            className="btn btn-secondary btn-sm hide-on-mobile"
            style={{ fontSize: '0.75rem', padding: '3px 8px' }}
          >
            Connect LC Handle
          </button>
        )}

        {/* Theme Toggle */}
        <button
          onClick={onToggleTheme}
          className="btn btn-secondary btn-icon"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
          style={{ padding: '5px' }}
        >
          {theme === 'dark' ? <Sun size={15} color="#FFA116" /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  );
}
