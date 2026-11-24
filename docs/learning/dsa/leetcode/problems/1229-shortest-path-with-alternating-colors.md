# 1229. Shortest Path With Alternating Colors

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1229-shortest-path-with-alternating-colors)

## Problem

<p>You are given an integer <code>n</code>, the number of nodes in a directed graph where the nodes are labeled from <code>0</code> to <code>n - 1</code>. Each edge is red or blue in this graph, and there could be self-edges and parallel edges.</p>

<p>You are given two arrays <code>redEdges</code> and <code>blueEdges</code> where:</p>

<ul>
	<li><code>redEdges[i] = [a<sub>i</sub>, b<sub>i</sub>]</code> indicates that there is a directed red edge from node <code>a<sub>i</sub></code> to node <code>b<sub>i</sub></code> in the graph, and</li>
	<li><code>blueEdges[j] = [u<sub>j</sub>, v<sub>j</sub>]</code> indicates that there is a directed blue edge from node <code>u<sub>j</sub></code> to node <code>v<sub>j</sub></code> in the graph.</li>
</ul>

<p>Return an array <code>answer</code> of length <code>n</code>, where each <code>answer[x]</code> is the length of the shortest path from node <code>0</code> to node <code>x</code> such that the edge colors alternate along the path, or <code>-1</code> if such a path does not exist.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> n = 3, redEdges = [[0,1],[1,2]], blueEdges = []
<strong>Output:</strong> [0,1,-1]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]
<strong>Output:</strong> [0,1,-1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 100</code></li>
	<li><code>0 &lt;= redEdges.length,&nbsp;blueEdges.length &lt;= 400</code></li>
	<li><code>redEdges[i].length == blueEdges[j].length == 2</code></li>
	<li><code>0 &lt;= a<sub>i</sub>, b<sub>i</sub>, u<sub>j</sub>, v<sub>j</sub> &lt; n</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1229-shortest-path-with-alternating-colors/solution.cpp)

```cpp
class Solution {
public:
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        
        queue<pair<int,pair<int, int>>>q;
        vector<vector<int>> dist(n, vector<int>(2, INT_MAX));
        dist[0][0] = 0; // i=0 j=0 is red
        dist[0][1] = 0; //  i=0 j=1 is blue

        q.push({0,{0, 0}});
        q.push({0,{1, 0}});

        // 0 means red, 1 means blue

        while(!q.empty()){
            auto [node, t] = q.front();
            q.pop();
            int color = t.first;
            int d = t.second;
            if(color == 0){
                int l = blueEdges.size();
                for(int i=0; i<l; i++){
                    int u = blueEdges[i][0];
                    int v = blueEdges[i][1];
                    if(u == node){
                        if(d != INT_MAX && dist[v][1] > d + 1){
                            dist[v][1] = d + 1;
                            q.push({v, {1, dist[v][1]}});
                        }
                    }
                }
            }
            if(color == 1){
                int l = redEdges.size();
                for(int i=0; i<l; i++){
                    int u = redEdges[i][0];
                    int v = redEdges[i][1];
                    if(u == node){
                        if(d != INT_MAX && dist[v][0] > d + 1){
                            dist[v][0] = d + 1;
                            q.push({v, {0, dist[v][0]}});
                        }
                    }
                }
            }
        }
        
        vector<int>answer(n, -1);

        for(int i=0; i<n; i++){
            if(dist[i][0] != INT_MAX){
                answer[i] = (min(dist[i][0], dist[i][1]));
            }
            else if(dist[i][1] != INT_MAX){
                answer[i] = (min(dist[i][0], dist[i][1]));
            }
            else{
                answer[i] = -1;
            }
        }

        return answer;

    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
