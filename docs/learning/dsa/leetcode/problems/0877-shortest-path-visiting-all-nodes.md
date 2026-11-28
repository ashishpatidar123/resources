# 877. Shortest Path Visiting All Nodes

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0877-shortest-path-visiting-all-nodes)

## Problem

<p>You have an undirected, connected graph of <code>n</code> nodes labeled from <code>0</code> to <code>n - 1</code>. You are given an array <code>graph</code> where <code>graph[i]</code> is a list of all the nodes connected with node <code>i</code> by an edge.</p>

<p>Return <em>the length of the shortest path that visits every node</em>. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/05/12/shortest1-graph.jpg" style="width: 222px; height: 183px;" />
<pre>
<strong>Input:</strong> graph = [[1,2,3],[0],[0],[0]]
<strong>Output:</strong> 4
<strong>Explanation:</strong> One possible path is [1,0,2,0,3]
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/05/12/shortest2-graph.jpg" style="width: 382px; height: 222px;" />
<pre>
<strong>Input:</strong> graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
<strong>Output:</strong> 4
<strong>Explanation:</strong> One possible path is [0,1,4,2,3]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == graph.length</code></li>
	<li><code>1 &lt;= n &lt;= 12</code></li>
	<li><code>0 &lt;= graph[i].length &lt;&nbsp;n</code></li>
	<li><code>graph[i]</code> does not contain <code>i</code>.</li>
	<li>If <code>graph[a]</code> contains <code>b</code>, then <code>graph[b]</code> contains <code>a</code>.</li>
	<li>The input graph is always connected.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0877-shortest-path-visiting-all-nodes/solution.cpp)

```cpp
class Solution {
public:
    int shortestPathLength(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<vector<bool>>visited(n, vector<bool>(1 << n));
        queue<pair<int, int>>q;
        for(int i=0; i<n; i++){
            q.push({i, 1 << i});
            visited[i][1 << i] = true;
        }
        int dist = 0;
        while(!q.empty()){
            int size = q.size();

            for(int i=0; i<size; i++){
                auto [node, bitmask] = q.front();
                q.pop();

                if(bitmask == ((1 << n) - 1)){
                    return dist;
                }
                for(auto v : graph[node]){
                    int newBitmask = bitmask | (1 << v);
                    if(!visited[v][newBitmask]){
                        q.push({v, newBitmask});
                        visited[v][newBitmask] = true;
                    }
                }
            }
            dist++;
        }
        return -1;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
