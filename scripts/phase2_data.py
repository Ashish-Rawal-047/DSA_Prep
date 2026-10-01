def get_phase2_questions(make_q):
    p2 = []
    
    # Day 11: Arrays + Graphs + Dynamic Programming
    p2.append(make_q(
        31, 11, "3Sum", "3sum",
        "Arrays", "Two Pointers", "Medium", "Sorting + Dual Pointers with Dedup",
        "Benchmark interview question testing two-pointer search with duplicate elimination.",
        "Find all unique triplets in array that sum to zero.",
        "Sort array. For each i, reduce problem to finding two elements summing to -nums[i] using two pointers. Skip duplicates for all three pointers.",
        "Sort nums. Iterate i from 0 to n-3. If i > 0 and nums[i] == nums[i-1] continue. Use left = i + 1, right = n - 1. When sum == 0, save triplet and advance left/right while skipping duplicates.",
        "Time: O(N^2), Space: O(1) or O(log N) auxiliary",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        int n = nums.size();
        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = n - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    res.push_back({nums[i], nums[l], nums[r]});
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (sum < 0) {
                    l++;
                } else {
                    r--;
                }
            }
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        32, 11, "Rotting Oranges", "rotting-oranges",
        "Graphs", "Multi-source BFS", "Medium", "Level-by-Level Multi-source BFS",
        "Classic multi-source BFS simulation representing contagion, fire spread, or signal propagation.",
        "Minimum minutes until all fresh oranges rot from multiple initial rotten oranges.",
        "Add all initially rotten oranges to the queue simultaneously. Each BFS level represents one minute elapsed.",
        "Enqueue all cells with val 2 and count fresh oranges (val 1). Run level-order BFS: pop current level, rot 4-directional fresh neighbors, decrement fresh count, enqueue them. Return fresh == 0 ? minutes : -1.",
        "Time: O(R * C), Space: O(R * C)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        queue<pair<int, int>> q;
        int fresh = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) q.push({i, j});
                else if (grid[i][j] == 1) fresh++;
            }
        }
        if (fresh == 0) return 0;
        int minutes = 0;
        int dirs[4][2] = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        while (!q.empty()) {
            int sz = q.size();
            bool rottedAny = false;
            for (int k = 0; k < sz; k++) {
                auto [r, c] = q.front(); q.pop();
                for (auto& d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;
                        fresh--;
                        q.push({nr, nc});
                        rottedAny = true;
                    }
                }
            }
            if (rottedAny) minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }
};"""
    ))

    p2.append(make_q(
        33, 11, "Longest Increasing Subsequence", "longest-increasing-subsequence",
        "Dynamic Programming", "LIS / Binary Search", "Medium", "Patience Sorting / Binary Search",
        "Premier subsequence problem testing both O(N^2) DP intuition and O(N log N) patience sorting.",
        "Length of longest strictly increasing subsequence in unsorted array.",
        "Maintain tails array where tails[i] stores smallest tail of all increasing subsequences of length i+1. Use binary search (lower_bound) to update.",
        "For each num, find position using lower_bound in tails vector. If iterator == tails.end(), append num. Otherwise overwrite *it = num. Result is tails.size().",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (int x : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x);
            else *it = x;
        }
        return tails.size();
    }
};"""
    ))

    # Day 12: Binary Search + Stack + Dynamic Programming
    p2.append(make_q(
        34, 12, "Find Peak Element", "find-peak-element",
        "Binary Search", "Unsorted Binary Search", "Medium", "Local Gradient Binary Search",
        "Demonstrates binary search on an unsorted array following local slope/derivative.",
        "Find a peak element strictly greater than its neighbors in O(log N).",
        "Compare nums[mid] with nums[mid + 1]. If nums[mid] < nums[mid + 1], an uphill slope guarantees a peak exists on the right half.",
        "Set low = 0, high = n - 1. While low < high: mid = low + (high - low) / 2. If nums[mid] < nums[mid + 1], low = mid + 1; else high = mid. Return low.",
        "Time: O(log N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int low = 0, high = nums.size() - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] < nums[mid + 1]) low = mid + 1;
            else high = mid;
        }
        return low;
    }
};"""
    ))

    p2.append(make_q(
        35, 12, "Next Greater Element II", "next-greater-element-ii",
        "Stack", "Circular Monotonic Stack", "Medium", "Circular Array Monotonic Stack",
        "Demonstrates standard technique for handling circular arrays: traversing up to 2 * N using modulo.",
        "Next greater element in circular array.",
        "Loop twice through the array (indices 0 to 2*n - 1) using i % n, maintaining monotonic decreasing stack.",
        "Initialize res vector with -1. Loop i from 0 to 2*n - 1. While stack has elements and nums[st.top()] < nums[i % n], pop index and set res[popped] = nums[i % n]. If i < n, push i to stack.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, -1);
        stack<int> st;
        for (int i = 0; i < 2 * n; i++) {
            int num = nums[i % n];
            while (!st.empty() && nums[st.top()] < num) {
                res[st.top()] = num;
                st.pop();
            }
            if (i < n) st.push(i);
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        36, 12, "Maximum Product Subarray", "maximum-product-subarray",
        "Dynamic Programming", "Subarray State DP", "Medium", "Dual Extremum Tracking",
        "Crucial interview pattern: tracking both max and min because multiplying by a negative flips minimum to maximum.",
        "Contiguous subarray with largest product, including negative values.",
        "When current number is negative, swapping maxProd and minProd captures the flip.",
        "Track maxProd and minProd. For each x: if x < 0, swap(maxProd, minProd). maxProd = max(x, maxProd * x), minProd = min(x, minProd * x). Update result with maxProd.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int maxP = nums[0], minP = nums[0], res = nums[0];
        for (size_t i = 1; i < nums.size(); i++) {
            if (nums[i] < 0) swap(maxP, minP);
            maxP = max(nums[i], maxP * nums[i]);
            minP = min(nums[i], minP * nums[i]);
            res = max(res, maxP);
        }
        return res;
    }
};"""
    ))

    # Day 13: Graphs + Trees + Dynamic Programming
    p2.append(make_q(
        37, 13, "Clone Graph", "clone-graph",
        "Graphs", "Graph Traversal / Deep Copy", "Medium", "Hash Map Visited Node Mapping",
        "Core design question testing deep copy of cyclic graph structures.",
        "Deep copy of connected undirected graph where nodes have neighbors list.",
        "Use a hash map mapping original Node* to cloned Node* to avoid infinite loops on cycles.",
        "DFS function takes original node. If in map, return clone. Create clone node, insert in map. Recursively clone all neighbors and push to clone->neighbors.",
        "Time: O(V + E), Space: O(V)",
        """#include <vector>
#include <unordered_map>
using namespace std;

class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node(int _val) : val(_val) {}
};

class Solution {
    unordered_map<Node*, Node*> clones;
public:
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        if (clones.count(node)) return clones[node];
        Node* copy = new Node(node->val);
        clones[node] = copy;
        for (Node* neighbor : node->neighbors) {
            copy->neighbors.push_back(cloneGraph(neighbor));
        }
        return copy;
    }
};"""
    ))

    p2.append(make_q(
        38, 13, "Validate Binary Search Tree", "validate-binary-search-tree",
        "Trees", "BST Invariants", "Medium", "Bounded Subtree Range Verification",
        "Checks understanding of global BST property (all left descendants < root < all right descendants).",
        "Determine if given binary tree is a valid Binary Search Tree.",
        "Passing a valid range [minVal, maxVal] downwards ensures no node violates ancestral boundaries.",
        "Helper dfs(node, low, high): if !node return true. If node->val <= low or node->val >= high return false. Recurse dfs(node->left, low, node->val) and dfs(node->right, node->val, high).",
        "Time: O(N), Space: O(H)",
        """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    bool validate(TreeNode* node, long long low, long long high) {
        if (!node) return true;
        if (node->val <= low || node->val >= high) return false;
        return validate(node->left, low, node->val) && validate(node->right, node->val, high);
    }
public:
    bool isValidBST(TreeNode* root) {
        return validate(root, -1e18, 1e18);
    }
};"""
    ))

    p2.append(make_q(
        39, 13, "Word Break", "word-break",
        "Dynamic Programming", "String DP", "Medium", "1D Prefix Partitioning DP",
        "Classic string segmentation problem asked in Google, Amazon, and Bloomberg rounds.",
        "Determine if string can be segmented into space-separated dictionary words.",
        "dp[i] is true if s[0..i-1] can be segmented. For j from 0 to i-1: if dp[j] is true and s[j..i-1] is in dict, dp[i] is true.",
        "Store dictionary in unordered_set. Initialize vector<bool> dp(n + 1, false) with dp[0] = true. For i from 1 to n: for j from 0 to i-1: if dp[j] and set.count(s.substr(j, i - j)), dp[i] = true, break.",
        "Time: O(N^2 * L), Space: O(N + DictSize)",
        """#include <string>
#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        int n = s.size();
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && dict.count(s.substr(j, i - j))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[n];
    }
};"""
    ))

    # Day 14: Strings / Sliding Window + Heap + Greedy
    p2.append(make_q(
        40, 14, "Minimum Window Substring", "minimum-window-substring",
        "Strings", "Sliding Window", "Hard", "Two Pointers with Character Frequency Matching",
        "Top-level sliding window interview problem requiring exact multiset frequency tracking.",
        "Smallest substring in S containing all characters of T.",
        "Keep target frequency map and count of required unique characters satisfied. Shrink left pointer when window is valid.",
        "Track char frequency of t. Expand right: if s[right] matches frequency in t, increment matched. While matched == required: update minWindow, increment left boundary and adjust frequency.",
        "Time: O(S + T), Space: O(128) = O(1)",
        """#include <string>
#include <vector>
#include <climits>
using namespace std;

class Solution {
public:
    string minWindow(string s, string t) {
        vector<int> target(128, 0), window(128, 0);
        for (char c : t) target[(unsigned char)c]++;
        int required = 0;
        for (int cnt : target) if (cnt > 0) required++;
        int formed = 0, l = 0, minLen = INT_MAX, startIdx = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            char c = s[r];
            window[(unsigned char)c]++;
            if (target[(unsigned char)c] > 0 && window[(unsigned char)c] == target[(unsigned char)c]) {
                formed++;
            }
            while (formed == required) {
                if (r - l + 1 < minLen) {
                    minLen = r - l + 1;
                    startIdx = l;
                }
                char lc = s[l++];
                window[(unsigned char)lc]--;
                if (target[(unsigned char)lc] > 0 && window[(unsigned char)lc] < target[(unsigned char)lc]) {
                    formed--;
                }
            }
        }
        return minLen == INT_MAX ? "" : s.substr(startIdx, minLen);
    }
};"""
    ))

    p2.append(make_q(
        41, 14, "Kth Largest Element in an Array", "kth-largest-element-in-an-array",
        "Heap", "Min-Heap / Quickselect", "Medium", "Min-Heap of Size K",
        "Benchmark question evaluating understanding of heaps vs quickselect for order statistics.",
        "Find the kth largest element in an unsorted array.",
        "Keep a min-heap of size k. The top will always be the kth largest seen so far.",
        "Push numbers into min-heap. When size > k, pop(). The top at the end is the kth largest.",
        "Time: O(N log K), Space: O(K)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (int x : nums) {
            minHeap.push(x);
            if (minHeap.size() > (size_t)k) minHeap.pop();
        }
        return minHeap.top();
    }
};"""
    ))

    p2.append(make_q(
        42, 14, "Task Scheduler", "task-scheduler",
        "Greedy", "Greedy Frequency Slotting", "Medium", "Formula-based Slot Allocation",
        "Tests calculating idle slots from the highest frequency task.",
        "Minimum CPU intervals to finish tasks with cooldown n between identical tasks.",
        "The task with maximum frequency determines the frame structure. Count how many tasks share this max frequency.",
        "Find maxFreq and count of tasks with maxFreq. Formula: max((int)tasks.size(), (maxFreq - 1) * (n + 1) + maxCount).",
        "Time: O(N), Space: O(1) [26 characters]",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> freq(26, 0);
        int maxFreq = 0;
        for (char t : tasks) {
            freq[t - 'A']++;
            maxFreq = max(maxFreq, freq[t - 'A']);
        }
        int maxCount = 0;
        for (int f : freq) if (f == maxFreq) maxCount++;
        int partCount = maxFreq - 1;
        int emptySlots = partCount * (n - (maxCount - 1));
        int availableTasks = tasks.size() - maxFreq * maxCount;
        int idles = max(0, emptySlots - availableTasks);
        return tasks.size() + idles;
    }
};"""
    ))

    # Day 15: Backtracking + Linked Lists + Bit Manipulation
    p2.append(make_q(
        43, 15, "Subsets II", "subsets-ii",
        "Backtracking", "Subsets with Duplicates", "Medium", "Sorted Branch Duplicate Elimination",
        "Pruning duplicate subset trees when elements are non-unique.",
        "Generate all possible subsets of array containing duplicate numbers.",
        "Sort input. At current recursion level, if i > start && nums[i] == nums[i-1], skip.",
        "Sort nums. Backtrack(start): push current to result. Loop i from start to n-1: if i > start && nums[i] == nums[i-1] continue; push nums[i], recurse backtrack(i+1), pop.",
        "Time: O(2^N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    void backtrack(const vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& res) {
        res.push_back(curr);
        for (int i = start; i < (int)nums.size(); i++) {
            if (i > start && nums[i] == nums[i - 1]) continue;
            curr.push_back(nums[i]);
            backtrack(nums, i + 1, curr, res);
            curr.pop_back();
        }
    }
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        vector<int> curr;
        backtrack(nums, 0, curr, res);
        return res;
    }
};"""
    ))

    p2.append(make_q(
        44, 15, "Copy List with Random Pointer", "copy-list-with-random-pointer",
        "Linked Lists", "Deep Copy / Interleaving", "Medium", "Node Interweaving in O(1) Memory",
        "Tests pointer replication without auxiliary hash map using node weaving.",
        "Clone singly linked list where nodes contain arbitrary random pointers.",
        "Weave cloned nodes right after original nodes: A -> A' -> B -> B'. Then clone random pointers: curr->next->random = curr->random->next.",
        "Pass 1: Insert copy node after each node. Pass 2: Set copy->random = orig->random ? orig->random->next : nullptr. Pass 3: Separate original and cloned lists.",
        "Time: O(N), Space: O(1) auxiliary",
        """class Node {
public:
    int val;
    Node* next;
    Node* random;
    Node(int _val) : val(_val), next(nullptr), random(nullptr) {}
};

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;
        Node* curr = head;
        while (curr) {
            Node* copy = new Node(curr->val);
            copy->next = curr->next;
            curr->next = copy;
            curr = copy->next;
        }
        curr = head;
        while (curr) {
            if (curr->random) curr->next->random = curr->random->next;
            curr = curr->next->next;
        }
        curr = head;
        Node* copyHead = head->next;
        while (curr) {
            Node* copy = curr->next;
            curr->next = copy->next;
            if (copy->next) copy->next = copy->next->next;
            curr = curr->next;
        }
        return copyHead;
    }
};"""
    ))

    p2.append(make_q(
        45, 15, "Bitwise AND of Numbers Range", "bitwise-and-of-numbers-range",
        "Bit Manipulation", "Common Prefix Bits", "Medium", "Common Bitwise Prefix Extraction",
        "Interview question testing bit-level range properties: any differing bit across range must become 0.",
        "Bitwise AND of all integers in range [left, right].",
        "Any bit that changes between left and right becomes 0. The result is the common binary prefix.",
        "Right shift left and right until left == right, counting shifts. Left shift back by that count.",
        "Time: O(log(right)) = O(32) = O(1), Space: O(1)",
        """class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int shift = 0;
        while (left < right) {
            left >>= 1;
            right >>= 1;
            shift++;
        }
        return left << shift;
    }
};"""
    ))

    # Day 16: Graphs + Trees + Dynamic Programming
    p2.append(make_q(
        46, 16, "Pacific Atlantic Water Flow", "pacific-atlantic-water-flow",
        "Graphs", "Multi-source DFS/BFS", "Medium", "Reverse Ocean Infiltration",
        "Teaches reversing the problem direction: starting from oceans inwards rather than cell by cell.",
        "Cells from which water can flow to both Pacific and Atlantic oceans.",
        "Start BFS/DFS from Pacific boundary inwards (climbing uphill >=). Do same for Atlantic. Cells reached by both are the answer.",
        "Run DFS from Pacific borders into pacificVisited, and Atlantic borders into atlanticVisited (only moving to neighbors with height >= current). Collect intersection cells.",
        "Time: O(R * C), Space: O(R * C)",
        """#include <vector>
using namespace std;

class Solution {
    int m, n;
    int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    void dfs(const vector<vector<int>>& heights, int r, int c, vector<vector<bool>>& ocean) {
        ocean[r][c] = true;
        for (auto& d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && !ocean[nr][nc] && heights[nr][nc] >= heights[r][c]) {
                dfs(heights, nr, nc, ocean);
            }
        }
    }
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        m = heights.size(); n = heights[0].size();
        vector<vector<bool>> pac(m, vector<bool>(n, false));
        vector<vector<bool>> atl(m, vector<bool>(n, false));
        for (int i = 0; i < m; i++) {
            dfs(heights, i, 0, pac);
            dfs(heights, i, n - 1, atl);
        }
        for (int j = 0; j < n; j++) {
            dfs(heights, 0, j, pac);
            dfs(heights, m - 1, j, atl);
        }
        vector<vector<int>> res;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (pac[i][j] && atl[i][j]) res.push_back({i, j});
            }
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        47, 16, "Construct Binary Tree from Preorder and Inorder Traversal", "construct-binary-tree-from-preorder-and-inorder-traversal",
        "Trees", "Tree Reconstruction", "Medium", "Preorder Root + Inorder Partitioning",
        "Classic tree reconstruction testing recursion boundaries and traversal properties.",
        "Reconstruct binary tree given preorder and inorder traversals.",
        "First element of preorder is root. Locate root in inorder: elements left of it form left subtree, elements right form right subtree.",
        "Use hashmap for O(1) lookup of root in inorder. Recursively build root, left child using left subtree size, and right child.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <unordered_map>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    unordered_map<int, int> inMap;
    int preIdx = 0;
    TreeNode* build(const vector<int>& preorder, int inStart, int inEnd) {
        if (inStart > inEnd) return nullptr;
        int rootVal = preorder[preIdx++];
        TreeNode* root = new TreeNode(rootVal);
        int mid = inMap[rootVal];
        root->left = build(preorder, inStart, mid - 1);
        root->right = build(preorder, mid + 1, inEnd);
        return root;
    }
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        for (int i = 0; i < (int)inorder.size(); i++) inMap[inorder[i]] = i;
        preIdx = 0;
        return build(preorder, 0, inorder.size() - 1);
    }
};"""
    ))

    p2.append(make_q(
        48, 16, "Target Sum", "target-sum",
        "Dynamic Programming", "0/1 Knapsack Transformation", "Medium", "Subset Sum Reduction",
        "Transforms assignment of +/- signs into finding positive subset sum (P = (target + total) / 2).",
        "Number of ways to assign + and - to achieve target sum.",
        "Let P be sum of positive numbers and N negative. P - N = target and P + N = total. So 2P = target + total -> P = (target + total) / 2.",
        "If (total + target) < 0 or (total + target) % 2 != 0, return 0. Target subset = (total + target) / 2. Run 1D 0/1 knapsack counting ways.",
        "Time: O(N * S), Space: O(S)",
        """#include <vector>
#include <numeric>
#include <cmath>
using namespace std;

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (abs(target) > total || (total + target) % 2 != 0) return 0;
        int s = (total + target) / 2;
        vector<int> dp(s + 1, 0);
        dp[0] = 1;
        for (int x : nums) {
            for (int j = s; j >= x; j--) {
                dp[j] += dp[j - x];
            }
        }
        return dp[s];
    }
};"""
    ))

    # Day 17: Binary Search / Matrix + Stack + Intervals
    p2.append(make_q(
        49, 17, "Search a 2D Matrix II", "search-a-2d-matrix-ii",
        "Binary Search", "Matrix Elimination", "Medium", "Staircase Search from Corner",
        "Tests pointer pruning in 2D sorted matrix starting from top-right or bottom-left.",
        "Search target in row-sorted and column-sorted matrix in O(M + N).",
        "Start at top-right corner. If value > target, col--. If value < target, row++.",
        "Initialize r = 0, c = cols - 1. While r < rows && c >= 0: if matrix[r][c] == target return true. If matrix[r][c] > target c--, else r++.",
        "Time: O(M + N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int r = 0, c = matrix[0].size() - 1;
        while (r < (int)matrix.size() && c >= 0) {
            if (matrix[r][c] == target) return true;
            if (matrix[r][c] > target) c--;
            else r++;
        }
        return false;
    }
};"""
    ))

    p2.append(make_q(
        50, 17, "Largest Rectangle in Histogram", "largest-rectangle-in-histogram",
        "Stack", "Monotonic Stack", "Hard", "Monotonic Increasing Stack with Width Calculation",
        "One of the most famous algorithmic interview challenges for monotonic stacks.",
        "Largest rectangular area possible in histogram heights.",
        "For each bar as the shortest bar, what is the farthest left and right it can extend?",
        "Maintain stack of indices with increasing heights. When popping bar at height h, right boundary is current index i and left boundary is new stack top. Width = i - stack.top() - 1. Area = h * width.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        heights.push_back(0); // sentinel
        stack<int> st;
        int maxArea = 0;
        for (int i = 0; i < (int)heights.size(); i++) {
            while (!st.empty() && heights[st.top()] > heights[i]) {
                int h = heights[st.top()]; st.pop();
                int w = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, h * w);
            }
            st.push(i);
        }
        return maxArea;
    }
};"""
    ))

    p2.append(make_q(
        51, 17, "Insert Interval", "insert-interval",
        "Intervals", "Interval Merging", "Medium", "Three-Phase Interval Stitching",
        "High-frequency interval question: insert and merge new interval into already sorted non-overlapping list.",
        "Insert new interval and merge overlapping intervals in sorted list.",
        "3 phases: add all intervals ending before newInterval starts; merge all overlapping intervals; add remaining intervals.",
        "Iterate intervals: 1. while interval[1] < newInterval[0], push. 2. while interval[0] <= newInterval[1], merge: newInterval[0] = min, newInterval[1] = max. 3. push newInterval, then push rest.",
        "Time: O(N), Space: O(1) auxiliary",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> res;
        int i = 0, n = intervals.size();
        while (i < n && intervals[i][1] < newInterval[0]) res.push_back(intervals[i++]);
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        res.push_back(newInterval);
        while (i < n) res.push_back(intervals[i++]);
        return res;
    }
};"""
    ))

    # Day 18: Backtracking + Heap + Dynamic Programming
    p2.append(make_q(
        52, 18, "Permutations II", "permutations-ii",
        "Backtracking", "Permutations with Duplicates", "Medium", "Visited Flag Duplicate Pruning",
        "Tests permutation generation with duplicate elements using sorting and visited flags.",
        "Unique permutations of collection of numbers containing duplicates.",
        "Sort array. If nums[i] == nums[i-1] and !visited[i-1], skip branch to enforce consistent relative ordering.",
        "Sort nums. Track vector<bool> used. Backtrack: if curr.size() == n, save. For i = 0..n-1: if used[i] or (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue. used[i] = true, recurse, used[i] = false.",
        "Time: O(N! * N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    void backtrack(const vector<int>& nums, vector<bool>& used, vector<int>& curr, vector<vector<int>>& res) {
        if (curr.size() == nums.size()) {
            res.push_back(curr);
            return;
        }
        for (int i = 0; i < (int)nums.size(); i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true;
            curr.push_back(nums[i]);
            backtrack(nums, used, curr, res);
            curr.pop_back();
            used[i] = false;
        }
    }
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        vector<int> curr;
        vector<bool> used(nums.size(), false);
        backtrack(nums, used, curr, res);
        return res;
    }
};"""
    ))

    p2.append(make_q(
        53, 18, "Top K Frequent Elements", "top-k-frequent-elements",
        "Heap", "Bucket Sort / Min-Heap", "Medium", "Bucket Sort Frequency Grouping",
        "Top interview question testing frequency counting and O(N) bucket sorting.",
        "Return the k most frequent elements in an integer array in better than O(N log N) time.",
        "Use buckets where index represents frequency! Since frequency <= n, we can gather from bucket n down to 1.",
        "Count frequencies in hash map. Create vector<vector<int>> buckets of size n + 1. Place numbers into their frequency buckets. Traverse buckets backwards and collect k elements.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> freq;
        for (int x : nums) freq[x]++;
        int n = nums.size();
        vector<vector<int>> buckets(n + 1);
        for (auto& [val, count] : freq) {
            buckets[count].push_back(val);
        }
        vector<int> res;
        for (int i = n; i >= 0 && res.size() < (size_t)k; i--) {
            for (int val : buckets[i]) {
                res.push_back(val);
                if (res.size() == (size_t)k) break;
            }
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        54, 18, "House Robber II", "house-robber-ii",
        "Dynamic Programming", "Circular DP", "Medium", "Circular Array Case Division",
        "Teaches circular DP reduction: breaking circular boundary into two linear subproblems [0..n-2] and [1..n-1].",
        "Rob houses arranged in a circle without triggering adjacent alarms.",
        "First house and last house cannot both be robbed. Run linear House Robber on [0..n-2] and on [1..n-1], take max.",
        "If n == 1 return nums[0]. Return max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1)).",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    int robLinear(const vector<int>& nums, int start, int end) {
        int prev1 = 0, prev2 = 0;
        for (int i = start; i <= end; i++) {
            int tmp = max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = tmp;
        }
        return prev1;
    }
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1));
    }
};"""
    ))

    # Day 19: Backtracking + Graphs / Dijkstra + Trees / BST
    p2.append(make_q(
        55, 19, "Word Search", "word-search",
        "Backtracking", "Matrix DFS with Backtracking", "Medium", "Grid In-place Visited Toggling",
        "Standard grid backtracking question asked across FAANG/Tier-1 interviews.",
        "Check if word exists in 2D grid of characters by moving adjacent cells without reusing a cell.",
        "Temporarily replace cell with '#' before recursive exploration, restore original character on backtrack.",
        "For each cell matching word[0], run dfs(r, c, index). If index == word.size() return true. Mark board[r][c] = '#', recurse 4 directions, restore board[r][c] = word[index].",
        "Time: O(M * N * 3^L), Space: O(L) recursion stack",
        """#include <vector>
#include <string>
using namespace std;

class Solution {
    bool dfs(vector<vector<char>>& board, const string& word, int r, int c, int idx) {
        if (idx == (int)word.size()) return true;
        if (r < 0 || r >= board.size() || c < 0 || c >= board[0].size() || board[r][c] != word[idx])
            return false;
        char temp = board[r][c];
        board[r][c] = '#';
        bool found = dfs(board, word, r + 1, c, idx + 1) ||
                     dfs(board, word, r - 1, c, idx + 1) ||
                     dfs(board, word, r, c + 1, idx + 1) ||
                     dfs(board, word, r, c - 1, idx + 1);
        board[r][c] = temp;
        return found;
    }
public:
    bool exist(vector<vector<char>>& board, string word) {
        for (int i = 0; i < board.size(); i++) {
            for (int j = 0; j < board[0].size(); j++) {
                if (board[i][j] == word[0] && dfs(board, word, i, j, 0)) return true;
            }
        }
        return false;
    }
};"""
    ))

    p2.append(make_q(
        56, 19, "Network Delay Time", "network-delay-time",
        "Graphs", "Shortest Path / Dijkstra", "Medium", "Dijkstra's Priority Queue Algorithm",
        "The standard Dijkstra's algorithm interview benchmark for single-source shortest path with non-negative weights.",
        "Time taken for signal from node k to reach all nodes in directed weighted network.",
        "Maintain min-heap of (dist, node). Update dist array when a shorter path is discovered.",
        "Build adjacency list of pairs (neighbor, weight). Initialize dist array with INF, dist[k] = 0. Use priority_queue minHeap. Extract min, relax edges. Return max(dist) if all reached else -1.",
        "Time: O((V + E) log V), Space: O(V + E)",
        """#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int, int>>> adj(n + 1);
        for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
        vector<int> dist(n + 1, 1e9);
        dist[k] = 0;
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, k});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d > dist[u]) continue;
            for (auto& [v, w] : adj[u]) {
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }
        int maxDist = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == 1e9) return -1;
            maxDist = max(maxDist, dist[i]);
        }
        return maxDist;
    }
};"""
    ))

    p2.append(make_q(
        57, 19, "Lowest Common Ancestor of a Binary Search Tree", "lowest-common-ancestor-of-a-binary-search-tree",
        "Trees", "BST Traversal", "Medium", "BST Value Directed Descent",
        "Contrasts general binary tree LCA with BST property to achieve O(H) iterative solution.",
        "Lowest common ancestor in a Binary Search Tree.",
        "If both p and q have values strictly less than root, LCA is in left subtree. If both greater, in right subtree. First node where they split is LCA!",
        "Start at root. While curr: if p->val < curr->val && q->val < curr->val curr = curr->left; else if p->val > curr->val && q->val > curr->val curr = curr->right; else return curr.",
        "Time: O(H), Space: O(1)",
        """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        TreeNode* curr = root;
        while (curr) {
            if (p->val < curr->val && q->val < curr->val) curr = curr->left;
            else if (p->val > curr->val && q->val > curr->val) curr = curr->right;
            else return curr;
        }
        return nullptr;
    }
};"""
    ))

    # Day 20: Arrays + Strings + Dynamic Programming
    p2.append(make_q(
        58, 20, "Product of Array Except Self", "product-of-array-except-self",
        "Arrays", "Prefix & Suffix Products", "Medium", "Two-Pass Prefix and Suffix Accumulation",
        "Essential interview question testing in-place prefix/suffix products without using division.",
        "Product of array except self in O(N) without using division operator and in O(1) auxiliary space.",
        "Compute prefix products in output array. In second pass backwards, multiply by running suffix product.",
        "Pass 1: res[i] = product of all elements to the left. Pass 2: maintain running rightProd from right to left, multiplying res[i] *= rightProd.",
        "Time: O(N), Space: O(1) auxiliary",
        """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        for (int i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
        int right = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= right;
            right *= nums[i];
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        59, 20, "Longest Repeating Character Replacement", "longest-repeating-character-replacement",
        "Strings", "Sliding Window", "Medium", "Frequency-bounded Sliding Window",
        "Sliding window interview pattern with condition: window_size - max_frequency <= k.",
        "Longest substring of same letter after at most k character replacements.",
        "In window [left, right], condition is valid if (windowLen - maxFreq) <= k. If invalid, increment left.",
        "Expand right, update count[s[right]] and maxFreq = max(maxFreq, count[s[right]]). If (right - left + 1 - maxFreq) > k, decrement count[s[left++]], else update maxLen.",
        "Time: O(N), Space: O(26) = O(1)",
        """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> count(26, 0);
        int maxCount = 0, left = 0, maxLen = 0;
        for (int right = 0; right < (int)s.size(); right++) {
            count[s[right] - 'A']++;
            maxCount = max(maxCount, count[s[right] - 'A']);
            while (right - left + 1 - maxCount > k) {
                count[s[left] - 'A']--;
                left++;
            }
            maxLen = max(maxLen, right - left + 1);
        }
        return maxLen;
    }
};"""
    ))

    p2.append(make_q(
        60, 20, "Decode Ways", "decode-ways",
        "Dynamic Programming", "String DP", "Medium", "Fibonacci-style Parsing DP",
        "Tests handling edge cases, zero encodings, and two-character window transitions.",
        "Total ways to decode numeric string where 'A' -> 1 .. 'Z' -> 26.",
        "At index i: if s[i-1] != '0', add dp[i-1]. If s[i-2..i-1] is between '10' and '26', add dp[i-2].",
        "Use dp[i] where dp[0] = 1. For i from 1 to n: check single digit s[i-1] != '0'; check double digit 10 <= num <= 26.",
        "Time: O(N), Space: O(1)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int numDecodings(string s) {
        if (s.empty() || s[0] == '0') return 0;
        int n = s.size();
        int prev2 = 1, prev1 = 1;
        for (int i = 1; i < n; i++) {
            int curr = 0;
            if (s[i] != '0') curr += prev1;
            int twoDigit = stoi(s.substr(i - 1, 2));
            if (twoDigit >= 10 && twoDigit <= 26) curr += prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }
};"""
    ))

    # Day 21: Graphs + Trees + Dynamic Programming
    p2.append(make_q(
        61, 21, "Surrounded Regions", "surrounded-regions",
        "Graphs", "Boundary Flood Fill", "Medium", "Boundary Connected Component Inversion",
        "Demonstrates boundary-connected logic: any 'O' connected to boundary cannot be captured.",
        "Capture surrounded regions: flip all 'O's surrounded by 'X' into 'X'.",
        "Flood fill from border 'O's and mark them as safe ('#'). Any remaining 'O' is surrounded and flipped to 'X'.",
        "Run DFS from all border cells with 'O' marking them as '#'. Then iterate entire board: change remaining 'O' to 'X', and '#' back to 'O'.",
        "Time: O(R * C), Space: O(R * C)",
        """#include <vector>
using namespace std;

class Solution {
    int m, n;
    void dfs(vector<vector<char>>& board, int r, int c) {
        if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] != 'O') return;
        board[r][c] = '#';
        dfs(board, r + 1, c);
        dfs(board, r - 1, c);
        dfs(board, r, c + 1);
        dfs(board, r, c - 1);
    }
public:
    void solve(vector<vector<char>>& board) {
        m = board.size(); n = board[0].size();
        for (int i = 0; i < m; i++) {
            if (board[i][0] == 'O') dfs(board, i, 0);
            if (board[i][n - 1] == 'O') dfs(board, i, n - 1);
        }
        for (int j = 0; j < n; j++) {
            if (board[0][j] == 'O') dfs(board, 0, j);
            if (board[m - 1][j] == 'O') dfs(board, m - 1, j);
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == 'O') board[i][j] = 'X';
                else if (board[i][j] == '#') board[i][j] = 'O';
            }
        }
    }
};"""
    ))

    p2.append(make_q(
        62, 21, "Kth Smallest Element in a BST", "kth-smallest-element-in-a-bst",
        "Trees", "Inorder BST Traversal", "Medium", "Iterative Inorder Search",
        "Tests property that inorder traversal of a BST yields values in strictly sorted order.",
        "Find kth smallest value in a Binary Search Tree.",
        "Inorder traversal visits BST elements in ascending order. Stop and return when counter reaches k.",
        "Iterative inorder using stack: push left nodes until null, pop node, decrement k. When k == 0, return node->val. Move to node->right.",
        "Time: O(H + K), Space: O(H)",
        """#include <stack>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st;
        TreeNode* curr = root;
        while (curr || !st.empty()) {
            while (curr) {
                st.push(curr);
                curr = curr->left;
            }
            curr = st.top(); st.pop();
            if (--k == 0) return curr->val;
            curr = curr->right;
        }
        return -1;
    }
};"""
    ))

    p2.append(make_q(
        63, 21, "Coin Change II", "coin-change-ii",
        "Dynamic Programming", "Unbounded Knapsack Combinations", "Medium", "Order-Independent Combinations DP",
        "Highlights key distinction between combinations (outer loop coins) vs permutations (outer loop amount).",
        "Number of combinations to make up amount with infinite supply of coins.",
        "Outer loop must iterate over coins to avoid counting permutations like {1, 2} and {2, 1} separately.",
        "Initialize dp array of size amount + 1 with 0, dp[0] = 1. For each coin: for j from coin to amount: dp[j] += dp[j - coin]. Return dp[amount].",
        "Time: O(Coins * Amount), Space: O(Amount)",
        """#include <vector>
using namespace std;

class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<unsigned long long> dp(amount + 1, 0);
        dp[0] = 1;
        for (int c : coins) {
            for (int j = c; j <= amount; j++) {
                dp[j] += dp[j - c];
            }
        }
        return dp[amount];
    }
};"""
    ))

    # Day 22: Binary Search + Stack + Greedy
    p2.append(make_q(
        64, 22, "Capacity To Ship Packages Within D Days", "capacity-to-ship-packages-within-d-days",
        "Binary Search", "Binary Search on Answer", "Medium", "Capacity Predicate Binary Search",
        "Classic binary search on answer testing capacity feasibility simulation.",
        "Least weight capacity of ship to deliver packages within days.",
        "Capacity ranges between max(weights) and sum(weights). Is the days-required function monotonic?",
        "Binary search low = max_element, high = accumulate. For mid: simulate days needed. If days <= D, high = mid - 1; else low = mid + 1.",
        "Time: O(N * log(Sum - Max)), Space: O(1)",
        """#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
    bool canShip(const vector<int>& weights, int days, int cap) {
        int d = 1, current = 0;
        for (int w : weights) {
            if (current + w > cap) {
                d++;
                current = 0;
            }
            current += w;
        }
        return d <= days;
    }
public:
    int shipWithinDays(vector<int>& weights, int days) {
        int low = *max_element(weights.begin(), weights.end());
        int high = accumulate(weights.begin(), weights.end(), 0);
        int ans = high;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canShip(weights, days, mid)) {
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

    p2.append(make_q(
        65, 22, "Asteroid Collision", "asteroid-collision",
        "Stack", "Collision Simulation", "Medium", "Directional Stack Collision Resolution",
        "Tests collision simulation where only positive (right-moving) followed by negative (left-moving) collide.",
        "State of asteroids after all collisions: positive moves right, negative moves left, larger destroys smaller.",
        "Collision happens only when stack top > 0 and incoming asteroid < 0.",
        "Traverse asteroids: while stack top > 0 and ast < 0: if abs(ast) > stack top, pop and continue. If equal, pop and destroy both. If smaller, destroy incoming. If survived, push.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <cmath>
using namespace std;

class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> st;
        for (int ast : asteroids) {
            bool alive = true;
            while (alive && ast < 0 && !st.empty() && st.back() > 0) {
                if (st.back() < -ast) {
                    st.pop_back();
                } else if (st.back() == -ast) {
                    st.pop_back();
                    alive = false;
                } else {
                    alive = false;
                }
            }
            if (alive) st.push_back(ast);
        }
        return st;
    }
};"""
    ))

    p2.append(make_q(
        66, 22, "Jump Game II", "jump-game-ii",
        "Greedy", "BFS Level Interval", "Medium", "Greedy Range Boundary Jump",
        "Greedy optimization modeling jumps as BFS levels in O(N) time and O(1) space.",
        "Minimum number of jumps to reach last index.",
        "Track current jump's reach limit and farthest reachable index from any point in current jump range.",
        "Maintain curEnd = 0, curFarthest = 0, jumps = 0. Iterate i from 0 to n - 2: update curFarthest = max(curFarthest, i + nums[i]). When i == curEnd, jumps++, curEnd = curFarthest.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int jump(vector<int>& nums) {
        int jumps = 0, curEnd = 0, curFarthest = 0;
        for (int i = 0; i < (int)nums.size() - 1; i++) {
            curFarthest = max(curFarthest, i + nums[i]);
            if (i == curEnd) {
                jumps++;
                curEnd = curFarthest;
            }
        }
        return jumps;
    }
};"""
    ))

    # Day 23: Linked Lists + Tries + Dynamic Programming
    p2.append(make_q(
        67, 23, "Remove Nth Node From End of List", "remove-nth-node-from-end-of-list",
        "Linked Lists", "Two Pointers Gap", "Medium", "Constant Gap Fast/Slow Pointers",
        "Classic one-pass interview question maintaining an n-node lead with fast pointer.",
        "Remove nth node from end of linked list in one pass.",
        "Advance fast pointer by n nodes ahead of slow. When fast reaches the end, slow is just before the target node.",
        "Use dummy head. Move fast pointer n + 1 steps forward. Then move both fast and slow until fast is null. Remove slow->next = slow->next->next.",
        "Time: O(N), Space: O(1)",
        """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode *fast = &dummy, *slow = &dummy;
        for (int i = 0; i <= n; i++) fast = fast->next;
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        slow->next = slow->next->next;
        return dummy.next;
    }
};"""
    ))

    p2.append(make_q(
        68, 23, "Design Add and Search Words Data Structure", "design-add-and-search-words-data-structure",
        "Tries", "Trie Wildcard Search", "Medium", "Trie DFS with '.' Wildcard",
        "Extends prefix tree with backtracking search across all 26 branches for '.' wildcards.",
        "Design data structure that supports adding words and searching words with '.' matching any letter.",
        "When encountering '.', recursively try all non-null child nodes.",
        "Build Trie. In searchHelper(word, idx, node): if idx == word.size() return node->isEnd. If word[idx] == '.', branch to all valid children. Else follow specific child.",
        "Time: Add O(L), Search O(26^L) worst-case wildcard, Space: O(Total chars * 26)",
        """#include <string>
using namespace std;

class WordDictionary {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root;
    bool searchInNode(const string& word, int idx, Node* node) {
        if (!node) return false;
        if (idx == (int)word.size()) return node->isEnd;
        char c = word[idx];
        if (c == '.') {
            for (int i = 0; i < 26; i++) {
                if (node->children[i] && searchInNode(word, idx + 1, node->children[i]))
                    return true;
            }
            return false;
        } else {
            return searchInNode(word, idx + 1, node->children[c - 'a']);
        }
    }
public:
    WordDictionary() { root = new Node(); }
    void addWord(string word) {
        Node* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) curr->children[idx] = new Node();
            curr = curr->children[idx];
        }
        curr->isEnd = true;
    }
    bool search(string word) {
        return searchInNode(word, 0, root);
    }
};"""
    ))

    p2.append(make_q(
        69, 23, "Maximum Length of Repeated Subarray", "maximum-length-of-repeated-subarray",
        "Dynamic Programming", "2D Longest Common Substring", "Medium", "Common Substring Grid DP",
        "Tests contiguous subarray matching (longest common substring) vs subsequences.",
        "Maximum length of contiguous subarray appearing in both nums1 and nums2.",
        "If nums1[i] == nums2[j], dp[i][j] = dp[i-1][j-1] + 1; otherwise reset to 0.",
        "2D DP table where dp[i][j] represents length of common subarray ending at nums1[i-1] and nums2[j-1]. Track max value seen.",
        "Time: O(M * N), Space: O(M * N) or O(N) optimized",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int findLength(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size(), n = nums2.size(), maxLen = 0;
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (nums1[i - 1] == nums2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                    maxLen = max(maxLen, dp[i][j]);
                }
            }
        }
        return maxLen;
    }
};"""
    ))

    # Day 24: Graphs / DSU + Trees + Sliding Window
    p2.append(make_q(
        70, 24, "Redundant Connection", "redundant-connection",
        "Graphs", "Union Find / DSU", "Medium", "Disjoint Set Cycle Detection",
        "Core interview question testing Disjoint Set Union (DSU) with path compression and rank.",
        "Find edge that creates cycle in undirected graph.",
        "Process edges one by one. If both endpoints already share the same root in DSU, this edge creates the cycle!",
        "Implement DSU with find(parent with path compression) and unite. For each edge (u, v): if find(u) == find(v) return edge; else unite(u, v).",
        "Time: O(N * alpha(N)) ~ O(N), Space: O(N)",
        """#include <vector>
#include <numeric>
using namespace std;

class Solution {
    vector<int> parent;
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }
    bool unite(int u, int v) {
        int rootU = find(u), rootV = find(v);
        if (rootU == rootV) return false;
        parent[rootU] = rootV;
        return true;
    }
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        parent.resize(n + 1);
        iota(parent.begin(), parent.end(), 0);
        for (auto& e : edges) {
            if (!unite(e[0], e[1])) return e;
        }
        return {};
    }
};"""
    ))

    p2.append(make_q(
        71, 24, "Flatten Binary Tree to Linked List", "flatten-binary-tree-to-linked-list",
        "Trees", "In-place Pointer Rewiring", "Medium", "Morris-like In-order Predecessor Splicing",
        "Tests in-place binary tree restructuring without allocating new nodes.",
        "Flatten binary tree into right-skewed linked list in-place matching preorder traversal.",
        "For any node with a left child, find rightmost node of left subtree. Connect that rightmost node to current's right child, then move left child to right.",
        "Iterate curr through tree. If curr has left child, find predecessor (rightmost node of left subtree). Connect predecessor->right = curr->right, then curr->right = curr->left, curr->left = null. Move curr = curr->right.",
        "Time: O(N), Space: O(1)",
        """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    void flatten(TreeNode* root) {
        TreeNode* curr = root;
        while (curr) {
            if (curr->left) {
                TreeNode* pred = curr->left;
                while (pred->right) pred = pred->right;
                pred->right = curr->right;
                curr->right = curr->left;
                curr->left = nullptr;
            }
            curr = curr->right;
        }
    }
};"""
    ))

    p2.append(make_q(
        72, 24, "Subarray Product Less Than K", "subarray-product-less-than-k",
        "Sliding Window", "Subarray Counting", "Medium", "Shrinking Window Subarray Counting",
        "Teaches counting valid subarrays ending at right pointer: right - left + 1.",
        "Count contiguous subarrays where product of all elements is strictly less than k.",
        "Every time window [left, right] is valid, how many new subarrays end at right?",
        "If k <= 1 return 0. Expand right, multiply prod *= nums[right]. While prod >= k, divide prod /= nums[left++]. Add (right - left + 1) to count.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        if (k <= 1) return 0;
        int count = 0, left = 0;
        long long prod = 1;
        for (int right = 0; right < (int)nums.size(); right++) {
            prod *= nums[right];
            while (prod >= k) {
                prod /= nums[left++];
            }
            count += right - left + 1;
        }
        return count;
    }
};"""
    ))

    # Day 25: Arrays + Matrix + Dynamic Programming
    p2.append(make_q(
        73, 25, "Trapping Rain Water", "trapping-rain-water",
        "Arrays", "Two Pointers / Prefix Max", "Hard", "Two Pointers Inward Max Bounding",
        "Top-tier classic interview problem testing two-pointer boundary derivation.",
        "Amount of trapped rainwater after raining.",
        "Water trapped on bar i is determined by min(maxLeft, maxRight) - height[i]. Move pointer with smaller maximum inward.",
        "left = 0, right = n - 1. Track leftMax, rightMax. If height[left] < height[right]: if height[left] >= leftMax update leftMax; else ans += leftMax - height[left]; left++. Else mirror for right.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int trap(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int leftMax = 0, rightMax = 0, trapped = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else trapped += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else trapped += rightMax - height[right];
                right--;
            }
        }
        return trapped;
    }
};"""
    ))

    p2.append(make_q(
        74, 25, "Spiral Matrix", "spiral-matrix",
        "Arrays", "Matrix Traversal Simulation", "Medium", "Four-Boundary Shrinking Loop",
        "Tests boundary conditions and index management during 2D matrix traversal.",
        "Return all elements of matrix in spiral order.",
        "Maintain 4 boundaries: top, bottom, left, right. Traverse right across top, down right column, left across bottom, up left column, shrinking boundaries after each edge.",
        "Loop while top <= bottom and left <= right. Check boundary validity before horizontal and vertical reverse traverses.",
        "Time: O(M * N), Space: O(1) auxiliary",
        """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> res;
        int top = 0, bottom = matrix.size() - 1;
        int left = 0, right = matrix[0].size() - 1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) res.push_back(matrix[top][j]);
            top++;
            for (int i = top; i <= bottom; i++) res.push_back(matrix[i][right]);
            right--;
            if (top <= bottom) {
                for (int j = right; j >= left; j--) res.push_back(matrix[bottom][j]);
                bottom--;
            }
            if (left <= right) {
                for (int i = bottom; i >= top; i--) res.push_back(matrix[i][left]);
                left++;
            }
        }
        return res;
    }
};"""
    ))

    p2.append(make_q(
        75, 25, "Min Cost Climbing Stairs", "min-cost-climbing-stairs",
        "Dynamic Programming", "1D DP", "Easy", "Fibonacci Cost DP",
        "Reinforces fundamental 1D dynamic programming transition with step constraints.",
        "Minimum cost to reach top of floor stepping 1 or 2 steps.",
        "At step i, min cost is cost[i] + min(cost from step i-1, cost from step i-2).",
        "Track two previous costs: prev1, prev2. Update curr = cost[i] + min(prev1, prev2). Result is min(prev1, prev2).",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int prev2 = cost[0], prev1 = cost[1];
        for (size_t i = 2; i < cost.size(); i++) {
            int curr = cost[i] + min(prev1, prev2);
            prev2 = prev1;
            prev1 = curr;
        }
        return min(prev1, prev2);
    }
};"""
    ))

    return p2
