import { initialQuestions } from '../data/questionsData';
import { replacementPool as initialReplacementPool } from '../data/replacementPool';

const STORAGE_KEY = 'dsa_prep_dashboard_v1';

export const DEFAULT_STATUSES = {
  NOT_STARTED: 'not-started',
  ATTEMPTED: 'attempted',
  SOLVED: 'solved',
  NEED_REVIEW: 'need-review',
};

// Calculate streak based on dates when questions were marked solved
export function calculateStreak(questions) {
  const solvedDates = new Set();
  
  questions.forEach(q => {
    if (q.status === DEFAULT_STATUSES.SOLVED && q.solvedAt) {
      const dateStr = new Date(q.solvedAt).toISOString().split('T')[0];
      solvedDates.add(dateStr);
    }
  });

  if (solvedDates.size === 0) {
    return { current: 0, longest: 0, dates: [] };
  }

  const sortedDates = Array.from(solvedDates).sort();
  let longest = 1;
  let currentStreak = 1;
  let running = 1;

  for (let i = 1; i < sortedDates.length; i++) {
    const prev = new Date(sortedDates[i - 1]);
    const curr = new Date(sortedDates[i]);
    const diffDays = Math.round((curr - prev) / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      running++;
      if (running > longest) longest = running;
    } else if (diffDays > 1) {
      running = 1;
    }
  }

  // Check if current streak is active (today or yesterday was active)
  const todayStr = new Date().toISOString().split('T')[0];
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().split('T')[0];

  const lastActive = sortedDates[sortedDates.length - 1];
  if (lastActive === todayStr || lastActive === yesterdayStr) {
    currentStreak = running;
  } else {
    currentStreak = 0;
  }

  return {
    current: currentStreak,
    longest: Math.max(longest, currentStreak),
    dates: sortedDates,
  };
}

export const storageService = {
  loadState: () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        // Ensure questions has all properties and full 135
        if (parsed.questions && parsed.questions.length === 135) {
          return parsed;
        }
      }
    } catch (e) {
      console.error('Failed to load state from localStorage:', e);
    }

    // Default initialized state
    const defaultQuestions = initialQuestions.map(q => ({
      ...q,
      status: DEFAULT_STATUSES.NOT_STARTED,
      notes: '',
      solvedAt: null,
      timeSpentSeconds: 0,
    }));

    const initialState = {
      questions: defaultQuestions,
      replacementPool: [...initialReplacementPool],
      currentDay: 1,
      userProfile: {
        username: '',
        profileUrl: '',
        targetDate: '',
      },
      theme: 'dark',
      interviewModeHistory: [],
    };

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(initialState));
    } catch (e) {
      console.warn('Could not save initial state to localStorage', e);
    }

    return initialState;
  },

  saveState: (state) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      console.error('Failed to save state to localStorage:', e);
    }
  },

  exportData: () => {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw || JSON.stringify(storageService.loadState());
  },

  importData: (jsonString) => {
    try {
      const parsed = JSON.parse(jsonString);
      if (!parsed.questions || parsed.questions.length !== 135) {
        throw new Error('Invalid backup file: must contain 135 questions.');
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
      return { success: true, state: parsed };
    } catch (err) {
      return { success: false, error: err.message };
    }
  },

  resetAll: () => {
    localStorage.removeItem(STORAGE_KEY);
    return storageService.loadState();
  },
};
