# 1300. Critical Connections In A Network

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/1300-critical-connections-in-a-network)

## Problem

<p>There are <code>n</code> servers numbered from <code>0</code> to <code>n - 1</code> connected by undirected server-to-server <code>connections</code> forming a network where <code>connections[i] = [a<sub>i</sub>, b<sub>i</sub>]</code> represents a connection between servers <code>a<sub>i</sub></code> and <code>b<sub>i</sub></code>. Any server can reach other servers directly or indirectly through the network.</p>

<p>A <em>critical connection</em> is a connection that, if removed, will make some servers unable to reach some other server.</p>

<p>Return all critical connections in the network in any order.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/09/03/1537_ex1_2.png" style="width: 198px; height: 248px;" />
<pre>
<strong>Input:</strong> n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
<strong>Output:</strong> [[1,3]]
<strong>Explanation:</strong> [[3,1]] is also accepted.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> n = 2, connections = [[0,1]]
<strong>Output:</strong> [[0,1]]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= n &lt;= 10<sup>5</sup></code></li>
	<li><code>n - 1 &lt;= connections.length &lt;= 10<sup>5</sup></code></li>
	<li><code>0 &lt;= a<sub>i</sub>, b<sub>i</sub> &lt;= n - 1</code></li>
	<li><code>a<sub>i</sub> != b<sub>i</sub></code></li>
	<li>There are no repeated connections.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/1300-critical-connections-in-a-network/solution.cpp)

```cpp
class Solution {
public:
    int n;
    vector<vector<int>>graph;
    vector<vector<int>>critical;
    vector<bool>visited;
    vector<int>tin, low;
    vector<int>parent;
    int timer;

    void dfs(int node, int p = -1){
        visited[node] = true;
        tin[node] = low[node] = timer++;

        bool parent_skipped = false;

        for(int v : graph[node]){
            if(v == p && !parent_skipped){
                parent_skipped = true;
                continue;
            }
            if(visited[v]){
                low[node] = min(low[node], tin[v]);
            }
            else{
                dfs(v, node);
                low[node] = min(low[node], low[v]);

                if(low[v] > tin[node]){
                    critical.push_back({node, v});
                }
            }
        }
    }
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        
        int l = connections.size();

        graph.resize(n);

        for(int i=0; i<l; i++){
            int u = connections[i][0];
            int v = connections[i][1];

            graph[u].push_back(v);
            graph[v].push_back(u);
        }
        
        visited.assign(n, false);
        tin.assign(n, -1);
        low.assign(n, -1);
        timer = 0;
        for(int i=0; i<n; i++){
            if(!visited[i]){
                dfs(i);
            }
        }
        return critical;

    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
