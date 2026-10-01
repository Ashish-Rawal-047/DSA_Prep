import React from 'react';
import {
  LayoutDashboard,
  CalendarDays,
  Flame,
  BookmarkCheck,
  BarChart3,
  Brain,
  Search,
  Map,
  Timer,
  Settings,
  X
} from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  currentDay,
  todaySolvedCount,
  reviewCount,
  isOpen,
  onClose
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'plan', label: '45-Day Plan', icon: CalendarDays },
    {
      id: 'today',
      label: `Day ${currentDay} Questions`,
      icon: Flame,
      badge: `${todaySolvedCount}/3`,
      badgeColor: todaySolvedCount === 3 ? '#2CBB5D' : '#FFA116'
    },
    {
      id: 'review',
      label: 'Review Queue',
      icon: BookmarkCheck,
      badge: reviewCount > 0 ? reviewCount : null,
      badgeColor: '#EF4743'
    },
    { id: 'analytics', label: 'Progress & Analytics', icon: BarChart3 },
    { id: 'topics', label: 'Topic Explorer', icon: Brain },
    { id: 'bank', label: 'Question Bank', icon: Search },
    { id: 'roadmap', label: '45-Day Roadmap', icon: Map },
    { id: 'interview', label: 'Interview Mode', icon: Timer },
    { id: 'settings', label: 'Profile & Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            backdropFilter: 'blur(2px)',
            zIndex: 90
          }}
          className="mobile-backdrop"
        />
      )}

      <aside style={{
        width: '250px',
        backgroundColor: 'var(--bg-sidebar)',
        borderRight: '1px solid var(--border-secondary)',
        display: 'flex',
        flexDirection: 'column',
        position: 'sticky',
        top: 0,
        height: '100vh',
        zIndex: 100,
        flexShrink: 0,
        transition: 'transform 0.25s ease'
      }} className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        {/* Brand Header */}
        <div style={{
          padding: '20px 18px',
          borderBottom: '1px solid var(--border-secondary)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: 32,
              height: 32,
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255, 161, 22, 0.12)',
              border: '1px solid rgba(255, 161, 22, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Flame size={18} color="#FFA116" />
            </div>
            <div>
              <div style={{
                fontWeight: 700,
                fontSize: '0.95rem',
                color: '#F5F5F5',
                letterSpacing: '-0.01em',
                lineHeight: 1.15
              }}>
                DSA 45-DAY
              </div>
              <div style={{
                fontSize: '0.68rem',
                color: '#FFA116',
                fontWeight: 700,
                letterSpacing: '0.08em',
                textTransform: 'uppercase'
              }}>
                Placement Prep
              </div>
            </div>
          </div>

          <button
            onClick={onClose}
            className="mobile-close-btn"
            style={{
              display: 'none',
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Navigation Items */}
        <nav style={{ flex: 1, padding: '14px 8px', overflowY: 'auto' }}>
          <div style={{
            fontSize: '0.68rem',
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            color: 'var(--text-muted)',
            fontWeight: 600,
            padding: '4px 10px 8px'
          }}>
            Menu
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    if (onClose) onClose();
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: isActive ? '0 var(--radius-md) var(--radius-md) 0' : 'var(--radius-md)',
                    border: 'none',
                    borderLeft: isActive ? '2px solid #FFA116' : '2px solid transparent',
                    background: isActive ? 'rgba(255, 161, 22, 0.10)' : 'transparent',
                    color: isActive ? '#FFA116' : '#A0A0A0',
                    fontWeight: isActive ? 600 : 400,
                    fontSize: '0.84rem',
                    cursor: 'pointer',
                    transition: 'background var(--transition-fast), color var(--transition-fast)',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = '#2A2A2A';
                      e.currentTarget.style.color = '#F5F5F5';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = 'transparent';
                      e.currentTarget.style.color = '#A0A0A0';
                    }
                  }}
                >
                  <span style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Icon size={16} color={isActive ? '#FFA116' : '#888888'} />
                    {item.label}
                  </span>

                  {item.badge && (
                    <span style={{
                      fontSize: '0.7rem',
                      fontWeight: 700,
                      padding: '1px 6px',
                      borderRadius: 'var(--radius-sm)',
                      backgroundColor: `${item.badgeColor}18`,
                      color: item.badgeColor,
                      border: `1px solid ${item.badgeColor}33`,
                      fontFamily: 'var(--font-mono)'
                    }}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </nav>

        {/* Footer info */}
        <div style={{
          padding: '12px 18px',
          borderTop: '1px solid var(--border-secondary)',
          backgroundColor: '#141414'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <span>Curriculum</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>135 Questions</span>
          </div>
        </div>
      </aside>
    </>
  );
}
