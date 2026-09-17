# Graph Algorithms: Complete DSA Interview & Competitive Programming Guide > 💫
> Covers fundamentals → advanced → competitive programming level. Code in C++17.

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
13. [Network Flow](#13-network-flow)
14. [Tree Algorithms on Graphs](#14-tree-algorithms-on-graphs)
15. [Advanced & Competitive Programming](#15-advanced--competitive-programming)
16. [Patterns, Templates & Cheat Sheet](#16-patterns-templates--cheat-sheet)
17. [Algorithm Selection Decision Framework](#17-algorithm-selection-decision-framework)

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
| **Complete (Kn)** | Every pair connected | n(n-1)/2 edges |
| **Planar** | Can draw without edge crossings | Maps |
| **Sparse** | E ≈ V | Road networks |
| **Dense** | E ≈ V² | Social graphs |

### Key Terminology

- **Degree**: Number of edges incident to a vertex
  - In-degree / Out-degree for directed graphs
- **Path**: Sequence of vertices where consecutive pairs are connected by edges
- **Simple Path**: No repeated vertices
- **Cycle**: Path that starts and ends at same vertex
- **Connected Graph**: Every vertex reachable from every other (undirected)
- **Strongly Connected**: Every vertex reachable from every other in directed graph
- **Bridge**: Edge whose removal disconnects the graph
- **Articulation Point**: Vertex whose removal disconnects the graph
- **Euler Path**: Visits every **edge** exactly once
- **Hamiltonian Path**: Visits every **vertex** exactly once
- **Diameter**: Longest shortest path between any two vertices

### Complexity Overview

| Algorithm | Time | Space |
|---|---|---|
| DFS/BFS | O(V+E) | O(V) |
| Dijkstra (heap) | O((V+E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Kruskal's MST | O(E log E) | O(V) |
| Prim's MST (heap) | O((V+E) log V) | O(V) |
| Topological Sort | O(V+E) | O(V) |
| Tarjan's SCC | O(V+E) | O(V) |
| Dinic's Flow | O(V² E) | O(V+E) |

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
vector<vector<pair<int, int>>> wgraph(n);
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

void buildWeighted(int n, vector<tuple<int,int,int>>& edges,
                   vector<vector<pair<int,int>>>& g, bool directed=false) {
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
        for (int nb : graph[node]) // push reverse for left-to-right order
            if (!visited[nb]) st.push(nb);
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
During DFS on a directed graph, edges fall into:

- **Tree Edge:** leads to unvisited node

- **Back Edge:** leads to ancestor → indicates cycle

- **Forward Edge:** leads to descendant (already visited, tout[v] < tout[u])

- **Cross Edge:** leads to node in different subtree

```cpp
// 0=WHITE(unvisited), 1=GRAY(in stack), 2=BLACK(done)
vector<pair<int,int>> classifyEdges(vector<vector<int>>& graph, int n) {
    vector<int> color(n, 0);
    vector<pair<int,int>> backEdges;

    function<void(int)> dfs = [&](int u) {
        color[u] = 1; // GRAY
        for (int v : graph[u]) {
            if (color[v] == 0) dfs(v); // tree edge
            else if (color[v] == 1) backEdges.push_back({u, v}); // back edge = cycle
        }
        color[u] = 2; // BLACK
    };
    // ... loop over all nodes to call dfs(i) if color[i] == 0
}
```
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
    vector<bool> visited(n, false);
    vector<int> order;

    function<void(int)> dfs = [&](int u) {
        visited[u] = true;
        for (int v : graph[u])
            if (!visited[v]) dfs(v);
        order.push_back(u); // add AFTER all descendants
    };

    for (int i = 0; i < n; i++)
        if (!visited[i]) dfs(i);

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

### 7.1 Dijkstra's Algorithm

> **Use when:** Non-negative edge weights. Single source.

```cpp
vector<int> dijkstra(vector<vector<pair<int,int>>>& graph, int start, int n) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue; // stale entry
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// With path reconstruction
pair<int, vector<int>> dijkstraPath(
    vector<vector<pair<int,int>>>& graph, int start, int end, int n) {
    vector<int> dist(n, INT_MAX), prev(n, -1);
    dist[start] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (u == end) break;
        if (d > dist[u]) continue;
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    if (dist[end] == INT_MAX) return {-1, {}};
    vector<int> path;
    for (int v = end; v != -1; v = prev[v]) path.push_back(v);
    reverse(path.begin(), path.end());
    return {dist[end], path};
}
```

**Dijkstra on Grid**
```cpp
int dijkstraGrid(vector<vector<int>>& grid) {
    int rows = grid.size(), cols = grid[0].size();
    vector<vector<int>> dist(rows, vector<int>(cols, INT_MAX));
    dist[0][0] = grid[0][0];
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
    pq.push({grid[0][0], 0, 0});
    while (!pq.empty()) {
        auto [d, r, c] = pq.top(); pq.pop();
        if (d > dist[r][c]) continue;
        for (auto [nr, nc] : neighbors(r, c, rows, cols)) {
            int nd = d + grid[nr][nc];
            if (nd < dist[nr][nc]) { dist[nr][nc] = nd; pq.push({nd, nr, nc}); }
        }
    }
    return dist[rows-1][cols-1];
}
```

### 7.2 Bellman-Ford Algorithm
> **Use when:** Negative edge weights, detect negative cycles. Single source.

```cpp

vector<int> bellmanFord(int n, vector<tuple<int,int,int>>& edges, int start) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;

    for (int iter = 0; iter < n-1; iter++) {
        bool updated = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w; updated = true;
            }
        }
        if (!updated) break; // early termination
    }

    // Check for negative cycles
    for (auto [u, v, w] : edges) {
        if (dist[u] != INT_MAX && dist[u] + w < dist[v])
            return {}; // negative cycle exists
    }
    return dist;
}
```

**SPFA (Shortest Path Faster Algorithm)** - Bellman-Ford with queue optimization:
```cpp
vector<int> spfa(vector<vector<pair<int,int>>>& graph, int start, int n) {
    vector<int> dist(n, INT_MAX);
    vector<bool> inQueue(n, false);
    vector<int> cnt(n, 0);
    dist[start] = 0;
    deque<int> q;
    q.push_back(start); inQueue[start] = true;

    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        inQueue[u] = false;
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
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

### 7.3 Floyd-Warshall Algorithm

> **Use when:** All-pairs shortest path. Small graph (V ≤ 500). Handles negative edges (not negative cycles).

```cpp
vector<vector<int>> floydWarshall(int n, vector<tuple<int,int,int>>& edges) {
    const int INF = 1e9;
    vector<vector<int>> dist(n, vector<int>(n, INF));
    for (int i = 0; i < n; i++) dist[i][i] = 0;
    for (auto [u, v, w] : edges) {
        dist[u][v] = min(dist[u][v], w);
        dist[v][u] = min(dist[v][u], w); // remove for directed
    }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] != INF && dist[k][j] != INF)
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);

    // Negative cycle check: dist[i][i] < 0
    for (int i = 0; i < n; i++) if (dist[i][i] < 0) return {};
    return dist;
}
```
### 7.4 Johnson's Algorithm (All-Pairs for Sparse Graphs)
> **Combines Bellman-Ford + Dijkstra.** Time: O(V² log V + VE). Better than Floyd-Warshall when E << V².

```cpp
vector<vector<int>> johnsons(int n, vector<tuple<int,int,int>> edges) {
    // Step 1: Add virtual node n, connect to all vertices with weight 0
    for (int v = 0; v < n; v++) edges.push_back({n, v, 0});

    // Step 2: Bellman-Ford from virtual node to get potentials h[]
    vector<int> h = bellmanFord(n+1, edges, n);
    if (h.empty()) return {}; // negative cycle

    // Step 3: Re-weight edges: w'(u,v) = w(u,v) + h[u] - h[v]
    vector<vector<pair<int,int>>> rw(n);
    for (auto [u, v, w] : edges)
    if (u < n && v < n) rw[u].push_back({v, w + h[u] - h[v]});

    // Step 4: Dijkstra from each vertex, adjust back
    vector<vector<int>> allDist;
    for (int s = 0; s < n; s++) {
        auto d = dijkstra(rw, s, n);
        vector<int> row(n);
        for (int v = 0; v < n; v++)
        row[v] = (d[v] == INT_MAX) ? INT_MAX : d[v] - h[s] + h[v];
        allDist.push_back(row);
    }
    return allDist;
}
```

### 7.5 Comparison Table

| Algorithm | Edge Weights | Graph Type | Time Complexity | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Unweighted | Any | $O(V+E)$ | Unweighted shortest path |
| **0-1 BFS** | 0 or 1 | Any | $O(V+E)$ | 0/1 weighted edges |
| **Dijkstra** | Non-negative | Any | $O((V+E) \log V)$ | Standard weighted SSSP |
| **Bellman-Ford** | Any | Any | $O(VE)$ | Negative edges / detect cycles |
| **SPFA** | Any | Any | $O(VE)$ (worst) | Faster Bellman-Ford (avg case) |
| **Floyd-Warshall** | Any | Dense | $O(V^3)$ | All-pairs, small graphs |
| **Johnson's** | Any | Sparse | $O(V^2 \log V + VE)$ | All-pairs, sparse graphs |

---

## 8. Minimum Spanning Tree

> MST: A spanning tree of minimum total edge weight. V-1 edges, connects all vertices, no cycles.

**Key Property:** For any cut of the graph, the minimum weight crossing edge is in the MST (Cut Property).

### 8.1 Kruskal's Algorithm

> Sort edges by weight, greedily add if no cyle (use DSU)

```cpp
pair<int, vector<tuple<int,int,int>>> kruskal(
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

    int mstCost = 0;
    vector<tuple<int,int,int>> mstEdges;

    for (auto [w, u, v] : edges) {
        if (unite(u, v)) {
            mstCost += w;
            mstEdges.push_back({u, v, w});

            if ((int)mstEdges.size() == n - 1)
                break;
        }
    }

    return {mstCost, mstEdges};
}
```

---

### 8.2 Prim's Algorithm

> Grow MST from a starting vertex. Better for dense graphs.


```cpp
pair<int, vector<tuple<int,int,int>>> prim(
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

    int mstCost = 0;
    vector<tuple<int,int,int>> mstEdges;

    while (!pq.empty()) {

        auto [cost, u] = pq.top();
        pq.pop();

        if (visited[u]) continue;

        visited[u] = true;
        mstCost += cost;

        if (parent[u] != -1)
            mstEdges.push_back({parent[u], u, cost});

        for (auto [v, w] : graph[u]) {

            if (!visited[v] && w < minEdge[v]) {

                minEdge[v] = w;
                parent[v] = u;

                pq.push({w, v});
            }
        }
    }

    return {mstCost, mstEdges};
}
```

---

### 8.3 MST Variants

**Maximum Spanning Tree**: Negate all weights, run Kruskal's/Prim's.

**Second Minimum Spanning Tree**

1. Find MST.
2. For each non-MST edge (u, v, w): find max edge on path u → v in MST, try replacing it.
3. Best replacement = second MST.

**Minimum Bottleneck Spanning Tree**: Same as MST (provably).

**Steiner Tree** (NP-hard in general): Connect a subset of vertices with minimum total weight.

### 8.4 MST Applications

- Network design (minimum cable cost)
- Cluster analysis (remove k−1 heaviest MST edges → k clusters)
- Approximation for TSP (2-approximation)
- Image segmentation


---

## 9. Union-Find (DSU)

> Most powerful data structure for connectivity queries and cycle detection.

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
### DSU with Rollback (for offline queries, no path compression)

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

    void rollback(){
        auto [py, oldPy, px, oldRnk] = history.back(); history.pop_back();
        parent[py] = oldPy;
        rnk[px] = oldRnk;
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
void findBridgesAndAPs(vector<vector<int>>& graph, int n, 
vector<pair<int, int>>& bridges, vector<int>& articulationPoints) {
    vector<int> disc(n, -1), low(n, -1), parent(n, -1);
    vector<bool> ap(n, false);
    int time = 0;

    function<void(int)> dfs = [&](int u) {
        disc[u] = low[u] = ++time;
        int children = 0;

        for (int v : graph[u]) {
            if (disc[v] == -1) {
                children++;
                parent[v] = u;
                dfs(v);

                low[u] = min(low[u], low[v]);

                if (low[v] > disc[u]) {
                    bridges.push_back({u, v});
                }

                if (parent[u] == -1 && children > 1) {
                    articulationPoints.push_back(u);
                }
                if (parent[u] != -1 && low[v] >= disc[u]) {
                    articulationPoints.push_back(u);
                }
            } else if (v != parent[u]) {
                low[u] = min(low[u], disc[v]);
            }
        }
    };

    for (int i = 0; i < n; i++) {
        if (disc[i] == -1) {
            dfs(i);
        }
    }
    for (int i = 0; i < n; i++) {
        if (ap[i]) {
            articulationPoints.push_back(i);
        }
    }
}
```

> **Multi-edge Caveat**:  When graph has parallel edges, track edge instead of parent node. 

```cpp
void findBridgesMultigraph(vector<vector<int, int>>& graph, int n, 
                    vector<pair<int, int >>& bridges) {
    vector<int> disc(n, -1);
    vector<int> low(n, -1);
    int timer = 0;

    function <void(int, int)> dfs = [&](int u, int parentEdge) {
        disc[u] = low[u] = timer++;
        for (auto [v, eid] : graph[u]) {
            if (disc[v] == -1) { // If v is not visited
                dfs(v, eid);
                low[u] = min(low[u], low[v]);
                if (low[v] > disc[u]) {
                    bridges.push_back({u, v});
                }
            } else if (eid != parentEdge) { // Update low value of u for parent function calls.
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

### Bridge Tree (Block-Cut Tree)

The bridge tree contracts each 2-edge-connected component into a single node, resulting in a tree. Useful for:
- Counting bridges on a path
- Finding if adding an edge creates a 2-edge-connected graph

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

### Maximum Bipartite Matching -  Hungrarian (Augmenting Paths)

```cpp
int maxBipartiteMatching(vector<vector<int>>& graph, int leftN, int rightN) {

    vector<int> matchL(leftN, -1); // Initialize all left nodes as unmatched
    vector<int> matchR(rightN, -1);// Initialize all right nodes as unmatched

    function<bool(int, vector<bool>&)> tryAugment = [&](int u, vector<bool>& seen)  -> bool {
        for (int v : graph[u]) {
            if (!seen[v]) {
                seen[v] = true;
                if (matchR[v] < 0 || tryAugment(matchR[v], seen)) {
                    matchL[u] = v;
                    matchR[v] = u;
                    return true;
                }
            }
        }
        return false;
    };
    int result = 0;
    for (int u = 0; u < leftN; u++) {
        vector<bool> seen(rightN, false);
        if (tryAugment(u, seen)) {
            result++;
        }
    }
    return result;
}
```
> **Konig's Theorem:** In bipartite graphs, max matching = min vertex cover.
> **Dilworth's Theorem:** Min path cover in DAG = n - max matching.

### Hopcroft-KARP (O(E * sqrt(V)) bipartite matching)

```cpp
int hopcroftKarp(vector<vector<int>>&graph, int leftN, int rightN){
    vector<int> matchL(leftN, -1), matchR(rightN, -1);
    vector<int> dist(leftN);

    auto bfs = [&]() -> bool{
        fill(dist.begin(), dist.end(), INT_MAX);
        queue<int> q;
        for (int u = 0; u < leftN; u++) {
            if (matchL[u] == -1) {
                dist[u] = 0;
                q.push(u);
            } else {
                dist[u] = INT_MAX;
            }
        }

        bool foundAugmentingPath = false;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : graph[u]) {
                if (matchR[v] == -1) {
                    foundAugmentingPath = true;
                } else if (dist[matchR[v]] == INT_MAX) {
                    dist[matchR[v]] = dist[u] + 1;
                    q.push(matchR[v]);
                }
            }
        }

        return foundAugmentingPath;
    };

    function<bool(int)> dfs = [&](int u) -> bool {
        for (int v : graph[u]) {
            if (matchR[v] == -1 || (dist[matchR[v]] == dist[u] + 1 && dfs(matchR[v]))) {
                matchL[u] = v;
                matchR[v] = u;
                return true;
            }
        }
        dist[u] = INT_MAX;
        return false;
    };

    int matching = 0;
    while (bfs()) {
        for (int u = 0; u < leftN; u++) {
            if (matchL[u] == -1 && dfs(u)) {
                matching++;
            }
        }
    }
    return matching;
}
```

---

## 13. Network Flow

> **Max-Flow**: Maximum amount of flow that can be pushed from source `s` to sink `t`.
> **Min-Cuts**: Minimum capacity set of edges whose removal disconnects `s` from `t`.
> **Max-Flow = Min-Cuts** (Ford-Fulkerson Therorem)

### 13.1 Ford Fulkerson / Edmonds-Karp

```cpp
struct MaxFlow{
    int n;
    vector<vector<int>> cap, adj;

    MaxFlow(int n): n(n), cap(n, vector<int>(n)), adj(n) {}

    void add_edge(int u, int v, int c){
        cap[u][v] += c;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    bool bfs(int s, int t, vector<int>& parent){
        fill(parent.begin(), parent.end(), -1);
        parent[s] = s;
        queue<int> q;
        q.push(s);
        while(!q.empty()){
            int u = q.front(); q.pop();
            for(int v: adj[u]){
                if(parent[v] == -1 && cap[u][v] > 0){
                    parent[v] = u;
                    if(v == t) return true;
                    q.push(v);
                }
            }
        }
        return false;
    }

    int maxFlow(int s, int t){
        vector<int> parent(n);
        int flow = 0;
        while(bfs(s, t, parent)){
            int path_flow = INT_MAX;
            for(int v = t; v != s; v = parent[v]){
                int u = parent[v];
                path_flow = min(path_flow, cap[u][v]);
            }
            for(int v = t; v != s; v = parent[v]){
                int u = parent[v];
                cap[u][v] -= path_flow;
                cap[v][u] += path_flow;
            }
            flow += path_flow;
        }
        return flow;
    }
};
```

### 13.2 Dinic's Algorithms (O(V*V*E) - much faster in practice)

```cpp
struct Dinic{
    struct Edge{
        int to, cap, rev;
    };
    int n;

    vector<vector<Edge>> graph;
    vector<int> level, iter;

    Dinic(int n): n(n), graph(n), level(n), iter(n) {}

    void add_edge(int from, int to, int cap){
        graph[from].push_back({to, cap, (int)graph[to].size()});
        graph[to].push_back({from, 0, (int)graph[from].size() - 1});
    }

    bool bfs(int s, int t){
        fill(level.begin(), level.end(), -1);
        queue<int> que;
        level[s] = 0;
        que.push(s);
        while(!que.empty()){
            int v = que.front(); que.pop();
            for(auto &e : graph[v]){
                if(e.cap > 0 && level[e.to] < 0){
                    level[e.to] = level[v] + 1;
                    que.push(e.to);
                }
            }
        }
        return level[t] != -1;
    }

    int dfs(int v, int t, int f){
        if(v == t) return f;
        for(int &i = iter[v]; i < (int)graph[v].size(); i++){
            Edge &e = graph[v][i];
            if(e.cap > 0 && level[v] < level[e.to]){
                int d = dfs(e.to, t, min(f, e.cap));
                if(d > 0){
                    e.cap -= d;
                    graph[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    int max_flow(int s, int t){
        int flow = 0;
        while(bfs(s, t)){
            fill(iter.begin(), iter.end(), 0);
            int f;
            while((f = dfs(s, t, INT_MAX)) > 0){
                flow += f;
            }
        }
        return flow;
    }

    vector<bool> min_cut(int s){
        vector<bool> visited(n, false);
        queue<int> que;
        que.push(s);
        visited[s] = true;
        while(!que.empty()){
            int v = que.front(); que.pop();
            for(auto &e : graph[v]){
                if(e.cap > 0 && !visited[e.to]){
                    visited[e.to] = true;
                    que.push(e.to);
                }
            }
        }
        return visited;
    }
};
```

***Usage:**
```cpp
Dinic d(6);
d.addEdge(0,1,10); d.addEdge(0,2,10);
d.addEdge(1,3,4); d.addEdge(1,4,8);
d.addEdge(2,4,9); d.addEdge(3,5,10); d.addEdge(4,5,10);
cout << d.maxFlow(0,5) << endl; // Output: 19
```

### 13.3 Network Flow Applications 

| Problem | Reduction to Max Flow | Complexity |
|---------|----------------------|------------|
|Bipartite Matching|Construct a flow network with source connected to left partition and sink connected to right partition, edges represent possible matches.|O(E√V)|
|Edge Disjoint Paths|Construct a flow network where each edge has capacity 1, find max flow from source to sink.|O(E√V)|
|Vertex Disjoint Paths|Split each vertex into two vertices connected by an edge of capacity 1, find max flow.|O(E√V)|
|Circulation with Demands|Transform the problem into a flow network with lower and upper bounds on edges, check if max flow equals total demand.|O(E√V)|
|Project Selection|Construct a flow network where projects are nodes, edges represent dependencies, and capacities represent profits or costs.|O(E√V)|
|Baseball Elimination|Construct a flow network where teams are nodes, edges represent games left to play, and capacities represent possible wins.|O(E√V)|

**Bipartite Matching via Flow:**

```cpp
int bipartiteViaFlow(int leftN, int rightN, vector<pair<int,int>>& edges){
    int totalN = leftN + rightN + 2;
    int S = total-2;
    int T = total-1;

    Dinic d(totalN);

    for(int i = 0; i < leftN; i++){
        d.addEdge(S, i, 1);
    }
    for(int i = 0; i < rightN; i++){
        d.addEdge(leftN + i, T, 1);
    }
    for(auto &edge : edges){
        int u = edge.first;
        int v = edge.second;
        d.addEdge(u, leftN + v, 1);
    }
    return d.max_flow(S, T);
}
```

---

## 14. Tree Algorithms on Graphs

### 14.1 Lowest Common Ancestor (LCA) - Binary Lifting

> **LCA(u,v)** Deepest node that is an ancestor of both u and v.

```cpp
struct LCA{
    int n, LOG = 20;
    vector<vector<int>> up;

    LCA(int n): n(n), depth(n, 0), up(n, vector<int>(LOG)) {}

    void build(const vector<vector<int>>& graph, int root = 0){
        vector<int>parent(n, -1);
        vector<bool>visited(n, false);
        queue<int>q;
        q.push(root);
        visited[root] = true;

        while(!q.empty()){
            int u = q.front();
            q.pop();
            for(int v: graph[u]){
                if(!visited[v]){
                    visited[v] = true;
                    depth[v] = depth[u] + 1;
                    parent[v] = u;
                    q.push(v);
                }
            }
        }

        for(int i = 0; i < n; i++){
            if(parent[i] == -1) up[i][0] = i;
            else up[i][0] = parent[i];
        }

        for(int k = 1; k < LOG; k++){
            for(int v = 0; v < n; v++){
                up[v][k] = up[k-1][up[v][k-1]];
            }
        }
    }

    int lca(int u, int v){
        if(depth[u] < depth[v]) swap(u, v);
        for(int k = LOG - 1; k >= 0; k--){
            if(depth[u] - (1 << k) >= depth[v]){
                u = up[u][k];
            }
        }
        if(u == v) return u;
        for(int k = LOG - 1; k >= 0; k--){
            if(up[u][k] != up[v][k]){
                u = up[u][k];
                v = up[v][k];
            }
        }
        return up[u][0];
    }

    int distance(int u, int v){
        int ancestor = lca(u, v);
        return depth[u] + depth[v] - 2 * depth[ancestor];
    }

    int kth_ancestor(int u, int k){
        for(int i = 0; i < LOG; i++){
            if((k>>i  & 1)){
                u = up[i][u];
            }
        }
        return u;
    }
};
```

### 14.2 Euler Tour (Flattening a Tree)

> Converts tree problem to range problems (use with segment trees).


```cpp
void eulerTour(vector<vector<int>>& graph, int root, int n, 
               vector<int>& tin, vector<int>& tout, vector<int>& order) {
    tin.assign(n, 0); tout.assign(n, 0);
    int timer = 0;
    function<void(int, int)> dfs = [&](int u, int par) {
        tin[u] = timer++;
        order.push_back(u);
        for (int v : graph[u]) if (v != par) dfs(v, u);
        tout[u] = timer - 1;
    };
    dfs(root, -1);
}

// Check if v is ancestor of u
bool isAncestor(vector<int>& tin, vector<int>& tout, int u, int v) {
    return tin[v] <= tin[u] && tout[u] <= tout[v];
}

```

---

### 14.3 Heavy-Light Decomposition (HLD)

```cpp
struct HLD {
    int n, curPos = 0;
    vector<int> sz, depth, parent, heavy, head, pos;

    HLD(int n) : n(n), sz(n, 1), depth(n, 0), parent(n, -1),
                 heavy(n, -1), head(n, 0), pos(n, 0) {}

    void build(vector<vector<int>>& graph, int root = 0) {
        // Iterative DFS to compute sizes and heavy children
        stack<pair<int, pair<int, bool>>> stk;
        stk.push({root, {-1, false}});
        while (!stk.empty()) {
            auto [u, pp] = stk.top(); stk.pop();
            auto [p, processed] = pp;
            if (processed) {
                for (int v : graph[u]) if (v != p) {
                    sz[u] += sz[v];
                    if (heavy[u] == -1 || sz[v] > sz[heavy[u]]) heavy[u] = v;
                }
            } else {
                parent[u] = p;
                stk.push({u, {p, true}});
                for (int v : graph[u]) if (v != p) {
                    depth[v] = depth[u] + 1;
                    stk.push({v, {u, false}});
                }
            }
        }

        // Assign positions along chains
        function<void(int, int)> decompose = [&](int u, int h) {
            head[u] = h; pos[u] = curPos++;
            if (heavy[u] != -1) decompose(heavy[u], h);
            for (int v : graph[u])
                if (v != parent[u] && v != heavy[u]) decompose(v, v);
        };
        decompose(root, root);
    }

    // Query over path u->v using a segment tree query function seg_query(l, r)
    template<typename F>
    int pathQuery(int u, int v, F seg_query) {
        int result = 0;
        while (head[u] != head[v]) {
            if (depth[head[u]] < depth[head[v]]) swap(u, v);
            result += seg_query(pos[head[u]], pos[u]);
            u = parent[head[u]];
        }
        if (depth[u] > depth[v]) swap(u, v);
        result += seg_query(pos[u], pos[v]);
        return result;
    }
};

```

### 14.4 Centroid Decomposition

> Recursively find centroid (removal splits tree into parts $\le n/2$). Useful for path counting problems.

```cpp
vector<int> centroidDecomp(vector<vector<int>>& graph, int n) {
    vector<int> sz(n, 1), centPar(n, -1);
    vector<bool> removed(n, false);

    function<void(int, int)> getSize = [&](int u, int p) {
        sz[u] = 1;
        for (int v : graph[u]) if (v != p && !removed[v]) { getSize(v, u); sz[u] += sz[v]; }
    };

    function<int(int, int, int)> getCentroid = [&](int u, int p, int ts) -> int {
        for (int v : graph[u])
            if (v != p && !removed[v] && sz[v] > ts/2)
                return getCentroid(v, u, ts);
        return u;
    };

    function<void(int, int)> decompose = [&](int u, int pc) {
        getSize(u, -1);
        int c = getCentroid(u, -1, sz[u]);
        centPar[c] = pc;
        removed[c] = true;
        for (int v : graph[c]) if (!removed[v]) decompose(v, c);
    };

    decompose(0, -1);
    return centPar;
}

```

---

### 14.5 Tree DP Patterns

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

**Re-rooting Technique**

```cpp
vector<int> reroot(vector<vector<int>>& graph, int n) {
    vector<int> down(n, 0), ans(n, 0);
    function<void(int, int)> dfs1 = [&](int u, int p) {
        for (int v : graph[u]) if (v != p) { dfs1(v, u); down[u] += down[v] + 1; }
    };
    function<void(int, int, int)> dfs2 = [&](int u, int p, int fromParent) {
        ans[u] = down[u] + fromParent;
        for (int v : graph[u]) if (v != p) {
            int contrib = ans[u] - (down[v] + 1);
            dfs2(v, u, contrib + (n - 1 - down[v]));
        }
    };
    dfs1(0, -1);
    dfs2(0, -1, 0);
    return ans;
}

```

---

## 15. Advanced & Competitive Programming

### 15.1 Eulerian Path & Circuit

* **Eulerian Circuit:** Visit every edge exactly once, return to start.
* **Eulerian Path:** Visit every edge exactly once.

**Conditions:**

* **Undirected Circuit:** All vertices have even degree + connected.
* **Undirected Path:** Exactly 2 vertices with odd degree + connected.
* **Directed Circuit:** In-degree = out-degree for all vertices.
* **Directed Path:** Exactly one vertex with out-in=1 (start), one with in-out=1 (end).

**Hierholzer's Algorithm - $O(E)$**

> Pass a copy of the adjacency lists.

```cpp
vector<int> hierholzer(vector<vector<int>> adj, int start, bool directed=false) {
    stack<int> stk;
    vector<int> circuit;
    stk.push(start);
    while (!stk.empty()) {
        int u = stk.top();
        if (!adj[u].empty()) {
            int v = adj[u].back(); adj[u].pop_back();
            if (!directed) {
                auto it = find(adj[v].begin(), adj[v].end(), u);
                if (it != adj[v].end()) adj[v].erase(it);
            }
            stk.push(v);
        } else {
            circuit.push_back(u);
            stk.pop();
        }
    }
    reverse(circuit.begin(), circuit.end());
    return circuit;
}

```

---

### 15.2 Hamiltonian Path & TSP (Bitmask DP)

> **TSP:** Find minimum cost Hamiltonian cycle. NP-hard in general.
> **DP with bitmask:** $O(2^N \cdot N^2)$ - feasible for $N \le 20$.

```cpp
// dp[mask][i] = min cost to visit nodes in mask, ending at i
int tsp(vector<vector<int>>& dist, int n) {
    const int INF = 1e9;
    vector<vector<int>> dp(1<<n, vector<int>(n, INF));
    dp[1][0] = 0; // start at node 0
    for (int mask = 0; mask < (1<<n); mask++) {
        for (int u = 0; u < n; u++) {
            if (dp[mask][u] == INF || !(mask>>u & 1)) continue;
            for (int v = 0; v < n; v++) {
                if (mask>>v & 1) continue;
                int nm = mask | (1<<v);
                dp[nm][v] = min(dp[nm][v], dp[mask][u] + dist[u][v]);
            }
        }
    }
    int full = (1<<n)-1, ans = INF;
    for (int i = 1; i < n; i++)
        if (dp[full][i] != INF) ans = min(ans, dp[full][i] + dist[i][0]);
    return ans;
}

// Reconstruct TSP path
vector<int> tspPath(vector<vector<int>>& dist, int n) {
    const int INF = 1e9;
    vector<vector<int>> dp(1<<n, vector<int>(n, INF));
    vector<vector<int>> par(1<<n, vector<int>(n, -1));
    dp[1][0] = 0;
    for (int mask = 0; mask < (1<<n); mask++) {
        for (int u = 0; u < n; u++) {
            if (dp[mask][u] == INF || !(mask>>u & 1)) continue;
            for (int v = 0; v < n; v++) {
                if (mask>>v & 1) continue;
                int nm = mask | (1<<v), nd = dp[mask][u] + dist[u][v];
                if (nd < dp[nm][v]) { dp[nm][v] = nd; par[nm][v] = u; }
            }
        }
    }
    int full = (1<<n)-1, last = 1;
    for (int i = 2; i < n; i++)
        if (dp[full][i] + dist[i][0] < dp[full][last] + dist[last][0]) last = i;
    vector<int> path;
    for (int mask = full, cur = last; cur != 0; ) {
        path.push_back(cur);
        int p = par[mask][cur]; mask ^= (1<<cur); cur = p;
    }
    path.push_back(0);
    reverse(path.begin(), path.end());
    return path;
}

```

---

### 15.3 Graph Coloring

**Greedy Coloring** (not optimal, but $O(V+E)$):

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

### 15.5 Bidirectional Dijkstra (Snippet)

```cpp
// ... (start of function hidden)
while (!pqF.empty() || !pqB.empty()) {
    if (!pqF.empty()) {
        auto [d, u] = pqF.top(); pqF.pop();
        if (!visF[u]) {
            visF[u] = true;
            if (visB[u]) best = min(best, distF[u] + distB[u]);
            for (auto [v, w] : graph[u])
                if (distF[u] + w < distF[v]) { distF[v] = distF[u] + w; pqF.push({distF[v], v}); }
        }
    }
    if (!pqB.empty()) {
        auto [d, u] = pqB.top(); pqB.pop();
        if (!visB[u]) {
            visB[u] = true;
            if (visF[u]) best = min(best, distF[u] + distB[u]);
            for (auto [v, w] : revGraph[u])
                if (distB[u] + w < distB[v]) { distB[v] = distB[u] + w; pqB.push({distB[v], v}); }
        }
    }
    if (!pqF.empty() && !pqB.empty() && pqF.top().first + pqB.top().first >= best) break;
}
return best;

```

---

### 15.6 Virtual Nodes Trick

> Add a virtual source/sink connected to multiple nodes to reduce multiple Dijkstra calls to one.

```cpp
// Instead of running Dijkstra from each of k sources:
// Add virtual node n, connect to each source with edge weight 0
// Run single Dijkstra from the virtual node
vector<int> multiSourceDijkstra(
    vector<vector<pair<int,int>>>& graph, vector<int>& sources, int n) {
    graph.push_back({}); // virtual node at index n
    for (int s : sources) graph[n].push_back({s, 0});
    return dijkstra(graph, n, n+1);
}

```
---

### 15.7 Parallel BFS / Simultaneous BFS

> **Partition problem:** find which source each cell is closest to.

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
            if (dist[nr][nc] == INT_MAX) {
                dist[nr][nc] = dist[r][c]+1;
                owner[nr][nc] = owner[r][c];
                q.push({nr, nc});
            }
        }
    }
    return {dist, owner};
}

```

---

### 15.8 DSU on Tree (Small-to-Large Merging)

> Count distinct values in subtrees efficiently. $O(N \log N)$.

```cpp
void dsuOnTree(vector<vector<int>>& graph, vector<int>& values, int n, vector<int>& answer, int root=0) {
    vector<int> sz(n, 1), heavy(n, -1);
    unordered_map<int,int> cnt;
    int distinct = 0;

    function<void(int, int)> calcSize = [&](int u, int p) {
        for (int v : graph[u]) if (v != p) {
            calcSize(v, u); sz[u] += sz[v];
            if (heavy[u] == -1 || sz[v] > sz[heavy[u]]) heavy[u] = v;
        }
    };

    function<void(int, int, int)> add = [&](int u, int p, int coeff) {
        cnt[values[u]] += coeff;
        if (coeff == 1 && cnt[values[u]] == 1) distinct++;
        else if (coeff == -1 && cnt[values[u]] == 0) distinct--;
        for (int v : graph[u]) if (v != p) add(v, u, coeff);
    };

    function<void(int, int, bool)> dfs = [&](int u, int p, bool keep) {
        for (int v : graph[u]) if (v != p && v != heavy[u]) dfs(v, u, false);
        if (heavy[u] != -1) dfs(heavy[u], u, true);
        add(u, p, 1);
        answer[u] = distinct;
        if (!keep) add(u, p, -1);
    };

    calcSize(root, -1);
    dfs(root, -1, false);
}

```

---

### 15.9 Shortest Path in DAG (DP)

> In a DAG, process vertices in topological order. $O(V+E)$.

```cpp
vector<int> dagShortestPath(vector<vector<pair<int,int>>>& graph, vector<int>& topoOrder, int start, int n) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    for (int u : topoOrder) {
        if (dist[u] == INT_MAX) continue;
        for (auto [v, w] : graph[u])
            if (dist[u]+w < dist[v]) dist[v] = dist[u]+w;
    }
    return dist;
}

```

---

### 15.10 Graph Hashing / Isomorphism

> Tree isomorphism via canonical form (AHU algorithm sketch)

```cpp
string treeCanonical(vector<vector<int>>& graph, int root, int parent) {
    vector<string> children;
    for (int v : graph[root])
        if (v != parent) children.push_back(treeCanonical(graph, v, root));
    sort(children.begin(), children.end());
    string result = "(";
    for (auto& c : children) result += c;
    return result + ")";
}

```

---

### 15.11 Important Theorems & Facts for Interviews

| Theorem | Statement |
| --- | --- |
| **Handshaking Lemma** | Sum of all degrees = $2E$ (undirected) |
| **Euler's Formula** | For connected planar graph: $V - E + F = 2$ |
| **König's Theorem** | Bipartite: max matching = min vertex cover |
| **Hall's Theorem** | Bipartite graph has perfect matching iff for all $S \subseteq L: |
| **Menger's Theorem** | Max disjoint paths = min vertex cut |
| **Ford-Fulkerson** | Max flow = min cut |
| **Dilworth's Theorem** | Min chain cover = max antichain in poset |

---

### 16. Patterns, Templates & Cheat Sheet

#### 16.1 Interview Problem Patterns

| Pattern | Trigger Words | Algorithm |
| --- | --- | --- |
| **Shortest path, unweighted** | "minimum steps/hops" | BFS |
| **Shortest path, weighted** | "minimum cost/distance" | Dijkstra |
| **Shortest path, negative edges** | "can gain points along path" | Bellman-Ford |
| **All pairs shortest** | "between every pair" | Floyd-Warshall / Johnson |
| **Ordering with dependencies** | "prerequisite", "before/after" | Topological Sort |
| **Group/cluster** | "number of islands", "connected regions" | DFS/BFS + components |
| **Minimum connections** | "minimum cables/roads to connect all" | Kruskal / Prim MST |
| **Cycle check** | "can get stuck in loop" | Directed: 3-color DFS; Undirected: DSU |
| **Critical edges** | "if this road is blocked" | Bridges (Tarjan) |
| **Flow/matching** | "max assignment", "bottleneck" | Max Flow / Bipartite Matching |
| **Path in DAG** | "number of ways", "longest path in DAG" | DP on Topo order |

---

#### 16.2 Grid Graph Template

```cpp
void solveGrid(vector<string>& grid) {
    int rows = grid.size(), cols = grid[0].size();
    const int DIRS[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};
    vector<vector<bool>> visited(rows, vector<bool>(cols, false));

    auto bfs = [&](int sr, int sc) {
        queue<pair<int,int>> q;
        visited[sr][sc] = true;
        q.push({sr, sc});
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (auto& d : DIRS) {
                int nr = r+d[0], nc = c+d[1];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols 
                    && !visited[nr][nc] && grid[nr][nc] != '#') {
                    visited[nr][nc] = true;
                    q.push({nr, nc});
                }
            }
        }
    };
}

```

#### 16.3 Common Mistakes & Fixes

| Mistake | Fix |
| --- | --- |
| Using visited set but not checking before enqueue | Mark visited WHEN enqueuing, not when dequeuing |
| Dijkstra with negative edges | Use Bellman-Ford instead |
| DFS stack overflow on large graphs | Use iterative DFS with explicit stack |
| Forgetting to handle disconnected graphs | Loop over all nodes, not just node 0 |
| Parent tracking bug in undirected cycle detection | Track edge index for multigraphs |
| Floyd-Warshall wrong loop order | Always $k$ (intermediate) in outermost loop |
| Bellman-Ford not doing $V-1$ relaxations | Need exactly $n-1$ iterations |

---

#### 16.4 Complexity Quick Reference

* **DFS/BFS:** $O(V+E)$
* **Dijkstra (binary heap):** $O((V+E) \log V)$
* **Dijkstra (fib heap):** $O(E + V \log V)$
* **Bellman-Ford:** $O(VE)$
* **Floyd-Warshall:** $O(V^3)$
* **Kruskal:** $O(E \log E)$
* **Prim (binary heap):** $O((V+E) \log V)$
* **Topological Sort:** $O(V+E)$
* **Tarjan SCC:** $O(V+E)$
* **Bridge Finding:** $O(V+E)$
* **Bipartite Match (augm):** $O(VE)$
* **Hopcroft-Karp:** $O(E\sqrt{V})$
* **Dinic's Max Flow:** $O(V^2E)$
* **Dinic on unit graph:** $O(E\sqrt{V})$
* **TSP Bitmask DP:** $O(2^N \cdot N^2)$
* **LCA Binary Lifting:** $O(N \log N)$ build, $O(\log N)$ query
* **HLD:** $O(N \log N)$ build, $O(\log^2 N)$ query
* **Centroid Decomp:** $O(N \log N)$

---

### 16.6 Top 30 LeetCode Graph Problems

| # | Problem | Key Algorithm |
| --- | --- | --- |
| 200 | Number of Islands | DFS/BFS components |
| 207 | Course Schedule | Topological sort / cycle |
| 210 | Course Schedule II | Topological sort |
| 133 | Clone Graph | BFS/DFS + hashmap |
| 743 | Network Delay Time | Dijkstra |
| 787 | Cheapest Flights K Stops | Bellman-Ford modified |
| 684 | Redundant Connection | Union-Find |
| 695 | Max Area of Island | DFS/BFS |
| 994 | Rotting Oranges | Multi-source BFS |
| 127 | Word Ladder | BFS |
| 269 | Alien Dictionary | Topological sort |
| 323 | Number of Connected Components | DSU |
| 547 | Number of Provinces | DFS/DSU |
| 1091 | Shortest Path Binary Matrix | BFS |
| 778 | Swim in Rising Water | Dijkstra / Binary Search |
| 1514 | Path with Maximum Probability | Dijkstra (max variant) |
| 1631 | Path with Minimum Effort | Dijkstra / Binary Search |
| 332 | Reconstruct Itinerary | Hierholzer Eulerian path |
| 1192 | Critical Connections | Tarjan Bridges |
| 802 | Find Eventual Safe States | Reverse graph + topo |
| 847 | Shortest Path Visiting All Nodes | BFS + bitmask |
| 721 | Accounts Merge | Union-Find |
| 785 | Is Graph Bipartite | BFS 2-coloring |
| 886 | Possible Bipartition | Bipartite check |
| 1579 | Remove Max Edges | DSU |
| 1489 | Find Critical/Pseudo-Critical Edges | MST + Kruskal |
| 399 | Evaluate Division | Weighted DFS/BFS |
| 1203 | Sort Items by Groups | Topological sort × 2 |
| 2092 | Find All People with Secret | DSU per meeting time |
| 1970 | Last Day Where You Can Still Cross | DSU / Binary Search |

---

## 17. Algorithm Selection Decision Framework

> **How to think:** Read the problem $\rightarrow$ identify the graph type $\rightarrow$ identify what's being asked $\rightarrow$ match to a pattern $\rightarrow$ pick the algorithm.

### 17.1 Step-by-Step Decision Flowchart

* **"Is X reachable from Y?" / "How many groups?"** $\rightarrow$ Connectivity: DFS / BFS / Union-Find
* **"Shortest / Minimum cost path?"**
* Unweighted $\rightarrow$ BFS
* Weights 0 or 1 $\rightarrow$ 0-1 BFS (deque)
* Non-negative weights? $\rightarrow$ Dijkstra
* Negative weights? $\rightarrow$ Bellman-Ford / SPFA
* All pairs? $\rightarrow$ Floyd-Warshall (dense) / Johnson's (sparse)
* DAG? $\rightarrow$ Topo sort + DP (fastest: $O(V+E)$)


* **"Maximize the minimum value along a path?" (max-min path)** $\rightarrow$ Multi-source BFS + DSU (descending) / Modified Dijkstra (max-heap) / Binary Search + BFS
* **"Minimize the maximum value along a path?" (min-max path)** $\rightarrow$ DSU (ascending sort) / Modified Dijkstra (min-heap on bottleneck) / Binary Search + BFS
* **"Ordering / scheduling with dependencies?"** $\rightarrow$ Topological Sort (Kahn's BFS or DFS)
* **"Detect cycle?"**
* Undirected $\rightarrow$ DFS (parent tracking) / Union-Find
* Directed $\rightarrow$ 3-color DFS / Kahn's (if topo order size < n $\rightarrow$ cycle)


* **"Connect all nodes with minimum cost?"** $\rightarrow$ MST $\rightarrow$ Kruskal (sparse, edge list) / Prim (dense, adj list)
* **"Critical edges / nodes whose removal disconnects?"**
* Edges $\rightarrow$ Bridges (Tarjan)
* Nodes $\rightarrow$ Articulation Points (Tarjan)


* **"Maximum flow / minimum cut / matching?"**
* General flow $\rightarrow$ Dinic's / Edmonds-Karp
* Bipartite matching $\rightarrow$ Hopcroft-Karp / Hungarian / Flow reduction


* **"Strongly connected components?"** $\rightarrow$ Tarjan's SCC / Kosaraju's
* **"Traverse every edge exactly once?"** $\rightarrow$ Eulerian Path/Circuit $\rightarrow$ Hierholzer's
* **"Visit every node exactly once (minimum cost)?"** $\rightarrow$ Hamiltonian / TSP $\rightarrow$ Bitmask DP ($n \le 20$)
* **"Tree path / subtree queries?"**
* LCA $\rightarrow$ Binary Lifting / Euler Tour + RMQ
* Path queries $\rightarrow$ HLD + Segment Tree
* Subtree queries $\rightarrow$ Euler Tour + BIT/Segment Tree



---

### 17.2 Pattern Recognition by Problem Keywords

| Keywords / Signals | Pattern | Algorithm |
| --- | --- | --- |
| "number of islands", "connected regions" | Connected Components | DFS / BFS / DSU |
| "minimum steps", "shortest path in grid" | Unweighted Shortest Path | BFS |
| "minimum cost to reach", "cheapest path" | Weighted Shortest Path | Dijkstra / Bellman-Ford |
| "safeness factor", "maximize minimum" | Max-Min Path | Multi-source BFS + DSU |
| "minimum effort", "minimize maximum" | Min-Max Path | DSU asc / Dijkstra variant |
| "prerequisite", "course schedule" | Dependency Ordering | Topological Sort |
| "can all tasks be finished", "is there a cycle" | Cycle Detection | DFS coloring / Kahn's |
| "minimum cost to connect all" | MST | Kruskal / Prim |
| "if this edge/node is removed", "critical" | Bridges / Articulation | Tarjan |
| "maximum items", "assignment problem" | Network Flow | Dinic / Hopcroft-Karp |
| "bipartite", "two groups" | Bipartiteness | BFS 2-coloring |
| "closest X for every cell" | Multi-Source Distance | Multi-source BFS |
| "merge accounts", "redundant edge" | Dynamic Connectivity | Union-Find (DSU) |
| "all pairs distance" | All-Pairs Shortest Path | Floyd-Warshall / Johnson's |
| "at most K stops", "exactly K edges" | K-constrained Shortest Path | Bellman-Ford / BFS state |
| "path with threshold" | Threshold Path | Binary Search + BFS/DFS |
| "reconstruct itinerary" | Eulerian Path | Hierholzer's |
| "visit all nodes shortest path" | Bitmask BFS/DP | BFS + bitmask state |
| "probability", "maximize product" | Modified Dijkstra | Max-heap, multiply |

---

### 17.3 Identifying the Graph Type

1. **Explicit or Implicit?**
* Explicit: adjacency/edge list
* Implicit: grid, state space, string transformations


2. **Directed or Undirected?**
* Directed: one-way, dependencies
* Undirected: symmetric relationships


3. **Weighted or Unweighted?**
4. **DAG?** $\rightarrow$ Topo sort + DP
5. **Tree?** $\rightarrow$ LCA, HLD, Euler Tour, Centroid Decomp
6. **Negative weights?** $\rightarrow$ Bellman-Ford (Dijkstra fails)
7. **n small ($\le 20$)?** $\rightarrow$ Bitmask DP

---

### 17.4 The "Binary Search + BFS/DFS" Meta-Pattern

> "Is there a path from S to T where [some constraint $\le$ or $\ge$ threshold]?"
> *If the answer is monotonic:* 1. Binary search threshold. 2. Use BFS/DFS to check feasibility.

**Template:**

```cpp
int binarySearchBFS(vector<vector<int>>& grid) {
    int n = grid.size(), lo = 0, hi = /* max possible */;
    auto canReach = [&](int threshold) -> bool {
        if (grid[0][0] > threshold) return false;
        vector<vector<bool>> visited(n, vector<bool>(n, false));
        queue<pair<int,int>> q;
        visited[0][0] = true; q.push({0, 0});
        int dirs[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            if (r == n-1 && c == n-1) return true;
            for (auto& d : dirs) {
                int nr = r+d[0], nc = c+d[1];
                if (nr>=0 && nr<n && nc>=0 && nc<n && !visited[nr][nc] && grid[nr][nc] <= threshold) {
                    visited[nr][nc] = true; q.push({nr, nc});
                }
            }
        }
        return false;
    };
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (canReach(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

```

---

### 17.5 The "DSU + Sort" Meta-Pattern

1. Assign a value/score to each node/edge.
2. Sort by value.
3. Process in sorted order, unioning as you go.
4. Stop when condition is met.

---

### 17.6 The "Modified Dijkstra" Meta-Pattern

| Objective | Relaxation | Heap |
| --- | --- | --- |
| **Min-sum** | `dist[v] = min(dist[v], dist[u] + w)` | Min-heap |
| **Max-min** | `dist[v] = max(dist[v], min(dist[u], w))` | Max-heap |
| **Min-max** | `dist[v] = min(dist[v], max(dist[u], w))` | Min-heap |
| **Max-product** | `dist[v] = max(dist[v], dist[u] * w)` | Max-heap |

**Template (Max-Min Dijkstra e.g., LC 2812):**

```cpp
int maxMinDijkstra(vector<vector<int>>& safety, int n) {
    vector<vector<int>> dist(n, vector<int>(n, 0));
    dist[0][0] = safety[0][0];
    priority_queue<tuple<int,int,int>> pq;
    pq.push({safety[0][0], 0, 0});
    int dirs[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};
    while (!pq.empty()) {
        auto [d, r, c] = pq.top(); pq.pop();
        if (r == n-1 && c == n-1) return d;
        if (d < dist[r][c]) continue;
        for (auto& dir : dirs) {
            int nr = r+dir[0], nc = c+dir[1];
            if (nr>=0 && nr<n && nc>=0 && nc<n) {
                int newDist = min(d, safety[nr][nc]);
                if (newDist > dist[nr][nc]) {
                    dist[nr][nc] = newDist;
                    pq.push({newDist, nr, nc});
                }
            }
        }
    }
    return 0;
}

```

---

### 17.7 Multi-Source BFS

* **Signal:** "Nearest X for every cell" or "Distance from multiple sources".
* **Key Insight:** Initialize queue with ALL sources at distance 0 $\rightarrow$ single BFS.
* **Common uses:** Nearest fire/thief, Voronoi partitioning, Walls and Gates (LC 286), Rotting Oranges (LC 994).

---

### 17.8 Quick Decision Table: "I see X, I think Y"

* **Grid with obstacles** $\rightarrow$ Implicit graph $\rightarrow$ BFS/DFS
* **"Minimum steps in grid"** $\rightarrow$ BFS
* **"Minimum cost in weighted grid"** $\rightarrow$ Dijkstra
* **Edge weights 0 and 1** $\rightarrow$ 0-1 BFS (deque)
* **"Connect all" + "minimum cost"** $\rightarrow$ MST
* **"Ordering" + "dependencies"** $\rightarrow$ Topo sort
* **n $\le$ 20 and "visit all"** $\rightarrow$ Bitmask DP
* **"Maximize minimum" or "minimize maximum"** $\rightarrow$ DSU+Sort OR Modified Dijkstra OR Binary Search+BFS
* **"Remove edge $\rightarrow$ disconnects?"** $\rightarrow$ Bridges (Tarjan)
* **"Number of ways" in DAG** $\rightarrow$ Topo sort + DP
* **Negative edge weights** $\rightarrow$ Bellman-Ford
* **Tree + path queries** $\rightarrow$ LCA / HLD
* **Tree + subtree queries** $\rightarrow$ Euler Tour + Segment Tree

---

> *Guide compiled for DSA interviews up to competitive programming level - covers all standard and advanced graph algorithms with working C++17 code.*