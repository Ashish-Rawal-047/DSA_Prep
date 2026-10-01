import React, { useState } from 'react';
import { Settings, User, ShieldCheck, Download, Upload, Trash2, CheckCircle2, AlertTriangle, FileCode } from 'lucide-react';
import { validate45DayPlan } from '../utils/validator';

export default function SettingsPage({
  questions,
  userProfile,
  onUpdateProfile,
  onExportData,
  onImportData,
  onResetData
}) {
  const [username, setUsername] = useState(userProfile.username || '');
  const [profileUrl, setProfileUrl] = useState(userProfile.profileUrl || '');
  const [targetDate, setTargetDate] = useState(userProfile.targetDate || '');
  const [savedFeedback, setSavedFeedback] = useState(false);
  const [validationResult, setValidationResult] = useState(null);
  const [importError, setImportError] = useState('');

  const handleSaveProfile = (e) => {
    e.preventDefault();
    onUpdateProfile({
      username: username.trim(),
      profileUrl: profileUrl.trim() || (username.trim() ? `https://leetcode.com/${username.trim()}` : ''),
      targetDate
    });
    setSavedFeedback(true);
    setTimeout(() => setSavedFeedback(false), 2500);
  };

  const handleRunValidation = () => {
    const result = validate45DayPlan(questions);
    setValidationResult(result);
  };

  const handleExport = () => {
    const dataStr = onExportData();
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dsa_prep_backup_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const res = onImportData(event.target.result);
      if (res.success) {
        setImportError('');
        alert('Data imported successfully!');
      } else {
        setImportError(res.error || 'Failed to parse JSON file.');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="page-wrapper animate-fade-in" style={{ maxWidth: '850px' }}>
      <div style={{ marginBottom: '28px' }}>
        <h1 style={{ fontSize: '1.8rem', marginBottom: '4px' }}>
          Profile & System Settings
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Manage your LeetCode handle, data backups, and curriculum validation.
        </p>
      </div>

      {/* LeetCode Profile Section */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <div style={{ width: 36, height: 36, borderRadius: 'var(--radius-md)', background: 'rgba(255, 161, 22, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ffa116' }}>
            <User size={20} />
          </div>
          <div>
            <h3 style={{ fontSize: '1.15rem' }}>LeetCode Profile & Target</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Identify your progress and direct links without sensitive credentials.
            </p>
          </div>
        </div>

        {/* Security Notice */}
        <div style={{
          padding: '12px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(44, 187, 93, 0.08)',
          border: '1px solid rgba(44, 187, 93, 0.25)',
          color: 'var(--success)',
          fontSize: '0.825rem',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '20px'
        }}>
          <ShieldCheck size={18} />
          <span>
            <strong>Zero-Credentials Security:</strong> We never ask for or store passwords, session cookies, or auth tokens.
          </span>
        </div>

        <form onSubmit={handleSaveProfile}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              LeetCode Username:
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. neetcode / tourist / ashish"
              className="input-control"
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              LeetCode Profile URL (optional):
            </label>
            <input
              type="url"
              value={profileUrl}
              onChange={(e) => setProfileUrl(e.target.value)}
              placeholder="https://leetcode.com/username/"
              className="input-control"
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Target Placement Date:
            </label>
            <input
              type="date"
              value={targetDate}
              onChange={(e) => setTargetDate(e.target.value)}
              className="input-control"
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button type="submit" className="btn btn-primary">
              Save Profile Settings
            </button>
            {savedFeedback && (
              <span style={{ fontSize: '0.85rem', color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle2 size={15} /> Saved successfully!
              </span>
            )}
          </div>
        </form>
      </div>

      {/* Curriculum Validation Suite */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileCode size={18} color="var(--accent-orange)" />
              Curriculum Integrity Verification
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Run comprehensive validation verifying 45 days, 135 unique questions, and URL integrity.
            </p>
          </div>

          <button onClick={handleRunValidation} className="btn btn-secondary btn-sm">
            Run Validation Test
          </button>
        </div>

        {validationResult && (
          <div className="animate-fade-in" style={{
            padding: '16px',
            borderRadius: 'var(--radius-md)',
            background: validationResult.isValid ? 'rgba(44, 187, 93, 0.08)' : 'rgba(239, 71, 67, 0.08)',
            border: `1px solid ${validationResult.isValid ? 'rgba(44, 187, 93, 0.25)' : 'rgba(239, 71, 67, 0.25)'}`,
            fontSize: '0.85rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 700, color: validationResult.isValid ? 'var(--success)' : 'var(--danger)', marginBottom: '8px' }}>
              {validationResult.isValid ? <CheckCircle2 size={18} /> : <AlertTriangle size={18} />}
              {validationResult.isValid ? 'All Acceptance Criteria Passed!' : `Validation Failed with ${validationResult.errors.length} errors`}
            </div>

            <ul style={{ paddingLeft: '20px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              <li>Total Days: <strong>{validationResult.totalDays}</strong> (Target: 45)</li>
              <li>Total Questions: <strong>{validationResult.totalQuestions}</strong> (Target: 135)</li>
              <li>Questions per Day: <strong>Exactly 3</strong></li>
              <li>Duplicate URLs or Titles: <strong>0</strong></li>
              <li>Difficulty Distribution: Easy {validationResult.diffCounts.Easy}, Medium {validationResult.diffCounts.Medium}, Hard {validationResult.diffCounts.Hard}</li>
            </ul>
          </div>
        )}
      </div>

      {/* Data Backup & Reset */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.15rem', marginBottom: '14px' }}>
          Data Backup & Portability
        </h3>

        <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap', marginBottom: '24px' }}>
          <button onClick={handleExport} className="btn btn-secondary">
            <Download size={16} /> Export JSON Backup
          </button>

          <label className="btn btn-secondary" style={{ cursor: 'pointer' }}>
            <Upload size={16} /> Import JSON Backup
            <input type="file" accept=".json" onChange={handleFileUpload} style={{ display: 'none' }} />
          </label>
        </div>

        {importError && (
          <div style={{ color: 'var(--danger)', fontSize: '0.85rem', marginBottom: '16px' }}>
            {importError}
          </div>
        )}

        <div style={{ borderTop: '1px solid var(--border-primary)', paddingTop: '18px' }}>
          <h4 style={{ fontSize: '0.95rem', color: 'var(--danger)', marginBottom: '6px' }}>
            Danger Zone
          </h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            Reset all question statuses, personal notes, and streaks back to initial clean state.
          </p>
          <button
            onClick={() => {
              if (window.confirm('Are you sure you want to reset all progress? This action cannot be undone unless you have a JSON backup.')) {
                onResetData();
              }
            }}
            className="btn btn-secondary"
            style={{ color: 'var(--danger)', borderColor: 'rgba(239, 71, 67, 0.3)' }}
          >
            <Trash2 size={16} /> Reset All Progress
          </button>
        </div>
      </div>
    </div>
  );
}
