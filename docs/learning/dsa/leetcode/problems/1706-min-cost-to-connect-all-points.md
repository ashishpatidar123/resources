# 1706. Min Cost To Connect All Points

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1706-min-cost-to-connect-all-points)

## Problem

<p>You are given an array <code>points</code> representing integer coordinates of some points on a 2D-plane, where <code>points[i] = [x<sub>i</sub>, y<sub>i</sub>]</code>.</p>

<p>The cost of connecting two points <code>[x<sub>i</sub>, y<sub>i</sub>]</code> and <code>[x<sub>j</sub>, y<sub>j</sub>]</code> is the <strong>manhattan distance</strong> between them: <code>|x<sub>i</sub> - x<sub>j</sub>| + |y<sub>i</sub> - y<sub>j</sub>|</code>, where <code>|val|</code> denotes the absolute value of <code>val</code>.</p>

<p>Return <em>the minimum cost to make all points connected.</em> All points are connected if there is <strong>exactly one</strong> simple path between any two points.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/08/26/d.png" style="width: 214px; height: 268px;" />
<pre>
<strong>Input:</strong> points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
<strong>Output:</strong> 20
<strong>Explanation:</strong> 
<img alt="" src="https://assets.leetcode.com/uploads/2020/08/26/c.png" style="width: 214px; height: 268px;" />
We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> points = [[3,12],[-2,5],[-4,1]]
<strong>Output:</strong> 18
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= points.length &lt;= 1000</code></li>
	<li><code>-10<sup>6</sup> &lt;= x<sub>i</sub>, y<sub>i</sub> &lt;= 10<sup>6</sup></code></li>
	<li>All pairs <code>(x<sub>i</sub>, y<sub>i</sub>)</code> are distinct.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1706-min-cost-to-connect-all-points/solution.cpp)

```cpp
class Solution {

    static bool compare(vector<int>&a, vector<int>&b){
        return a[2]<b[2];
    }
    int find(int node, vector<int>&parent){
        if(parent[node]==node){
            return node;
        }
        return parent[node]=find(parent[node],parent);
    }
    
    void Union(int u, int v, vector<int>&parent, vector<int>&rank){
        u = find(u,parent);
        v = find(v,parent);
        if(u==v){
            return;
        }
        if(rank[u]<rank[v]){
            parent[u]=v;
        }
        else if(rank[u]>rank[v]){
            parent[v]=u;
        }
        else{
            parent[v]=u;
            rank[u]++;
        }
    }
    int distance(int x1, int y1, int x2, int y2){
        return abs(x1-x2) + abs(y1-y2);
    }

public:
    int minCostConnectPoints(vector<vector<int>>& p) {
        // using kruskal's algorithm
        int v = p.size();
        vector<int>parent(v);
        vector<int>rank(v);
        for(int i=0; i<v; i++){
            rank[i]=0;
            parent[i]=i;
        }
        // sinces edges are not there 
        // so first we create edges
        vector<vector<int>> edges;
        for(int i=0; i<v; i++){
            for(int j=i+1; j<v; j++){
                vector<int> temp(3);
                temp[0] = i;
                temp[1] = j;
                temp[2] = distance(p[i][0],p[i][1],p[j][0],p[j][1]);
                edges.push_back(temp);

            }
        }
        int minWeight = 0;
        sort(edges.begin(),edges.end(),compare);
        for(int i=0; i<edges.size(); i++){
            int u = find(edges[i][0],parent);
            int v = find(edges[i][1],parent);
            int weight = edges[i][2];
            if(u==v){
                continue;
            }
            if(u!=v){
                Union(u,v,parent,rank);
                minWeight+=weight;
            }
        }
        return minWeight;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
