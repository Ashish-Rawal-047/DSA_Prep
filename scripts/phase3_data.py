def get_phase3_questions(make_q):
    p3 = []

    # Day 26: Graphs + Trees + Dynamic Programming
    p3.append(make_q(
        76, 26, "Cheapest Flights Within K Stops", "cheapest-flights-within-k-stops",
        "Graphs", "Shortest Path with Step Limit", "Medium", "Bellman-Ford / K-step Relaxation",
        "Classic constrained shortest path: Bellman-Ford relaxed exactly k + 1 times using previous round copies.",
        "Cheapest flight price from src to dst with at most k stops.",
        "Run Bellman-Ford edge relaxation k + 1 times. Keep a copy of previous prices array to avoid using > k stops in one iteration.",
        "Initialize prices array with INF, prices[src] = 0. Repeat k + 1 times: create copy tmp = prices. For each flight (u, v, w): if prices[u] != INF, tmp[v] = min(tmp[v], prices[u] + w). prices = tmp.",
        "Time: O(K * E), Space: O(V)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, 1e9);
        prices[src] = 0;
        for (int i = 0; i <= k; i++) {
            vector<int> tmp = prices;
            for (auto& f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (prices[u] != 1e9 && prices[u] + w < tmp[v]) {
                    tmp[v] = prices[u] + w;
                }
            }
            prices = tmp;
        }
        return prices[dst] == 1e9 ? -1 : prices[dst];
    }
};"""
    ))

    p3.append(make_q(
        77, 26, "Binary Tree Right Side View", "binary-tree-right-side-view",
        "Trees", "Tree Level-Order Traversal", "Medium", "Level-Order Last Node Extraction",
        "High-frequency interview question testing level-order traversal and right-first DFS.",
        "Nodes visible when looking at binary tree from right side.",
        "At each level of BFS, the last node processed in that level is visible from the right.",
        "BFS queue: loop level by level. In each level, iterate over all nodes of that level; push the value of the last node into result.",
        "Time: O(N), Space: O(W) where W is max tree width",
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
    vector<int> rightSideView(TreeNode* root) {
        if (!root) return {};
        vector<int> view;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                TreeNode* node = q.front(); q.pop();
                if (i == sz - 1) view.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        return view;
    }
};"""
    ))

    p3.append(make_q(
        78, 26, "Longest Common Subsequence", "longest-common-subsequence",
        "Dynamic Programming", "2D String DP", "Medium", "Classic 2D Grid Subsequence DP",
        "Foundational 2D dynamic programming problem forming the basis for diff tools and bioinformatics.",
        "Length of longest common subsequence between two strings.",
        "If text1[i-1] == text2[j-1], dp[i][j] = dp[i-1][j-1] + 1; otherwise max(dp[i-1][j], dp[i][j-1]).",
        "Build (m+1) x (n+1) table. Fill cells using standard transition. Space can be optimized to two rows.",
        "Time: O(M * N), Space: O(M * N) or O(min(M, N))",
        """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size(), n = text2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1[i - 1] == text2[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
                else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }
};"""
    ))

    # Day 27: Strings + Stack + Greedy
    p3.append(make_q(
        79, 27, "Find All Anagrams in a String", "find-all-anagrams-in-a-string",
        "Strings", "Sliding Window", "Medium", "Fixed-Size Sliding Window Frequency Vector",
        "Fixed-size sliding window with constant-time frequency equality checking.",
        "Find all start indices of anagrams of p in s.",
        "Window size is fixed at p.length(). Update count vectors as window moves right. Compare vectors in O(26) time.",
        "Track char counts of p and current window of s of length p.size(). When vectors match, push start index. Shift window right.",
        "Time: O(S), Space: O(26) = O(1)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        if (s.size() < p.size()) return {};
        vector<int> pCount(26, 0), sCount(26, 0), res;
        for (char c : p) pCount[c - 'a']++;
        int k = p.size();
        for (int i = 0; i < (int)s.size(); i++) {
            sCount[s[i] - 'a']++;
            if (i >= k) sCount[s[i - k] - 'a']--;
            if (sCount == pCount) res.push_back(i - k + 1);
        }
        return res;
    }
};"""
    ))

    p3.append(make_q(
        80, 27, "Evaluate Reverse Polish Notation", "evaluate-reverse-polish-notation",
        "Stack", "Postfix Expression Evaluation", "Medium", "Operand Stack Arithmetic Reduction",
        "Tests stack application in arithmetic parser evaluation.",
        "Evaluate arithmetic expression in Reverse Polish Notation (postfix).",
        "Push numbers to stack. When an operator is encountered, pop top two operands, apply operator, push result.",
        "Loop tokens: if token is operator (+, -, *, /), pop op2 then op1, compute op1 (op) op2, push back. Else push stoi(token). Return stack top.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <string>
#include <stack>
using namespace std;

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<long long> st;
        for (const string& t : tokens) {
            if (t == "+" || t == "-" || t == "*" || t == "/") {
                long long b = st.top(); st.pop();
                long long a = st.top(); st.pop();
                if (t == "+") st.push(a + b);
                else if (t == "-") st.push(a - b);
                else if (t == "*") st.push(a * b);
                else st.push(a / b);
            } else {
                st.push(stoll(t));
            }
        }
        return st.top();
    }
};"""
    ))

    p3.append(make_q(
        81, 27, "Partition Labels", "partition-labels",
        "Greedy", "Interval Partitioning", "Medium", "Farthest Occurrence Boundary Extension",
        "Tests partition boundary extension: each letter must appear in at most one partition.",
        "Partition string into as many parts as possible so that each letter appears in at most one part.",
        "Precompute last occurrence index of each character. Current partition must extend to max(lastOccurrence) of all characters inside it.",
        "Pass 1: record lastIndex[c]. Pass 2: track maxEnd = max(maxEnd, lastIndex[s[i]]). When i == maxEnd, partition finishes! Record length.",
        "Time: O(N), Space: O(26) = O(1)",
        """#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> partitionLabels(string s) {
        vector<int> last(26, 0);
        for (int i = 0; i < (int)s.size(); i++) last[s[i] - 'a'] = i;
        vector<int> res;
        int start = 0, end = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            end = max(end, last[s[i] - 'a']);
            if (i == end) {
                res.push_back(end - start + 1);
                start = i + 1;
            }
        }
        return res;
    }
};"""
    ))

    # Day 28: Graphs + Trees + Dynamic Programming
    p3.append(make_q(
        82, 28, "Accounts Merge", "accounts-merge",
        "Graphs", "Union Find / Connected Components", "Medium", "Email Disjoint Set Union",
        "Complex real-world entity resolution problem testing DSU or DFS connected components.",
        "Merge accounts sharing common emails.",
        "Union all emails within the same account. Group emails by parent representative root, sort, and attach account name.",
        "Assign an ID to each email. Union emails within each account list. Map each email to root ID, gather lists, sort emails, prepend name.",
        "Time: O(N * K log(N * K)), Space: O(N * K)",
        """#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
    unordered_map<string, string> parent;
    string find(const string& s) {
        if (!parent.count(s) || parent[s] == s) return parent[s] = s;
        return parent[s] = find(parent[s]);
    }
    void unite(const string& a, const string& b) {
        string rootA = find(a), rootB = find(b);
        if (rootA != rootB) parent[rootA] = rootB;
    }
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        unordered_map<string, string> emailToName;
        for (auto& acc : accounts) {
            string name = acc[0];
            for (size_t i = 1; i < acc.size(); i++) {
                emailToName[acc[i]] = name;
                unite(acc[1], acc[i]);
            }
        }
        unordered_map<string, vector<string>> groups;
        for (auto& [email, name] : emailToName) {
            groups[find(email)].push_back(email);
        }
        vector<vector<string>> res;
        for (auto& [root, emails] : groups) {
            sort(emails.begin(), emails.end());
            emails.insert(emails.begin(), emailToName[root]);
            res.push_back(emails);
        }
        return res;
    }
};"""
    ))

    p3.append(make_q(
        83, 28, "Binary Tree Zigzag Level Order Traversal", "binary-tree-zigzag-level-order-traversal",
        "Trees", "BFS Level-Order", "Medium", "Alternating Direction Level BFS",
        "Tests level-order traversal with alternating insertion index.",
        "Level order traversal of binary tree alternating left-to-right and right-to-left.",
        "Use normal BFS queue. If current level is right-to-left, fill vector positions from back to front (size - 1 - i).",
        "Standard BFS level size loop. Allocate vector<int> level(sz). If leftToRight index = i, else sz - 1 - i. Toggle leftToRight flag after each level.",
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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        if (!root) return {};
        vector<vector<int>> res;
        queue<TreeNode*> q;
        q.push(root);
        bool l2r = true;
        while (!q.empty()) {
            int sz = q.size();
            vector<int> level(sz);
            for (int i = 0; i < sz; i++) {
                TreeNode* node = q.front(); q.pop();
                int idx = l2r ? i : sz - 1 - i;
                level[idx] = node->val;
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            res.push_back(level);
            l2r = !l2r;
        }
        return res;
    }
};"""
    ))

    p3.append(make_q(
        84, 28, "Edit Distance", "edit-distance",
        "Dynamic Programming", "2D String DP", "Medium", "Levenshtein Distance Matrix",
        "The classic string edit distance problem tested at Google, Meta, and Uber.",
        "Minimum operations (insert, delete, replace) to convert word1 to word2.",
        "If word1[i-1] == word2[j-1], dp[i][j] = dp[i-1][j-1]. Otherwise 1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1]).",
        "2D DP table (m+1) x (n+1). dp[i][0] = i, dp[0][j] = j. Compute cell values by taking min of the 3 operation costs.",
        "Time: O(M * N), Space: O(M * N)",
        """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
                }
            }
        }
        return dp[m][n];
    }
};"""
    ))

    # Day 29: Binary Search + Arrays + Bit Manipulation
    p3.append(make_q(
        85, 29, "Find Minimum in Rotated Sorted Array", "find-minimum-in-rotated-sorted-array",
        "Binary Search", "Modified Binary Search", "Medium", "Inflection Point Binary Search",
        "Tests finding the inflection / pivot point in a rotated sorted array in O(log N).",
        "Find minimum element in rotated sorted array of unique elements.",
        "Compare nums[mid] with nums[high]. If nums[mid] > nums[high], min is strictly to the right (low = mid + 1). Else min is at or left of mid (high = mid).",
        "low = 0, high = n - 1. While low < high: mid = low + (high - low) / 2. If nums[mid] > nums[high] low = mid + 1; else high = mid. Return nums[low].",
        "Time: O(log N), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    int findMin(vector<int>& nums) {
        int low = 0, high = nums.size() - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] > nums[high]) low = mid + 1;
            else high = mid;
        }
        return nums[low];
    }
};"""
    ))

    p3.append(make_q(
        86, 29, "Sort Colors", "sort-colors",
        "Arrays", "3-Way Partitioning", "Medium", "Dutch National Flag Algorithm",
        "Classic Dijkstra three-way partitioning in a single pass with O(1) space.",
        "Sort array with values 0, 1, and 2 in-place in one pass.",
        "Maintain three pointers: low (boundary of 0s), mid (current element), high (boundary of 2s).",
        "While mid <= high: if nums[mid] == 0, swap(nums[low++], nums[mid++]); if nums[mid] == 1, mid++; if nums[mid] == 2, swap(nums[mid], nums[high--]).",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        int low = 0, mid = 0, high = nums.size() - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums[low++], nums[mid++]);
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                swap(nums[mid], nums[high--]);
            }
        }
    }
};"""
    ))

    p3.append(make_q(
        87, 29, "Sum of Two Integers", "sum-of-two-integers",
        "Bit Manipulation", "Bitwise Arithmetic", "Medium", "Half-Adder Logic Circuit",
        "Simulates hardware adder circuit using XOR for sum and AND with shift for carry.",
        "Sum two integers without using + or - operators.",
        "a ^ b adds bits without carry. (a & b) << 1 calculates carry bits. Repeat until carry is zero.",
        "While b != 0: carry = (unsigned int)(a & b) << 1, a = a ^ b, b = carry. Return a.",
        "Time: O(32) = O(1), Space: O(1)",
        """class Solution {
public:
    int getSum(int a, int b) {
        while (b != 0) {
            unsigned int carry = (unsigned int)(a & b) << 1;
            a = a ^ b;
            b = carry;
        }
        return a;
    }
};"""
    ))

    # Day 30: Trees + Backtracking + Dynamic Programming
    p3.append(make_q(
        88, 30, "Path Sum III", "path-sum-iii",
        "Trees", "Prefix Sum on Trees", "Medium", "Tree Traversal with Running Prefix Frequency",
        "Combines Subarray Sum Equals K hashmap technique with tree recursion and backtracking.",
        "Number of paths in binary tree summing to targetSum, paths only go downwards.",
        "Maintain running prefix sum map. Current node prefixSum - targetSum count gives paths ending at this node. Backtrack map count on return!",
        "DFS with map prefixCount[sum]. Add map[currSum - targetSum] to answer. Increment map[currSum], recurse left and right, decrement map[currSum].",
        "Time: O(N), Space: O(H)",
        """#include <unordered_map>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    unordered_map<long long, int> prefixCount;
    int totalPaths = 0;
    void dfs(TreeNode* node, long long currentSum, int targetSum) {
        if (!node) return;
        currentSum += node->val;
        if (prefixCount.count(currentSum - targetSum)) {
            totalPaths += prefixCount[currentSum - targetSum];
        }
        prefixCount[currentSum]++;
        dfs(node->left, currentSum, targetSum);
        dfs(node->right, currentSum, targetSum);
        prefixCount[currentSum]--;
    }
public:
    int pathSum(TreeNode* root, int targetSum) {
        prefixCount[0] = 1;
        totalPaths = 0;
        dfs(root, 0, targetSum);
        return totalPaths;
    }
};"""
    ))

    p3.append(make_q(
        89, 30, "Palindrome Partitioning", "palindrome-partitioning",
        "Backtracking", "String Partitioning", "Medium", "Backtracking with Palindrome Check",
        "Standard backtracking interview question partitioning strings into symmetric components.",
        "All possible palindrome partitionings of string s.",
        "From index start, try all substring cuts s[start..i]. If substring is palindrome, add to current list and recurse from i + 1.",
        "Backtrack(start): if start == s.size() save current. Loop i from start to s.size()-1: if isPalindrome(s, start, i), push substr, recurse backtrack(i + 1), pop.",
        "Time: O(N * 2^N), Space: O(N)",
        """#include <vector>
#include <string>
using namespace std;

class Solution {
    bool isPalindrome(const string& s, int l, int r) {
        while (l < r) {
            if (s[l++] != s[r--]) return false;
        }
        return true;
    }
    void backtrack(const string& s, int start, vector<string>& curr, vector<vector<string>>& res) {
        if (start == (int)s.size()) {
            res.push_back(curr);
            return;
        }
        for (int i = start; i < (int)s.size(); i++) {
            if (isPalindrome(s, start, i)) {
                curr.push_back(s.substr(start, i - start + 1));
                backtrack(s, i + 1, curr, res);
                curr.pop_back();
            }
        }
    }
public:
    vector<vector<string>> partition(string s) {
        vector<vector<string>> res;
        vector<string> curr;
        backtrack(s, 0, curr, res);
        return res;
    }
};"""
    ))

    p3.append(make_q(
        90, 30, "Best Time to Buy and Sell Stock with Cooldown", "best-time-to-buy-and-sell-stock-with-cooldown",
        "Dynamic Programming", "State Machine DP", "Medium", "Three-State Finite Automaton DP",
        "Premier state machine DP interview question with distinct hold, sold, and rest states.",
        "Max stock profit with 1-day cooldown after selling.",
        "Model 3 states: Hold (holding stock), Sold (just sold today, must cooldown tomorrow), Rest (cooldown completed, ready to buy).",
        "Hold[i] = max(Hold[i-1], Rest[i-1] - price). Sold[i] = Hold[i-1] + price. Rest[i] = max(Rest[i-1], Sold[i-1]). Update states sequentially.",
        "Time: O(N), Space: O(1)",
        """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int hold = -1e9, sold = 0, rest = 0;
        for (int p : prices) {
            int prevSold = sold;
            sold = hold + p;
            hold = max(hold, rest - p);
            rest = max(rest, prevSold);
        }
        return max(sold, rest);
    }
};"""
    ))

    # Day 31: Graphs + Binary Search + Arrays
    p3.append(make_q(
        91, 31, "Word Ladder", "word-ladder",
        "Graphs", "BFS Shortest Path", "Hard", "Bidirectional / Level BFS on Word Graph",
        "Very common interview problem modeling dictionary transformation as shortest path in unweighted graph.",
        "Shortest transformation sequence from beginWord to endWord changing one letter at a time.",
        "BFS level traversal guarantees the first time endWord is reached is the shortest transformation sequence.",
        "Put wordList in unordered_set. Run BFS with queue of strings, tracking ladder length. For each word, try changing each of L positions to 'a'-'z'. If word in set, erase and enqueue.",
        "Time: O(N * L * 26), Space: O(N * L)",
        """#include <string>
#include <vector>
#include <unordered_set>
#include <queue>
using namespace std;

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> words(wordList.begin(), wordList.end());
        if (!words.count(endWord)) return 0;
        queue<string> q;
        q.push(beginWord);
        int steps = 1;
        while (!q.empty()) {
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                string w = q.front(); q.pop();
                if (w == endWord) return steps;
                for (int i = 0; i < (int)w.size(); i++) {
                    char orig = w[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        w[i] = c;
                        if (words.count(w)) {
                            words.erase(w);
                            q.push(w);
                        }
                    }
                    w[i] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
};"""
    ))

    p3.append(make_q(
        92, 31, "Kth Smallest Element in a Sorted Matrix", "kth-smallest-element-in-a-sorted-matrix",
        "Binary Search", "Binary Search on Value Range", "Medium", "2D Sorted Matrix Count Predicate",
        "Demonstrates binary search on numerical range, counting elements <= mid in O(N) using staircase.",
        "Find kth smallest element in row and column sorted matrix.",
        "Range is between matrix[0][0] and matrix[n-1][n-1]. In O(N), count how many elements are <= mid using staircase traversal.",
        "Binary search low = matrix[0][0], high = matrix[n-1][n-1]. Count elements <= mid: start bottom-left, if matrix[r][c] <= mid add r + 1, c++; else r--. Adjust low/high.",
        "Time: O(N * log(Max - Min)), Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
    int countLessEqual(const vector<vector<int>>& matrix, int mid) {
        int n = matrix.size(), count = 0, r = n - 1, c = 0;
        while (r >= 0 && c < n) {
            if (matrix[r][c] <= mid) {
                count += r + 1;
                c++;
            } else {
                r--;
            }
        }
        return count;
    }
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();
        int low = matrix[0][0], high = matrix[n - 1][n - 1];
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (countLessEqual(matrix, mid) < k) low = mid + 1;
            else high = mid;
        }
        return low;
    }
};"""
    ))

    p3.append(make_q(
        93, 31, "Continuous Subarray Sum", "continuous-subarray-sum",
        "Arrays", "Prefix Sum Modulo Hashing", "Medium", "Modulo Equivalence Interval Hashing",
        "Tests mathematical principle: if prefixSum[j] % k == prefixSum[i] % k, subarray sum between i and j is divisible by k.",
        "Good subarray of length at least 2 whose sum is a multiple of k.",
        "Store the earliest seen index of (prefixSum % k). If current remainder matches an earlier index with distance >= 2, return true.",
        "Keep map remainder -> earliestIndex, initialized with {0, -1}. Update running sum, rem = sum % k. If map has rem: check i - map[rem] >= 2. Else store map[rem] = i.",
        "Time: O(N), Space: O(min(N, K))",
        """#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> remainderMap;
        remainderMap[0] = -1;
        int sum = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            sum += nums[i];
            int rem = sum % k;
            if (remainderMap.count(rem)) {
                if (i - remainderMap[rem] >= 2) return true;
            } else {
                remainderMap[rem] = i;
            }
        }
        return false;
    }
};"""
    ))

    # Day 32: Linked Lists / Design + Trees + Dynamic Programming
    p3.append(make_q(
        94, 32, "LRU Cache", "lru-cache",
        "Linked Lists", "Cache Design", "Medium", "Hash Map + Doubly Linked List",
        "The universally famous system design coding question testing O(1) get and put.",
        "Implement Least Recently Used (LRU) cache with O(1) get and put operations.",
        "Combine hash map with doubly linked list. Most recently accessed items move to head; eviction removes from tail.",
        "Define DNode struct (key, val, prev, next). Map stores key -> DNode*. On get, move node to head. On put, update or insert at head. If capacity exceeded, evict tail->prev.",
        "Time: O(1) all ops, Space: O(Capacity)",
        """#include <unordered_map>
using namespace std;

class LRUCache {
    struct Node {
        int key, val;
        Node *prev, *next;
        Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
    };
    int cap;
    unordered_map<int, Node*> map;
    Node *head, *tail;
    void addNode(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }
    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }
    void moveToHead(Node* node) {
        removeNode(node);
        addNode(node);
    }
public:
    LRUCache(int capacity) : cap(capacity) {
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head->next = tail;
        tail->prev = head;
    }
    int get(int key) {
        if (!map.count(key)) return -1;
        Node* node = map[key];
        moveToHead(node);
        return node->val;
    }
    void put(int key, int value) {
        if (map.count(key)) {
            Node* node = map[key];
            node->val = value;
            moveToHead(node);
        } else {
            if ((int)map.size() == cap) {
                Node* lru = tail->prev;
                map.erase(lru->key);
                removeNode(lru);
                delete lru;
            }
            Node* newNode = new Node(key, value);
            map[key] = newNode;
            addNode(newNode);
        }
    }
};"""
    ))

    p3.append(make_q(
        95, 32, "Maximum Width of Binary Tree", "maximum-width-of-binary-tree",
        "Trees", "BFS Node Indexing", "Medium", "64-bit Heap-style Index Normalization",
        "Tests tree indexing (left = 2*i, right = 2*i + 1) with integer overflow prevention.",
        "Maximum width of binary tree considering null nodes between end nodes at any level.",
        "Assign 1-based heap indices to nodes. Normalize indices at each level by subtracting the level's minimum index.",
        "BFS queue of pair<TreeNode*, unsigned long long>. At each level: width = last_idx - first_idx + 1. Children get indices 2*(idx - min_idx) and 2*(idx - min_idx) + 1.",
        "Time: O(N), Space: O(W)",
        """#include <queue>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    int widthOfBinaryTree(TreeNode* root) {
        if (!root) return 0;
        queue<pair<TreeNode*, unsigned long long>> q;
        q.push({root, 0});
        unsigned long long maxWidth = 0;
        while (!q.empty()) {
            int sz = q.size();
            unsigned long long minIdx = q.front().second;
            unsigned long long first = 0, last = 0;
            for (int i = 0; i < sz; i++) {
                auto [node, idx] = q.front(); q.pop();
                unsigned long long normIdx = idx - minIdx;
                if (i == 0) first = normIdx;
                if (i == sz - 1) last = normIdx;
                if (node->left) q.push({node->left, 2 * normIdx});
                if (node->right) q.push({node->right, 2 * normIdx + 1});
            }
            maxWidth = max(maxWidth, last - first + 1);
        }
        return maxWidth;
    }
};"""
    ))

    p3.append(make_q(
        96, 32, "Interleaving String", "interleaving-string",
        "Dynamic Programming", "2D String Matching DP", "Medium", "Dual Pointer DP Grid Reachability",
        "Tests interleaving sequence matching across two source strings.",
        "Determine if s3 is formed by an interleaving of s1 and s2.",
        "dp[i][j] is true if s1[0..i-1] and s2[0..j-1] interleave to form s3[0..i+j-1].",
        "If s1.size() + s2.size() != s3.size() return false. dp[i][j] = (dp[i-1][j] && s1[i-1] == s3[i+j-1]) || (dp[i][j-1] && s2[j-1] == s3[i+j-1]).",
        "Time: O(M * N), Space: O(N)",
        """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != (int)s3.size()) return false;
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int j = 1; j <= n; j++) dp[j] = dp[j - 1] && (s2[j - 1] == s3[j - 1]);
        for (int i = 1; i <= m; i++) {
            dp[0] = dp[0] && (s1[i - 1] == s3[i - 1]);
            for (int j = 1; j <= n; j++) {
                dp[j] = (dp[j] && s1[i - 1] == s3[i + j - 1]) || (dp[j - 1] && s2[j - 1] == s3[i + j - 1]);
            }
        }
        return dp[n];
    }
};"""
    ))

    # Day 33: Graphs + Stack + Greedy
    p3.append(make_q(
        97, 33, "Find Eventual Safe States", "find-eventual-safe-states",
        "Graphs", "Cycle Detection / 3-Color DFS", "Medium", "Tri-Color DFS State Coloring",
        "Tests 3-state graph node coloring (unvisited=0, visiting=1, safe=2) to detect all nodes that never enter cycles.",
        "Find all nodes from which every path leads to a terminal node.",
        "Nodes trapped in or leading into a cycle are unsafe. Use 3-color DFS to mark safe nodes.",
        "Color array 0=unvisited, 1=in-stack, 2=safe. DFS(u): mark 1. For neighbor v: if color[v] == 1 or (!color[v] && !dfs(v)) return false. Mark color[u] = 2, return true.",
        "Time: O(V + E), Space: O(V)",
        """#include <vector>
using namespace std;

class Solution {
    bool dfs(const vector<vector<int>>& graph, int u, vector<int>& color) {
        color[u] = 1;
        for (int v : graph[u]) {
            if (color[v] == 1) return false;
            if (color[v] == 0 && !dfs(graph, v, color)) return false;
        }
        color[u] = 2;
        return true;
    }
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, 0), res;
        for (int i = 0; i < n; i++) {
            if (color[i] == 2 || (color[i] == 0 && dfs(graph, i, color))) {
                res.push_back(i);
            }
        }
        return res;
    }
};"""
    ))

    p3.append(make_q(
        98, 33, "Online Stock Span", "online-stock-span",
        "Stack", "Monotonic Stack", "Medium", "Monotonic Stack with Aggregated Weights",
        "Demonstrates accumulating span weights inside monotonic stack entries in amortized O(1).",
        "Collect consecutive previous days with stock price <= today's price.",
        "Maintain stack of (price, span). While current price >= stack top price, pop and add stack top's span to current span.",
        "Initialize stack<pair<int, int>>. next(price): span = 1. While stack non-empty and st.top().first <= price, span += st.top().second, st.pop(). Push {price, span}, return span.",
        "Time: Amortized O(1) per call, Space: O(N)",
        """#include <stack>
using namespace std;

class StockSpanner {
    stack<pair<int, int>> st; // {price, span}
public:
    StockSpanner() {}
    int next(int price) {
        int span = 1;
        while (!st.empty() && st.top().first <= price) {
            span += st.top().second;
            st.pop();
        }
        st.push({price, span});
        return span;
    }
};"""
    ))

    p3.append(make_q(
        99, 33, "Candy", "candy",
        "Greedy", "Two-Pass Slope Analysis", "Hard", "Left-to-Right and Right-to-Left Greedy Passes",
        "Top-rated greedy interview problem proving optimal local distribution guarantees global minimum.",
        "Minimum candies to distribute so higher rating neighbors get more candies and everyone gets >= 1.",
        "Left pass ensures rating[i] > rating[i-1] gets candies[i-1] + 1. Right pass ensures rating[i] > rating[i+1] gets max(candies[i], candies[i+1] + 1).",
        "Initialize vector<int> candies(n, 1). Pass 1 (1..n-1): if rating[i] > rating[i-1] candies[i] = candies[i-1] + 1. Pass 2 (n-2..0): if rating[i] > rating[i+1] candies[i] = max(candies[i], candies[i+1] + 1). Sum all.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> candies(n, 1);
        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i - 1]) candies[i] = candies[i - 1] + 1;
        }
        for (int i = n - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1]) candies[i] = max(candies[i], candies[i + 1] + 1);
        }
        return accumulate(candies.begin(), candies.end(), 0);
    }
};"""
    ))

    # Day 34: Trees + Dynamic Programming + Graphs
    p3.append(make_q(
        100, 34, "Binary Search Tree Iterator", "binary-search-tree-iterator",
        "Trees", "BST Design / Inorder Stack", "Medium", "Controlled Stack Inorder Stepping",
        "Tests implementing controlled step-by-step traversal with O(H) memory and amortized O(1) time.",
        "Design BST iterator with hasNext() and next() in O(1) average time and O(H) memory.",
        "Push all left nodes into stack initially. In next(), pop top, push all left descendants of its right child, return value.",
        "Stack of TreeNode*. Helper pushAllLeft(node): while node: push, node = node->left. next(): top = st.top(), st.pop(), pushAllLeft(top->right), return top->val.",
        "Time: next() amortized O(1), hasNext() O(1), Space: O(H)",
        """#include <stack>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class BSTIterator {
    stack<TreeNode*> st;
    void pushAllLeft(TreeNode* node) {
        while (node) {
            st.push(node);
            node = node->left;
        }
    }
public:
    BSTIterator(TreeNode* root) {
        pushAllLeft(root);
    }
    int next() {
        TreeNode* top = st.top(); st.pop();
        pushAllLeft(top->right);
        return top->val;
    }
    bool hasNext() {
        return !st.empty();
    }
};"""
    ))

    p3.append(make_q(
        101, 34, "Minimum Path Sum", "minimum-path-sum",
        "Dynamic Programming", "Grid DP", "Medium", "In-Place Grid Cost Minimization",
        "Benchmark grid path minimization problem.",
        "Minimum sum path from top-left to bottom-right of matrix moving only right and down.",
        "grid[i][j] += min(grid[i-1][j], grid[i][j-1]). Boundary cells can only come from one direction.",
        "Update grid in-place: first row accumulates left, first column accumulates top. Inner cells take min(top, left) + val.",
        "Time: O(M * N), Space: O(1) in-place",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        for (int i = 1; i < m; i++) grid[i][0] += grid[i - 1][0];
        for (int j = 1; j < n; j++) grid[0][j] += grid[0][j - 1];
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1]);
            }
        }
        return grid[m - 1][n - 1];
    }
};"""
    ))

    p3.append(make_q(
        102, 34, "Minimum Height Trees", "minimum-height-trees",
        "Graphs", "Topological Pruning / Centroid", "Medium", "Inward Leaf Trimming to Centroid",
        "Teaches tree centroids: a tree has at most 2 centroid nodes minimizing maximum height.",
        "Find all roots that give minimum height trees.",
        "Trim leaves layer by layer inwards until 1 or 2 nodes remain (the centroid(s)).",
        "Build adjacency list and degree array. Enqueue all nodes with degree == 1. While remainingNodes > 2: pop leaves of current round, decrement neighbors' degrees, enqueue new leaves.",
        "Time: O(V), Space: O(V)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if (n == 1) return {0};
        vector<vector<int>> adj(n);
        vector<int> deg(n, 0);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
            deg[e[0]]++; deg[e[1]]++;
        }
        queue<int> q;
        for (int i = 0; i < n; i++) if (deg[i] == 1) q.push(i);
        int rem = n;
        while (rem > 2) {
            int sz = q.size();
            rem -= sz;
            for (int i = 0; i < sz; i++) {
                int leaf = q.front(); q.pop();
                for (int nb : adj[leaf]) {
                    if (--deg[nb] == 1) q.push(nb);
                }
            }
        }
        vector<int> res;
        while (!q.empty()) { res.push_back(q.front()); q.pop(); }
        return res;
    }
};"""
    ))

    # Day 35: Graphs + Trees + Dynamic Programming
    p3.append(make_q(
        103, 35, "Shortest Bridge", "shortest-bridge",
        "Graphs", "DFS + Multi-source BFS", "Medium", "Island Identification + Multi-source BFS Expansion",
        "Combines DFS (to identify first component) with BFS (to find shortest path to second component).",
        "Smallest number of 0s to flip to connect two separate islands.",
        "DFS to find all cells of the first island and push them into BFS queue. Then run BFS outward until touching '1' from second island.",
        "Locate first '1'. DFS marks all its cells as 2 and adds to queue. Run level-order BFS: expand 4 directions; first time reaching cell with 1, return current distance.",
        "Time: O(R * C), Space: O(R * C)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
    int m, n;
    int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    void dfs(vector<vector<int>>& grid, int r, int c, queue<pair<int, int>>& q) {
        grid[r][c] = 2;
        q.push({r, c});
        for (auto& d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == 1) {
                dfs(grid, nr, nc, q);
            }
        }
    }
public:
    int shortestBridge(vector<vector<int>>& grid) {
        m = grid.size(); n = grid[0].size();
        queue<pair<int, int>> q;
        bool found = false;
        for (int i = 0; i < m && !found; i++) {
            for (int j = 0; j < n && !found; j++) {
                if (grid[i][j] == 1) {
                    dfs(grid, i, j, q);
                    found = true;
                }
            }
        }
        int steps = 0;
        while (!q.empty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                auto [r, c] = q.front(); q.pop();
                for (auto& d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                        if (grid[nr][nc] == 1) return steps;
                        if (grid[nr][nc] == 0) {
                            grid[nr][nc] = 2;
                            q.push({nr, nc});
                        }
                    }
                }
            }
            steps++;
        }
        return -1;
    }
};"""
    ))

    p3.append(make_q(
        104, 35, "All Nodes Distance K in Binary Tree", "all-nodes-distance-k-in-binary-tree",
        "Trees", "Graph Conversion / Parent Pointers", "Medium", "Tree to Undirected Graph Transformation",
        "Tests navigating upwards in binary trees by storing parent pointers or modeling as graph.",
        "All nodes distance k from target node in binary tree.",
        "Add parent pointers with DFS so tree becomes an undirected graph. Then run BFS distance k from target node.",
        "DFS to populate parent map. Run BFS starting at target node: explore left, right, and parent. After k levels, queue contains all distance k nodes.",
        "Time: O(N), Space: O(N)",
        """#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    unordered_map<TreeNode*, TreeNode*> parent;
    void mapParents(TreeNode* node, TreeNode* p) {
        if (!node) return;
        parent[node] = p;
        mapParents(node->left, node);
        mapParents(node->right, node);
    }
public:
    vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
        mapParents(root, nullptr);
        queue<TreeNode*> q;
        unordered_set<TreeNode*> visited;
        q.push(target);
        visited.insert(target);
        int dist = 0;
        while (!q.empty()) {
            if (dist == k) break;
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                TreeNode* curr = q.front(); q.pop();
                if (curr->left && !visited.count(curr->left)) {
                    visited.insert(curr->left); q.push(curr->left);
                }
                if (curr->right && !visited.count(curr->right)) {
                    visited.insert(curr->right); q.push(curr->right);
                }
                if (parent[curr] && !visited.count(parent[curr])) {
                    visited.insert(parent[curr]); q.push(parent[curr]);
                }
            }
            dist++;
        }
        vector<int> res;
        while (!q.empty()) { res.push_back(q.front()->val); q.pop(); }
        return res;
    }
};"""
    ))

    p3.append(make_q(
        105, 35, "Maximal Square", "maximal-square",
        "Dynamic Programming", "2D Grid DP", "Medium", "Square Side Expansion DP",
        "Elegant DP relation where side length is bounded by minimum of top, left, and diagonal neighbors.",
        "Largest square containing only 1s in binary matrix.",
        "dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]}) when matrix[i-1][j-1] == '1'.",
        "Create dp table (m+1) x (n+1). For each cell with '1', compute min of the 3 adjacent squares + 1. Track max side length. Return maxSide * maxSide.",
        "Time: O(M * N), Space: O(M * N) or O(N)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), maxSide = 0;
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
                    maxSide = max(maxSide, dp[i][j]);
                }
            }
        }
        return maxSide * maxSide;
    }
};"""
    ))

    # Day 36: Binary Search + Graphs + Dynamic Programming
    p3.append(make_q(
        106, 36, "Search in Rotated Sorted Array II", "search-in-rotated-sorted-array-ii",
        "Binary Search", "Modified Binary Search with Duplicates", "Medium", "Duplicate Trimming Binary Search",
        "Tests worst-case handling in rotated array with duplicate elements: trimming pointers when nums[low] == nums[mid] == nums[high].",
        "Search target in rotated sorted array that may contain duplicates.",
        "When nums[low] == nums[mid] == nums[high], we cannot determine which half is sorted; increment low and decrement high.",
        "Standard rotated binary search, but if nums[low] == nums[mid] && nums[mid] == nums[high]: low++; high--; continue.",
        "Time: O(log N) average, O(N) worst case, Space: O(1)",
        """#include <vector>
using namespace std;

class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int low = 0, high = nums.size() - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return true;
            if (nums[low] == nums[mid] && nums[mid] == nums[high]) {
                low++; high--;
            } else if (nums[low] <= nums[mid]) {
                if (nums[low] <= target && target < nums[mid]) high = mid - 1;
                else low = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[high]) low = mid + 1;
                else high = mid - 1;
            }
        }
        return false;
    }
};"""
    ))

    p3.append(make_q(
        107, 36, "01 Matrix", "01-matrix",
        "Graphs", "Multi-source BFS", "Medium", "All-Zeros Inward Distance BFS",
        "Standard multi-source BFS calculating nearest distance from multiple origins.",
        "Distance of nearest 0 for each cell in binary matrix.",
        "Enqueue all cells containing 0 with dist 0. Initialize 1-cells with -1 (unvisited). BFS expands distances level by level.",
        "Iterate grid: push all 0-cells to queue; set 1-cells to -1. While queue non-empty: pop cell, for 4 neighbors: if dist is -1, dist = current + 1 and enqueue.",
        "Time: O(R * C), Space: O(R * C)",
        """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        queue<pair<int, int>> q;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (mat[i][j] == 0) q.push({i, j});
                else mat[i][j] = -1;
            }
        }
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (auto& d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && mat[nr][nc] == -1) {
                    mat[nr][nc] = mat[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
        return mat;
    }
};"""
    ))

    p3.append(make_q(
        108, 36, "Longest Palindromic Subsequence", "longest-palindromic-subsequence",
        "Dynamic Programming", "Interval DP", "Medium", "Opposite-End Character Matching Interval DP",
        "Demonstrates interval DP where subproblems are defined over string substrings [i..j].",
        "Longest palindromic subsequence length in string s.",
        "If s[i] == s[j], dp[i][j] = 2 + dp[i+1][j-1]. Otherwise max(dp[i+1][j], dp[i][j-1]).",
        "DP table (n) x (n), dp[i][i] = 1. Iterate length from 2 to n, start i from 0 to n - len: calculate j = i + len - 1 using transition.",
        "Time: O(N^2), Space: O(N^2) or O(N)",
        """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) dp[i][i] = 1;
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;
                if (s[i] == s[j]) dp[i][j] = 2 + dp[i + 1][j - 1];
                else dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
            }
        }
        return dp[0][n - 1];
    }
};"""
    ))

    # Day 37: Trees + Intervals + Graphs
    p3.append(make_q(
        109, 37, "Binary Tree Cameras", "binary-tree-cameras",
        "Trees", "Tree DP / Greedy", "Hard", "Three-State Bottom-Up Coverage Induction",
        "Sophisticated tree greedy problem testing bottom-up state machine: 0=uncovered, 1=covered, 2=has camera.",
        "Minimum cameras to monitor all nodes of binary tree.",
        "Leaf nodes should never have cameras; their parents should have cameras to maximize coverage!",
        "Post-order DFS returns state: 0 (uncovered), 1 (covered no camera), 2 (has camera). If either child is 0, node must install camera (return 2, cameras++). If either child has camera, node is covered (return 1). Else return 0.",
        "Time: O(N), Space: O(H)",
        """struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    int cameras = 0;
    // 0: needs cover, 1: covered, 2: has camera
    int dfs(TreeNode* node) {
        if (!node) return 1;
        int l = dfs(node->left);
        int r = dfs(node->right);
        if (l == 0 || r == 0) {
            cameras++;
            return 2;
        }
        if (l == 2 || r == 2) return 1;
        return 0;
    }
public:
    int minCameraCover(TreeNode* root) {
        if (dfs(root) == 0) cameras++;
        return cameras;
    }
};"""
    ))

    p3.append(make_q(
        110, 37, "Meeting Rooms II", "meeting-rooms-ii",
        "Intervals", "Min-Heap / Sweep Line", "Medium", "Earliest Available Room Min-Heap",
        "The canonical meeting room scheduling interview problem.",
        "Minimum conference rooms required for set of meeting intervals.",
        "Sort meetings by start time. Use min-heap of meeting end times. If earliest meeting ends before new one starts, reuse that room.",
        "Sort intervals by start. Min-heap stores end times. For each interval: if heap non-empty and heap.top() <= start, pop(). Push end. Max heap size is answer.",
        "Time: O(N log N), Space: O(N)",
        """#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minMeetingRooms(vector<vector<int>>& intervals) {
        if (intervals.empty()) return 0;
        sort(intervals.begin(), intervals.end());
        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (auto& iv : intervals) {
            if (!minHeap.empty() && minHeap.top() <= iv[0]) {
                minHeap.pop();
            }
            minHeap.push(iv[1]);
        }
        return minHeap.size();
    }
};"""
    ))

    p3.append(make_q(
        111, 37, "Reconstruct Itinerary", "reconstruct-itinerary",
        "Graphs", "Hierholzer's Algorithm", "Hard", "Eulerian Path with Lexicographical Min-Heap",
        "Hierholzer's algorithm for finding Eulerian path in directed multigraph.",
        "Reconstruct itinerary starting at 'JFK' using all tickets exactly once, lexicographically smallest first.",
        "Adjacency list with multiset/priority_queue for lexicographical order. Run post-order DFS; prepend to itinerary.",
        "Map src -> priority_queue<string, vector<string>, greater<string>>. DFS: while adj[u] has destinations, pop top and recurse. Add u to itinerary, reverse at end.",
        "Time: O(E log E), Space: O(V + E)",
        """#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
    unordered_map<string, priority_queue<string, vector<string>, greater<string>>> adj;
    vector<string> route;
    void dfs(const string& airport) {
        while (!adj[airport].empty()) {
            string next = adj[airport].top();
            adj[airport].pop();
            dfs(next);
        }
        route.push_back(airport);
    }
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        for (auto& t : tickets) adj[t[0]].push(t[1]);
        dfs("JFK");
        reverse(route.begin(), route.end());
        return route;
    }
};"""
    ))

    # Day 38: Dynamic Programming + Binary Search
    p3.append(make_q(
        112, 38, "Burst Balloons", "burst-balloons",
        "Dynamic Programming", "Interval DP", "Hard", "Last Burst Balloon Subproblem Separation",
        "Top-level interval DP: thinking backwards about which balloon is burst LAST so subproblems remain independent.",
        "Maximum coins collected by bursting balloons.",
        "If balloon k is burst LAST in range [i..j], the coins gained are nums[i-1] * nums[k] * nums[j+1] + dp[i][k-1] + dp[k+1][j].",
        "Pad array with 1 at both ends. DP table dp[i][j]. Iterate range lengths from 1 to n. For every k between i and j, find max coins.",
        "Time: O(N^3), Space: O(N^2)",
        """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxCoins(vector<int>& nums) {
        int n = nums.size();
        vector<int> b(n + 2, 1);
        for (int i = 0; i < n; i++) b[i + 1] = nums[i];
        vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
        for (int len = 1; len <= n; len++) {
            for (int i = 1; i <= n - len + 1; i++) {
                int j = i + len - 1;
                for (int k = i; k <= j; k++) {
                    dp[i][j] = max(dp[i][j], b[i - 1] * b[k] * b[j + 1] + dp[i][k - 1] + dp[k + 1][j]);
                }
            }
        }
        return dp[1][n];
    }
};"""
    ))

    p3.append(make_q(
        113, 38, "Median of Two Sorted Arrays", "median-of-two-sorted-arrays",
        "Binary Search", "Dual Partitioning", "Hard", "Binary Search on Shorter Array Cut Point",
        "The gold standard binary search interview question testing partition invariants in O(log(min(M, N))).",
        "Median of two sorted arrays in O(log(min(m, n))) time.",
        "Partition both arrays such that left half and right half have equal elements, and maxLeftA <= minRightB && maxLeftB <= minRightA.",
        "Binary search partition cut on smaller array. Compute corresponding cut in larger array. Compare boundary values. Return median based on total length parity.",
        "Time: O(log(min(M, N))), Space: O(1)",
        """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.size(), n = nums2.size();
        int low = 0, high = m;
        while (low <= high) {
            int i = (low + high) / 2;
            int j = (m + n + 1) / 2 - i;
            int maxLeft1 = (i == 0) ? INT_MIN : nums1[i - 1];
            int minRight1 = (i == m) ? INT_MAX : nums1[i];
            int maxLeft2 = (j == 0) ? INT_MIN : nums2[j - 1];
            int minRight2 = (j == n) ? INT_MAX : nums2[j];
            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((m + n) % 2 == 1) return max(maxLeft1, maxLeft2);
                return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0;
            } else if (maxLeft1 > minRight2) {
                high = i - 1;
            } else {
                low = i + 1;
            }
        }
        return 0.0;
    }
};"""
    ))

    p3.append(make_q(
        114, 38, "Minimum Cost For Tickets", "minimum-cost-for-tickets",
        "Dynamic Programming", "Calendar 1D DP", "Medium", "365-Day Calendar Sliding Window DP",
        "Tests practical calendar cost minimization over non-uniform interval passes (1-day, 7-day, 30-day).",
        "Minimum money needed to travel on given calendar travel days.",
        "For non-travel days, dp[i] = dp[i-1]. For travel days, min of 1-day pass dp[i-1]+costs[0], 7-day pass dp[max(0, i-7)]+costs[1], 30-day pass dp[max(0, i-30)]+costs[2].",
        "Keep boolean set of travel days. dp array up to last travel day. Fill 1..lastDay with transition.",
        "Time: O(LastDay) <= O(365) = O(1), Space: O(LastDay)",
        """#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        unordered_set<int> travel(days.begin(), days.end());
        int lastDay = days.back();
        vector<int> dp(lastDay + 1, 0);
        for (int i = 1; i <= lastDay; i++) {
            if (!travel.count(i)) {
                dp[i] = dp[i - 1];
            } else {
                dp[i] = min({
                    dp[i - 1] + costs[0],
                    dp[max(0, i - 7)] + costs[1],
                    dp[max(0, i - 30)] + costs[2]
                });
            }
        }
        return dp[lastDay];
    }
};"""
    ))

    return p3
