# 2038. Nearest Exit From Entrance In Maze

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2038-nearest-exit-from-entrance-in-maze)

## Problem

<p>You are given an <code>m x n</code> matrix <code>maze</code> (<strong>0-indexed</strong>) with empty cells (represented as <code>&#39;.&#39;</code>) and walls (represented as <code>&#39;+&#39;</code>). You are also given the <code>entrance</code> of the maze, where <code>entrance = [entrance<sub>row</sub>, entrance<sub>col</sub>]</code> denotes the row and column of the cell you are initially standing at.</p>

<p>In one step, you can move one cell <strong>up</strong>, <strong>down</strong>, <strong>left</strong>, or <strong>right</strong>. You cannot step into a cell with a wall, and you cannot step outside the maze. Your goal is to find the <strong>nearest exit</strong> from the <code>entrance</code>. An <strong>exit</strong> is defined as an <strong>empty cell</strong> that is at the <strong>border</strong> of the <code>maze</code>. The <code>entrance</code> <strong>does not count</strong> as an exit.</p>

<p>Return <em>the <strong>number of steps</strong> in the shortest path from the </em><code>entrance</code><em> to the nearest exit, or </em><code>-1</code><em> if no such path exists</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/06/04/nearest1-grid.jpg" style="width: 333px; height: 253px;" />
<pre>
<strong>Input:</strong> maze = [[&quot;+&quot;,&quot;+&quot;,&quot;.&quot;,&quot;+&quot;],[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;+&quot;],[&quot;+&quot;,&quot;+&quot;,&quot;+&quot;,&quot;.&quot;]], entrance = [1,2]
<strong>Output:</strong> 1
<strong>Explanation:</strong> There are 3 exits in this maze at [1,0], [0,2], and [2,3].
Initially, you are at the entrance cell [1,2].
- You can reach [1,0] by moving 2 steps left.
- You can reach [0,2] by moving 1 step up.
It is impossible to reach [2,3] from the entrance.
Thus, the nearest exit is [0,2], which is 1 step away.
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/06/04/nearesr2-grid.jpg" style="width: 253px; height: 253px;" />
<pre>
<strong>Input:</strong> maze = [[&quot;+&quot;,&quot;+&quot;,&quot;+&quot;],[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;],[&quot;+&quot;,&quot;+&quot;,&quot;+&quot;]], entrance = [1,0]
<strong>Output:</strong> 2
<strong>Explanation:</strong> There is 1 exit in this maze at [1,2].
[1,0] does not count as an exit since it is the entrance cell.
Initially, you are at the entrance cell [1,0].
- You can reach [1,2] by moving 2 steps right.
Thus, the nearest exit is [1,2], which is 2 steps away.
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/06/04/nearest3-grid.jpg" style="width: 173px; height: 93px;" />
<pre>
<strong>Input:</strong> maze = [[&quot;.&quot;,&quot;+&quot;]], entrance = [0,0]
<strong>Output:</strong> -1
<strong>Explanation:</strong> There are no exits in this maze.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>maze.length == m</code></li>
	<li><code>maze[i].length == n</code></li>
	<li><code>1 &lt;= m, n &lt;= 100</code></li>
	<li><code>maze[i][j]</code> is either <code>&#39;.&#39;</code> or <code>&#39;+&#39;</code>.</li>
	<li><code>entrance.length == 2</code></li>
	<li><code>0 &lt;= entrance<sub>row</sub> &lt; m</code></li>
	<li><code>0 &lt;= entrance<sub>col</sub> &lt; n</code></li>
	<li><code>entrance</code> will always be an empty cell.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2038-nearest-exit-from-entrance-in-maze/solution.cpp)

```cpp
class Solution {
public:
    int nearestExit(vector<vector<char>>& maze, vector<int>& entrance) {

        int m = maze.size();
        int n = maze[0].size();
        vector<vector<int>>dist(m, vector<int>(n, -1));
        vector<vector<int>>dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        int mini = INT_MAX;
        queue<pair<int, int>>q;
        dist[entrance[0]][entrance[1]] = 0;
        q.push({entrance[0], entrance[1]});

        while(!q.empty()){
            auto [r, c] = q.front();
            q.pop();

            for(int i=0; i<4; i++){
                int nr = r + dirs[i][0];
                int nc = c + dirs[i][1];

                if((nr >= 0 && nr < m && nc >=0 && nc < n) && (maze[nr][nc] == '.') && (dist[nr][nc] == -1)){

                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});

                    if(nr == 0 || nr == m-1 && dist[nr][nc] > 0){
                        mini = min(dist[nr][nc], mini);
                    }
                    if(nc == 0 || nc == n-1 && dist[nr][nc] > 0){
                        mini = min(dist[nr][nc], mini);
                    }

                }
            }
        }

        

        // for(int i=0; i<n; i++){
            
        //     if(dist[0][i] > 0){
        //         mini = min(dist[0][i], mini);
        //     }
        //     if(dist[m-1][i] > 0){
        //         mini = min(dist[m-1][i], mini);
        //     }
        // }
        // for(int i=0; i<m; i++){
           
        //     if(dist[i][0] > 0){
        //         mini = min(dist[i][0], mini);
        //     }
        //     if(dist[i][n-1] > 0){
        //         mini = min(dist[i][n-1], mini);
        //     }
        // }
        if(mini == INT_MAX || mini == 0){
            return -1;
        }
        return mini;


        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
