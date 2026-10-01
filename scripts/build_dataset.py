"""
Script to build and validate the 45-Day DSA Placement Preparation Dataset.
Generates:
  - src/data/questionsData.js (135 questions, 45 days, 3 questions/day)
  - src/data/replacementPool.js (30+ replacement questions)
  - src/utils/validator.js (Validation suite)
"""

import json
import os
import re

questions = [
    # ----------------------------------------------------
    # PHASE 1: FOUNDATIONS & PATTERN RECOGNITION (DAYS 1-10)
    # ----------------------------------------------------
    # Day 1: Arrays (Two Pointers) + Strings (Sliding Window) + Bit Manipulation
    {
        "id": 1, "day": 1,
        "title": "Two Sum II - Input Array Is Sorted",
        "leetcodeUrl": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
        "topic": "Arrays", "subtopic": "Two Pointers", "difficulty": "Medium",
        "pattern": "Opposite-Direction Two Pointers",
        "whyItMatters": "Tests whether you recognize sorted order allows monotonic movement of pointers in O(1) space, avoiding hash map overhead.",
        "interviewSignal": "Sorted array, find pair satisfying target sum, O(1) auxiliary space constraint.",
        "hint": "Since the array is sorted, how does moving the left pointer right or the right pointer left affect the sum?",
        "approach": "Initialize left = 0, right = n - 1. If sum == target, return indices (1-indexed). If sum < target, left++ to increase sum. If sum > target, right-- to decrease sum.",
        "complexity": "Time: O(N), Space: O(1)",
        "solution": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left = 0, right = numbers.size() - 1;
        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) return {left + 1, right + 1};
            if (sum < target) left++;
            else right--;
        }
        return {};
    }
};"""
    },
    {
        "id": 2, "day": 1,
        "title": "Longest Substring Without Repeating Characters",
        "leetcodeUrl": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "topic": "Strings", "subtopic": "Sliding Window", "difficulty": "Medium",
        "pattern": "Variable-Size Sliding Window",
        "whyItMatters": "The quintessential variable sliding window problem tested at almost every top tech interview.",
        "interviewSignal": "Longest substring with non-repeating/unique constraint.",
        "hint": "Maintain the last seen index of each character. When a duplicate is encountered, where should the left window boundary jump?",
        "approach": "Expand right pointer. Use an array/hashmap of last seen character indices. If s[right] was seen inside current window [left, right], advance left = lastSeen[s[right]] + 1. Update maxLen = max(maxLen, right - left + 1).",
        "complexity": "Time: O(N), Space: O(min(N, AlphabetSize))",
        "solution": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        vector<int> lastIndex(128, -1);
        int maxLen = 0, left = 0;
        for (int right = 0; right < (int)s.size(); right++) {
            if (lastIndex[(unsigned char)s[right]] >= left) {
                left = lastIndex[(unsigned char)s[right]] + 1;
            }
            lastIndex[(unsigned char)s[right]] = right;
            maxLen = max(maxLen, right - left + 1);
        }
        return maxLen;
    }
};"""
    },
    {
        "id": 3, "day": 1,
        "title": "Counting Bits",
        "leetcodeUrl": "https://leetcode.com/problems/counting-bits/",
        "topic": "Bit Manipulation", "subtopic": "Bitwise DP", "difficulty": "Easy",
        "pattern": "Bitwise Transitions & Kernighan's Identity",
        "whyItMatters": "Foundational interview problem bridging bit manipulation and dynamic programming in O(N) time.",
        "interviewSignal": "Count set bits for all numbers from 0 to N in linear time without built-ins.",
        "hint": "How relates the number of set bits of i to i >> 1 or i & (i - 1)?",
        "approach": "Use dp[i] = dp[i >> 1] + (i & 1). Shifting right removes the lowest bit; the count is the bits in i/2 plus 1 if i is odd.",
        "complexity": "Time: O(N), Space: O(1) auxiliary (excluding output array)",
        "solution": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> ans(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }
};"""
    },

    # Day 2: Graphs + Trees + Dynamic Programming
    {
        "id": 4, "day": 2,
        "title": "Number of Islands",
        "leetcodeUrl": "https://leetcode.com/problems/number-of-islands/",
        "topic": "Graphs", "subtopic": "Grid BFS / DFS", "difficulty": "Medium",
        "pattern": "Connected Components via Flood Fill",
        "whyItMatters": "Benchmark interview question testing graph modeling from a 2D matrix and in-place visited marking.",
        "interviewSignal": "Count connected regions in 2D grid where adjacent '1's form a cluster.",
        "hint": "Iterate through cells. Whenever you encounter '1', trigger DFS/BFS to sink the entire island to '0' and increment the island counter.",
        "approach": "Traverse grid. When grid[r][c] == '1', increment island count and recursively mark all 4-directional adjacent '1's as '0' (visited).",
        "complexity": "Time: O(R * C), Space: O(R * C) worst-case recursion stack",
        "solution": """#include <vector>
using namespace std;

class Solution {
    void dfs(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || r >= grid.size() || c < 0 || c >= grid[0].size() || grid[r][c] != '1')
            return;
        grid[r][c] = '0'; // Sink island
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
public:
    int numIslands(vector<vector<char>>& grid) {
        int count = 0;
        for (int i = 0; i < grid.size(); i++) {
            for (int j = 0; j < grid[0].size(); j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
};"""
    },
    {
        "id": 5, "day": 2,
        "title": "Diameter of Binary Tree",
        "leetcodeUrl": "https://leetcode.com/problems/diameter-of-binary-tree/",
        "topic": "Trees", "subtopic": "Binary Tree Depth & Path", "difficulty": "Easy",
        "pattern": "Post-Order Tree Traversal & Bottom-Up Calculation",
        "whyItMatters": "Teaches maintaining a global answer while returning a local property (subtree height) upwards.",
        "interviewSignal": "Longest path between any two nodes in a tree, path does not necessarily pass through root.",
        "hint": "At each node, the longest path passing through it is left_height + right_height. Return 1 + max(left_height, right_height) to parent.",
        "approach": "Post-order DFS returns the depth of current node. During traversal, compute leftDepth + rightDepth and update maxDiameter.",
        "complexity": "Time: O(N), Space: O(H) where H is tree height",
        "solution": """#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    int maxDiameter = 0;
    int depth(TreeNode* root) {
        if (!root) return 0;
        int L = depth(root->left);
        int R = depth(root->right);
        maxDiameter = max(maxDiameter, L + R);
        return 1 + max(L, R);
    }
public:
    int diameterOfBinaryTree(TreeNode* root) {
        maxDiameter = 0;
        depth(root);
        return maxDiameter;
    }
};"""
    },
    {
        "id": 6, "day": 2,
        "title": "Maximum Subarray",
        "leetcodeUrl": "https://leetcode.com/problems/maximum-subarray/",
        "topic": "Dynamic Programming", "subtopic": "1D DP / Kadane", "difficulty": "Medium",
        "pattern": "Kadane's Algorithm",
        "whyItMatters": "Core interview pattern for state transitions on contiguous subarrays.",
        "interviewSignal": "Contiguous subarray with largest sum, negative numbers included.",
        "hint": "At each index, do you extend the previous subarray sum or start fresh from current element?",
        "approach": "currentSum = max(nums[i], currentSum + nums[i]). maxSum = max(maxSum, currentSum).",
        "complexity": "Time: O(N), Space: O(1)",
        "solution": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maxSum = nums[0], currentSum = nums[0];
        for (size_t i = 1; i < nums.size(); i++) {
            currentSum = max(nums[i], currentSum + nums[i]);
            maxSum = max(maxSum, currentSum);
        }
        return maxSum;
    }
};"""
    },

    # Day 3: Binary Search + Stack / Monotonic Stack + Greedy / Intervals
    {
        "id": 7, "day": 3,
        "title": "Koko Eating Bananas",
        "leetcodeUrl": "https://leetcode.com/problems/koko-eating-bananas/",
        "topic": "Binary Search", "subtopic": "Binary Search on Answer", "difficulty": "Medium",
        "pattern": "Binary Search on Monotonic Predicate",
        "whyItMatters": "One of the most requested patterns in tech rounds: finding minimum rate/speed/threshold.",
        "interviewSignal": "Find minimum speed/capacity k such that work is completed within H hours.",
        "hint": "The eating speed k ranges between 1 and max(piles). Is the feasibility function monotonic with respect to k?",
        "approach": "Binary search on speed k in [1, max(piles)]. Feasibility check: sum of ceil(pile / k) <= h. If feasible, search left half (high = mid); else search right half (low = mid + 1).",
        "complexity": "Time: O(N * log(max(piles))), Space: O(1)",
        "solution": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    bool canEatAll(const vector<int>& piles, int h, int k) {
        long long hours = 0;
        for (int p : piles) {
            hours += (p + k - 1) / k;
        }
        return hours <= h;
    }
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int low = 1, high = *max_element(piles.begin(), piles.end());
        int ans = high;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canEatAll(piles, h, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }
};"""
    },
    {
        "id": 8, "day": 3,
        "title": "Daily Temperatures",
        "leetcodeUrl": "https://leetcode.com/problems/daily-temperatures/",
        "topic": "Stack", "subtopic": "Monotonic Stack", "difficulty": "Medium",
        "pattern": "Monotonic Decreasing Stack",
        "whyItMatters": "Essential for understanding how to resolve unresolved previous elements in linear time.",
        "interviewSignal": "Find the distance to the next warmer/greater element.",
        "hint": "Store indices of unresolved temperatures in a stack. When current temperature is higher than stack top, pop and compute difference in indices.",
        "approach": "Maintain a stack of indices. For each index i, while stack is non-empty and temperatures[i] > temperatures[st.top()], pop index prev and set ans[prev] = i - prev. Push i.",
        "complexity": "Time: O(N), Space: O(N)",
        "solution": """#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
                int prev = st.top();
                st.pop();
                ans[prev] = i - prev;
            }
            st.push(i);
        }
        return ans;
    }
};"""
    },
    {
        "id": 9, "day": 3,
        "title": "Non-overlapping Intervals",
        "leetcodeUrl": "https://leetcode.com/problems/non-overlapping-intervals/",
        "topic": "Intervals", "subtopic": "Greedy Scheduling", "difficulty": "Medium",
        "pattern": "Interval Scheduling via Earliest End Time",
        "whyItMatters": "Classic greedy interval scheduling theorem applied in interview settings.",
        "interviewSignal": "Minimum removals to make remaining intervals non-overlapping.",
        "hint": "Sort intervals by end time. If an interval starts before the previous one ends, it must be removed.",
        "approach": "Sort by end time. Keep the interval that finishes earliest to leave maximum room for future intervals. If next interval starts before current end, increment removal count. Otherwise update end.",
        "complexity": "Time: O(N log N), Space: O(1) or O(log N) for sort",
        "solution": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        if (intervals.empty()) return 0;
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });
        int removed = 0, lastEnd = intervals[0][1];
        for (size_t i = 1; i < intervals.size(); i++) {
            if (intervals[i][0] < lastEnd) {
                removed++;
            } else {
                lastEnd = intervals[i][1];
            }
        }
        return removed;
    }
};"""
    },

    # Day 4: Linked List + Heap / Priority Queue + Dynamic Programming
    {
        "id": 10, "day": 4,
        "title": "Reorder List",
        "leetcodeUrl": "https://leetcode.com/problems/reorder-list/",
        "topic": "Linked Lists", "subtopic": "Two Pointers & In-place Reversal", "difficulty": "Medium",
        "pattern": "Find Middle + Reverse Second Half + Interleave",
        "whyItMatters": "Tests three fundamental linked list operations combined in one question without extra memory.",
        "interviewSignal": "Reorder list L0 -> Ln-1 -> L1 -> Ln-2 in O(1) space.",
        "hint": "Break into 3 steps: slow/fast pointer to find middle, reverse second half, weave two halves together.",
        "approach": "1. Find middle with slow/fast pointers. 2. Cut list and reverse second half. 3. Interleave nodes from first and second half.",
        "complexity": "Time: O(N), Space: O(1)",
        "solution": """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
    ListNode* reverse(ListNode* head) {
        ListNode* prev = nullptr;
        while (head) {
            ListNode* nxt = head->next;
            head->next = prev;
            prev = head;
            head = nxt;
        }
        return prev;
    }
public:
    void reorderList(ListNode* head) {
        if (!head || !head->next) return;
        ListNode *slow = head, *fast = head;
        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* second = reverse(slow->next);
        slow->next = nullptr;
        ListNode* first = head;
        while (second) {
            ListNode *tmp1 = first->next, *tmp2 = second->next;
            first->next = second;
            second->next = tmp1;
            first = tmp1;
            second = tmp2;
        }
    }
};"""
    },
    {
        "id": 11, "day": 4,
        "title": "Find Median from Data Stream",
        "leetcodeUrl": "https://leetcode.com/problems/find-median-from-data-stream/",
        "topic": "Heap", "subtopic": "Two Heaps Pattern", "difficulty": "Hard",
        "pattern": "Two Heaps (Max-Heap + Min-Heap)",
        "whyItMatters": "The standard design pattern for tracking rolling medians and percentiles in real-time streams.",
        "interviewSignal": "Add numbers dynamically from data stream and find median in O(1) or O(log N).",
        "hint": "Divide numbers into lower half (max-heap) and upper half (min-heap). Keep their sizes balanced within 1 element difference.",
        "approach": "Push to max_heap. Pop top of max_heap and push to min_heap. If min_heap size > max_heap size, move top from min_heap to max_heap. Median is either max_heap.top() or average of both tops.",
        "complexity": "Time: addNum O(log N), findMedian O(1), Space: O(N)",
        "solution": """#include <queue>
#include <vector>
using namespace std;

class MedianFinder {
    priority_queue<int> maxHeap; // stores smaller half
    priority_queue<int, vector<int>, greater<int>> minHeap; // stores larger half
public:
    MedianFinder() {}
    
    void addNum(int num) {
        maxHeap.push(num);
        minHeap.push(maxHeap.top());
        maxHeap.pop();
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }
    
    double findMedian() {
        if (maxHeap.size() > minHeap.size()) return maxHeap.top();
        return (maxHeap.top() + minHeap.top()) / 2.0;
    }
};"""
    },
    {
        "id": 12, "day": 4,
        "title": "Partition Equal Subset Sum",
        "leetcodeUrl": "https://leetcode.com/problems/partition-equal-subset-sum/",
        "topic": "Dynamic Programming", "subtopic": "0/1 Knapsack", "difficulty": "Medium",
        "pattern": "0/1 Knapsack Subset DP",
        "whyItMatters": "Transforms an equal partition problem into classic 0/1 knapsack with target = totalSum / 2.",
        "interviewSignal": "Partition array into two subsets with equal sum.",
        "hint": "If total sum is odd, return false. Otherwise, can we find a subset with sum equal to totalSum / 2?",
        "approach": "Compute total sum. If sum % 2 != 0, return false. Target = sum / 2. Use a 1D boolean DP array traversed backwards: dp[j] = dp[j] || dp[j - num].",
        "complexity": "Time: O(N * Target), Space: O(Target)",
        "solution": """#include <vector>
#include <numeric>
using namespace std;

class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % 2 != 0) return false;
        int target = total / 2;
        vector<bool> dp(target + 1, false);
        dp[0] = true;
        for (int num : nums) {
            for (int j = target; j >= num; j--) {
                dp[j] = dp[j] || dp[j - num];
            }
        }
        return dp[target];
    }
};"""
    },

    # Day 5: Arrays / Prefix Sum + Graphs / DFS + Strings / Trie
    {
        "id": 13, "day": 5,
        "title": "Subarray Sum Equals K",
        "leetcodeUrl": "https://leetcode.com/problems/subarray-sum-equals-k/",
        "topic": "Arrays", "subtopic": "Prefix Sum + Hash Map", "difficulty": "Medium",
        "pattern": "Prefix Sum Difference with Hash Frequency",
        "whyItMatters": "Teaches prefix difference trick (prefix[j] - prefix[i] = k) when array elements can be negative, ruling out two pointers.",
        "interviewSignal": "Count continuous subarrays whose sum equals k, negative values permitted.",
        "hint": "If prefixSum - k exists in your hash map, how many subarrays ending at current index sum to k?",
        "approach": "Maintain running sum. Check if (sum - k) is in hash map; if so, add its frequency to answer. Increment map[sum]. Base case: map[0] = 1.",
        "complexity": "Time: O(N), Space: O(N)",
        "solution": """#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixFreq;
        prefixFreq[0] = 1;
        int sum = 0, count = 0;
        for (int x : nums) {
            sum += x;
            if (prefixFreq.count(sum - k)) {
                count += prefixFreq[sum - k];
            }
            prefixFreq[sum]++;
        }
        return count;
    }
};"""
    },
    {
        "id": 14, "day": 5,
        "title": "Course Schedule",
        "leetcodeUrl": "https://leetcode.com/problems/course-schedule/",
        "topic": "Graphs", "subtopic": "Cycle Detection / Topological Sort", "difficulty": "Medium",
        "pattern": "Directed Graph Cycle Detection",
        "whyItMatters": "The definitive dependency resolution problem asked by Google, Meta, and Microsoft.",
        "interviewSignal": "Prerequisites / dependencies, determine if it is possible to finish all courses.",
        "hint": "Can you complete all courses if there is a cycle in the directed dependency graph?",
        "approach": "Use Kahn's algorithm (BFS with in-degrees). Calculate in-degrees. Push 0 in-degree nodes to queue. Pop node, decrement neighbor in-degrees. Count visited nodes. If visitedCount == numCourses, valid.",
        "complexity": "Time: O(V + E), Space: O(V + E)",
        "solution": """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);
        for (const auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            inDegree[p[0]]++;
        }
        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.push(i);
        }
        int processed = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            processed++;
            for (int v : adj[u]) {
                if (--inDegree[v] == 0) q.push(v);
            }
        }
        return processed == numCourses;
    }
};"""
    },
    {
        "id": 15, "day": 5,
        "title": "Implement Trie (Prefix Tree)",
        "leetcodeUrl": "https://leetcode.com/problems/implement-trie-prefix-tree/",
        "topic": "Tries", "subtopic": "Prefix Tree Design", "difficulty": "Medium",
        "pattern": "Trie Data Structure Design",
        "whyItMatters": "Core interview problem for prefix search, autocomplete, and string dictionaries.",
        "interviewSignal": "Implement insert, search, and startsWith for dictionary of words.",
        "hint": "Each node should store an array/map of child pointers (size 26) and a boolean flag isEndOfWord.",
        "approach": "Create TrieNode structure with child array and boolean isEnd. For insert/search, walk character by character. For startsWith, check if path exists.",
        "complexity": "Time: O(L) per operation where L is string length, Space: O(Total characters * AlphabetSize)",
        "solution": """#include <string>
#include <vector>
using namespace std;

class Trie {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root;
public:
    Trie() { root = new Node(); }
    
    void insert(string word) {
        Node* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) curr->children[idx] = new Node();
            curr = curr->children[idx];
        }
        curr->isEnd = true;
    }
    
    bool search(string word) {
        Node* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return curr->isEnd;
    }
    
    bool startsWith(string prefix) {
        Node* curr = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return true;
    }
};"""
    }
]

print(f"Loaded initial batch. Current question count: {len(questions)}")
