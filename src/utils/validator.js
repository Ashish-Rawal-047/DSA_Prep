/**
 * Validates the 45-Day DSA Preparation Plan against strict criteria:
 * - Exactly 45 days
 * - Exactly 3 questions per day
 * - Exactly 135 questions
 * - No duplicate questions or LeetCode URLs
 * - Topic rotation (diverse topics per day)
 * - Valid LeetCode URLs
 */
export function validate45DayPlan(questions) {
  const errors = [];
  const titles = new Set();
  const urls = new Set();
  const ids = new Set();
  const dayCounts = {};
  const dayTopics = {};
  const diffCounts = { Easy: 0, Medium: 0, Hard: 0 };
  const topicCounts = {};

  if (!questions || questions.length !== 135) {
    errors.push(`Expected 135 questions, got ${questions ? questions.length : 0}`);
  }

  questions.forEach(q => {
    if (ids.has(q.id)) errors.push(`Duplicate ID: ${q.id}`);
    ids.add(q.id);

    if (titles.has(q.title)) errors.push(`Duplicate Title: ${q.title}`);
    titles.add(q.title);

    if (urls.has(q.leetcodeUrl)) errors.push(`Duplicate LeetCode URL: ${q.leetcodeUrl}`);
    urls.add(q.leetcodeUrl);

    if (!q.leetcodeUrl || !q.leetcodeUrl.startsWith("https://leetcode.com/problems/")) {
      errors.push(`Invalid LeetCode URL for ${q.title}: ${q.leetcodeUrl}`);
    }

    dayCounts[q.day] = (dayCounts[q.day] || 0) + 1;
    if (!dayTopics[q.day]) dayTopics[q.day] = [];
    dayTopics[q.day].push(q.topic);

    diffCounts[q.difficulty] = (diffCounts[q.difficulty] || 0) + 1;
    topicCounts[q.topic] = (topicCounts[q.topic] || 0) + 1;

    if (!q.hint) errors.push(`Missing hint for ${q.title}`);
    if (!q.solution) errors.push(`Missing solution for ${q.title}`);
    if (!q.pattern) errors.push(`Missing pattern for ${q.title}`);
  });

  for (let d = 1; d <= 45; d++) {
    if (dayCounts[d] !== 3) {
      errors.push(`Day ${d} has ${dayCounts[d] || 0} questions (expected 3)`);
    }
  }

  Object.entries(dayTopics).forEach(([day, tops]) => {
    const unique = new Set(tops);
    if (unique.size < 2) {
      errors.push(`Day ${day} lacks topic variety: ${tops.join(", ")}`);
    }
  });

  return {
    isValid: errors.length === 0,
    errors,
    diffCounts,
    topicCounts,
    totalQuestions: questions.length,
    totalDays: Object.keys(dayCounts).length
  };
}
