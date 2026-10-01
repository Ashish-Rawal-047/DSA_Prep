import json
import sys
import os

from generate_all_135 import questions_data, make_q
from phase2_data import get_phase2_questions
from phase3_data import get_phase3_questions
from phase4_data import get_phase4_questions
from replacement_data import get_replacement_pool

# Combine all phases
all_questions = list(questions_data)
all_questions.extend(get_phase2_questions(make_q))
all_questions.extend(get_phase3_questions(make_q))
all_questions.extend(get_phase4_questions(make_q))

replacement_pool = get_replacement_pool(make_q)

print(f"Total questions assembled: {len(all_questions)}")
print(f"Total replacement candidates: {len(replacement_pool)}")

# Validation checks
def validate_dataset(qs):
    errors = []
    
    # Check total count
    if len(qs) != 135:
        errors.append(f"Expected 135 questions, got {len(qs)}")
        
    # Check days 1 to 45
    day_counts = {}
    titles = set()
    urls = set()
    ids = set()
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    topics_count = {}
    
    for q in qs:
        # ID check
        if q["id"] in ids:
            errors.append(f"Duplicate question id: {q['id']}")
        ids.add(q["id"])
        
        # Title check
        if q["title"] in titles:
            errors.append(f"Duplicate title: {q['title']}")
        titles.add(q["title"])
        
        # LeetCode URL check
        if q["leetcodeUrl"] in urls:
            errors.append(f"Duplicate LeetCode URL: {q['leetcodeUrl']}")
        urls.add(q["leetcodeUrl"])
        
        if not q["leetcodeUrl"].startswith("https://leetcode.com/problems/"):
            errors.append(f"Invalid LeetCode URL format: {q['leetcodeUrl']}")
            
        # Day counts
        d = q["day"]
        day_counts[d] = day_counts.get(d, 0) + 1
        
        # Difficulty
        diff = q["difficulty"]
        if diff not in diff_counts:
            errors.append(f"Invalid difficulty {diff} for Q{q['id']}")
        else:
            diff_counts[diff] += 1
            
        # Topic
        t = q["topic"]
        topics_count[t] = topics_count.get(t, 0) + 1
        
        # Content checks
        for field in ["hint", "approach", "complexity", "solution", "pattern", "whyItMatters", "interviewSignal"]:
            if not q.get(field):
                errors.append(f"Missing {field} for Q{q['id']}: {q['title']}")
                
    # Check exactly 45 days and 3 questions per day
    for day in range(1, 46):
        cnt = day_counts.get(day, 0)
        if cnt != 3:
            errors.append(f"Day {day} has {cnt} questions (expected 3)")
            
    # Check topic rotation (no 3 questions of same topic in a single day)
    day_topics = {}
    for q in qs:
        day_topics.setdefault(q["day"], []).append(q["topic"])
        
    for day, tops in day_topics.items():
        if len(set(tops)) < 2:
            errors.append(f"Day {day} has too little topic variety: {tops}")
            
    return errors, diff_counts, topics_count

errors, diff_counts, topics_count = validate_dataset(all_questions)

print("\n--- VALIDATION RESULTS ---")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("SUCCESS: All 135 questions passed strict validation!")

print(f"\nDifficulty Breakdown:")
for d, count in diff_counts.items():
    pct = (count / len(all_questions)) * 100
    print(f"  {d}: {count} ({pct:.1f}%)")

print(f"\nTopic Distribution ({len(topics_count)} topics):")
for t, count in sorted(topics_count.items(), key=lambda x: -x[1]):
    print(f"  {t}: {count}")

# Generate JS files
os.makedirs("src/data", exist_ok=True)
os.makedirs("src/utils", exist_ok=True)

# 1. src/data/questionsData.js
js_content = "// 45-Day DSA Placement Preparation Dataset\n"
js_content += "// 135 curated questions with patterns, hints, complexities, and C++ solutions\n\n"
js_content += "export const initialQuestions = " + json.dumps(all_questions, indent=2) + ";\n"

with open("src/data/questionsData.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print("\nWrote src/data/questionsData.js")

# 2. src/data/replacementPool.js
pool_js = "// Replacement question candidates pool for swapping questions\n\n"
pool_js += "export const replacementPool = " + json.dumps(replacement_pool, indent=2) + ";\n"

with open("src/data/replacementPool.js", "w", encoding="utf-8") as f:
    f.write(pool_js)
print("Wrote src/data/replacementPool.js")

# 3. src/utils/validator.js (for client-side or programmatic validation)
validator_js = """/**
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
"""

with open("src/utils/validator.js", "w", encoding="utf-8") as f:
    f.write(validator_js)
print("Wrote src/utils/validator.js")
