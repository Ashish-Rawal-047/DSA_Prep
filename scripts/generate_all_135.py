import json
import re

# Helper function to generate clean C++ solutions and question objects
def make_q(id_num, day_num, title, slug, topic, subtopic, difficulty, pattern, why_matters, signal, hint, approach, complexity, solution):
    return {
        "id": id_num,
        "day": day_num,
        "title": title,
        "leetcodeUrl": f"https://leetcode.com/problems/{slug}/",
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "pattern": pattern,
        "whyItMatters": why_matters,
        "interviewSignal": signal,
        "hint": hint,
        "approach": approach,
        "complexity": complexity,
        "solution": solution.strip()
    }

questions_data = []

# ==============================================================================
# PHASE 1: DAYS 1 - 10 (30 questions)
# ==============================================================================

# Day 1: Arrays + Strings + Bit Manipulation
questions_data.append(make_q(
    1, 1, "Two Sum II - Input Array Is Sorted", "two-sum-ii-input-array-is-sorted",
    "Arrays", "Two Pointers", "Medium", "Opposite-Direction Two Pointers",
    "Tests recognizing sorted property to achieve O(1) auxiliary space without hashing overhead.",
    "Sorted array, find pair satisfying target sum in O(1) extra space.",
    "Since the array is sorted in ascending order, how does moving the left pointer right or the right pointer left change the sum?",
    "Initialize left = 0, right = n - 1. If numbers[left] + numbers[right] == target, return {left+1, right+1}. If sum < target, advance left++. If sum > target, decrement right--.",
    "Time: O(N), Space: O(1)",
    """#include <vector>
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
))

questions_data.append(make_q(
    2, 1, "Longest Substring Without Repeating Characters", "longest-substring-without-repeating-characters",
    "Strings", "Sliding Window", "Medium", "Variable-Size Sliding Window",
    "Fundamental benchmark problem for variable-size sliding window with lookup tables.",
    "Longest contiguous substring containing unique/non-repeating elements.",
    "Store the last seen index of each character. When a repeating character is encountered, can you jump the window's left boundary?",
    "Maintain a sliding window [left, right] and a vector or hash table of last seen indices. When s[right] was seen >= left, update left = lastSeen[s[right]] + 1. Update maxLen = max(maxLen, right - left + 1).",
    "Time: O(N), Space: O(min(N, Sigma)) where Sigma is alphabet size",
    """#include <string>
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
))

questions_data.append(make_q(
    3, 1, "Counting Bits", "counting-bits",
    "Bit Manipulation", "Bitwise DP", "Easy", "Bitwise State Transition",
    "Foundational bridge between bit manipulation and dynamic programming in linear time.",
    "Count set bits for all numbers from 0 to N in O(N) time without built-ins.",
    "How does the number of set bits of x relate to x >> 1 and x & 1?",
    "Use relation dp[i] = dp[i >> 1] + (i & 1). Right shift removes least significant bit whose count was previously computed; add lowest bit parity.",
    "Time: O(N), Space: O(1) auxiliary",
    """#include <vector>
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
))

# Day 2: Graphs + Trees + Dynamic Programming
questions_data.append(make_q(
    4, 2, "Number of Islands", "number-of-islands",
    "Graphs", "Grid BFS/DFS", "Medium", "Connected Components via Flood Fill",
    "Essential interview question for modeling 2D matrix as an implicit graph with connected component traversal.",
    "Count distinct connected clusters in a 2D matrix.",
    "When you find a '1', sink the entire connected landmass to '0' using DFS/BFS so it won't be counted again.",
    "Iterate through grid cells. When grid[r][c] == '1', increment island count and call DFS to visit and mark all 4-directional connected '1's as '0'.",
    "Time: O(R * C), Space: O(R * C) recursion depth",
    """#include <vector>
using namespace std;

class Solution {
    void dfs(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || r >= grid.size() || c < 0 || c >= grid[0].size() || grid[r][c] != '1')
            return;
        grid[r][c] = '0';
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
))

questions_data.append(make_q(
    5, 2, "Diameter of Binary Tree", "diameter-of-binary-tree",
    "Trees", "Tree Depth / Path", "Easy", "Post-Order Tree Traversal",
    "Teaches maintaining a global optimum while returning a local subtree metric to parent.",
    "Longest path between any two nodes in a tree, not necessarily through the root.",
    "The longest path passing through current node as highest point is left_height + right_height.",
    "Use post-order DFS returning the height of node. At node, update maxDiameter = max(maxDiameter, leftH + rightH). Return 1 + max(leftH, rightH).",
    "Time: O(N), Space: O(H)",
    """#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    int maxDiameter = 0;
    int height(TreeNode* node) {
        if (!node) return 0;
        int lh = height(node->left);
        int rh = height(node->right);
        maxDiameter = max(maxDiameter, lh + rh);
        return 1 + max(lh, rh);
    }
public:
    int diameterOfBinaryTree(TreeNode* root) {
        maxDiameter = 0;
        height(root);
        return maxDiameter;
    }
};"""
))

questions_data.append(make_q(
    6, 2, "Maximum Subarray", "maximum-subarray",
    "Dynamic Programming", "1D DP / Kadane", "Medium", "Kadane's Algorithm",
    "Foundational dynamic programming and greedy subarray pattern.",
    "Contiguous subarray with largest sum with negative values.",
    "At every element, decide: extend existing running subarray or restart fresh from this element?",
    "Maintain currentSum = max(nums[i], currentSum + nums[i]) and track global maximum maxSum.",
    "Time: O(N), Space: O(1)",
    """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int currentSum = nums[0], maxSum = nums[0];
        for (size_t i = 1; i < nums.size(); i++) {
            currentSum = max(nums[i], currentSum + nums[i]);
            maxSum = max(maxSum, currentSum);
        }
        return maxSum;
    }
};"""
))

# Day 3: Binary Search + Stack + Intervals
questions_data.append(make_q(
    7, 3, "Koko Eating Bananas", "koko-eating-bananas",
    "Binary Search", "Binary Search on Answer", "Medium", "Binary Search on Monotonic Predicate",
    "High-frequency interview question checking ability to recognize binary search on a search space rather than an array.",
    "Find minimum rate/speed/threshold such that condition is satisfied within given time.",
    "Speed k ranges from 1 to max(piles). As k increases, hours needed strictly decreases. Can we binary search on k?",
    "Binary search range [1, max(piles)]. For mid, calculate total hours sum(ceil(p / mid)). If total <= h, search left half (high = mid - 1); otherwise search right (low = mid + 1).",
    "Time: O(N * log(max(piles))), Space: O(1)",
    """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    bool canFinish(const vector<int>& piles, int h, int k) {
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
            if (canFinish(piles, h, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }
};"""
))

questions_data.append(make_q(
    8, 3, "Daily Temperatures", "daily-temperatures",
    "Stack", "Monotonic Stack", "Medium", "Monotonic Decreasing Stack",
    "Core monotonic stack template for finding next greater element distance in linear time.",
    "Distance to next strictly greater element in sequence.",
    "Store indices in stack. When current temperature is higher than stack top, the waiting days for stack top is resolved!",
    "Traverse array. While stack non-empty and temperatures[i] > temperatures[st.top()], pop index prev and set ans[prev] = i - prev. Push current index i.",
    "Time: O(N), Space: O(N)",
    """#include <vector>
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
))

questions_data.append(make_q(
    9, 3, "Non-overlapping Intervals", "non-overlapping-intervals",
    "Intervals", "Greedy Scheduling", "Medium", "Earliest End Time Scheduling",
    "Classic interval scheduling theorem: minimize removals by keeping earliest finishing intervals.",
    "Minimum number of intervals to remove to eliminate all overlaps.",
    "Sort intervals by end time. If an interval starts before previous chosen interval ends, remove it.",
    "Sort by interval[1]. Keep track of end time of last retained interval. If intervals[i][0] < lastEnd, increment removals. Else, update lastEnd = intervals[i][1].",
    "Time: O(N log N), Space: O(1)",
    """#include <vector>
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
))

# Day 4: Linked Lists + Heap + Dynamic Programming
questions_data.append(make_q(
    10, 4, "Reorder List", "reorder-list",
    "Linked Lists", "Two Pointers & In-place Reversal", "Medium", "Middle + Reverse + Interleave",
    "Combines three indispensable pointer manipulation techniques into one in-place algorithm.",
    "Reorder singly linked list L0 -> Ln-1 -> L1 -> Ln-2 in O(1) auxiliary memory.",
    "Can you split list in half, reverse the second half, and alternate nodes from both halves?",
    "1. Use slow/fast pointers to find the middle node. 2. Cut list and reverse the second half. 3. Merge/interleave first half and reversed second half alternately.",
    "Time: O(N), Space: O(1)",
    """struct ListNode {
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
))

questions_data.append(make_q(
    11, 4, "Find Median from Data Stream", "find-median-from-data-stream",
    "Heap", "Two Heaps", "Hard", "Two Heaps (Balanced Median Tracking)",
    "Standard system design and algorithmic interview pattern for continuous percentile tracking.",
    "Real-time stream of numbers, dynamically query median in O(1).",
    "Split numbers into smaller half (max-heap) and larger half (min-heap). Maintain sizes balanced within difference 1.",
    "Push num to maxHeap, then pop top and push to minHeap. If minHeap has more elements than maxHeap, pop top to maxHeap. Median is maxHeap.top() or average of both tops.",
    "Time: addNum O(log N), findMedian O(1), Space: O(N)",
    """#include <queue>
#include <vector>
using namespace std;

class MedianFinder {
    priority_queue<int> maxHeap;
    priority_queue<int, vector<int>, greater<int>> minHeap;
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
))

questions_data.append(make_q(
    12, 4, "Partition Equal Subset Sum", "partition-equal-subset-sum",
    "Dynamic Programming", "0/1 Knapsack", "Medium", "0/1 Knapsack Subset DP",
    "Reduces subset partitioning to standard 0/1 knapsack with space-optimized 1D boolean table.",
    "Partition array into two subsets with equal sum.",
    "If total sum is odd, it's impossible. If even, can we find a subset summing to sum / 2?",
    "Calculate total sum. If sum % 2 != 0 return false. Target = sum / 2. Use 1D bool vector dp[target + 1], dp[0] = true. For each num, iterate j from target down to num: dp[j] = dp[j] || dp[j - num].",
    "Time: O(N * Target), Space: O(Target)",
    """#include <vector>
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
))

# Day 5: Arrays / Prefix Sum + Graphs / DFS + Tries
questions_data.append(make_q(
    13, 5, "Subarray Sum Equals K", "subarray-sum-equals-k",
    "Arrays", "Prefix Sum + Hash Map", "Medium", "Prefix Sum Difference Hashing",
    "Critique interview pattern: prefix sum differences prefix[j] - prefix[i] = k when elements include negative values.",
    "Count contiguous subarrays summing to k with negative numbers present.",
    "If prefixSum - k was seen earlier in the hash map, how many subarrays ending at the current index sum to k?",
    "Keep running prefix sum. If (sum - k) is in hash map, add its frequency to answer. Increment count of sum in map. Base case: map[0] = 1.",
    "Time: O(N), Space: O(N)",
    """#include <vector>
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
))

questions_data.append(make_q(
    14, 5, "Course Schedule", "course-schedule",
    "Graphs", "Topological Sort / Cycle Detection", "Medium", "Directed Graph Cycle Detection",
    "Universal graph dependency problem asked by Tier-1 tech companies.",
    "Course prerequisites, determine if all courses can be finished without deadlock.",
    "Can courses be completed if and only if the directed dependency graph has no directed cycle?",
    "Build adjacency list and in-degree array. Push all nodes with in-degree 0 into queue. Dequeue node, decrement neighbors' in-degrees, and push newly 0-in-degree nodes. Return processedCount == numCourses.",
    "Time: O(V + E), Space: O(V + E)",
    """#include <vector>
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
))

questions_data.append(make_q(
    15, 5, "Implement Trie (Prefix Tree)", "implement-trie-prefix-tree",
    "Tries", "Prefix Tree Design", "Medium", "Trie Node Architecture",
    "Fundamental data structure implementation for autocomplete, dictionary, and prefix queries.",
    "Implement insert, search, and startsWith for string prefix operations.",
    "Each node has an array of child node pointers (size 26) and a boolean isEnd.",
    "Define Node struct with children[26] and bool isEnd. Traverse character by character: create new node if missing on insert; return false if missing on search/startsWith.",
    "Time: O(L) per operation, Space: O(Total characters * 26)",
    """#include <string>
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
))

# Day 6: Trees + Sliding Window + Dynamic Programming
questions_data.append(make_q(
    16, 6, "Lowest Common Ancestor of a Binary Tree", "lowest-common-ancestor-of-a-binary-tree",
    "Trees", "Lowest Common Ancestor", "Medium", "Recursive Tree Division",
    "Fundamental tree recursion pattern where results from left and right subtrees are merged.",
    "Find lowest node in binary tree that has both p and q as descendants.",
    "If current node is p or q or null, return it. If both left and right recursive calls return non-null, what is current node?",
    "Recursive post-order: if root is null or root == p or root == q, return root. Recurse left and right. If both return non-null, root is LCA. If only one returns non-null, return that non-null child.",
    "Time: O(N), Space: O(H)",
    """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) return root;
        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right, p, q);
        if (left && right) return root;
        return left ? left : right;
    }
};"""
))

questions_data.append(make_q(
    17, 6, "Minimum Size Subarray Sum", "minimum-size-subarray-sum",
    "Sliding Window", "Variable-Size Sliding Window", "Medium", "Shrinking Window on Monotonic Sum",
    "Key interview problem demonstrating shrinking window when condition is satisfied (all positive integers).",
    "Shortest subarray with sum >= target in positive integer array.",
    "Expand right to increase sum. Once sum >= target, can you shrink left while maintaining sum >= target?",
    "Expand window by adding nums[right] to sum. While sum >= target, update minLen = min(minLen, right - left + 1), and subtract nums[left++] to shrink window.",
    "Time: O(N), Space: O(1)",
    """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int left = 0, sum = 0, minLen = INT_MAX;
        for (int right = 0; right < (int)nums.size(); right++) {
            sum += nums[right];
            while (sum >= target) {
                minLen = min(minLen, right - left + 1);
                sum -= nums[left++];
            }
        }
        return minLen == INT_MAX ? 0 : minLen;
    }
};"""
))

questions_data.append(make_q(
    18, 6, "Unique Paths II", "unique-paths-ii",
    "Dynamic Programming", "2D Grid DP", "Medium", "Grid DP with Obstacles",
    "Tests state transitions in a matrix with blocked states and space optimization.",
    "Unique paths in grid from top-left to bottom-right with obstacles.",
    "If cell has an obstacle, dp[r][c] = 0. Otherwise, paths equal sum of paths from top and left cells.",
    "Use 1D dp array of size cols. If obstacleGrid[i][j] == 1, dp[j] = 0; else if j > 0, dp[j] += dp[j - 1]. Initialize dp[0] = (obstacleGrid[0][0] == 0).",
    "Time: O(R * C), Space: O(C)",
    """#include <vector>
using namespace std;

class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        int m = obstacleGrid.size(), n = obstacleGrid[0].size();
        vector<long long> dp(n, 0);
        dp[0] = obstacleGrid[0][0] == 0 ? 1 : 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (obstacleGrid[i][j] == 1) {
                    dp[j] = 0;
                } else if (j > 0) {
                    dp[j] += dp[j - 1];
                }
            }
        }
        return dp[n - 1];
    }
};"""
))

# Day 7: Stack / Deque + Backtracking + Bit Manipulation
questions_data.append(make_q(
    19, 7, "Sliding Window Maximum", "sliding-window-maximum",
    "Stack", "Monotonic Deque", "Hard", "Monotonic Decreasing Deque",
    "Top-tier interview question on maintaining elements in a sliding window in amortized O(1) time.",
    "Maximum element in sliding window of size k moving across array.",
    "Use a double-ended queue storing indices in decreasing order of element values.",
    "Maintain deque of indices: 1. Remove indices outside [i - k + 1, i]. 2. While deque back has element <= nums[i], pop_back. 3. Push i. Once i >= k - 1, nums[dq.front()] is maximum.",
    "Time: O(N), Space: O(K)",
    """#include <vector>
#include <deque>
using namespace std;

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (!dq.empty() && dq.front() <= i - k) dq.pop_front();
            while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();
            dq.push_back(i);
            if (i >= k - 1) result.push_back(nums[dq.front()]);
        }
        return result;
    }
};"""
))

questions_data.append(make_q(
    20, 7, "Combination Sum II", "combination-sum-ii",
    "Backtracking", "Subsets with Pruning", "Medium", "Backtracking with Duplicate Skipping",
    "Teaches duplicate elimination in backtracking when candidates array contains duplicate numbers.",
    "Combinations that sum to target, each number used once, input has duplicate elements.",
    "Sort the array. During iteration, if nums[i] == nums[i-1] and i > start, skip this duplicate branch.",
    "Sort array. In backtrack(start, target): if target == 0 record combination. For i from start to n-1: if nums[i] > target break; if i > start && nums[i] == nums[i-1] continue. Push nums[i], recurse backtrack(i + 1, target - nums[i]), pop.",
    "Time: O(2^N), Space: O(N)",
    """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    void backtrack(const vector<int>& nums, int start, int target, vector<int>& current, vector<vector<int>>& result) {
        if (target == 0) {
            result.push_back(current);
            return;
        }
        for (int i = start; i < (int)nums.size(); i++) {
            if (nums[i] > target) break;
            if (i > start && nums[i] == nums[i - 1]) continue;
            current.push_back(nums[i]);
            backtrack(nums, i + 1, target - nums[i], current, result);
            current.pop_back();
        }
    }
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        vector<vector<int>> result;
        vector<int> current;
        backtrack(candidates, 0, target, current, result);
        return result;
    }
};"""
))

questions_data.append(make_q(
    21, 7, "Single Number II", "single-number-ii",
    "Bit Manipulation", "Bit Counting / State Machine", "Medium", "Modulo 3 Bit Counter",
    "Tests bitwise counting where every number appears k times except one.",
    "Every element appears 3 times except one which appears once, find it in O(1) space.",
    "Count set bits at each of the 32 bit positions across all numbers. What does count % 3 give?",
    "For each bit pos 0..31, sum bits of all numbers at pos. If sum % 3 != 0, set that bit in result. Alternatively, use ones and twos state machine.",
    "Time: O(32 * N) = O(N), Space: O(1)",
    """#include <vector>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int ones = 0, twos = 0;
        for (int x : nums) {
            ones = (ones ^ x) & ~twos;
            twos = (twos ^ x) & ~ones;
        }
        return ones;
    }
};"""
))

# Day 8: Binary Search + Linked Lists + Greedy
questions_data.append(make_q(
    22, 8, "Search in Rotated Sorted Array", "search-in-rotated-sorted-array",
    "Binary Search", "Modified Binary Search", "Medium", "Halved Sorted Property Search",
    "Definitive modified binary search interview question testing invariant identification.",
    "Search target in rotated sorted array in O(log N).",
    "In any rotated sorted array, dividing at mid leaves at least one half strictly sorted.",
    "Compute mid. If nums[mid] == target, return mid. Check if left half [low..mid] is sorted: if nums[low] <= nums[mid], check if target lies within [nums[low], nums[mid]]; if so high = mid - 1, else low = mid + 1. Otherwise right half is sorted.",
    "Time: O(log N), Space: O(1)",
    """#include <vector>
using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int low = 0, high = nums.size() - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;
            if (nums[low] <= nums[mid]) {
                if (nums[low] <= target && target < nums[mid]) high = mid - 1;
                else low = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[high]) low = mid + 1;
                else high = mid - 1;
            }
        }
        return -1;
    }
};"""
))

questions_data.append(make_q(
    23, 8, "Reverse Nodes in k-Group", "reverse-nodes-in-k-group",
    "Linked Lists", "Grouped Pointer Reversal", "Hard", "K-Group In-place Reversal",
    "Renowned pointer challenge testing boundary conditions and clean pointer updates.",
    "Reverse linked list k nodes at a time in O(1) space.",
    "Check if k nodes exist ahead. If yes, reverse those k nodes, stitch pointers, and move prevGroup to tail of reversed segment.",
    "Use a dummy head. Find kth node from current segment. If fewer than k nodes remain, stop. Otherwise reverse the k-node segment and re-link with prev and next groups.",
    "Time: O(N), Space: O(1)",
    """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* prevGroup = &dummy;
        while (true) {
            ListNode* kth = prevGroup;
            for (int i = 0; i < k && kth; i++) kth = kth->next;
            if (!kth) break;
            ListNode* nextGroup = kth->next;
            ListNode* prev = nextGroup;
            ListNode* curr = prevGroup->next;
            while (curr != nextGroup) {
                ListNode* tmp = curr->next;
                curr->next = prev;
                prev = curr;
                curr = tmp;
            }
            ListNode* tmp = prevGroup->next;
            prevGroup->next = kth;
            prevGroup = tmp;
        }
        return dummy.next;
    }
};"""
))

questions_data.append(make_q(
    24, 8, "Gas Station", "gas-station",
    "Greedy", "Circular Array Traversal", "Medium", "Prefix Fuel Accumulation",
    "Tests greedy deduction: if starting at A fails at B, no station between A and B can reach B.",
    "Circular route of gas stations, find starting index to complete circuit.",
    "If total gas < total cost, completion is impossible. If current tank drops below 0, can any station between start and current be the starting point?",
    "Track totalSurplus and currentTank. If currentTank < 0, reset currentTank = 0 and candidate start = i + 1. At end, return totalSurplus >= 0 ? start : -1.",
    "Time: O(N), Space: O(1)",
    """#include <vector>
using namespace std;

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int totalSurplus = 0, currentTank = 0, startIndex = 0;
        for (int i = 0; i < (int)gas.size(); i++) {
            int net = gas[i] - cost[i];
            totalSurplus += net;
            currentTank += net;
            if (currentTank < 0) {
                startIndex = i + 1;
                currentTank = 0;
            }
        }
        return totalSurplus >= 0 ? startIndex : -1;
    }
};"""
))

# Day 9: Graphs + Heap + Dynamic Programming
questions_data.append(make_q(
    25, 9, "Course Schedule II", "course-schedule-ii",
    "Graphs", "Topological Sort", "Medium", "Kahn's Algorithm Ordering",
    "Extends cycle detection to producing a valid topological order.",
    "Find valid ordering of courses given prerequisite pairs.",
    "Collect nodes as they are popped with in-degree 0. If count == numCourses, the collection is the topological ordering.",
    "Compute in-degrees and build adjacency list. Push nodes with in-degree 0 into queue. Dequeue node, append to order, decrement neighbors' in-degree. Return order if order.size() == numCourses else {}.",
    "Time: O(V + E), Space: O(V + E)",
    """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
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
        vector<int> order;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (int v : adj[u]) {
                if (--inDegree[v] == 0) q.push(v);
            }
        }
        return order.size() == (size_t)numCourses ? order : vector<int>{};
    }
};"""
))

questions_data.append(make_q(
    26, 9, "Merge k Sorted Lists", "merge-k-sorted-lists",
    "Heap", "K-Way Merge", "Hard", "Min-Heap K-Way Pointer Merge",
    "Classic multi-way merge pattern used in external sorting and priority queues.",
    "Merge k sorted linked lists into one sorted list.",
    "Put the heads of all k lists into a min-heap. Pop the smallest node, link it, and push its next node into the heap.",
    "Maintain a min-heap of ListNode* comparing node->val. Insert non-null heads. Repeatedly extract min, append to result list, and if extracted node has a next, push next into min-heap.",
    "Time: O(N log K) where N is total nodes, Space: O(K)",
    """#include <vector>
#include <queue>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
    struct Compare {
        bool operator()(const ListNode* a, const ListNode* b) {
            return a->val > b->val;
        }
    };
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        priority_queue<ListNode*, vector<ListNode*>, Compare> minHeap;
        for (auto l : lists) {
            if (l) minHeap.push(l);
        }
        ListNode dummy(0);
        ListNode* tail = &dummy;
        while (!minHeap.empty()) {
            ListNode* node = minHeap.top();
            minHeap.pop();
            tail->next = node;
            tail = tail->next;
            if (node->next) minHeap.push(node->next);
        }
        return dummy.next;
    }
};"""
))

questions_data.append(make_q(
    27, 9, "Coin Change", "coin-change",
    "Dynamic Programming", "Unbounded Knapsack", "Medium", "Unbounded Knapsack DP",
    "Fundamental DP question on bottom-up state transition with unlimited item usage.",
    "Fewest coins to make up given amount with infinite coin supply.",
    "Let dp[i] be min coins for amount i. For every coin, dp[i] = min(dp[i], dp[i - coin] + 1).",
    "Initialize dp array of size amount + 1 with amount + 1. dp[0] = 0. For i from 1 to amount, for each coin in coins: if i >= coin, dp[i] = min(dp[i], dp[i - coin] + 1). Return dp[amount] > amount ? -1 : dp[amount].",
    "Time: O(Amount * Coins), Space: O(Amount)",
    """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int c : coins) {
                if (i >= c) dp[i] = min(dp[i], dp[i - c] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
};"""
))

# Day 10: Trees + Arrays / Hash Map + Strings / DP
questions_data.append(make_q(
    28, 10, "Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum",
    "Trees", "Tree DP", "Hard", "Tree Bottom-Up Path Sum",
    "One of the most frequently asked tree problems by Meta and Google.",
    "Maximum path sum in binary tree, any node to any node.",
    "At any node, the maximum path with that node as peak is node->val + max(0, leftGain) + max(0, rightGain).",
    "Post-order traversal: compute max gain from left and right children (floored at 0). Update global max with node->val + leftGain + rightGain. Return node->val + max(leftGain, rightGain) to parent.",
    "Time: O(N), Space: O(H)",
    """#include <algorithm>
#include <climits>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    int maxSum = INT_MIN;
    int maxGain(TreeNode* node) {
        if (!node) return 0;
        int left = max(0, maxGain(node->left));
        int right = max(0, maxGain(node->right));
        maxSum = max(maxSum, node->val + left + right);
        return node->val + max(left, right);
    }
public:
    int maxPathSum(TreeNode* root) {
        maxSum = INT_MIN;
        maxGain(root);
        return maxSum;
    }
};"""
))

questions_data.append(make_q(
    29, 10, "Longest Consecutive Sequence", "longest-consecutive-sequence",
    "Arrays", "Hash Set Sequence Building", "Medium", "Sequence Origin Identification",
    "Tests solving sequence problems in O(N) time without sorting.",
    "Longest consecutive numbers sequence in unsorted array in O(N).",
    "Put all numbers in hash set. An element x starts a sequence only if x - 1 is NOT in the set.",
    "Insert all elements into unordered_set. Loop through elements: if !set.count(x - 1), it is the start of a streak! Count while set.count(x + len) is true. Update maxStreak.",
    "Time: O(N), Space: O(N)",
    """#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> numSet(nums.begin(), nums.end());
        int longest = 0;
        for (int num : numSet) {
            if (!numSet.count(num - 1)) {
                int current = num;
                int streak = 1;
                while (numSet.count(current + 1)) {
                    current++;
                    streak++;
                }
                longest = max(longest, streak);
            }
        }
        return longest;
    }
};"""
))

questions_data.append(make_q(
    30, 10, "Palindromic Substrings", "palindromic-substrings",
    "Strings", "Expand Around Center", "Medium", "Center Expansion / Two Pointers",
    "Tests dual center expansion (odd and even length) in O(N^2) time and O(1) space.",
    "Count all palindromic substrings in a string.",
    "Every palindrome has a center: either a single character (odd length) or a character pair (even length).",
    "For each index i, expand outward for odd center (i, i) and even center (i, i + 1). While characters match, increment palindrome count and expand pointers.",
    "Time: O(N^2), Space: O(1)",
    """#include <string>
using namespace std;

class Solution {
    int countCenters(const string& s, int l, int r) {
        int cnt = 0;
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) {
            cnt++;
            l--;
            r++;
        }
        return cnt;
    }
public:
    int countSubstrings(string s) {
        int total = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            total += countCenters(s, i, i);     // odd length
            total += countCenters(s, i, i + 1); // even length
        }
        return total;
    }
};"""
))

print(f"Phase 1 complete. Question count: {len(questions_data)}")
