# 744. Network Delay Time

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0744-network-delay-time)

## Problem

# Network Delay Time

### Difficulty: Medium
### Topics: Depth-First Search, Breadth-First Search, Graph Theory, Heap (Priority Queue), Shortest Path, Dijkstra's Algorithm

<p>You are given a network of <code>n</code> nodes, labeled from <code>1</code> to <code>n</code>. You are also given <code>times</code>, a list of travel times as directed edges <code>times[i] = (u<sub>i</sub>, v<sub>i</sub>, w<sub>i</sub>)</code>, where <code>u<sub>i</sub></code> is the source node, <code>v<sub>i</sub></code> is the target node, and <code>w<sub>i</sub></code> is the time it takes for a signal to travel from source to target.</p>

<p>We will send a signal from a given node <code>k</code>. Return <em>the <strong>minimum</strong> time it takes for all the</em> <code>n</code> <em>nodes to receive the signal</em>. If it is impossible for all the <code>n</code> nodes to receive the signal, return <code>-1</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/05/23/931_example_1.png" style="width: 217px; height: 239px;" />
<pre>
<strong>Input:</strong> times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> times = [[1,2,1]], n = 2, k = 1
<strong>Output:</strong> 1
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> times = [[1,2,1]], n = 2, k = 2
<strong>Output:</strong> -1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= k &lt;= n &lt;= 100</code></li>
	<li><code>1 &lt;= times.length &lt;= 6000</code></li>
	<li><code>times[i].length == 3</code></li>
	<li><code>1 &lt;= u<sub>i</sub>, v<sub>i</sub> &lt;= n</code></li>
	<li><code>u<sub>i</sub> != v<sub>i</sub></code></li>
	<li><code>0 &lt;= w<sub>i</sub> &lt;= 100</code></li>
	<li>All the pairs <code>(u<sub>i</sub>, v<sub>i</sub>)</code> are <strong>unique</strong>. (i.e., no multiple edges.)</li>
</ul>

## My C++ Submissions

### `solution_2202132395.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0744-network-delay-time/solution_2202132395.cpp)

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {

        int m  = times.size();

        vector<vector<pair<int,long long>>>adj(n+1);

        for(int i=0; i<m; i++){
            int u = times[i][0];
            int v = times[i][1];
            long long w = times[i][2];

            adj[u].push_back({v,w});
        }

        vector<long long>dist(n+1, INT_MAX);
        dist[k] = 0;

        priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
        pq.push({0, k});

        while(!pq.empty()){
            auto [d, u] = pq.top();
            pq.pop();
            
            if(d != dist[u]) continue;

            for(auto [v, w] : adj[u]){
                long long newd = dist[u] + w;

                if(newd < dist[v]){
                    dist[v] = newd;
                    pq.push({dist[v], v});
                }
            }

        }

        long long int ans = -1;

        for(int i=1; i<=n; i++){
            ans = max(ans, dist[i]);
        }
        if(ans == INT_MAX) return -1;
        return ans;


    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
