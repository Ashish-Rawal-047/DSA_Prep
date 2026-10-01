import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ReplaceQuestionModal from './components/ReplaceQuestionModal';
import DailyCompleteModal from './components/DailyCompleteModal';

// Pages
import DashboardPage from './pages/DashboardPage';
import TodayQuestionsPage from './pages/TodayQuestionsPage';
import PlanPage from './pages/PlanPage';
import ReviewQueuePage from './pages/ReviewQueuePage';
import AnalyticsPage from './pages/AnalyticsPage';
import TopicsPage from './pages/TopicsPage';
import QuestionBankPage from './pages/QuestionBankPage';
import RoadmapPage from './pages/RoadmapPage';
import InterviewModePage from './pages/InterviewModePage';
import SettingsPage from './pages/SettingsPage';

import { storageService, calculateStreak, DEFAULT_STATUSES } from './services/storageService';

export default function App() {
  const [appState, setAppState] = useState(() => storageService.loadState());
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Modals state
  const [replaceTargetQuestion, setReplaceTargetQuestion] = useState(null);
  const [dailyCompleteDay, setDailyCompleteDay] = useState(null);

  // Sync theme attribute to document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', appState.theme || 'dark');
  }, [appState.theme]);

  // Persist state updates to localStorage
  const updateStateAndPersist = (updater) => {
    setAppState((prev) => {
      const next = typeof updater === 'function' ? updater(prev) : { ...prev, ...updater };
      storageService.saveState(next);
      return next;
    });
  };

  const streak = calculateStreak(appState.questions);
  const todayQuestions = appState.questions.filter((q) => q.day === appState.currentDay);
  const todaySolvedCount = todayQuestions.filter((q) => q.status === DEFAULT_STATUSES.SOLVED).length;
  const completedCount = appState.questions.filter((q) => q.status === DEFAULT_STATUSES.SOLVED).length;
  const reviewCount = appState.questions.filter((q) => q.status === DEFAULT_STATUSES.NEED_REVIEW).length;

  // Question Status Change Handler
  const handleStatusChange = (questionId, newStatus) => {
    updateStateAndPersist((prev) => {
      const targetQ = prev.questions.find((q) => q.id === questionId);
      const wasAlreadySolved = targetQ && targetQ.status === DEFAULT_STATUSES.SOLVED;

      const updatedQuestions = prev.questions.map((q) => {
        if (q.id === questionId) {
          const isNowSolved = newStatus === DEFAULT_STATUSES.SOLVED;
          return {
            ...q,
            status: newStatus,
            solvedAt: isNowSolved ? new Date().toISOString() : q.solvedAt
          };
        }
        return q;
      });

      // Check if this solved action completes the day!
      if (newStatus === DEFAULT_STATUSES.SOLVED && !wasAlreadySolved && targetQ) {
        const dayQuestions = updatedQuestions.filter((q) => q.day === targetQ.day);
        const allDaySolved = dayQuestions.length === 3 && dayQuestions.every((q) => q.status === DEFAULT_STATUSES.SOLVED);
        if (allDaySolved) {
          // Trigger Daily Complete celebration modal
          setTimeout(() => setDailyCompleteDay(targetQ.day), 150);
        }
      }

      return {
        ...prev,
        questions: updatedQuestions
      };
    });
  };

  // Personal Note Save Handler
  const handleSaveNote = (questionId, noteText) => {
    updateStateAndPersist((prev) => ({
      ...prev,
      questions: prev.questions.map((q) =>
        q.id === questionId ? { ...q, notes: noteText } : q
      )
    }));
  };

  // Replace Question Handler
  const handleOpenReplaceModal = (question) => {
    setReplaceTargetQuestion(question);
  };

  const handleConfirmReplace = (oldQuestionId, candidateId) => {
    updateStateAndPersist((prev) => {
      const candidate = prev.replacementPool.find((c) => c.id === candidateId);
      if (!candidate) return prev;

      const oldQuestion = prev.questions.find((q) => q.id === oldQuestionId);
      if (!oldQuestion) return prev;

      // Construct replaced question keeping same day
      const replacedQuestion = {
        ...candidate,
        id: candidate.id,
        day: oldQuestion.day,
        status: DEFAULT_STATUSES.NOT_STARTED,
        notes: '',
        solvedAt: null
      };

      const updatedQuestions = prev.questions.map((q) =>
        q.id === oldQuestionId ? replacedQuestion : q
      );

      const updatedPool = prev.replacementPool.filter((c) => c.id !== candidateId);

      return {
        ...prev,
        questions: updatedQuestions,
        replacementPool: updatedPool
      };
    });

    setReplaceTargetQuestion(null);
  };

  // Get replacement candidates for the current target question
  const getCandidatesForReplace = () => {
    if (!replaceTargetQuestion) return [];
    const pool = appState.replacementPool || [];
    
    // Exact topic match candidates
    const topicMatches = pool.filter((c) => c.topic === replaceTargetQuestion.topic);
    if (topicMatches.length >= 2) return topicMatches.slice(0, 4);

    // Fallback: difficulty matches or general candidates
    const diffMatches = pool.filter((c) => c.difficulty === replaceTargetQuestion.difficulty);
    return diffMatches.length > 0 ? diffMatches.slice(0, 4) : pool.slice(0, 4);
  };

  // Daily Navigation & Continuation
  const handleSelectDay = (dayNum) => {
    updateStateAndPersist((prev) => ({ ...prev, currentDay: dayNum }));
  };

  const handleContinueToNextDay = () => {
    if (dailyCompleteDay && dailyCompleteDay < 45) {
      handleSelectDay(dailyCompleteDay + 1);
      setActiveTab('today');
    }
    setDailyCompleteDay(null);
  };

  // Toggle Theme
  const handleToggleTheme = () => {
    updateStateAndPersist((prev) => ({
      ...prev,
      theme: prev.theme === 'light' ? 'dark' : 'light'
    }));
  };

  // Profile Update
  const handleUpdateProfile = (profileData) => {
    updateStateAndPersist((prev) => ({
      ...prev,
      userProfile: { ...prev.userProfile, ...profileData }
    }));
  };

  // Reset Progress
  const handleResetData = () => {
    const freshState = storageService.resetAll();
    setAppState(freshState);
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentDay={appState.currentDay}
        todaySolvedCount={todaySolvedCount}
        reviewCount={reviewCount}
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Header
          currentDay={appState.currentDay}
          onSelectDay={handleSelectDay}
          completedCount={completedCount}
          totalQuestions={135}
          streak={streak}
          userProfile={appState.userProfile}
          theme={appState.theme}
          onToggleTheme={handleToggleTheme}
          onOpenMobileMenu={() => setMobileMenuOpen(true)}
          onOpenSettings={() => setActiveTab('settings')}
        />

        {/* Tab Routing */}
        <main>
          {activeTab === 'dashboard' && (
            <DashboardPage
              questions={appState.questions}
              currentDay={appState.currentDay}
              onSelectDay={handleSelectDay}
              onStatusChange={handleStatusChange}
              onSaveNote={handleSaveNote}
              onOpenReplaceModal={handleOpenReplaceModal}
              onNavigateTab={setActiveTab}
              streak={streak}
              userProfile={appState.userProfile}
            />
          )}

          {activeTab === 'today' && (
            <TodayQuestionsPage
              questions={appState.questions}
              currentDay={appState.currentDay}
              onSelectDay={handleSelectDay}
              onStatusChange={handleStatusChange}
              onSaveNote={handleSaveNote}
              onOpenReplaceModal={handleOpenReplaceModal}
              onTriggerDailyComplete={() => setDailyCompleteDay(appState.currentDay)}
            />
          )}

          {activeTab === 'plan' && (
            <PlanPage
              questions={appState.questions}
              currentDay={appState.currentDay}
              onSelectDay={handleSelectDay}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'review' && (
            <ReviewQueuePage
              questions={appState.questions}
              onStatusChange={handleStatusChange}
              onSaveNote={handleSaveNote}
              onOpenReplaceModal={handleOpenReplaceModal}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsPage
              questions={appState.questions}
              streak={streak}
            />
          )}

          {activeTab === 'topics' && (
            <TopicsPage
              questions={appState.questions}
              onSelectDay={handleSelectDay}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'bank' && (
            <QuestionBankPage
              questions={appState.questions}
              onStatusChange={handleStatusChange}
              onSaveNote={handleSaveNote}
              onOpenReplaceModal={handleOpenReplaceModal}
            />
          )}

          {activeTab === 'roadmap' && (
            <RoadmapPage
              questions={appState.questions}
              currentDay={appState.currentDay}
              onSelectDay={handleSelectDay}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'interview' && (
            <InterviewModePage
              questions={appState.questions}
              currentDay={appState.currentDay}
              onStatusChange={handleStatusChange}
              onSaveNote={handleSaveNote}
            />
          )}

          {activeTab === 'settings' && (
            <SettingsPage
              questions={appState.questions}
              userProfile={appState.userProfile}
              onUpdateProfile={handleUpdateProfile}
              onExportData={() => storageService.exportData()}
              onImportData={(jsonStr) => {
                const res = storageService.importData(jsonStr);
                if (res.success) setAppState(res.state);
                return res;
              }}
              onResetData={handleResetData}
            />
          )}
        </main>
      </div>

      {/* Replace Question Modal */}
      {replaceTargetQuestion && (
        <ReplaceQuestionModal
          currentQuestion={replaceTargetQuestion}
          candidates={getCandidatesForReplace()}
          onClose={() => setReplaceTargetQuestion(null)}
          onConfirmReplace={handleConfirmReplace}
        />
      )}

      {/* Daily Complete Celebration Modal */}
      {dailyCompleteDay && (
        <DailyCompleteModal
          day={dailyCompleteDay}
          todayQuestions={appState.questions.filter((q) => q.day === dailyCompleteDay)}
          tomorrowQuestions={
            dailyCompleteDay < 45
              ? appState.questions.filter((q) => q.day === dailyCompleteDay + 1)
              : []
          }
          onClose={() => setDailyCompleteDay(null)}
          onContinueToNextDay={handleContinueToNextDay}
        />
      )}
    </div>
  );
}
