# 971. Shortest Bridge

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0971-shortest-bridge)

## Problem

<p>You are given an <code>n x n</code> binary matrix <code>grid</code> where <code>1</code> represents land and <code>0</code> represents water.</p>

<p>An <strong>island</strong> is a 4-directionally connected group of <code>1</code>&#39;s not connected to any other <code>1</code>&#39;s. There are <strong>exactly two islands</strong> in <code>grid</code>.</p>

<p>You may change <code>0</code>&#39;s to <code>1</code>&#39;s to connect the two islands to form <strong>one island</strong>.</p>

<p>Return <em>the smallest number of </em><code>0</code><em>&#39;s you must flip to connect the two islands</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> grid = [[0,1],[1,0]]
<strong>Output:</strong> 1
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> grid = [[0,1,0],[0,0,0],[0,0,1]]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == grid.length == grid[i].length</code></li>
	<li><code>2 &lt;= n &lt;= 100</code></li>
	<li><code>grid[i][j]</code> is either <code>0</code> or <code>1</code>.</li>
	<li>There are exactly two islands in <code>grid</code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0971-shortest-bridge/solution.cpp)

```cpp
class Solution {
public:
    vector<vector<int>>dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    void dfs(int r, int c, int n,vector<vector<int>>& grid,vector<vector<int>>& color,
                vector<vector<bool>>& visited, int& change){
        
        visited[r][c] = true;
        if(color[r][c] == -1){
            color[r][c] = change;
        }
        
        

        

        for(int i=0; i<4; i++){
            int nr = r + dirs[i][0];
            int nc = c + dirs[i][1];

            if(nr>=0 && nr<n && nc>=0 && nc<n && !visited[nr][nc] && grid[nr][nc] == 1){
                dfs(nr, nc, n, grid, color, visited,change);
            }
        }
    }
    int shortestBridge(vector<vector<int>>& grid) {
        
        int n = grid.size();

        vector<vector<int>>color(n, vector<int>(n, -1));

        vector<vector<bool>>visited(n, vector<bool>(n, false));
        int change = 1;
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(grid[i][j] == 1 && !visited[i][j]){
                    dfs(i,j,n,grid,color,visited,change);
                    change = 2;
                    
                }
            }
        }

        queue<pair<int,int>>q;
        
        vector<vector<int>>dist(n, vector<int>(n, -1));
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(color[i][j] == 1){
                    q.push({i,j});
                    visited[i][j] = true;
                    dist[i][j] = 0;
                }
            }
        }
        

        while(!q.empty()){
            auto [r,c] = q.front();
            q.pop();

            

            for(int i=0; i<4; i++){
                int nr = r + dirs[i][0];
                int nc = c + dirs[i][1];
                if(nr>=0 && nr<n && nc>=0 && nc<n && grid[nr][nc] == 1 && color[nr][nc] == 2){
                    return dist[r][c];
                }
                if(nr>=0 && nr<n && nc>=0 && nc<n && !visited[nr][nc] && grid[nr][nc] == 0){
                    visited[nr][nc] = true;
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }

        }

        return -1;


    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
