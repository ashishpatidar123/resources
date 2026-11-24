# 547. Number Of Provinces

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0547-number-of-provinces)

## Problem

<p>There are <code>n</code> cities. Some of them are connected, while some are not. If city <code>a</code> is connected directly with city <code>b</code>, and city <code>b</code> is connected directly with city <code>c</code>, then city <code>a</code> is connected indirectly with city <code>c</code>.</p>

<p>A <strong>province</strong> is a group of directly or indirectly connected cities and no other cities outside of the group.</p>

<p>You are given an <code>n x n</code> matrix <code>isConnected</code> where <code>isConnected[i][j] = 1</code> if the <code>i<sup>th</sup></code> city and the <code>j<sup>th</sup></code> city are directly connected, and <code>isConnected[i][j] = 0</code> otherwise.</p>

<p>Return <em>the total number of <strong>provinces</strong></em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/12/24/graph1.jpg" style="width: 222px; height: 142px;" />
<pre>
<strong>Input:</strong> isConnected = [[1,1,0],[1,1,0],[0,0,1]]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/12/24/graph2.jpg" style="width: 222px; height: 142px;" />
<pre>
<strong>Input:</strong> isConnected = [[1,0,0],[0,1,0],[0,0,1]]
<strong>Output:</strong> 3
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 200</code></li>
	<li><code>n == isConnected.length</code></li>
	<li><code>n == isConnected[i].length</code></li>
	<li><code>isConnected[i][j]</code> is <code>1</code> or <code>0</code>.</li>
	<li><code>isConnected[i][i] == 1</code></li>
	<li><code>isConnected[i][j] == isConnected[j][i]</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0547-number-of-provinces/solution.cpp)

```cpp
class Solution {
public:
    void dfs(int node, vector<bool>&visited, vector<vector<int>>& graph){
        visited[node] = true;

        for(auto v : graph[node]){
            if(!visited[v]){
                dfs(v, visited, graph);
            }
        }

        return;
    }
    int findCircleNum(vector<vector<int>>& isConnected) {
        
        int n = isConnected.size();

        vector<vector<int>>graph(n);
        vector<bool>visited(n, false);
        int count = 0;


        for(int i=0; i<n; i++){
            for(int j=i; j<n; j++){
                int u = i;
                int v = j;

                if(isConnected[i][j] == 1){
                    graph[u].push_back(v);
                    graph[v].push_back(u);
                }
            }
        }

        for(int u=0; u<n; u++){
            if(!visited[u]){
                dfs(u, visited, graph);
                count++;
            }
        }

        return count;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
