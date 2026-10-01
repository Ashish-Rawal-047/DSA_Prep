def get_replacement_pool(make_q):
    pool = []

    # 1. Arrays / Two Pointers
    pool.append(make_q(
        201, 0, "Container With Most Water", "container-with-most-water",
        "Arrays", "Two Pointers", "Medium", "Two Pointers Max Area Bounding",
        "Essential two-pointer question proving why moving the shorter wall can never miss an optimal solution.",
        "Maximum water a container formed by two vertical lines can hold.",
        "Area is bounded by shorter wall. Moving the taller wall inwards can only decrease or keep width lower with same or lower height limit.",
        "left = 0, right = n - 1. While left < right: maxArea = max(maxArea, min(h[l], h[r]) * (r - l)). If h[l] < h[r] l++ else r--.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0, r = height.size() - 1, maxA = 0;
        while (l < r) {
            maxA = max(maxA, min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return maxA;
    }
};"""
    ))

    # 2. Arrays / Matrix
    pool.append(make_q(
        202, 0, "Rotate Image", "rotate-image",
        "Arrays", "Matrix Manipulation", "Medium", "Transpose + Reverse Reflection",
        "Classic in-place 2D matrix transformation without extra memory.",
        "Rotate n x n 2D matrix by 90 degrees clockwise in-place.",
        "A 90-degree clockwise rotation is equivalent to transposing the matrix across main diagonal, then reversing each row.",
        "1. Transpose: swap(matrix[i][j], matrix[j][i]) for j > i. 2. Reverse each row: reverse(matrix[i].begin(), matrix[i].end()).",
        "Time: O(N^2), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                swap(matrix[i][j], matrix[j][i]);
            }
        }
        for (int i = 0; i < n; i++) {
            reverse(matrix[i].begin(), matrix[i].end());
        }
    }
};"""
    ))

    # 3. Strings / Sliding Window
    pool.append(make_q(
        203, 0, "Permutation in String", "permutation-in-string",
        "Strings", "Sliding Window", "Medium", "Fixed-Window Frequency Array Matching",
        "Sister problem to Find All Anagrams in a String with early return.",
        "Check if s2 contains a permutation of s1 as a contiguous substring.",
        "Maintain fixed window of length s1.length() in s2. If frequency vectors match, return true immediately.",
        "Track char counts of s1 and current window in s2 of length s1.size(). Compare arrays in O(26) time.",
        "Time: O(N), Space: O(26) = O(1)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.size() > s2.size()) return false;
        vector<int> c1(26, 0), c2(26, 0);
        for (char c : s1) c1[c - 'a']++;
        int k = s1.size();
        for (int i = 0; i < (int)s2.size(); i++) {
            c2[s2[i] - 'a']++;
            if (i >= k) c2[s2[i - k] - 'a']--;
            if (c1 == c2) return true;
        }
        return false;
    }
};"""
    ))

    # 4. Graphs / BFS
    pool.append(make_q(
        204, 0, "Snakes and Ladders", "snakes-and-ladders",
        "Graphs", "BFS Shortest Path", "Medium", "Board BFS with Direct Jump Mapping",
        "Models board game as unweighted directed graph where BFS finds minimum die rolls.",
        "Least number of dice rolls to reach square n^2 on snakes and ladders board.",
        "Square numbers 1 to n^2 map to 2D coordinates. BFS queue stores (square, rolls).",
        "Helper to map 1D square to (r, c). BFS from square 1. For die roll 1..6: if next square has snake/ladder jump, take destination; else use square. Return rolls upon reaching n^2.",
        "Time: O(N^2), Space: O(N^2)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
    pair<int, int> getPos(int s, int n) {
        int r = (s - 1) / n;
        int c = (s - 1) % n;
        if (r % 2 == 1) c = n - 1 - c;
        return {n - 1 - r, c};
    }
public:
    int snakesAndLadders(vector<vector<int>>& board) {
        int n = board.size(), target = n * n;
        vector<int> dist(target + 1, -1);
        queue<int> q;
        q.push(1);
        dist[1] = 0;
        while (!q.empty()) {
            int curr = q.front(); q.pop();
            if (curr == target) return dist[curr];
            for (int roll = 1; roll <= 6 && curr + roll <= target; roll++) {
                int nextSq = curr + roll;
                auto [r, c] = getPos(nextSq, n);
                int dest = (board[r][c] != -1) ? board[r][c] : nextSq;
                if (dist[dest] == -1) {
                    dist[dest] = dist[curr] + 1;
                    q.push(dest);
                }
            }
        }
        return -1;
    }
};"""
    ))

    # 5. Graphs / Union Find
    pool.append(make_q(
        205, 0, "Number of Provinces", "number-of-provinces",
        "Graphs", "Union Find / Connected Components", "Medium", "Adjacency Matrix Connected Components",
        "Foundational connected components question solvable via DFS, BFS, or DSU.",
        "Total number of connected provinces in given adjacency matrix.",
        "Each unvisited city initiates a traversal discovering its full province.",
        "Track vector<bool> visited. Loop i = 0..n-1: if !visited[i], count++, run DFS/BFS to visit all reachable cities.",
        "Time: O(N^2), Space: O(N)",
        """#include <vector>
using namespace std;

class Solution {
    void dfs(const vector<vector<int>>& isConnected, int u, vector<bool>& visited) {
        visited[u] = true;
        for (int v = 0; v < (int)isConnected.size(); v++) {
            if (isConnected[u][v] && !visited[v]) dfs(isConnected, v, visited);
        }
    }
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size(), provinces = 0;
        vector<bool> visited(n, false);
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                provinces++;
                dfs(isConnected, i, visited);
            }
        }
        return provinces;
    }
};"""
    ))

    # 6. Trees / BFS
    pool.append(make_q(
        206, 0, "Populating Next Right Pointers in Each Node", "populating-next-right-pointers-in-each-node",
        "Trees", "Tree Level-Order Traversal", "Medium", "O(1) Space Pointer Stitching",
        "Connects sibling nodes at the same level using already established next pointers in O(1) space.",
        "Populate next right pointer for each node in perfect binary tree in O(1) extra space.",
        "For node curr: curr->left->next = curr->right. If curr->next exists, curr->right->next = curr->next->left.",
        "Level-by-level traversal using left-most pointer. For each node on current level, stitch children's next pointers.",
        "Time: O(N), Space: O(1)",
        """class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;
    Node(int _val) : val(_val), left(nullptr), right(nullptr), next(nullptr) {}
};

class Solution {
public:
    Node* connect(Node* root) {
        if (!root) return nullptr;
        Node* leftMost = root;
        while (leftMost->left) {
            Node* curr = leftMost;
            while (curr) {
                curr->left->next = curr->right;
                if (curr->next) curr->right->next = curr->next->left;
                curr = curr->next;
            }
            leftMost = leftMost->left;
        }
        return root;
    }
};"""
    ))

    # 7. Trees / Path
    pool.append(make_q(
        207, 0, "Path Sum II", "path-sum-ii",
        "Trees", "Backtracking on Trees", "Medium", "Root-to-Leaf Path Collection",
        "Standard tree backtracking tracking current path and remaining target.",
        "Find all root-to-leaf paths where sum of node values equals targetSum.",
        "Push node->val to path. If leaf and val == targetSum, add path to result. Recurse left and right, then pop node->val.",
        "DFS helper(node, target, path, res): add val, check leaf. Recurse children with target - val, pop.",
        "Time: O(N^2) worst case paths, Space: O(H)",
        """#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    void dfs(TreeNode* node, int target, vector<int>& path, vector<vector<int>>& res) {
        if (!node) return;
        path.push_back(node->val);
        if (!node->left && !node->right && target == node->val) {
            res.push_back(path);
        }
        dfs(node->left, target - node->val, path, res);
        dfs(node->right, target - node->val, path, res);
        path.pop_back();
    }
public:
    vector<vector<int>> pathSum(TreeNode* root, int targetSum) {
        vector<vector<int>> res;
        vector<int> path;
        dfs(root, targetSum, path, res);
        return res;
    }
};"""
    ))

    # 8. Dynamic Programming / Grid
    pool.append(make_q(
        208, 0, "Dungeon Game", "dungeon-game",
        "Dynamic Programming", "Reverse Grid DP", "Hard", "Bottom-Up Backward Health Induction",
        "Must be solved backwards: from destination to start, because health needed depends on future requirements.",
        "Minimum initial health of knight to rescue princess in dungeon grid.",
        "dp[i][j] is minimum health needed entering cell (i, j). dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]).",
        "Initialize dp table with INF. dp[m][n-1] = dp[m-1][n] = 1. Fill table backwards from (m-1, n-1) to (0, 0).",
        "Time: O(M * N), Space: O(M * N) or O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int calculateMinimumHP(vector<vector<int>>& dungeon) {
        int m = dungeon.size(), n = dungeon[0].size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 1e9));
        dp[m][n - 1] = dp[m - 1][n] = 1;
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                int need = min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j];
                dp[i][j] = max(1, need);
            }
        }
        return dp[0][0];
    }
};"""
    ))

    # 9. Dynamic Programming / Subsequence
    pool.append(make_q(
        209, 0, "Longest Palindromic Substring", "longest-palindromic-substring",
        "Dynamic Programming", "Expand Around Center", "Medium", "Center Expansion Substring Search",
        "High-frequency string question solvable in O(N^2) time and O(1) space via center expansion.",
        "Longest palindromic substring in s.",
        "Expand outward from each index for odd and even centers, updating max length and start index.",
        "For i = 0..n-1: expand(i, i) and expand(i, i+1). If len > maxLen, update start = i - (len - 1)/2.",
        "Time: O(N^2), Space: O(1)",
        """#include <string>
using namespace std;

class Solution {
    int expand(const string& s, int l, int r) {
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) {
            l--; r++;
        }
        return r - l - 1;
    }
public:
    string longestPalindrome(string s) {
        int start = 0, maxLen = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            int len1 = expand(s, i, i);
            int len2 = expand(s, i, i + 1);
            int len = max(len1, len2);
            if (len > maxLen) {
                maxLen = len;
                start = i - (len - 1) / 2;
            }
        }
        return s.substr(start, maxLen);
    }
};"""
    ))

    # 10. Binary Search
    pool.append(make_q(
        210, 0, "Find First and Last Position of Element in Sorted Array", "find-first-and-last-position-of-element-in-sorted-array",
        "Binary Search", "Boundary Binary Search", "Medium", "Lower Bound and Upper Bound Search",
        "Tests finding the exact starting and ending boundaries of duplicated targets in sorted arrays.",
        "Starting and ending position of target value in sorted array in O(log N).",
        "Run two binary searches: one seeking first occurrence (high = mid - 1 on match), one seeking last occurrence (low = mid + 1 on match).",
        "Helper binarySearch(isFirst): on nums[mid] == target, save ans and adjust pointer towards target side.",
        "Time: O(log N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
    int findBound(const vector<int>& nums, int target, bool isFirst) {
        int low = 0, high = nums.size() - 1, ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) {
                ans = mid;
                if (isFirst) high = mid - 1;
                else low = mid + 1;
            } else if (nums[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return ans;
    }
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        return {findBound(nums, target, true), findBound(nums, target, false)};
    }
};"""
    ))

    # 11. Linked Lists
    pool.append(make_q(
        211, 0, "Swap Nodes in Pairs", "swap-nodes-in-pairs",
        "Linked Lists", "Pairwise Reversal", "Medium", "Dummy Head Pointer Rewiring",
        "Standard pointer rewiring problem testing dummy node manipulation.",
        "Swap every two adjacent nodes in linked list and return head.",
        "Use dummy head. For pair (first, second): prev->next = second; first->next = second->next; second->next = first; prev = first.",
        "Loop while curr->next && curr->next->next: reassign pointers of the two adjacent nodes and advance.",
        "Time: O(N), Space: O(1)",
        """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* prev = &dummy;
        while (prev->next && prev->next->next) {
            ListNode* first = prev->next;
            ListNode* second = prev->next->next;
            first->next = second->next;
            second->next = first;
            prev->next = second;
            prev = first;
        }
        return dummy.next;
    }
};"""
    ))

    # 12. Heap
    pool.append(make_q(
        212, 0, "K Closest Points to Origin", "k-closest-points-to-origin",
        "Heap", "Max-Heap / Geometry", "Medium", "Max-Heap of Bounded Size K",
        "Tests keeping track of k smallest distances using max-heap of size k.",
        "Find the k closest points to the origin (0, 0) on the X-Y plane.",
        "Max-heap of size k storing (dist, point). If heap size > k, pop the farthest point.",
        "Iterate points: calculate dist = x*x + y*y. Push to max-heap. If size > k, pop top. Remaining k elements are closest.",
        "Time: O(N log K), Space: O(K)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        priority_queue<pair<long long, vector<int>>> maxHeap;
        for (auto& p : points) {
            long long d = (long long)p[0]*p[0] + (long long)p[1]*p[1];
            maxHeap.push({d, p});
            if (maxHeap.size() > (size_t)k) maxHeap.pop();
        }
        vector<vector<int>> res;
        while (!maxHeap.empty()) {
            res.push_back(maxHeap.top().second);
            maxHeap.pop();
        }
        return res;
    }
};"""
    ))

    # 13. Stack
    pool.append(make_q(
        213, 0, "Decode String", "decode-string",
        "Stack", "String Parsing Stack", "Medium", "Nested Multiplier and String Stack",
        "Tests nested string decoding using stacks for counts and strings.",
        "Decode encoded string like '3[a2[c]]' -> 'accaccacc'.",
        "When encountering '[', push current count and current string to stacks. When ']', pop and repeat.",
        "Track currNum and currStr. '[': push currNum and currStr, reset both. ']': pop count and prevStr, currStr = prevStr + repeat(currStr, count).",
        "Time: O(Output length), Space: O(Output length)",
        """#include <string>
#include <stack>
using namespace std;

class Solution {
public:
    string decodeString(string s) {
        stack<int> numSt;
        stack<string> strSt;
        string currStr = "";
        int currNum = 0;
        for (char c : s) {
            if (isdigit(c)) {
                currNum = currNum * 10 + (c - '0');
            } else if (c == '[') {
                numSt.push(currNum);
                strSt.push(currStr);
                currNum = 0;
                currStr = "";
            } else if (c == ']') {
                int repeat = numSt.top(); numSt.pop();
                string prev = strSt.top(); strSt.pop();
                string expanded = "";
                while (repeat--) expanded += currStr;
                currStr = prev + expanded;
            } else {
                currStr += c;
            }
        }
        return currStr;
    }
};"""
    ))

    # 14. Greedy
    pool.append(make_q(
        214, 0, "Jump Game", "jump-game",
        "Greedy", "Reachable Index Tracking", "Medium", "Farthest Reachable Index",
        "Foundational greedy problem tracking maximum reachability.",
        "Determine if you are able to reach the last index from index 0.",
        "Maintain maxReach. If current index i > maxReach, you are stuck and can never proceed.",
        "Loop i from 0 to n-1: if i > maxReach return false; maxReach = max(maxReach, i + nums[i]); if maxReach >= n - 1 return true.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int maxReach = 0, n = nums.size();
        for (int i = 0; i < n; i++) {
            if (i > maxReach) return false;
            maxReach = max(maxReach, i + nums[i]);
            if (maxReach >= n - 1) return true;
        }
        return true;
    }
};"""
    ))

    # 15. Backtracking
    pool.append(make_q(
        215, 0, "Generate Parentheses", "generate-parentheses",
        "Backtracking", "Balanced String Backtracking", "Medium", "Open and Close Count Constraints",
        "Top-frequency interview question generating all valid combinations of n pairs of parentheses.",
        "Generate all combinations of well-formed parentheses for n pairs.",
        "Add '(' if open < n. Add ')' only if close < open.",
        "Backtrack(open, close, curr): if open == n && close == n save curr. If open < n: recurse with open + 1. If close < open: recurse with close + 1.",
        "Time: O(4^n / sqrt(n)), Space: O(n)",
        """#include <vector>
#include <string>
using namespace std;

class Solution {
    void backtrack(int open, int close, int n, string& curr, vector<string>& res) {
        if (open == n && close == n) {
            res.push_back(curr);
            return;
        }
        if (open < n) {
            curr.push_back('(');
            backtrack(open + 1, close, n, curr, res);
            curr.pop_back();
        }
        if (close < open) {
            curr.push_back(')');
            backtrack(open, close + 1, n, curr, res);
            curr.pop_back();
        }
    }
public:
    vector<string> generateParenthesis(int n) {
        vector<string> res;
        string curr = "";
        backtrack(0, 0, n, curr, res);
        return res;
    }
};"""
    ))

    # 16. Bit Manipulation
    pool.append(make_q(
        216, 0, "Subsets", "subsets",
        "Bit Manipulation", "Power Set Generation", "Medium", "Bitmask Power Set Enumeration",
        "Demonstrates generating all 2^N subsets using binary bitmasks 0 to 2^N - 1.",
        "All possible subsets (the power set) of an array of unique integers.",
        "Each subset corresponds to a bitmask of length n where bit i set means include nums[i].",
        "Loop mask from 0 to (1 << n) - 1. For each bit i: if (mask >> i) & 1, include nums[i]. Add subset to result.",
        "Time: O(N * 2^N), Space: O(1) auxiliary",
        """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        int n = nums.size();
        int total = 1 << n;
        vector<vector<int>> res;
        for (int mask = 0; mask < total; mask++) {
            vector<int> sub;
            for (int i = 0; i < n; i++) {
                if ((mask >> i) & 1) sub.push_back(nums[i]);
            }
            res.push_back(sub);
        }
        return res;
    }
};"""
    ))

    # 17. Trees
    pool.append(make_q(
        217, 0, "Binary Tree Level Order Traversal", "binary-tree-level-order-traversal",
        "Trees", "BFS Level-Order", "Medium", "Queue-Based Level Order Processing",
        "The canonical level order traversal problem returning nodes level by level.",
        "Level order traversal of binary tree nodes' values.",
        "Standard BFS using queue size to process each level as a discrete batch.",
        "Push root. While queue is non-empty, loop for queue.size() times, pop node, append value to level list, push children.",
        "Time: O(N), Space: O(W)",
        """#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        if (!root) return {};
        vector<vector<int>> res;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            vector<int> level;
            for (int i = 0; i < sz; i++) {
                TreeNode* node = q.front(); q.pop();
                level.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            res.push_back(level);
        }
        return res;
    }
};"""
    ))

    # 18. Graphs
    pool.append(make_q(
        218, 0, "Is Graph Bipartite?", "is-graph-bipartite",
        "Graphs", "2-Coloring BFS/DFS", "Medium", "Bipartite Graph 2-Coloring",
        "Core interview question testing graph 2-colorability to verify bipartite property.",
        "Determine if undirected graph is bipartite (nodes can be partitioned into two independent sets).",
        "Color graph with 1 and -1. If an adjacent neighbor has the same color, graph is not bipartite.",
        "Track color array (0=unvisited). For each unvisited component, start BFS/DFS with color 1. Alternate color for neighbors; if neighbor has same color, return false.",
        "Time: O(V + E), Space: O(V)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, 0);
        for (int i = 0; i < n; i++) {
            if (color[i] != 0) continue;
            queue<int> q;
            q.push(i);
            color[i] = 1;
            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (int v : graph[u]) {
                    if (color[v] == color[u]) return false;
                    if (color[v] == 0) {
                        color[v] = -color[u];
                        q.push(v);
                    }
                }
            }
        }
        return true;
    }
};"""
    ))

    # 19. Dynamic Programming
    pool.append(make_q(
        219, 0, "House Robber", "house-robber",
        "Dynamic Programming", "1D DP", "Medium", "Non-Adjacent Maximum Sum DP",
        "The quintessential non-adjacent selection dynamic programming pattern.",
        "Max money you can rob from houses along a street without robbing two adjacent houses.",
        "At each house: either skip it (keep prev1) or rob it (nums[i] + prev2).",
        "Maintain prev1 and prev2. curr = max(prev1, prev2 + nums[i]). prev2 = prev1, prev1 = curr.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int rob(vector<int>& nums) {
        int prev1 = 0, prev2 = 0;
        for (int x : nums) {
            int tmp = max(prev1, prev2 + x);
            prev2 = prev1;
            prev1 = tmp;
        }
        return prev1;
    }
};"""
    ))

    # 20. Dynamic Programming / Hard
    pool.append(make_q(
        220, 0, "Trapping Rain Water II", "trapping-rain-water-ii",
        "Dynamic Programming", "2D Min-Heap / Priority Queue", "Hard", "Boundary Min-Heap Water Infiltration",
        "2D generalization of Trapping Rain Water using min-heap priority queue on perimeter cells.",
        "Volume of water trapped in a 3D elevation map grid.",
        "Water spilled from boundary inwards. Push all boundary cells to min-heap. Pop lowest height bar and inspect neighbors.",
        "Priority queue of cell {height, r, c}. Initialize with all boundary cells. Pop lowest cell, update water level, push unvisited neighbors with max(neighbor_h, current_h).",
        "Time: O(M * N log(M * N)), Space: O(M * N)",
        """#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
    struct Cell {
        int h, r, c;
        bool operator>(const Cell& o) const { return h > o.h; }
    };
public:
    int trapRainWater(vector<vector<int>>& heightMap) {
        int m = heightMap.size(), n = heightMap[0].size();
        if (m <= 2 || n <= 2) return 0;
        priority_queue<Cell, vector<Cell>, greater<Cell>> pq;
        vector<vector<bool>> visited(m, vector<bool>(n, false));
        for (int i = 0; i < m; i++) {
            pq.push({heightMap[i][0], i, 0}); visited[i][0] = true;
            pq.push({heightMap[i][n - 1], i, n - 1}); visited[i][n - 1] = true;
        }
        for (int j = 1; j < n - 1; j++) {
            pq.push({heightMap[0][j], 0, j}); visited[0][j] = true;
            pq.push({heightMap[m - 1][j], m - 1, j}); visited[m - 1][j] = true;
        }
        int trapped = 0;
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        while (!pq.empty()) {
            auto curr = pq.top(); pq.pop();
            for (auto& d : dirs) {
                int nr = curr.r + d[0], nc = curr.c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {
                    visited[nr][nc] = true;
                    trapped += max(0, curr.h - heightMap[nr][nc]);
                    pq.push({max(curr.h, heightMap[nr][nc]), nr, nc});
                }
            }
        }
        return trapped;
    }
};"""
    ))

    # 21. Intervals
    pool.append(make_q(
        221, 0, "Merge Intervals", "merge-intervals",
        "Intervals", "Sorting Intervals", "Medium", "Start-Time Sorting with Continuous Merge",
        "Definitive interval problem testing sorting and contiguous overlapping range merging.",
        "Merge all overlapping intervals into non-overlapping intervals.",
        "Sort intervals by start time. If current interval overlaps with last merged interval, extend merged interval end.",
        "Sort intervals. Add first interval to result. For rest: if interval[0] <= res.back()[1], res.back()[1] = max(res.back()[1], interval[1]); else push interval.",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        if (intervals.empty()) return {};
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> res;
        res.push_back(intervals[0]);
        for (size_t i = 1; i < intervals.size(); i++) {
            if (intervals[i][0] <= res.back()[1]) {
                res.back()[1] = max(res.back()[1], intervals[i][1]);
            } else {
                res.push_back(intervals[i]);
            }
        }
        return res;
    }
};"""
    ))

    # 22. Binary Search
    pool.append(make_q(
        222, 0, "Search a 2D Matrix", "search-a-2d-matrix",
        "Binary Search", "Virtual 1D Binary Search", "Medium", "Matrix Flattened Binary Search",
        "Treating 2D matrix as flattened 1D array using division and modulo indexing.",
        "Search value in m x n matrix where each row is sorted and first integer of row > last of previous row in O(log(M * N)).",
        "Map 1D index mid to 2D coordinates: row = mid / cols, col = mid % cols.",
        "Binary search low = 0, high = m * n - 1. Compute val = matrix[mid / n][mid % n]. Compare with target.",
        "Time: O(log(M * N)), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int low = 0, high = m * n - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            if (val < target) low = mid + 1;
            else high = mid - 1;
        }
        return false;
    }
};"""
    ))

    # 23. Heap
    pool.append(make_q(
        223, 0, "Kth Largest Element in a Stream", "kth-largest-element-in-a-stream",
        "Heap", "Min-Heap Stream", "Easy", "Min-Heap Stream Window of Size K",
        "Design class that maintains the kth largest element of a stream dynamically.",
        "Maintain kth largest score in data stream.",
        "Min-heap of size k: top is always the kth largest element seen so far.",
        "Constructor pushes elements and trims heap size to k. add(val) pushes val, pops if size > k, returns minHeap.top().",
        "Time: O(log K) per add, Space: O(K)",
        """#include <vector>
#include <queue>
using namespace std;

class KthLargest {
    priority_queue<int, vector<int>, greater<int>> minHeap;
    int k;
public:
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int x : nums) {
            minHeap.push(x);
            if ((int)minHeap.size() > k) minHeap.pop();
        }
    }
    int add(int val) {
        minHeap.push(val);
        if ((int)minHeap.size() > k) minHeap.pop();
        return minHeap.top();
    }
};"""
    ))

    # 24. Backtracking
    pool.append(make_q(
        224, 0, "Sudoku Solver", "sudoku-solver",
        "Backtracking", "Grid Constraint Backtracking", "Hard", "Backtracking with Row, Col, Box Constraint Checks",
        "Classic constraint satisfaction problem using backtracking and early pruning.",
        "Solve a 9x9 Sudoku puzzle by filling empty cells with digits 1-9.",
        "Find next empty cell. Try digits '1'-'9': if digit does not violate row, column, or 3x3 box, place digit and recurse.",
        "Backtrack(board): find empty cell. If no empty cell, puzzle solved. Try digits '1'..'9': if isValid(r, c, d), place, if backtrack() return true, else unplace. Return false.",
        "Time: O(9^(M)), Space: O(81) = O(1)",
        """#include <vector>
using namespace std;

class Solution {
    bool isValid(const vector<vector<char>>& board, int r, int c, char ch) {
        for (int i = 0; i < 9; i++) {
            if (board[r][i] == ch) return false;
            if (board[i][c] == ch) return false;
            if (board[3 * (r / 3) + i / 3][3 * (c / 3) + i % 3] == ch) return false;
        }
        return true;
    }
    bool solve(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') {
                    for (char c = '1'; c <= '9'; c++) {
                        if (isValid(board, i, j, c)) {
                            board[i][j] = c;
                            if (solve(board)) return true;
                            board[i][j] = '.';
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }
public:
    void solveSudoku(vector<vector<char>>& board) {
        solve(board);
    }
};"""
    ))

    # 25. Linked Lists
    pool.append(make_q(
        225, 0, "Linked List Cycle II", "linked-list-cycle-ii",
        "Linked Lists", "Fast & Slow Pointers", "Medium", "Floyd's Cycle Finding Proof",
        "Mathematical proof: when slow and fast meet, moving one pointer to head and advancing both by 1 meets at cycle entrance.",
        "Find node where cycle begins in linked list, or return null if no cycle.",
        "Phase 1: detect cycle with slow and fast pointers. Phase 2: reset slow to head, advance both by 1 step until they meet.",
        "slow = head, fast = head. While fast && fast->next: slow = slow->next, fast = fast->next->next. If slow == fast: move slow to head; while slow != fast: slow = slow->next, fast = fast->next; return slow.",
        "Time: O(N), Space: O(1)",
        """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode *slow = head, *fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                slow = head;
                while (slow != fast) {
                    slow = slow->next;
                    fast = fast->next;
                }
                return slow;
            }
        }
        return nullptr;
    }
};"""
    ))

    # 26. Bit Manipulation
    pool.append(make_q(
        226, 0, "Single Number", "single-number",
        "Bit Manipulation", "XOR Invariants", "Easy", "XOR Self-Inverse Property",
        "Foundational XOR property: x ^ x = 0 and x ^ 0 = x.",
        "Every element appears twice except for one, find it in O(N) time and O(1) space.",
        "XOR-ing all numbers cancels out paired elements, leaving the single unique number.",
        "int ans = 0; for (int x : nums) ans ^= x; return ans;",
        "Time: O(N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int ans = 0;
        for (int x : nums) ans ^= x;
        return ans;
    }
};"""
    ))

    return pool
