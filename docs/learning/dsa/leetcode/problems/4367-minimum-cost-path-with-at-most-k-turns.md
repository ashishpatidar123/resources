# 4367. Minimum Cost Path With At Most K Turns

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/4367-minimum-cost-path-with-at-most-k-turns)

## Problem

# Minimum Cost Path With At Most K Turns

### Difficulty: Hard
### Topics: 

<p>You are given a 2D integer array <code>grid</code> of size <code>m x n</code>, where <code>grid[i][j]</code> represents the cost of visiting cell <code>(i, j)</code>, and an integer <code>k</code>.</p>

<p>You start at the <strong>top-left</strong> cell <code>(0, 0)</code> and want to reach the <strong>bottom-right</strong> cell <code>(m - 1, n - 1)</code>.</p>

<p>From each cell, you may move one step in any of the four directions: <strong>up</strong>, <strong>down</strong>, <strong>left</strong>, or <strong>right</strong>.</p>

<p>The cost of a path is the sum of the values of all visited cells, <strong>including</strong> the starting and ending cells. If a cell is visited more than once, its value is included each time it is visited.</p>

<p>Return the <strong>minimum</strong> possible path cost to reach <code>(m - 1, n - 1)</code> using <strong>at most</strong> <code>k</code> turns. If no such path exists, return <code>-1</code>.</p>

<p>A <strong>turn</strong> occurs when the direction changes between two consecutive moves. For example, moving right and then down counts as one turn, while moving right and then right does not.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">grid = [[2,7,3],[1,4,5]], k = 1</span></p>

<p><strong>Output:</strong> <span class="example-io">12</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>An optimal path is <code>(0, 0) &rarr; (1, 0) &rarr; (1, 1) &rarr; (1, 2)</code>. The moves are down, right, right.</li>
	<li>The direction changes from down to right once, so the path uses exactly <code>k = 1</code> turn.</li>
	<li>The total path cost is <code>2 + 1 + 4 + 5 = 12</code>.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">grid = [[4,1,9],[3,2,5],[4,8,6]], k = 2</span></p>

<p><strong>Output:</strong> <span class="example-io">20</span></p>

<p><strong>Explanation:</strong>​​​​​​​</p>

<ul>
	<li>An optimal path is <code>(0, 0) &rarr; (1, 0) &rarr; (1, 1) &rarr; (1, 2) &rarr; (2, 2)</code>. The moves are down, right, right, down.</li>
	<li>The direction changes from down to right and from right to down, so the path uses exactly <code>k = 2</code> turns.</li>
	<li>The total path cost is <code>4 + 3 + 2 + 5 + 6 = 20</code>.</li>
</ul>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">grid = [[1,9],[3,4]], k = 0</span></p>

<p><strong>Output:</strong> <span class="example-io">-1</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>It is impossible to reach <code>(1, 1)</code> using <code>k = 0</code> turns. Thus, the answer is -1.</li>
</ul>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= m == grid.length &lt;= 75</code></li>
	<li><code>1 &lt;= n == grid[i].length &lt;= 75</code></li>
	<li><code>0 &lt;= grid[i][j] &lt;= 1000</code></li>
	<li><code>0 &lt;= k &lt; min(m, n)</code></li>
</ul>

## My C++ Submissions

### `solution_2142865852.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/4367-minimum-cost-path-with-at-most-k-turns/solution_2142865852.cpp)

```cpp
class Solution {
public:
    struct State {
        int cost;
        int r;
        int c;
        int dir;
        int turns;
        
        bool operator>(const State& other) const{
            return cost > other.cost;
        }
    };
    int minCost(vector<vector<int>>& grid, int k) {
        int m = grid.size();
        int n = grid[0].size();

        if(m == 1 && n == 1){
            return grid[0][0];
        }

        int dist[75][75][4][76];

        for(int i=0; i<75; i++){
            for(int j=0; j<75; j++){
                for(int d=0; d<4; d++){
                    for(int t=0; t<75; t++){
                        dist[i][j][d][t] = INT_MAX;
                    }
                }
            }
        }

        priority_queue<State, vector<State>, greater<State>> pq;

        int dr[] = {-1, 0, 1, 0};
        int dc[] = {0, 1, 0, -1};

        if(n > 1){
            pq.push({grid[0][0] + grid[0][1], 0, 1, 1, 0});
            dist[0][1][1][0] = grid[0][0] + grid[0][1];
        }

        if(m > 1){
            pq.push({grid[0][0] + grid[1][0], 1, 0, 2, 0});
            dist[1][0][2][0] = grid[0][0] + grid[1][0];
        }

        while(!pq.empty()){
            State curr = pq.top();
            pq.pop();

            if(curr.r == m-1 && curr.c == n-1){
                return curr.cost;
            }

            if(curr.cost > dist[curr.r][curr.c][curr.dir][curr.turns]){
                continue;
            }

            for(int d=0; d<4; d++){
                int nr = curr.r + dr[d];
                int nc = curr.c + dc[d];

                if(nr >=0 && nr < m && nc >= 0 && nc < n){
                    int nturns = curr.turns + (d != curr.dir ? 1 : 0);

                    if(nturns <= k){
                        int ncost = curr.cost + grid[nr][nc];

                        if(ncost < dist[nr][nc][d][nturns]){
                            dist[nr][nc][d][nturns] = ncost;

                            pq.push({ncost, nr, nc, d, nturns});
                        }
                    }
                }
            }
        }
        return -1;

    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
