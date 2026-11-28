# 1032. Satisfiability Of Equality Equations

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1032-satisfiability-of-equality-equations)

## Problem

# Satisfiability of Equality Equations

### Difficulty: Medium
### Topics: Array, String, Union-Find, Graph Theory

<p>You are given an array of strings <code>equations</code> that represent relationships between variables where each string <code>equations[i]</code> is of length <code>4</code> and takes one of two different forms: <code>&quot;x<sub>i</sub>==y<sub>i</sub>&quot;</code> or <code>&quot;x<sub>i</sub>!=y<sub>i</sub>&quot;</code>.Here, <code>x<sub>i</sub></code> and <code>y<sub>i</sub></code> are lowercase letters (not necessarily different) that represent one-letter variable names.</p>

<p>Return <code>true</code><em> if it is possible to assign integers to variable names so as to satisfy all the given equations, or </em><code>false</code><em> otherwise</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> equations = [&quot;a==b&quot;,&quot;b!=a&quot;]
<strong>Output:</strong> false
<strong>Explanation:</strong> If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
There is no way to assign the variables to satisfy both equations.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> equations = [&quot;b==a&quot;,&quot;a==b&quot;]
<strong>Output:</strong> true
<strong>Explanation:</strong> We could assign a = 1 and b = 1 to satisfy both equations.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= equations.length &lt;= 500</code></li>
	<li><code>equations[i].length == 4</code></li>
	<li><code>equations[i][0]</code> is a lowercase letter.</li>
	<li><code>equations[i][1]</code> is either <code>&#39;=&#39;</code> or <code>&#39;!&#39;</code>.</li>
	<li><code>equations[i][2]</code> is <code>&#39;=&#39;</code>.</li>
	<li><code>equations[i][3]</code> is a lowercase letter.</li>
</ul>

## My C++ Submissions

### `solution_2152435269.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1032-satisfiability-of-equality-equations/solution_2152435269.cpp)

```cpp
class Solution {
    vector<int> parent;
    vector<int> rank;

    int find(int x){
        // move up in the tree to reach the root node, because root node has parent equal to itself
        // also while doing this map each node to root only
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);
        // if both belongs to same set then no unite
        if(px == py) return;
        // check the height of the trees, we will add the smaller to larger one
        if(rank[px] < rank[py]){
            swap(px, py);
        }
        // now make the parent of smaller tree as large tree
        parent[py] = px;
        // if their current ranks are same then on addition rank (height increases by 1)
        if(rank[px] == rank[py]){
            rank[px]++;
        }
    }
public:
    bool equationsPossible(vector<string>& equations) {

        int n = equations.size();
        unordered_map<char, int>index;

        int id = 0;
        for(int i=0; i<n; i++){
            if(index.find(equations[i][0]) == index.end()){
                index[equations[i][0]] = id;
                id++;
            }
            if(index.find(equations[i][3]) == index.end()){
                index[equations[i][3]] = id;
                id++;
            }
        }
        parent.resize(id);
        for(int i=0; i<id; i++){
            parent[i] = i;
        }
        rank.resize(id, 0); // rank array - height of the tree

        for(int i=0; i<n; i++){
            char x = equations[i][0];
            char y = equations[i][3];
            string sign = equations[i].substr(1, 2);

            if(sign == "=="){
                unite(index[x], index[y]);
            }
        }

        bool check = true;
        for(int i=0; i<n; i++){
            char x = equations[i][0];
            char y = equations[i][3];
            string sign = equations[i].substr(1, 2);

            if(sign == "!="){
                int px = find(index[x]);
                int py = find(index[y]);

                if(px == py){
                    return false; 
                }
            }
        }
        return true;
        
        
    }
};
```

### `solution_2152437381.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1032-satisfiability-of-equality-equations/solution_2152437381.cpp)

```cpp
class Solution {
    vector<int> parent;
    vector<int> rank;

    int find(int x){
        // move up in the tree to reach the root node, because root node has parent equal to itself
        // also while doing this map each node to root only
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);
        // if both belongs to same set then no unite
        if(px == py) return;
        // check the height of the trees, we will add the smaller to larger one
        if(rank[px] < rank[py]){
            swap(px, py);
        }
        // now make the parent of smaller tree as large tree
        parent[py] = px;
        // if their current ranks are same then on addition rank (height increases by 1)
        if(rank[px] == rank[py]){
            rank[px]++;
        }
    }
public:
    bool equationsPossible(vector<string>& equations) {

        int n = equations.size();
        
        parent.resize(26);
        for(int i=0; i<26; i++){
            parent[i] = i;
        }
        rank.assign(26, 0); // rank array - height of the tree

        for(int i=0; i<n; i++){
            char x = equations[i][0];
            char y = equations[i][3];
            char sign = equations[i][1];

            if(sign == '='){
                unite(x - 'a', y - 'a');
            }
        }

        
        for(int i=0; i<n; i++){
            char x = equations[i][0];
            char y = equations[i][3];
            char sign = equations[i][1];

            if(sign == '!'){
                int px = find(x - 'a');
                int py = find(y - 'a');

                if(px == py){
                    return false; 
                }
            }
        }
        return true;
        
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
