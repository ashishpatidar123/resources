# 130. Surrounded Regions

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0130-surrounded-regions)

## Problem

<p>You are given an <code>m x n</code> matrix <code>board</code> containing <strong>letters</strong> <code>&#39;X&#39;</code> and <code>&#39;O&#39;</code>, <strong>capture regions</strong> that are <strong>surrounded</strong>:</p>

<ul>
	<li><strong>Connect</strong>: A cell is connected to adjacent cells horizontally or vertically.</li>
	<li><strong>Region</strong>: To form a region <strong>connect every</strong> <code>&#39;O&#39;</code> cell.</li>
	<li><strong>Surround</strong>: A region is surrounded if none of the <code>&#39;O&#39;</code> cells in that region are on the edge of the board. Such regions are <strong>completely enclosed </strong>by <code>&#39;X&#39;</code> cells.</li>
</ul>

<p>To capture a <strong>surrounded region</strong>, replace all <code>&#39;O&#39;</code>s with <code>&#39;X&#39;</code>s <strong>in-place</strong> within the original board. You do not need to return anything.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">board = [[&quot;X&quot;,&quot;X&quot;,&quot;X&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;O&quot;,&quot;O&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;X&quot;,&quot;O&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;O&quot;,&quot;X&quot;,&quot;X&quot;]]</span></p>

<p><strong>Output:</strong> <span class="example-io">[[&quot;X&quot;,&quot;X&quot;,&quot;X&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;X&quot;,&quot;X&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;X&quot;,&quot;X&quot;,&quot;X&quot;],[&quot;X&quot;,&quot;O&quot;,&quot;X&quot;,&quot;X&quot;]]</span></p>

<p><strong>Explanation:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/02/19/xogrid.jpg" style="width: 367px; height: 158px;" />
<p>In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">board = [[&quot;X&quot;]]</span></p>

<p><strong>Output:</strong> <span class="example-io">[[&quot;X&quot;]]</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>m == board.length</code></li>
	<li><code>n == board[i].length</code></li>
	<li><code>1 &lt;= m, n &lt;= 200</code></li>
	<li><code>board[i][j]</code> is <code>&#39;X&#39;</code> or <code>&#39;O&#39;</code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0130-surrounded-regions/solution.cpp)

```cpp
class Solution {
public:

    vector<pair<int,int>>moves = {{1,0},{0,1},{-1,0},{0,-1}};

    void solve(vector<vector<char>>& board) {
        
        int n = board.size();
        int m = board[0].size();

        vector<vector<bool>>visited(n,vector<bool>(m,false));

        queue<pair<int,int>>q;

        for(int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                if(board[i][j]=='O' && (i==0 || i==n-1 || j==0 || j==m-1)){
                    visited[i][j]=true;
                    q.push({i,j});
                }
            }
        }

        while(!q.empty()){
            
            pair<int,int>temp = q.front();
            q.pop();
            
            int x = temp.first;
            int y = temp.second;

            for(int k=0; k<4; k++){
                int i = x + moves[k].first;
                int j = y + moves[k].second;

                if(i<n && i>=0 && j<m && j>=0 && board[i][j]=='O' && visited[i][j]==false){
                    visited[i][j]=true;
                    q.push({i,j});
                }
            }
                        
        }
        for(int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                if(board[i][j]=='O' && visited[i][j]==false){
                    board[i][j]='X';
                }
            }
        }

    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
