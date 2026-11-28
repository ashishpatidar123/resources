# 1171. Shortest Path In Binary Matrix

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1171-shortest-path-in-binary-matrix)

## Problem

<p>Given an <code>n x n</code> binary matrix <code>grid</code>, return <em>the length of the shortest <strong>clear path</strong> in the matrix</em>. If there is no clear path, return <code>-1</code>.</p>

<p>A <strong>clear path</strong> in a binary matrix is a path from the <strong>top-left</strong> cell (i.e., <code>(0, 0)</code>) to the <strong>bottom-right</strong> cell (i.e., <code>(n - 1, n - 1)</code>) such that:</p>

<ul>
	<li>All the visited cells of the path are <code>0</code>.</li>
	<li>All the adjacent cells of the path are <strong>8-directionally</strong> connected (i.e., they are different and they share an edge or a corner).</li>
</ul>

<p>The <strong>length of a clear path</strong> is the number of visited cells of this path.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/02/18/example1_1.png" style="width: 500px; height: 234px;" />
<pre>
<strong>Input:</strong> grid = [[0,1],[1,0]]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/02/18/example2_1.png" style="height: 216px; width: 500px;" />
<pre>
<strong>Input:</strong> grid = [[0,0,0],[1,1,0],[1,1,0]]
<strong>Output:</strong> 4
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> grid = [[1,0,0],[1,1,0],[1,1,0]]
<strong>Output:</strong> -1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == grid.length</code></li>
	<li><code>n == grid[i].length</code></li>
	<li><code>1 &lt;= n &lt;= 100</code></li>
	<li><code>grid[i][j] is 0 or 1</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1171-shortest-path-in-binary-matrix/solution.cpp)

```cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        
        int n = grid.size();

        vector<vector<int>>dist(n, vector<int>(n, -1));

        vector<vector<int>> dirs = {{1,0},{1,-1},{0,1},{0,-1},{1,1},{-1,-1},{-1,0},{-1,1}};

        queue<pair<int,int>>q;

        if(grid[0][0] == 0){
            q.push({0,0});
            dist[0][0] = 1;
        }

        while(!q.empty()){
            auto [r,c] = q.front();
            q.pop();

            if(r == n-1 && c == n-1){
                return dist[n-1][n-1];
            }

            for(int i=0; i<8; i++){
                int nr = r + dirs[i][0];
                int nc = c + dirs[i][1];

                if(nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1 && grid[nr][nc] == 0){
                    
                    // cout<<nr<<" "<<nc<<endl;
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                    // grid[nr][nc] = 1;

                }
            }
        }

        return -1;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
