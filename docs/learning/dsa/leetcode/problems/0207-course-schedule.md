# 207. Course Schedule

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0207-course-schedule)

## Problem

# Course Schedule

### Difficulty: Medium
### Topics: Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort, Directed Acyclic Graph

<p>There are a total of <code>numCourses</code> courses you have to take, labeled from <code>0</code> to <code>numCourses - 1</code>. You are given an array <code>prerequisites</code> where <code>prerequisites[i] = [a<sub>i</sub>, b<sub>i</sub>]</code> indicates that you <strong>must</strong> take course <code>b<sub>i</sub></code> first if you want to take course <code>a<sub>i</sub></code>.</p>

<ul>
	<li>For example, the pair <code>[0, 1]</code>, indicates that to take course <code>0</code> you have to first take course <code>1</code>.</li>
</ul>

<p>Return <code>true</code> if you can finish all courses. Otherwise, return <code>false</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> numCourses = 2, prerequisites = [[1,0]]
<strong>Output:</strong> true
<strong>Explanation:</strong> There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> numCourses = 2, prerequisites = [[1,0],[0,1]]
<strong>Output:</strong> false
<strong>Explanation:</strong> There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= numCourses &lt;= 2000</code></li>
	<li><code>0 &lt;= prerequisites.length &lt;= 5000</code></li>
	<li><code>prerequisites[i].length == 2</code></li>
	<li><code>0 &lt;= a<sub>i</sub>, b<sub>i</sub> &lt; numCourses</code></li>
	<li>All the pairs prerequisites[i] are <strong>unique</strong>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0207-course-schedule/solution.cpp)

```cpp
class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        
        vector<vector<int>>adj(numCourses);

        int m = prerequisites.size();

        for(int i=0; i<m; i++){
            int u = prerequisites[i][0];
            int v = prerequisites[i][1];
            if(v==u){
                return false;
            }
            adj[v].push_back(u);
        }
        
        if(m==1 || m==0){
            return true;
        }
        
        queue<int>q;
       
        for(int k=0; k<numCourses; k++){
            vector<int>visited(numCourses,0);
            q.push(k);
            visited[k]=1;
            
            while(!q.empty()){

                int u = q.front();
                q.pop();
                for(auto v:adj[u]){
                    if(visited[v] && v==k){
                        return false;
                    }
                    if(!visited[v]){
                        q.push(v);
                        visited[v]=true;
                    }
                }
            }
        }

        return true;

    }
};
```

### `solution_2163297138.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0207-course-schedule/solution_2163297138.cpp)

```cpp
class Solution {
    bool dfs(int node, vector<vector<int>>& adj, vector<int>& color){
        if(color[node] == 1){
            return true;
        }
        color[node] = 1;
        for(auto v: adj[node]){
            if(color[v] == 1){
                return true;
            }
            else if(color[v] == 0){
                if(dfs(v, adj, color)){
                    return true;
                }
            }
        }
        color[node] = 2;
        return false;
    }
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {

        int n = prerequisites.size();
        vector<vector<int>>adj(numCourses);

        for(int i=0; i<n; i++){
            int first = prerequisites[i][0];
            int second = prerequisites[i][1];

            adj[second].push_back(first);
        }

        vector<int>color(numCourses,0);
        for(int i=0; i<numCourses; i++){
            if(color[i] == 0){
                bool check = dfs(i, adj, color);
                if(check){
                    return false;
                }
            }
        }

        return true;
        
    }
};
```

### `solution_2163311421.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0207-course-schedule/solution_2163311421.cpp)

```cpp
class Solution {
    
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {

        int n = prerequisites.size();
        vector<vector<int>>adj(numCourses);
        vector<int>indegree(numCourses,0);
        for(int i=0; i<n; i++){
            int first = prerequisites[i][0];
            int second = prerequisites[i][1];

            adj[second].push_back(first);
            indegree[first]++;
        }
        queue<int>q;
        for(int i=0; i<numCourses; i++){
            if(indegree[i] == 0){
                q.push(i);
            }
        }

        if(q.empty()){
            return false;
        }
        int count = 0;
        while(!q.empty()){
            int node = q.front();
            q.pop();
            count++;

            for(auto v : adj[node]){
                indegree[v]--;
                if(indegree[v] == 0){
                    q.push(v);
                }
            }
        }
        if(count < numCourses){
            return false;
        }
        return true;
        
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
