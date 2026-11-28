# 895. Shortest Path To Get All Keys

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0895-shortest-path-to-get-all-keys)

## Problem

<p>You are given an <code>m x n</code> grid <code>grid</code> where:</p>

<ul>
	<li><code>&#39;.&#39;</code> is an empty cell.</li>
	<li><code>&#39;#&#39;</code> is a wall.</li>
	<li><code>&#39;@&#39;</code> is the starting point.</li>
	<li>Lowercase letters represent keys.</li>
	<li>Uppercase letters represent locks.</li>
</ul>

<p>You start at the starting point and one move consists of walking one space in one of the four cardinal directions. You cannot walk outside the grid, or walk into a wall.</p>

<p>If you walk over a key, you can pick it up and you cannot walk over a lock unless you have its corresponding key.</p>

<p>For some <code><font face="monospace">1 &lt;= k &lt;= 6</font></code>, there is exactly one lowercase and one uppercase letter of the first <code>k</code> letters of the English alphabet in the grid. This means that there is exactly one key for each lock, and one lock for each key; and also that the letters used to represent the keys and locks were chosen in the same order as the English alphabet.</p>

<p>Return <em>the lowest number of moves to acquire all keys</em>. If it is impossible, return <code>-1</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/07/23/lc-keys2.jpg" style="width: 404px; height: 245px;" />
<pre>
<strong>Input:</strong> grid = [&quot;@.a..&quot;,&quot;###.#&quot;,&quot;b.A.B&quot;]
<strong>Output:</strong> 8
<strong>Explanation:</strong> Note that the goal is to obtain all the keys not to open all the locks.
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/07/23/lc-key2.jpg" style="width: 404px; height: 245px;" />
<pre>
<strong>Input:</strong> grid = [&quot;@..aA&quot;,&quot;..B#.&quot;,&quot;....b&quot;]
<strong>Output:</strong> 6
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/07/23/lc-keys3.jpg" style="width: 244px; height: 85px;" />
<pre>
<strong>Input:</strong> grid = [&quot;@Aa&quot;]
<strong>Output:</strong> -1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>m == grid.length</code></li>
	<li><code>n == grid[i].length</code></li>
	<li><code>1 &lt;= m, n &lt;= 30</code></li>
	<li><code>grid[i][j]</code> is either an English letter, <code>&#39;.&#39;</code>, <code>&#39;#&#39;</code>, or <code>&#39;@&#39;</code>.&nbsp;</li>
	<li>There is exactly one&nbsp;<code>&#39;@&#39;</code>&nbsp;in the grid.</li>
	<li>The number of keys in the grid is in the range <code>[1, 6]</code>.</li>
	<li>Each key in the grid is <strong>unique</strong>.</li>
	<li>Each key in the grid has a matching lock.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0895-shortest-path-to-get-all-keys/solution.cpp)

```cpp
class Solution {

public:
    int shortestPathAllKeys(vector<string>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        int startx = 0;
        int starty = 0;
        int keys = 0;
        for(int i=0; i<m; i++){
            for(int j=0; j<n; j++){
                if(grid[i][j] == '@'){
                    startx = i;
                    starty = j;
                }
                if(grid[i][j] >= 'a' && grid[i][j] <= 'f'){
                    keys++;
                }
            }
        }
        vector<vector<vector<bool>>> visited(m, vector<vector<bool>>(n, vector<bool>(1 << keys)));
        visited[startx][starty][0] = true;
        queue<pair<pair<int,int>, int>> q;
        q.push({{startx, starty}, 0});
        int moves = 0;
        vector<vector<int>> dirs = {{1,0},{0,1},{-1,0},{0,-1}};
        while(!q.empty()){
            
            int size = q.size();
            for(int i=0; i<size; i++){
                pair<pair<int,int>, int> p = q.front();
                q.pop();
                int r = p.first.first;
                int c = p.first.second;
                int state = p.second;
                if(state == (1 << keys) - 1){
                    return moves;
                }
                for(int j=0; j<4; j++){
                    int nr = r + dirs[j][0];
                    int nc = c + dirs[j][1];
                    if(nr >= m || nr < 0 || nc >= n || nc < 0 || grid[nr][nc] == '#'){
                        continue;
                    }
                    if((grid[nr][nc] >= 'A' && grid[nr][nc] <= 'F') && (((state >> (grid[nr][nc] - 'A')) & 1) == 0)){
                        continue;
                    }
                    else{
                        int newState = state;
                        if(grid[nr][nc] >= 'a' && grid[nr][nc] <= 'f'){
                            newState = newState | (1 << (grid[nr][nc] - 'a'));
                        }
                        if(!visited[nr][nc][newState]){
                            visited[nr][nc][newState] = true;
                            q.push({{nr, nc}, newState});
                        }
                    }
                }
            }
            moves++;
        }
        return -1;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
