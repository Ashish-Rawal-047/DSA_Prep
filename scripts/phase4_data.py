def get_phase4_questions(make_q):
    p4 = []

    # Day 39: Greedy + Trees + Dynamic Programming
    p4.append(make_q(
        115, 39, "Course Schedule III", "course-schedule-iii",
        "Greedy", "Max-Heap Scheduling", "Hard", "Greedy Deadline Sorting with Max Duration Eviction",
        "Sophisticated greedy scheduling: swapping out the longest course when a deadline is breached.",
        "Maximum number of courses you can take given [duration, lastDay].",
        "Sort courses by deadline. Maintain a max-heap of taken durations. If total time exceeds deadline, evict the longest duration course seen so far.",
        "Sort by lastDay. Track totalTime. For each course: add duration to heap and totalTime. If totalTime > lastDay, subtract heap.top() from totalTime and pop. Return heap.size().",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    int scheduleCourse(vector<vector<int>>& courses) {
        sort(courses.begin(), courses.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });
        priority_queue<int> maxHeap;
        int time = 0;
        for (const auto& c : courses) {
            time += c[0];
            maxHeap.push(c[0]);
            if (time > c[1]) {
                time -= maxHeap.top();
                maxHeap.pop();
            }
        }
        return maxHeap.size();
    }
};"""
    ))

    p4.append(make_q(
        116, 39, "Serialize and Deserialize Binary Tree", "serialize-and-deserialize-binary-tree",
        "Trees", "Tree Serialization Design", "Hard", "Preorder Traversal Stream Encoding",
        "Classic system design coding problem testing serialization format, delimiters, and recursion.",
        "Design an algorithm to serialize and deserialize a binary tree.",
        "Preorder traversal with '#' for null and commas separating values gives unambiguous reconstruction.",
        "Serialize: DFS preorder appending val + ',' or '#,'. Deserialize: stringstream reads tokens; recursively construct root, left, and right.",
        "Time: O(N), Space: O(N)",
        """#include <string>
#include <sstream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Codec {
    void serializeDfs(TreeNode* root, ostringstream& out) {
        if (!root) {
            out << "# ";
            return;
        }
        out << root->val << " ";
        serializeDfs(root->left, out);
        serializeDfs(root->right, out);
    }
    TreeNode* deserializeDfs(istringstream& in) {
        string val;
        in >> val;
        if (val == "#") return nullptr;
        TreeNode* node = new TreeNode(stoi(val));
        node->left = deserializeDfs(in);
        node->right = deserializeDfs(in);
        return node;
    }
public:
    string serialize(TreeNode* root) {
        ostringstream out;
        serializeDfs(root, out);
        return out.str();
    }
    TreeNode* deserialize(string data) {
        istringstream in(data);
        return deserializeDfs(in);
    }
};"""
    ))

    p4.append(make_q(
        117, 39, "Regular Expression Matching", "regular-expression-matching",
        "Dynamic Programming", "2D String DP", "Hard", "Pattern Automaton with Kleene Star",
        "Premier string parsing DP challenge testing zero-or-more '*' transitions.",
        "Regular expression matching with '.' and '*'.",
        "If p[j-1] == '*', check zero occurrences (dp[i][j-2]) or one/more occurrences (dp[i-1][j] if char matches).",
        "Table dp[s.len + 1][p.len + 1]. dp[0][0] = true. Handle empty string against patterns like 'a*b*'. Transition based on '.' and '*'.",
        "Time: O(M * N), Space: O(M * N)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
        dp[0][0] = true;
        for (int j = 2; j <= n; j++) {
            if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];
        }
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (p[j - 1] == '*') {
                    dp[i][j] = dp[i][j - 2] || (dp[i - 1][j] && (p[j - 2] == '.' || p[j - 2] == s[i - 1]));
                } else {
                    dp[i][j] = dp[i - 1][j - 1] && (p[j - 1] == '.' || p[j - 1] == s[i - 1]);
                }
            }
        }
        return dp[m][n];
    }
};"""
    ))

    # Day 40: Graphs + Dynamic Programming + Backtracking
    p4.append(make_q(
        118, 40, "Sliding Puzzle", "sliding-puzzle",
        "Graphs", "State-Space BFS", "Hard", "BFS on Board State String Permutations",
        "Tests shortest path on state transitions by encoding board configuration as a string.",
        "Least number of moves to solve 2x3 sliding puzzle from initial board to [[1,2,3],[4,5,0]].",
        "Represent board as string of 6 chars. Target is '123450'. Precompute valid swap neighbors for each index of '0'.",
        "BFS with queue<string> and unordered_set<string> visited. At each step, find position of '0', generate neighbor states by swapping, return steps when target reached.",
        "Time: O(6!), Space: O(6!)",
        """#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
using namespace std;

class Solution {
public:
    int slidingPuzzle(vector<vector<int>>& board) {
        string start = "";
        for (auto& row : board) for (int x : row) start += to_string(x);
        string target = "123450";
        vector<vector<int>> dirs = {
            {1, 3}, {0, 2, 4}, {1, 5},
            {0, 4}, {1, 3, 5}, {2, 4}
        };
        queue<pair<string, int>> q;
        unordered_set<string> visited;
        q.push({start, 0});
        visited.insert(start);
        while (!q.empty()) {
            auto [curr, steps] = q.front(); q.pop();
            if (curr == target) return steps;
            int zeroIdx = curr.find('0');
            for (int nextIdx : dirs[zeroIdx]) {
                string nextStr = curr;
                swap(nextStr[zeroIdx], nextStr[nextIdx]);
                if (!visited.count(nextStr)) {
                    visited.insert(nextStr);
                    q.push({nextStr, steps + 1});
                }
            }
        }
        return -1;
    }
};"""
    ))

    p4.append(make_q(
        119, 40, "Distinct Subsequences", "distinct-subsequences",
        "Dynamic Programming", "2D Subsequence DP", "Hard", "Exact Match Subsequence Counting",
        "High-level counting DP problem testing state transition combinations on character matches.",
        "Number of distinct subsequences of s which equals t.",
        "If s[i-1] == t[j-1], dp[i][j] = dp[i-1][j-1] (use char) + dp[i-1][j] (skip char). Otherwise dp[i-1][j].",
        "1D space-optimized vector dp of size t.size() + 1, dp[0] = 1. Traverse s, update dp backwards when s[i] == t[j-1].",
        "Time: O(S * T), Space: O(T)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        vector<unsigned long long> dp(n + 1, 0);
        dp[0] = 1;
        for (int i = 1; i <= m; i++) {
            for (int j = n; j >= 1; j--) {
                if (s[i - 1] == t[j - 1]) {
                    dp[j] += dp[j - 1];
                }
            }
        }
        return dp[n];
    }
};"""
    ))

    p4.append(make_q(
        120, 40, "N-Queens", "n-queens",
        "Backtracking", "Bitmask / Constraint Pruning", "Hard", "Row-by-Row Diagonal Constraint Pruning",
        "The quintessential backtracking interview problem testing row, column, and diagonal constraint tracking.",
        "Place N non-attacking queens on an N x N chessboard.",
        "Place one queen per row. Track attacked columns, main diagonals (r - c), and anti-diagonals (r + c).",
        "Use boolean vectors for cols, diag1 (r - c + n), diag2 (r + c). Backtrack row by row: for col 0..n-1: if valid, place 'Q', mark vectors, recurse, unmark.",
        "Time: O(N!), Space: O(N)",
        """#include <vector>
#include <string>
using namespace std;

class Solution {
    vector<vector<string>> res;
    vector<bool> cols, diag1, diag2;
    void solve(int row, int n, vector<string>& board) {
        if (row == n) {
            res.push_back(board);
            return;
        }
        for (int col = 0; col < n; col++) {
            if (cols[col] || diag1[row - col + n] || diag2[row + col]) continue;
            board[row][col] = 'Q';
            cols[col] = diag1[row - col + n] = diag2[row + col] = true;
            solve(row + 1, n, board);
            cols[col] = diag1[row - col + n] = diag2[row + col] = false;
            board[row][col] = '.';
        }
    }
public:
    vector<vector<string>> solveNQueens(int n) {
        cols.assign(n, false);
        diag1.assign(2 * n, false);
        diag2.assign(2 * n, false);
        vector<string> board(n, string(n, '.'));
        solve(0, n, board);
        return res;
    }
};"""
    ))

    # Day 41: Graphs + Trees + Dynamic Programming
    p4.append(make_q(
        121, 41, "Critical Connections in a Network", "critical-connections-in-a-network",
        "Graphs", "Tarjan's Bridge Algorithm", "Hard", "DFS Discovery and Low-Link Bridges",
        "Tarjan's bridge-finding algorithm: identifying single points of failure in networks.",
        "Find all critical connections (bridges) whose removal disconnects the server network.",
        "Maintain discovery time and low-link value. An edge (u, v) is a bridge if low[v] > disc[u].",
        "DFS tracking discovery times and low values. For each neighbor: if unvisited, recurse; if low[v] > disc[u], add {u, v} to bridges. If visited and not parent, low[u] = min(low[u], disc[v]).",
        "Time: O(V + E), Space: O(V + E)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    int timer = 1;
    vector<vector<int>> bridges;
    void dfs(int u, int p, const vector<vector<int>>& adj, vector<int>& disc, vector<int>& low) {
        disc[u] = low[u] = timer++;
        for (int v : adj[u]) {
            if (v == p) continue;
            if (disc[v]) {
                low[u] = min(low[u], disc[v]);
            } else {
                dfs(v, u, adj, disc, low);
                low[u] = min(low[u], low[v]);
                if (low[v] > disc[u]) {
                    bridges.push_back({u, v});
                }
            }
        }
    }
public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        vector<vector<int>> adj(n);
        for (auto& c : connections) {
            adj[c[0]].push_back(c[1]);
            adj[c[1]].push_back(c[0]);
        }
        vector<int> disc(n, 0), low(n, 0);
        dfs(0, -1, adj, disc, low);
        return bridges;
    }
};"""
    ))

    p4.append(make_q(
        122, 41, "Vertical Order Traversal of a Binary Tree", "vertical-order-traversal-of-a-binary-tree",
        "Trees", "Coordinate Tree Traversal", "Hard", "2D Spatial Coordinates with Multiset Sorting",
        "Meta's top tree interview problem: sorting nodes by column, row, and value tie-breaking.",
        "Vertical order traversal of binary tree sorted by column, then row, then value.",
        "Assign (col, row) coordinates to each node. Group nodes in map<col, map<row, multiset<val>>>.",
        "DFS/BFS with coordinates (col, row). Store values in nested maps. Iterate outer map columns and inner map rows to assemble ordered column lists.",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <map>
#include <set>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    map<int, map<int, multiset<int>>> nodes;
    void dfs(TreeNode* node, int col, int row) {
        if (!node) return;
        nodes[col][row].insert(node->val);
        dfs(node->left, col - 1, row + 1);
        dfs(node->right, col + 1, row + 1);
    }
public:
    vector<vector<int>> verticalTraversal(TreeNode* root) {
        dfs(root, 0, 0);
        vector<vector<int>> res;
        for (auto& [col, rowMap] : nodes) {
            vector<int> colVals;
            for (auto& [row, valSet] : rowMap) {
                for (int v : valSet) colVals.push_back(v);
            }
            res.push_back(colVals);
        }
        return res;
    }
};"""
    ))

    p4.append(make_q(
        123, 41, "Wildcard Matching", "wildcard-matching",
        "Dynamic Programming", "Two Pointers / String DP", "Hard", "Greedy Star Backtracking in O(1) Memory",
        "Tests handling wildcard '*' matching any sequence of characters in linear time.",
        "String matching with '?' (any single character) and '*' (any character sequence).",
        "Use two pointers with star backtracking: record position of last '*' and match index in s to backtrack greedily.",
        "Track sIdx, pIdx, starIdx = -1, matchIdx = 0. If chars match or p is '?', advance both. If p is '*', record starIdx and matchIdx. If mismatch and star seen, advance matchIdx.",
        "Time: O(S * P) worst, O(S + P) average, Space: O(1)",
        """#include <string>
using namespace std;

class Solution {
public:
    bool isMatch(string s, string p) {
        int sIdx = 0, pIdx = 0, starIdx = -1, match = 0;
        int m = s.size(), n = p.size();
        while (sIdx < m) {
            if (pIdx < n && (p[pIdx] == '?' || p[pIdx] == s[sIdx])) {
                sIdx++; pIdx++;
            } else if (pIdx < n && p[pIdx] == '*') {
                starIdx = pIdx++;
                match = sIdx;
            } else if (starIdx != -1) {
                pIdx = starIdx + 1;
                sIdx = ++match;
            } else {
                return false;
            }
        }
        while (pIdx < n && p[pIdx] == '*') pIdx++;
        return pIdx == n;
    }
};"""
    ))

    # Day 42: Strings + Graphs + Stack / DP
    p4.append(make_q(
        124, 42, "Minimum Window Subsequence", "minimum-window-subsequence",
        "Strings", "Two Pointers with Reverse Scanning", "Hard", "Greedy Forward Scan + Reverse Optimization",
        "Tests finding shortest substring in s that contains t as a subsequence using forward-and-backward pointer scan.",
        "Smallest contiguous substring of S that contains T as a subsequence.",
        "Match T forward in S. Once matched, scan backward from that endpoint to find the tightest starting point.",
        "Loop through S. Forward scan: when tIdx reaches t.size(), scan backward from sIdx to find optimal start. Update minLen. Restart forward scan from start + 1.",
        "Time: O(S * T), Space: O(1)",
        """#include <string>
#include <climits>
using namespace std;

class Solution {
public:
    string minWindow(string s1, string s2) {
        int m = s1.size(), n = s2.size();
        int sIdx = 0, start = -1, minLen = INT_MAX;
        while (sIdx < m) {
            int tIdx = 0;
            while (sIdx < m) {
                if (s1[sIdx] == s2[tIdx]) tIdx++;
                if (tIdx == n) break;
                sIdx++;
            }
            if (sIdx == m) break;
            int right = sIdx;
            tIdx = n - 1;
            while (sIdx >= 0) {
                if (s1[sIdx] == s2[tIdx]) tIdx--;
                if (tIdx < 0) break;
                sIdx--;
            }
            int left = sIdx;
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            sIdx = left + 1;
        }
        return start == -1 ? "" : s1.substr(start, minLen);
    }
};"""
    ))

    p4.append(make_q(
        125, 42, "Swim in Rising Water", "swim-in-rising-water",
        "Graphs", "Dijkstra / Min-Heap", "Hard", "Minimax Path Dijkstra",
        "Models 2D grid path finding where edge cost is max(elevation, current_time) using Dijkstra.",
        "Least time until you can reach bottom-right square when water rises by 1 unit per second.",
        "Use Dijkstra with min-heap storing {maxElevationOnPath, r, c}. First time reaching destination gives answer.",
        "Priority queue of tuple (time, r, c). Initialize visited matrix. Extract min, explore 4 neighbors: nextTime = max(currentTime, grid[nr][nc]). Return time when reaching (n-1, n-1).",
        "Time: O(N^2 log N), Space: O(N^2)",
        """#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        vector<vector<bool>> visited(n, vector<bool>(n, false));
        pq.push({grid[0][0], 0, 0});
        visited[0][0] = true;
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        while (!pq.empty()) {
            auto curr = pq.top(); pq.pop();
            int t = curr[0], r = curr[1], c = curr[2];
            if (r == n - 1 && c == n - 1) return t;
            for (auto& d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc]) {
                    visited[nr][nc] = true;
                    pq.push({max(t, grid[nr][nc]), nr, nc});
                }
            }
        }
        return 0;
    }
};"""
    ))

    p4.append(make_q(
        126, 42, "Longest Valid Parentheses", "longest-valid-parentheses",
        "Stack", "Monotonic Index Stack", "Hard", "Stack Index Baseline Tracking",
        "Renowned interview problem testing stack index baselines or DP transitions for nested substrings.",
        "Length of longest valid (well-formed) parentheses substring.",
        "Push -1 to stack as baseline. For '(', push index. For ')', pop: if empty, push current index as new baseline; else maxLen = max(maxLen, i - st.top()).",
        "Initialize stack with -1. For i = 0..n-1: if s[i] == '(', push i. Else pop: if empty push i; else maxLen = max(maxLen, i - st.top()).",
        "Time: O(N), Space: O(N)",
        """#include <string>
#include <stack>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestValidParentheses(string s) {
        stack<int> st;
        st.push(-1);
        int maxLen = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                st.push(i);
            } else {
                st.pop();
                if (st.empty()) {
                    st.push(i);
                } else {
                    maxLen = max(maxLen, i - st.top());
                }
            }
        }
        return maxLen;
    }
};"""
    ))

    # Day 43: Dynamic Programming + Tries + Graphs
    p4.append(make_q(
        127, 43, "Maximum Profit in Job Scheduling", "maximum-profit-in-job-scheduling",
        "Dynamic Programming", "DP with Binary Search", "Hard", "Job Interval Sorting with Binary Search DP",
        "Classic interview problem combining weighted interval scheduling with binary search (upper_bound).",
        "Maximum profit by scheduling non-overlapping jobs.",
        "Sort jobs by end time. For job i, either skip it (dp[i-1]) or take it (profit + dp[latest non-overlapping job found via binary search]).",
        "Structure Job (startTime, endTime, profit). Sort by endTime. DP array of pairs (endTime, maxProfit). For each job, binary search latest job with endTime <= start, update max profit.",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    struct Job { int s, e, p; };
public:
    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<Job> jobs(n);
        for (int i = 0; i < n; i++) jobs[i] = {startTime[i], endTime[i], profit[i]};
        sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) { return a.e < b.e; });
        vector<pair<int, int>> dp = {{0, 0}}; // {endTime, maxProfit}
        for (const auto& j : jobs) {
            auto it = upper_bound(dp.begin(), dp.end(), make_pair(j.s, 2000000000)) - 1;
            int takeProfit = it->second + j.p;
            if (takeProfit > dp.back().second) {
                dp.push_back({j.e, takeProfit});
            }
        }
        return dp.back().second;
    }
};"""
    ))

    p4.append(make_q(
        128, 43, "Word Search II", "word-search-ii",
        "Tries", "Trie + Grid Backtracking", "Hard", "Simultaneous Multi-word Trie Backtracking",
        "Demonstrates pruning 2D grid DFS using Trie so multiple dictionary words are searched simultaneously.",
        "Find all words from dictionary present in 2D character board.",
        "Build a Trie of all words. Run DFS on board, stepping into Trie children. Prune leaves as words are found.",
        "Insert all words into Trie, storing word string at terminal node. DFS grid: follow Trie child pointers; when word found, add to result and set terminal null to avoid duplicate results.",
        "Time: O(M * N * 4 * 3^(L-1)), Space: O(Total letters in words)",
        """#include <vector>
#include <string>
using namespace std;

class Solution {
    struct TrieNode {
        TrieNode* children[26] = {};
        string word = "";
    };
    TrieNode* buildTrie(const vector<string>& words) {
        TrieNode* root = new TrieNode();
        for (const string& w : words) {
            TrieNode* curr = root;
            for (char c : w) {
                int idx = c - 'a';
                if (!curr->children[idx]) curr->children[idx] = new TrieNode();
                curr = curr->children[idx];
            }
            curr->word = w;
        }
        return root;
    }
    void dfs(vector<vector<char>>& board, int r, int c, TrieNode* node, vector<string>& res) {
        char ch = board[r][c];
        if (ch == '#' || !node->children[ch - 'a']) return;
        node = node->children[ch - 'a'];
        if (!node->word.empty()) {
            res.push_back(node->word);
            node->word = "";
        }
        board[r][c] = '#';
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        for (auto& d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < (int)board.size() && nc >= 0 && nc < (int)board[0].size()) {
                dfs(board, nr, nc, node, res);
            }
        }
        board[r][c] = ch;
    }
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        TrieNode* root = buildTrie(words);
        vector<string> res;
        for (int i = 0; i < (int)board.size(); i++) {
            for (int j = 0; j < (int)board[0].size(); j++) {
                dfs(board, i, j, root, res);
            }
        }
        return res;
    }
};"""
    ))

    p4.append(make_q(
        129, 43, "Shortest Path in a Grid with Obstacles Elimination", "shortest-path-in-a-grid-with-obstacles-elimination",
        "Graphs", "3D State BFS", "Hard", "State Augmentation BFS (r, c, remainingK)",
        "Tests augmenting BFS state with resource constraints (remaining obstacle eliminations).",
        "Shortest path in grid from (0, 0) to (m-1, n-1) eliminating at most k obstacles.",
        "State in BFS is (row, col, remainingK). Track visited[r][c] with maximum remainingK seen so far.",
        "Queue contains tuple (r, c, kRemaining, steps). If k >= m + n - 2, Manhattan distance is answer. BFS expands 4 directions, updating remainingK.",
        "Time: O(M * N * K), Space: O(M * N * K)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int shortestPath(vector<vector<int>>& grid, int k) {
        int m = grid.size(), n = grid[0].size();
        if (k >= m + n - 2) return m + n - 2;
        vector<vector<int>> visited(m, vector<int>(n, -1));
        queue<vector<int>> q; // {r, c, remainingK, steps}
        q.push({0, 0, k, 0});
        visited[0][0] = k;
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        while (!q.empty()) {
            auto curr = q.front(); q.pop();
            int r = curr[0], c = curr[1], rem = curr[2], steps = curr[3];
            if (r == m - 1 && c == n - 1) return steps;
            for (auto& d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int nextRem = rem - grid[nr][nc];
                    if (nextRem >= 0 && nextRem > visited[nr][nc]) {
                        visited[nr][nc] = nextRem;
                        q.push({nr, nc, nextRem, steps + 1});
                    }
                }
            }
        }
        return -1;
    }
};"""
    ))

    # Day 44: Heap + Dynamic Programming + Design
    p4.append(make_q(
        130, 44, "Smallest Range Covering Elements from K Lists", "smallest-range-covering-elements-from-k-lists",
        "Heap", "K-Way Pointer Sliding Window", "Hard", "Min-Heap + Rolling Max Window",
        "Combines k-way merge with sliding window to find minimum range containing at least one number from each of k sorted lists.",
        "Smallest range [a, b] that includes at least one number from each of k sorted lists.",
        "Min-heap stores current element from each of k lists along with current max element in the heap. Range is [minHeap.top(), maxVal].",
        "Push first element of each list to min-heap while tracking currentMax. Loop: pop min, compare range (currentMax - min) with best range. Advance pointer in popped element's list and push next; break if any list exhausts.",
        "Time: O(N log K), Space: O(K)",
        """#include <vector>
#include <queue>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
    struct Element {
        int val, listIdx, elemIdx;
        bool operator>(const Element& other) const { return val > other.val; }
    };
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        priority_queue<Element, vector<Element>, greater<Element>> pq;
        int curMax = INT_MIN;
        for (int i = 0; i < (int)nums.size(); i++) {
            pq.push({nums[i][0], i, 0});
            curMax = max(curMax, nums[i][0]);
        }
        int start = 0, end = INT_MAX;
        while (pq.size() == nums.size()) {
            auto [val, r, c] = pq.top(); pq.pop();
            if (curMax - val < end - start) {
                start = val;
                end = curMax;
            }
            if (c + 1 < (int)nums[r].size()) {
                pq.push({nums[r][c + 1], r, c + 1});
                curMax = max(curMax, nums[r][c + 1]);
            }
        }
        return {start, end};
    }
};"""
    ))

    p4.append(make_q(
        131, 44, "Russian Doll Envelopes", "russian-doll-envelopes",
        "Dynamic Programming", "2D LIS with Sorting", "Hard", "Custom Sort + LIS Binary Search",
        "Elegant transformation: sorting width ascending and height descending reduces 2D nesting into 1D LIS.",
        "Maximum number of envelopes you can Russian doll (fit inside one another).",
        "Sort envelopes by width ascending; for equal widths, sort height descending! Then find LIS on heights.",
        "Custom sort ensures same width cannot nest. Run patience sorting (lower_bound) on height array.",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        sort(envelopes.begin(), envelopes.end(), [](const vector<int>& a, const vector<int>& b) {
            if (a[0] == b[0]) return a[1] > b[1];
            return a[0] < b[0];
        });
        vector<int> lis;
        for (const auto& env : envelopes) {
            int h = env[1];
            auto it = lower_bound(lis.begin(), lis.end(), h);
            if (it == lis.end()) lis.push_back(h);
            else *it = h;
        }
        return lis.size();
    }
};"""
    ))

    p4.append(make_q(
        132, 44, "Maximum Frequency Stack", "maximum-frequency-stack",
        "Stack", "Design / Frequency Stack", "Hard", "Hash Map of Frequency Bucketed Stacks",
        "System design problem achieving O(1) push and pop based on element frequency.",
        "Stack-like data structure that pops the most frequent element, breaking ties with recency.",
        "Map frequency to a stack of elements. Track maxFrequency. On pop, pop from group[maxFrequency].",
        "Two hash maps: freq[val] and group[frequency] -> stack<int>. push(x): freq[x]++, maxFreq = max(maxFreq, freq[x]), group[freq[x]].push(x). pop(): x = group[maxFreq].top(), pop(), freq[x]--, if empty decrement maxFreq.",
        "Time: O(1) push & pop, Space: O(N)",
        """#include <unordered_map>
#include <stack>
#include <algorithm>
using namespace std;

class FreqStack {
    unordered_map<int, int> freq;
    unordered_map<int, stack<int>> group;
    int maxFreq = 0;
public:
    FreqStack() {}
    void push(int val) {
        int f = ++freq[val];
        maxFreq = max(maxFreq, f);
        group[f].push(val);
    }
    int pop() {
        int val = group[maxFreq].top();
        group[maxFreq].pop();
        freq[val]--;
        if (group[maxFreq].empty()) maxFreq--;
        return val;
    }
};"""
    ))

    # Day 45: Final Day - Mixed Interview Simulation (Graph + DP + Trees)
    p4.append(make_q(
        133, 45, "Bus Routes", "bus-routes",
        "Graphs", "Multi-source BFS on Routes", "Hard", "Bipartite Route-Stop Graph BFS",
        "Models bus network as graph of bus routes rather than individual stops to minimize state expansion.",
        "Least number of buses to take to travel from source to target bus stop.",
        "Map each stop to the list of buses visiting it. Run BFS over buses taken rather than stops.",
        "Map stop -> vector of route indices. Queue stores (routeIndex, busCount). Mark visited routes and stops to avoid repeating transfers. Return bus count upon reaching target stop.",
        "Time: O(Total stops across all routes), Space: O(Total stops)",
        """#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
using namespace std;

class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int source, int target) {
        if (source == target) return 0;
        unordered_map<int, vector<int>> stopToRoutes;
        for (int i = 0; i < (int)routes.size(); i++) {
            for (int stop : routes[i]) stopToRoutes[stop].push_back(i);
        }
        queue<pair<int, int>> q; // {stop, busesTaken}
        unordered_set<int> visitedStops;
        vector<bool> visitedRoutes(routes.size(), false);
        q.push({source, 0});
        visitedStops.insert(source);
        while (!q.empty()) {
            auto [stop, count] = q.front(); q.pop();
            if (stop == target) return count;
            for (int r : stopToRoutes[stop]) {
                if (visitedRoutes[r]) continue;
                visitedRoutes[r] = true;
                for (int nextStop : routes[r]) {
                    if (!visitedStops.count(nextStop)) {
                        visitedStops.insert(nextStop);
                        q.push({nextStop, count + 1});
                    }
                }
            }
        }
        return -1;
    }
};"""
    ))

    p4.append(make_q(
        134, 45, "Palindrome Partitioning II", "palindrome-partitioning-ii",
        "Dynamic Programming", "1D DP with Palindrome Matrix", "Hard", "1D Cuts DP with Precomputed Palindrome Table",
        "Cuts minimization problem combining palindrome table precomputation with 1D DP.",
        "Minimum cuts needed for a palindrome partitioning of string s.",
        "dp[i] is minimum cuts for s[0..i]. If s[j..i] is a palindrome, dp[i] = min(dp[i], dp[j-1] + 1).",
        "Expand palindromes around centers to fill cuts array in-place, or precompute isPal[i][j]. Update dp[i] = min cuts.",
        "Time: O(N^2), Space: O(N)",
        """#include <string>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minCut(string s) {
        int n = s.size();
        vector<int> dp(n);
        iota(dp.begin(), dp.end(), 0);
        for (int mid = 0; mid < n; mid++) {
            // odd palindrome
            for (int l = mid, r = mid; l >= 0 && r < n && s[l] == s[r]; l--, r++) {
                int cuts = (l == 0) ? 0 : dp[l - 1] + 1;
                dp[r] = min(dp[r], cuts);
            }
            // even palindrome
            for (int l = mid, r = mid + 1; l >= 0 && r < n && s[l] == s[r]; l--, r++) {
                int cuts = (l == 0) ? 0 : dp[l - 1] + 1;
                dp[r] = min(dp[r], cuts);
            }
        }
        return dp[n - 1];
    }
};"""
    ))

    p4.append(make_q(
        135, 45, "Recover Binary Search Tree", "recover-binary-search-tree",
        "Trees", "Inorder BST Recovery", "Medium", "Inorder Inversion Pair Identification",
        "Final capstone problem: identifying exactly two swapped nodes in BST in O(1) space using Morris traversal.",
        "Recover BST where exactly two nodes were swapped by mistake without changing tree structure.",
        "Inorder traversal of valid BST is strictly increasing. Find the two inversion points where prev->val > curr->val.",
        "Track prev, first, second. If prev->val > curr->val: if !first first = prev; second = curr. Swap first->val and second->val.",
        "Time: O(N), Space: O(H) or O(1) with Morris",
        """#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    TreeNode *first = nullptr, *second = nullptr, *prev = nullptr;
    void inorder(TreeNode* root) {
        if (!root) return;
        inorder(root->left);
        if (prev && prev->val > root->val) {
            if (!first) first = prev;
            second = root;
        }
        prev = root;
        inorder(root->right);
    }
public:
    void recoverTree(TreeNode* root) {
        inorder(root);
        if (first && second) swap(first->val, second->val);
    }
};"""
    ))

    return p4
