# Graph Algorithms

---

## Table of Contents

1. [Graph Fundamentals](#1-graph-fundamentals)
2. [Graph Representations](#2-graph-representations)
3. [DFS (Depth-First Search)](#3-dfs-depth-first-search)
4. [BFS (Breadth-First Search)](#4-bfs-breadth-first-search)
5. [Cycle Detection](#5-cycle-detection)
6. [Topological Sort](#6-topological-sort)
7. [Shortest Path Algorithms](#7-shortest-path-algorithms)
8. [Minimum Spanning Tree](#8-minimum-spanning-tree)
9. [Union-Find (DSU)](#9-union-find-dsu)
10. [Connected Components & SCC](#10-connected-components--scc)
11. [Bridges & Articulation Points](#11-bridges--articulation-points)
12. [Bipartite Graphs & Matching](#12-bipartite-graphs--matching)
13. [Patterns, Templates & Cheat Sheet](#16-patterns-templates--cheat-sheet)

---

## 1. Graph Fundamentals

### What is a Graph?
A graph G = (V, E), where 'V' = vertices (nodes) and 'E' = edges (connections).

### Types of Graphs

| Type | Description | Example |
|---|---|---|
| **Undirected** | Edges have no direction | Social network friendships |
| **Directed (Digraph)** | Edges have direction | Twitter follows |
| **Weighted** | Edges have costs | Road distances |
| **Unweighted** | All edges equal | Grid mazes |
| **DAG** | Directed Acyclic Graph | Task dependencies |
| **Tree** | Connected acyclic undirected | File system |
| **Bipartite** | 2-colorable, no odd cycles | Job-applicant matching |
| **Complete ($K_n$)** | Every pair of distinct vertices connected | $n(n-1)/2$ edges for undirected graphs |
| **Planar** | Can draw without edge crossings | Maps |
| **Sparse** | Typically $E = O(V)$ or much smaller than $V^2$ | Road networks |
| **Dense** | Typically $E = \Theta(V^2)$ | Dense communication/network graphs |

### Key Terminology

- **Degree**: Number of edges incident to a vertex
  - In-degree / Out-degree for directed graphs
- **Path**: Sequence of vertices where consecutive pairs are connected by edges
- **Simple Path**: No repeated vertices
- **Cycle**: A closed path with no repeated vertices other than the starting/ending vertex
- **Connected Graph**: Every vertex reachable from every other (undirected)
- **Strongly Connected**: Every vertex reachable from every other in directed graph
- **Bridge**: Edge whose removal increases the number of connected components
- **Articulation Point**: Vertex whose removal increases the number of connected components
- **Euler Path**: Visits every **edge** exactly once
- **Hamiltonian Path**: Visits every **vertex** exactly once
- **Diameter**: Longest shortest path between any two vertices

### Complexity Overview

> Unless stated otherwise, graph storage is not counted in these auxiliary-space figures. Recursive DFS-based algorithms may additionally use O(V) call-stack space.

| Algorithm | Time | Auxiliary Space |
|---|---|---|
| DFS/BFS | O(V+E) | O(V) |
| Dijkstra (binary heap) | O((V+E) log V) | O(V+E) worst case with lazy heap entries |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Kruskal's MST | O(E log E) | O(V) auxiliary; O(E) for the edge input |
| Prim's MST (binary heap) | O(E log V) | O(V+E) including adjacency/heap |
| Topological Sort | O(V+E) | O(V) |
| Tarjan's SCC | O(V+E) | O(V) |
| Bridges / Articulation Points | O(V+E) | O(V) |


---

## 2. Graph Representations

### Adjacency List (preferred for sparse graphs)

```cpp
#include <bits/stdc++.h>
using namespace std;

// Unweighted adjacency list
vector<vector<int>> graph(n);
graph[0].push_back(1);
graph[0].push_back(2);

// Weighted adjacency list: graph[u] = {v, w}
vector<vector<pair<int, long long>>> wgraph(n);
wgraph[0].push_back({1, 5});
wgraph[0].push_back({2, 3});

// Build from edge list
void buildGraph(int n, vector<pair<int,int>>& edges,
                vector<vector<int>>& g, bool directed=false) {
    g.assign(n, {});
    for (auto [u, v] : edges) {
        g[u].push_back(v);
        if (!directed) g[v].push_back(u);
    }
}

void buildWeighted(int n, const vector<tuple<int,int,long long>>& edges,
                   vector<vector<pair<int,long long>>>& g, bool directed=false) {
    g.assign(n, {});
    for (auto [u, v, w] : edges) {
        g[u].push_back({v, w});
        if (!directed) g[v].push_back({u, w});
    }
}
```
### Adjacency Matrix (for dense graphs, Floyd-Warshall)

```cpp
const int INF = 1e9;

vector<vector<int>> buildMatrix(int n, vector<tuple<int,int,int>>& edges,
                               bool directed=false) {
    vector<vector<int>> mat(n, vector<int>(n, INF));
    for (int i = 0; i < n; i++) mat[i][i] = 0;
    for (auto [u, v, w] : edges) {
        mat[u][v] = min(mat[u][v], w);
        if (!directed) mat[v][u] = min(mat[v][u], w);
    }
    return mat;
}
```
### Edge List (for Kruskal's MST)
```cpp
// {weight, u, v} - sort by weight for Kruskal's
vector<tuple<int,int,int>> edges; // {w, u, v}
sort(edges.begin(), edges.end());
```

### Implicit Graph (grid problems)

```cpp
const int DIRS[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};
const int DIRS8[8][2] = {{0,1},{0,-1},{1,0},{-1,0},{1,1},{1,-1},{-1,1},{-1,-1}};

vector<pair<int,int>> neighbors(int r, int c, int rows, int cols) {
    vector<pair<int,int>> res;
    for (auto& d : DIRS) {
        int nr = r+d[0], nc = c+d[1];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols)
            res.push_back({nr, nc});
    }
    return res;
}
```

## 3. DFS (Depth-first Search)

### Core Algorithms

```cpp
// Recursive DFS
void dfsRecursive(vector<vector<int>>& graph, int node, vector<bool>& visited) {
    visited[node] = true;
    for (int nb : graph[node])
        if (!visited[nb])
            dfsRecursive(graph, nb, visited);
}

// Iterative DFS
vector<int> dfsIterative(vector<vector<int>>& graph, int start) {
    int n = graph.size();
    vector<bool> visited(n, false);
    vector<int> order;
    stack<int> st;
    st.push(start);
    while (!st.empty()) {
        int node = st.top(); st.pop();
        if (visited[node]) continue;
        visited[node] = true;
        order.push_back(node);
        // Push in reverse adjacency order if you want the same left-to-right
        // visitation order as recursive DFS on the adjacency list.
        for (auto it = graph[node].rbegin(); it != graph[node].rend(); ++it)
            if (!visited[*it]) st.push(*it);
    }
    return order;
}
```
### DFS with Entry/Exit Times (critical for many algorithms)

```cpp
void dfsTimestamps(vector<vector<int>>& graph, int n,
                   vector<int>& tin, vector<int>& tout) {
    tin.assign(n, -1); tout.assign(n, -1);
    int timer = 0;
    vector<bool> visited(n, false);

    function<void(int)> dfs = [&](int u) {
        visited[u] = true;
        tin[u] = timer++;
        for (int v : graph[u])
            if (!visited[v]) dfs(v);
        tout[u] = timer++;
    };

    for (int i = 0; i < n; i++)
        if (!visited[i]) dfs(i);
}
```
### DFS Tree Edge Classification
During DFS on a **directed graph**, edges fall into four categories:

- **Tree Edge:** leads to an unvisited node.
- **Back Edge:** leads to an ancestor currently on the recursion stack; a back edge implies a directed cycle.
- **Forward Edge:** leads to a proper descendant that has already been discovered.
- **Cross Edge:** connects vertices with no ancestor/descendant relationship (typically different DFS subtrees).

The most common interview use is detecting **back edges** with the three-color technique below. The code intentionally returns back edges rather than pretending to classify every edge.

```cpp
// 0 = WHITE (unvisited), 1 = GRAY (in current DFS stack), 2 = BLACK (finished)
vector<pair<int,int>> findBackEdges(vector<vector<int>>& graph, int n) {
    vector<int> color(n, 0);
    vector<pair<int,int>> backEdges;

    function<void(int)> dfs = [&](int u) {
        color[u] = 1;
        for (int v : graph[u]) {
            if (color[v] == 0) {
                dfs(v);
            } else if (color[v] == 1) {
                backEdges.push_back({u, v});
            }
        }
        color[u] = 2;
    };

    for (int i = 0; i < n; ++i)
        if (color[i] == 0)
            dfs(i);

    return backEdges;
}
```

For full four-way classification, use DFS entry/exit timestamps: an edge `u -> v` is a forward edge when `v` is a descendant of `u`, while a cross edge connects unrelated DFS subtrees.


### Applications of DFS
- Path existence check
- Connected components
- Cycle detection
- Topological sort
- SCC (Kosaraju, Tarjan)
- Bridges and articulation points
- Maze solving
- Flood fill

## 4. BFS (Breadth-First Search)

### Core Algorithm

```cpp
vector<int> bfs(vector<vector<int>>& graph, int start) {
    int n = graph.size();
    vector<bool> visited(n, false);
    vector<int> order;
    queue<int> q;
    visited[start] = true;
    q.push(start);
    while (!q.empty()) {
        int node = q.front(); q.pop();
        order.push_back(node);
        for (int nb : graph[node])
            if (!visited[nb]) { visited[nb] = true; q.push(nb); }
    }
    return order;
}
```

### BFS for Shortest Path (unweighted)

```cpp
pair<int, vector<int>> bfsShortest(vector<vector<int>>& graph, int start, int end) {
    int n = graph.size();
    vector<int> dist(n, -1), parent(n, -1);
    dist[start] = 0;
    queue<int> q;
    q.push(start);
    while (!q.empty()) {
        int node = q.front(); q.pop();
        if (node == end) {
            vector<int> path;
            for (int v = end; v != -1; v = parent[v]) path.push_back(v);
            reverse(path.begin(), path.end());
            return {dist[end], path};
        }
        for (int nb : graph[node])
            if (dist[nb] == -1) {
                dist[nb] = dist[node] + 1;
                parent[nb] = node;
                q.push(nb);
            }
    }
    return {-1, {}}; // unreachable
}
```
### Multi-Source BFS

```cpp
// Start BFS from multiple sources simultaneously
vector<vector<int>> multiSourceBFS(vector<string>& grid,
                                   vector<pair<int,int>>& sources) {
    int rows = grid.size(), cols = grid[0].size();
    vector<vector<int>> dist(rows, vector<int>(cols, -1));
    queue<pair<int,int>> q;
    for (auto [r, c] : sources) { dist[r][c] = 0; q.push({r, c}); }
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (auto [nr, nc] : neighbors(r, c, rows, cols))
            if (dist[nr][nc] == -1 && grid[nr][nc] != '#') {
                dist[nr][nc] = dist[r][c] + 1;
                q.push({nr, nc});
            }
    }
    return dist;
}
```
### BFS Level-by-Level

```cpp
vector<vector<int>> bfsLevels(vector<vector<int>>& graph, int start) {
    int n = graph.size();
    vector<bool> visited(n, false);
    visited[start] = true;
    vector<vector<int>> levels;
    vector<int> current = {start};
    while (!current.empty()) {
        levels.push_back(current);
        vector<int> next;
        for (int node : current) {
            for (int nb : graph[node])
                if (!visited[nb]) { visited[nb] = true; next.push_back(nb); }
        }
        current = next;
    }
    return levels;
}
```

### 0-1 BFS (edges with weight 0 or 1)

```cpp
vector<int> bfs01(vector<vector<pair<int,int>>>& graph, int start, int n) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    deque<int> dq;
    dq.push_back(start);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v); // free edge -> front
                else dq.push_back(v);        // cost-1 -> back
            }
        }
    }
    return dist;
}
```
> **When to use 0-1 BFS?** When edge weights are only 0 or 1. Runs in O(V+E), faster than Dijkstra's O((V+E) log V).

## 5. Cycle Detection

### Undirected Graph - DFS

```cpp
bool hasCycleUndirected(vector<vector<int>>& graph, int n) {
    vector<bool> visited(n, false);
    function<bool(int, int)> dfs = [&](int u, int parent) -> bool {
        visited[u] = true;
        for (int v : graph[u]) {
            if (!visited[v]) { if (dfs(v, u)) return true; }
            else if (v != parent) return true; // back edge -> cycle
        }
        return false;
    };
    for (int i = 0; i < n; i++)
        if (!visited[i] && dfs(i, -1)) return true;
    return false;
}
```
### Undirected Graph - Union-Find (preferred for edge-list input)

```cpp
bool hasCycleUF(int n, vector<pair<int,int>>& edges) {
    vector<int> parent(n);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) -> int {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    };
    for (auto [u, v] : edges) {
        int pu = find(u); int pv = find(v);
        if (pu == pv) return true; // same component -> cycle
        parent[pu] = pv;
    }
    return false;
}
```
### Directed Graph - DFS with 3-Color Marking
```cpp
bool hasCycleDirected(vector<vector<int>>& graph, int n) {
    vector<int> color(n, 0); // 0=white, 1=gray, 2=black
    function<bool(int)> dfs = [&](int u) -> bool {
        color[u] = 1;
        for (int v : graph[u]) {
            if (color[v] == 1) return true; // back edge
            if (color[v] == 0 && dfs(v)) return true;
        }
        color[u] = 2;
        return false;
    };
    for (int i = 0; i < n; i++)
        if (color[i] == 0 && dfs(i)) return true;
    return false;
}
```

### Finding the Actual Cycle

```cpp 
vector<int> findCycle(vector<vector<int>>& graph, int n) {
    vector<int> color(n, 0), parent(n, -1);
    int cycleStart = -1;

    function<void(int)> dfs = [&](int u) {
        if (cycleStart != -1) return;
        color[u] = 1;
        for (int v : graph[u]) {
            if (cycleStart != -1) return;
            if (color[v] == 1) { cycleStart = v; parent[v] = u; return; }
            if (color[v] == 0) { parent[v] = u; dfs(v); }
        }
        color[u] = 2;
    };

    for (int i = 0; i < n && cycleStart == -1; i++)
        if (color[i] == 0) dfs(i);

    if (cycleStart == -1) return {};
    vector<int> cycle;
    for (int v = cycleStart; ; v = parent[v]) {
        cycle.push_back(v);
        if (parent[v] == cycleStart) break;
    }
    cycle.push_back(cycleStart);
    reverse(cycle.begin(), cycle.end());
    return cycle;
}
```

## 6. Topological Sort

> Only valid for **DAGs** (Directed Acyclic Graphs). Produces linear ordering where for every edge u→v, u appears before v.

### Kahn's Algorithm (BFS / In-degree)

```cpp
vector<int> topoSortKahn(vector<vector<int>>& graph, int n) {
    vector<int> inDeg(n, 0);
    for (int u = 0; u < n; u++)
        for (int v : graph[u]) inDeg[v]++;

    queue<int> q;
    for (int i = 0; i < n; i++) if (inDeg[i] == 0) q.push(i);
    vector<int> order;

    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : graph[u])
            if (--inDeg[v] == 0) q.push(v);
    }

    return (int)order.size() == n ? order : vector<int>{}; // empty = cycle
}
```
### DFS-Based Topological Sort

```cpp

vector<int> topoSortDFS(vector<vector<int>>& graph, int n) {
    vector<int> color(n, 0); // 0=WHITE, 1=GRAY, 2=BLACK
    vector<int> order;
    bool hasCycle = false;

    function<void(int)> dfs = [&](int u) {
        color[u] = 1;
        for (int v : graph[u]) {
            if (color[v] == 1) {
                hasCycle = true;
                return;
            }
            if (color[v] == 0) {
                dfs(v);
                if (hasCycle) return;
            }
        }
        color[u] = 2;
        order.push_back(u); // add AFTER all descendants
    };

    for (int i = 0; i < n && !hasCycle; ++i)
        if (color[i] == 0)
            dfs(i);

    if (hasCycle) return {};
    reverse(order.begin(), order.end());
    return order;
}
```

### Classic Interview Problems
**Course Schedule (LeetCode 207/210)**
```cpp
bool canFinish(int n, vector<pair<int,int>>& prereqs) {
    vector<vector<int>> graph(n);
    for (auto [a, b] : prereqs) graph[b].push_back(a);
    return (int)topoSortKahn(graph, n).size() == n;
}

vector<int> findOrder(int n, vector<pair<int,int>>& prereqs) {
    vector<vector<int>> graph(n);
    for (auto [a, b] : prereqs) graph[b].push_back(a);
    return topoSortKahn(graph, n);
}
```

**Alien Dictionary (LeetCode 269)**
```cpp
string alienOrder(vector<string>& words) {
    map<char,set<char>> graph;
    map<char,int> inDeg;
    for (auto& w : words) for (char c : w) inDeg[c] = 0;

    for (int i = 0; i + 1 < (int)words.size(); i++) {
        string& w1 = words[i], &w2 = words[i+1];
        int len = min(w1.size(), w2.size());
        if (w1.size() > w2.size() && w1.substr(0,len) == w2.substr(0,len)) return "";
        for (int j = 0; j < (int)len; j++) {
            if (w1[j] != w2[j]) {
                if (!graph[w1[j]].count(w2[j])) { graph[w1[j]].insert(w2[j]); inDeg[w2[j]]++; }
                break;
            }
        }
    }

    queue<char> q;
    for (auto [c, d] : inDeg) if (d == 0) q.push(c);
    string result;
    while (!q.empty()) {
        char c = q.front(); q.pop();
        result += c;
        for (char nb : graph[c]) if (--inDeg[nb] == 0) q.push(nb);
    }
    return (int)result.size() == (int)inDeg.size() ? result : "";
}
```

## 7. Shortest Path Algorithms

### Dijkstra's Algorithm

> **Use when:** Single-source shortest paths with **non-negative edge weights**.
> For robust reusable code, use `long long` for distances so path sums do not overflow `int`.

```cpp
vector<long long> dijkstra(const vector<vector<pair<int,long long>>>& graph, int start, int n) {
    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    dist[start] = 0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue; // stale entry

        for (auto [v, w] : graph[u]) {
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    return dist;
}

// With path reconstruction
pair<long long, vector<int>> dijkstraPath(
    const vector<vector<pair<int,long long>>>& graph, int start, int end, int n) {
    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    vector<int> prev(n, -1);
    dist[start] = 0;

    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        if (u == end) break; // first non-stale pop is optimal

        for (auto [v, w] : graph[u]) {
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                prev[v] = u;
                pq.push({nd, v});
            }
        }
    }

    if (dist[end] == INF) return {-1, {}};

    vector<int> path;
    for (int v = end; v != -1; v = prev[v]) path.push_back(v);
    reverse(path.begin(), path.end());
    return {dist[end], path};
}
```

**Dijkstra on Grid**
```cpp
long long dijkstraGrid(vector<vector<int>>& grid) {
    int rows = grid.size(), cols = grid[0].size();
    const long long INF = (1LL << 60);
    vector<vector<long long>> dist(rows, vector<long long>(cols, INF));
    dist[0][0] = grid[0][0];

    priority_queue<tuple<long long,int,int>,
                   vector<tuple<long long,int,int>>, greater<>> pq;
    pq.push({dist[0][0], 0, 0});

    while (!pq.empty()) {
        auto [d, r, c] = pq.top(); pq.pop();
        if (d != dist[r][c]) continue;
        for (auto [nr, nc] : neighbors(r, c, rows, cols)) {
            long long nd = d + grid[nr][nc];
            if (nd < dist[nr][nc]) {
                dist[nr][nc] = nd;
                pq.push({nd, nr, nc});
            }
        }
    }
    return dist[rows-1][cols-1];
}
```

### Bellman-Ford Algorithm
> **Use when:** Single-source shortest paths with negative edges; also detects reachable negative cycles.
> Negative cycles make shortest paths undefined for vertices reachable from the cycle.

```cpp

vector<long long> bellmanFord(int n, vector<tuple<int,int,int>>& edges, int start) {
    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    dist[start] = 0;

    for (int iter = 0; iter < n - 1; ++iter) {
        bool updated = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        if (!updated) break; // valid early termination
    }

    // A further relaxation means a reachable negative cycle exists.
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF && dist[u] + w < dist[v])
            return {};
    }
    return dist;
}
```

**SPFA (Shortest Path Faster Algorithm)** - Bellman-Ford with queue optimization:
```cpp
vector<long long> spfa(const vector<vector<pair<int,long long>>>& graph, int start, int n) {
    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    vector<bool> inQueue(n, false);
    vector<int> cnt(n, 0);
    dist[start] = 0;
    deque<int> q;
    q.push_back(start); inQueue[start] = true;

    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        inQueue[u] = false;
        for (auto [v, w] : graph[u]) {
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (!inQueue[v]) {
                    q.push_back(v); inQueue[v] = true;
                    if (++cnt[v] >= n) return {}; // negative cycle
                }
            }
        }
    }
    return dist;
}
```

### Floyd-Warshall Algorithm

> **Use when:** All-pairs shortest path on a relatively small graph. Works for directed or undirected graphs and allows negative edges, but a negative cycle makes shortest paths undefined.

```cpp
vector<vector<long long>> floydWarshall(
    int n,
    const vector<tuple<int,int,int>>& edges,
    bool directed = false) {

    const long long INF = (1LL << 60);
    vector<vector<long long>> dist(n, vector<long long>(n, INF));
    for (int i = 0; i < n; ++i) dist[i][i] = 0;

    for (auto [u, v, w] : edges) {
        dist[u][v] = min(dist[u][v], (long long)w);
        if (!directed)
            dist[v][u] = min(dist[v][u], (long long)w);
    }

    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; ++j) {
                if (dist[k][j] == INF) continue;
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }

    // Negative cycle check: some dist[i][i] < 0.
    for (int i = 0; i < n; ++i)
        if (dist[i][i] < 0)
            return {};

    return dist;
}
```

---

### Comparison Table

| Algorithm | Edge Weights | Graph Type | Time Complexity | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Unweighted | Any | $O(V+E)$ | Unweighted shortest path |
| **0-1 BFS** | 0 or 1 | Any | $O(V+E)$ | 0/1 weighted edges |
| **Dijkstra** | Non-negative | Any | $O((V+E) \log V)$ | Standard weighted SSSP |
| **Bellman-Ford** | Any | Any | $O(VE)$ | Negative edges / detect cycles |
| **SPFA** | Any | Any | $O(VE)$ worst case | Queue-based Bellman-Ford variant; can be fast on some inputs but poor on adversarial graphs |
| **Floyd-Warshall** | Any (no negative-cycle shortest paths) | Any | $O(V^3)$ | All-pairs on smaller graphs |

---

## 8. Minimum Spanning Tree

> MST: A spanning tree of minimum total edge weight. V-1 edges, connects all vertices, no cycles.

**Key Property:** For any cut of the graph, the minimum weight crossing edge is in the MST (Cut Property).

### Kruskal's Algorithm

> Sort edges by weight, greedily add an edge when it does not create a cycle (use DSU).

```cpp
pair<long long, vector<tuple<int,int,int>>> kruskal(
    int n, vector<tuple<int,int,int>> edges) { // {w, u, v}

    sort(edges.begin(), edges.end());

    vector<int> parent(n), rnk(n, 0);
    iota(parent.begin(), parent.end(), 0);

    function<int(int)> find = [&](int x) -> int {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    };

    auto unite = [&](int x, int y) -> bool {
        int px = find(x), py = find(y);
        if (px == py) return false;

        if (rnk[px] < rnk[py]) swap(px, py);
        parent[py] = px;
        if (rnk[px] == rnk[py]) rnk[px]++;

        return true;
    };

    long long mstCost = 0;
    vector<tuple<int,int,int>> mstEdges;

    for (auto [w, u, v] : edges) {
        if (unite(u, v)) {
            mstCost += w;
            mstEdges.push_back({w, u, v}); // keep the documented {w,u,v} convention

            if ((int)mstEdges.size() == n - 1)
                break;
        }
    }

    if ((int)mstEdges.size() != max(0, n - 1)) return {-1, {}}; // graph disconnected
    return {mstCost, mstEdges};
}
```

---

### Prim's Algorithm

> Grow an MST from a starting vertex. This binary-heap + adjacency-list implementation is typically preferred for sparse graphs; the classic O(V²) matrix version is often useful on dense graphs.


```cpp
pair<long long, vector<tuple<int,int,int>>> prim(
    vector<vector<pair<int,int>>>& graph,
    int n,
    int start = 0) {

    vector<bool> visited(n, false);
    vector<int> minEdge(n, INT_MAX), parent(n, -1);

    minEdge[start] = 0;

    priority_queue<
        pair<int,int>,
        vector<pair<int,int>>,
        greater<>
    > pq;

    pq.push({0, start});

    long long mstCost = 0;
    vector<tuple<int,int,int>> mstEdges;

    while (!pq.empty()) {

        auto [cost, u] = pq.top();
        pq.pop();

        if (visited[u]) continue;

        visited[u] = true;
        mstCost += cost;

        if (parent[u] != -1)
            mstEdges.push_back({cost, parent[u], u});

        for (auto [v, w] : graph[u]) {

            if (!visited[v] && w < minEdge[v]) {

                minEdge[v] = w;
                parent[v] = u;

                pq.push({w, v});
            }
        }
    }

    if ((int)mstEdges.size() != max(0, n - 1)) return {-1, {}}; // graph disconnected
    return {mstCost, mstEdges};
}
```

---

### MST Variants

**Maximum Spanning Tree**: Negate all weights, run Kruskal's/Prim's.

**Second Minimum Spanning Tree**

1. Find MST.
2. For each non-MST edge (u, v, w): find max edge on path u → v in MST, try replacing it.
3. Best replacement = second MST.

**Minimum Bottleneck Spanning Tree**: Every MST is a minimum-bottleneck spanning tree, but the reverse is not necessarily true. A bottleneck spanning tree minimizes the maximum edge weight used.

**Steiner Tree** (NP-hard in general): Connect a subset of vertices with minimum total weight.

### MST Applications

- Network design (minimum cable cost)
- Cluster analysis (remove k−1 heaviest MST edges → k clusters)
- Approximation for **metric TSP** (MST-doubling gives a 2-approximation under the triangle inequality)
- Image segmentation


---

## 9. Union-Find (DSU)

> A near-constant-time structure for connectivity, cycle detection, Kruskal, and many offline dynamic-connectivity techniques.

### Full Implementation with All Optimizations

```cpp
struct DSU {

    vector<int> parent, rnk, sz;
    int components;

    DSU(int n)
        : parent(n), rnk(n, 0), sz(n, 1), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {

        int root = x;

        while (parent[root] != root)
            root = parent[root];

        while (parent[x] != root) {
            int next = parent[x];
            parent[x] = root;
            x = next;
        }

        return root;
    }

    bool unite(int x, int y){
        int px = find(x), py = find(y);
        if(px == py) return false;
        if(rnk[px] < rnk[py]) swap(px, py);
        parent[py] = px;
        sz[px] += sz[py];
        if(rnk[px] == rnk[py]) rnk[px]++;
        components--;
        return true;
    }

    bool connected(int x, int y) {return find(x) == find(y); }
    int componentSize(int x) {return sz[find(x)]; }

};
```
### DSU with Rollback (for offline dynamic connectivity, no path compression)

```cpp
struct DSURollback {
    vector<int> parent, rnk;
    vector<tuple<int,int,int,int>> history; // (py, oldParent, px, oldRank)

    DSURollback(int n) : parent(n), rnk(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        while (parent[x] != x) x = parent[x]; // no path compression
        return x;
    }

    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rnk[px] < rnk[py]) swap(px, py);
        history.push_back({py, parent[py], px, rnk[px]});
        parent[py] = px;
        if (rnk[px] == rnk[py]) rnk[px]++;
        return true;
    }

    int snapshot() const {
        return (int)history.size();
    }

    void rollback(int snap) {
        while ((int)history.size() > snap) {
            auto [py, oldPy, px, oldRnk] = history.back();
            history.pop_back();
            parent[py] = oldPy;
            rnk[px] = oldRnk;
        }
    }
};
```

### Weighted DSU (for edge differences/potentials)

```cpp
struct WeightedDSU {
    vector<int> parent;
    vector<long long> weight;   // weight[x] = dist from x to parent

    WeightedDSU(int n) : parent(n), weight(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }

    pair<int, long long> find(int x) {
        if (parent[x] == x)
            return {x, 0};

        auto [root, w] = find(parent[x]);
        parent[x] = root;
        weight[x] += w;

        return {root, weight[x]};
    }

    bool unite(int x, int y, long long w) {   // weight[x] - weight[y] = w
        auto [rx, wx] = find(x);
        auto [ry, wy] = find(y);

        if (rx == ry)
            return wx - wy == w;   // check consistency

        // Attach rx below ry. Union-by-size/rank can be added if desired;
        // here we keep the formula explicit for readability.
        parent[rx] = ry;
        weight[rx] = wy - wx + w;
        return true;
    }
};
```

---

## 10. Connected Components & SCC

### Undirected Connected Components

```cpp
int countComponents(vector<vector<int>>& graph, int n) {

    vector<bool> visited(n, false);
    int count = 0;

    function<void(int)> dfs = [&](int u) {
        visited[u] = true;
        for (int v : graph[u])
            if (!visited[v])
                dfs(v);
    };

    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i);
            count++;
        }
    }

    return count;
}
```

### Strongly Connected Components (SCC) — Directed Graphs

**Kosaraju's Algorithm (two DFS passes)**

```cpp
vector<vector<int>> kosaraju(vector<vector<int>>& graph, int n) {

    // Step 1: DFS on original graph, push by finish time
    vector<bool> visited(n, false);
    vector<int> order;

    function<void(int)> dfs1 = [&](int u) {
        visited[u] = true;
        for (int v : graph[u])
            if (!visited[v])
                dfs1(v);

        order.push_back(u);
    };

    for (int i = 0; i < n; i++)
        if (!visited[i])
            dfs1(i);

    // Step 2: Build reverse graph
    vector<vector<int>> rev(n);

    for (int u = 0; u < n; u++)
        for (int v : graph[u])
            rev[v].push_back(u);

    // Step 3: DFS on reverse graph in reverse finish order
    fill(visited.begin(), visited.end(), false);

    vector<vector<int>> sccs;

    function<void(int, vector<int>&)> dfs2 =
        [&](int u, vector<int>& comp) {
            visited[u] = true;
            comp.push_back(u);

            for (int v : rev[u])
                if (!visited[v])
                    dfs2(v, comp);
        };

    for (int i = n - 1; i >= 0; i--) {
        if (!visited[order[i]]) {
            sccs.push_back({});
            dfs2(order[i], sccs.back());
        }
    }

    return sccs;
}
```

**Tarjan's Algorithm** (single DFS pass — preferred)

```cpp
vector<vector<int>> tarjanSCC(vector<vector<int>>& graph, int n) {

    vector<int> idx(n, -1), low(n, 0);
    vector<bool> onStack(n, false);
    stack<int> st;

    vector<vector<int>> sccs;
    int timer = 0;

    function<void(int)> strongconnect = [&](int v) {

        idx[v] = low[v] = timer++;

        st.push(v);
        onStack[v] = true;

        for (int w : graph[v]) {

            if (idx[w] == -1) {
                strongconnect(w);
                low[v] = min(low[v], low[w]);
            }
            else if (onStack[w]) {
                low[v] = min(low[v], idx[w]);
            }
        }

        if (low[v] == idx[v]) {   // root of SCC

            sccs.push_back({});

            while (true) {

                int w = st.top();
                st.pop();

                onStack[w] = false;
                sccs.back().push_back(w);

                if (w == v)
                    break;
            }
        }
    };  

    for (int v = 0; v < n; v++)
        if (idx[v] == -1)
            strongconnect(v);

    return sccs;
}
```

> **Condensation Graph:** After finding SCCs, build a DAG where each SCC is a node. This DAG can be topologically sorted.

```cpp
pair<vector<vector<int>>, vector<int>> condensation(
    vector<vector<int>>& graph,
    int n) {

    auto sccs = tarjanSCC(graph, n);

    vector<int> compId(n);

    for (int i = 0; i < (int)sccs.size(); i++)
        for (int v : sccs[i])
            compId[v] = i;

    int k = sccs.size();

    vector<set<int>> dagSet(k);

    for (int u = 0; u < n; u++)
        for (int v : graph[u])
            if (compId[u] != compId[v])
                dagSet[compId[u]].insert(compId[v]);

    vector<vector<int>> dag(k);

    for (int i = 0; i < k; i++)
        dag[i].assign(dagSet[i].begin(), dagSet[i].end());

    return {dag, compId};
}
```

---

## 11. Bridges & Articulation Points

> **Bridges:** Edge (u, v) whose removal increases the number of connected components.
> **Articulation Points:** Vertex whose removal increases the number of connected components.

### Tarjan's Bridge & AP Algorithms

```cpp
void findBridgesAndAPs(
    vector<vector<int>>& graph,
    int n,
    vector<pair<int,int>>& bridges,
    vector<int>& articulationPoints) {

    vector<int> disc(n, -1), low(n, -1), parent(n, -1);
    vector<bool> isAP(n, false);
    int timer = 0;

    function<void(int)> dfs = [&](int u) {
        disc[u] = low[u] = ++timer;
        int children = 0;

        for (int v : graph[u]) {
            if (disc[v] == -1) {
                parent[v] = u;
                ++children;
                dfs(v);

                low[u] = min(low[u], low[v]);

                // No back edge from v's subtree can reach u or above.
                if (low[v] > disc[u])
                    bridges.push_back({u, v});

                // Root is an AP only with at least two DFS children.
                if (parent[u] == -1 && children > 1)
                    isAP[u] = true;

                // Non-root u is an AP if a child subtree cannot reach
                // a strict ancestor of u.
                if (parent[u] != -1 && low[v] >= disc[u])
                    isAP[u] = true;
            } else if (v != parent[u]) {
                low[u] = min(low[u], disc[v]);
            }
        }
    };

    for (int u = 0; u < n; ++u)
        if (disc[u] == -1)
            dfs(u);

    for (int u = 0; u < n; ++u)
        if (isAP[u])
            articulationPoints.push_back(u);
}
```

> **Multi-edge Caveat**:  When graph has parallel edges, track edge instead of parent node. 

```cpp
void findBridgesMultigraph(vector<vector<pair<int, int>>>& graph, int n, vector<pair<int, int>>& bridges) {
    vector<int> disc(n, -1);
    vector<int> low(n, -1);
    int timer = 0;
    
    function <void(int, int)> dfs = [&](int u, int parentEdge) {
        disc[u] = low[u] = timer++;
        for (auto [v, eid] : graph[u]) {
            if (disc[v] == -1) { 
                dfs(v, eid);
                low[u] = min(low[u], low[v]);
                if (low[v] > disc[u]) {
                    bridges.push_back({u, v});
                }
            } else if (eid != parentEdge) { 
                low[u] = min(low[u], disc[v]);
            }
        }
    };
    for (int i = 0; i < n; ++i) {
        if (disc[i] == -1) {
            dfs(i, -1);
        }
    }
}
```

---

## 12. Bipartite Graphs & Matching

### Bipartite Check (2-coloring)

```cpp
bool isBipartite(vector<vector<int>>& graph) {
    int n = graph.size();
    vector<int> color(n, -1); // -1 means uncolored

    for (int i = 0; i < n; ++i) {
        if(color[i] != -1) continue; // Skip already colored nodes

        // Not colored yet
        queue<int> q;
        q.push(i);
        color[i] = 0; // Color the first node with color 0

        while (!q.empty()) {
            int node = q.front();
            q.pop();

            for (int neighbor : graph[node]) {
                if (color[neighbor] == -1) { // If the neighbor is not colored
                    color[neighbor] = 1 - color[node]; // Color with opposite color
                    q.push(neighbor);
                } else if (color[neighbor] == color[node]) { // If the neighbor has the same color
                    return false; // Not bipartite
                }
            }
        }
        
    }
    return true; // Graph is bipartite
}
```

---


### Tree DP Patterns

**Tree Diameter**

```cpp
int treeDiameter(vector<vector<int>>& graph, int n) {
    int diameter = 0;
    function<int(int, int)> dfs = [&](int u, int p) -> int {
        int max1 = 0, max2 = 0;
        for (int v : graph[u]) if (v != p) {
            int d = dfs(v, u) + 1;
            if (d > max1) { max2 = max1; max1 = d; } else if (d > max2) max2 = d;
        }
        diameter = max(diameter, max1 + max2);
        return max1;
    };
    dfs(0, -1);
    return diameter;
}

```

**Tree DP - Max Independent Set on Tree**

```cpp
int maxIndependentSet(vector<vector<int>>& graph, int n, int root=0) {
    // dp[u][0] = max when u NOT selected, dp[u][1] = max when u IS selected
    vector<array<int, 2>> dp(n, {0, 1});
    function<void(int, int)> dfs = [&](int u, int p) {
        for (int v : graph[u]) if (v != p) {
            dfs(v, u);
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };
    dfs(root, -1);
    return max(dp[root][0], dp[root][1]);
}

```

---

### Graph Coloring

**Greedy Coloring** (not optimal; with the `set` used below, roughly O((V+E) log V)):

```cpp
pair<vector<int>,int> greedyColoring(vector<vector<int>>& graph, int n) {
    vector<int> color(n, -1);
    for (int u = 0; u < n; u++) {
        set<int> used;
        for (int v : graph[u]) if (color[v] != -1) used.insert(color[v]);
        int c = 0;
        while (used.count(c)) c++;
        color[u] = c;
    }
    return {color, *max_element(color.begin(), color.end()) + 1};
}

```

**Check if k-colorable** (backtracking):

```cpp
bool isKColorable(vector<vector<int>>& graph, int n, int k) {
    vector<int> color(n, 0);
    function<bool(int)> backtrack = [&](int u) -> bool {
        if (u == n) return true;
        for (int c = 1; c <= k; c++) {
            bool ok = true;
            for (int v : graph[u]) if (color[v] == c) { ok = false; break; }
            if (ok) {
                color[u] = c;
                if (backtrack(u + 1)) return true;
                color[u] = 0;
            }
        }
        return false;
    };
    return backtrack(0);
}

```

---

### Virtual Nodes Trick

> Add a virtual source/sink connected to multiple nodes to reduce multiple Dijkstra calls to one.

```cpp
vector<long long> multiSourceDijkstra(
    vector<vector<pair<int,long long>>> graph,
    const vector<int>& sources,
    int n) {

    graph.push_back({}); // virtual node at index n
    for (int s : sources)
        graph[n].push_back({s, 0});

    return dijkstra(graph, n, n + 1);
}
```

---

### Parallel BFS / Simultaneous BFS

> **Partition problem:** find which source each cell is closest to. Ties are broken by source insertion order; add an obstacle check if `#` cells are blocked.

```cpp
pair<vector<vector<int>>, vector<vector<int>>> voronoiBFS(vector<string>& grid, vector<pair<int,int>>& sources) {
    int rows = grid.size(), cols = grid[0].size();
    vector<vector<int>> dist(rows, vector<int>(cols, INT_MAX));
    vector<vector<int>> owner(rows, vector<int>(cols, -1));
    queue<pair<int,int>> q;
    for (int idx = 0; idx < (int)sources.size(); idx++) {
        auto [r, c] = sources[idx];
        dist[r][c] = 0; owner[r][c] = idx; q.push({r, c});
    }
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (auto [nr, nc] : neighbors(r, c, rows, cols)) {
            if (grid[nr][nc] != '#' && dist[nr][nc] == INT_MAX) {
                dist[nr][nc] = dist[r][c] + 1;
                owner[nr][nc] = owner[r][c];
                q.push({nr, nc});
            }
        }
    }
    return {dist, owner};
}

```

---



### Shortest Path in DAG (DP)

> In a DAG, process vertices in topological order. O(V+E). This also works with negative edge weights because a DAG has no cycles.

```cpp
vector<long long> dagShortestPath(
    const vector<vector<pair<int,long long>>>& graph,
    const vector<int>& topoOrder,
    int start,
    int n) {

    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    dist[start] = 0;

    for (int u : topoOrder) {
        if (dist[u] == INF) continue;
        for (auto [v, w] : graph[u])
            dist[v] = min(dist[v], dist[u] + w);
    }
    return dist;
}

```

---

## 16. Problems

| Category | Problem | Platform |
|----------|---------|----------|
| **DFS / BFS** | Pacific Atlantic Water Flow | LeetCode 417 |
| | Walls and Gates | LeetCode 286 |
| | Shortest Path in Grid with Obstacles | LeetCode 1293 |
| | Labyrinth | CSES |
| | Grid - Shortest Path | AtCoder ABC088D |
| | Number of Islands | LeetCode 200 |
| | Clone Graph | LeetCode 133 |
| | Max Area of Island | LeetCode 695 |
| | Rotting Oranges | LeetCode 994 |
| | Word Ladder | LeetCode 127 |
| | Shortest Path Binary Matrix | LeetCode 1091 |
| | Shortest Path Visiting All Nodes | LeetCode 847 |
| | Evaluate Division | LeetCode 399 |
| **Topological Sort** | Parallel Courses | LeetCode 1136 |
| | Longest Path in DAG | GeeksForGeeks |
| | Course Schedule IV | LeetCode 1462 |
| | Game Routes | CSES |
| | Fox and Names | Codeforces 510C |
| | Course Schedule | LeetCode 207 |
| | Course Schedule II | LeetCode 210 |
| | Alien Dictionary | LeetCode 269 |
| | Find Eventual Safe States | LeetCode 802 |
| | Sort Items by Groups | LeetCode 1203 |
| **Shortest Path (Dijkstra / Bellman-Ford)** | Path with Maximum Probability | LeetCode 1514 |
| | Number of Ways to Arrive at Destination | LeetCode 1976 |
| | Find the City With the Smallest Number of Neighbors | LeetCode 1334 |
| | Shortest Routes I | CSES |
| | Dijkstra? | Codeforces 20C |
| | Network Delay Time | LeetCode 743 |
| | Cheapest Flights K Stops | LeetCode 787 |
| | Swim in Rising Water | LeetCode 778 |
| | Path with Minimum Effort | LeetCode 1631 |
| **MST (Kruskal / Prim)** | Min Cost to Connect All Points | LeetCode 1584 |
| | Optimize Water Distribution | LeetCode 1168 |
| | Road Reparation | CSES |
| | Dark Roads | UVa 11631 |
| | MST - Kruskal | AtCoder ABC065D |
| | Find Critical/Pseudo-Critical Edges | LeetCode 1489 |
| **Union-Find / DSU** | Largest Component Size by Common Factor | LeetCode 952 |
| | Satisfiability of Equality Equations | LeetCode 990 |
| | Regions Cut by Slashes | LeetCode 959 |
| | Road Construction | CSES |
| | Roads Not Only in Berland | Codeforces 25D |
| | Redundant Connection | LeetCode 684 |
| | Number of Connected Components | LeetCode 323 |
| | Number of Provinces | LeetCode 547 |
| | Accounts Merge | LeetCode 721 |
| | Remove Max Edges | LeetCode 1579 |
| | Find All People with Secret | LeetCode 2092 |
| | Last Day Where You Can Still Cross | LeetCode 1970 |
| **SCC / Tarjan** | Strongly Connected Components | CSES |
| | Minimum Number of Days to Disconnect Island | LeetCode 1568 |
| | 2-SAT Problem | CSES |
| | Condensation Graph | Codeforces EDU |
| | Kosaraju's SCC | GeeksForGeeks |
| | Critical Connections | LeetCode 1192 |
| **Bipartite / Matching** | Maximum Number of Accepted Invitations | LeetCode 1820 |
| | Is Graph Bipartite | LeetCode 785 |
| | Building Teams | CSES |
| | König's Theorem - Minimum Vertex Cover | CP-Algorithms |
| | MATCHING - Hopcroft-Karp | SPOJ |
| | Possible Bipartition | LeetCode 886 |

---

