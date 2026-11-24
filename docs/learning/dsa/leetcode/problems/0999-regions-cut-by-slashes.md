# 999. Regions Cut By Slashes

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0999-regions-cut-by-slashes)

## Problem

# Regions Cut By Slashes

### Difficulty: Medium
### Topics: Array, Hash Table, Depth-First Search, Breadth-First Search, Union-Find, Matrix, Planar Graph

<p>An <code>n x n</code> grid is composed of <code>1 x 1</code> squares where each <code>1 x 1</code> square consists of a <code>&#39;/&#39;</code>, <code>&#39;\&#39;</code>, or blank space <code>&#39; &#39;</code>. These characters divide the square into contiguous regions.</p>

<p>Given the grid <code>grid</code> represented as a string array, return <em>the number of regions</em>.</p>

<p>Note that backslash characters are escaped, so a <code>&#39;\&#39;</code> is represented as <code>&#39;\\&#39;</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/15/1.png" style="width: 200px; height: 200px;" />
<pre>
<strong>Input:</strong> grid = [&quot; /&quot;,&quot;/ &quot;]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/15/2.png" style="width: 200px; height: 198px;" />
<pre>
<strong>Input:</strong> grid = [&quot; /&quot;,&quot;  &quot;]
<strong>Output:</strong> 1
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/15/4.png" style="width: 200px; height: 200px;" />
<pre>
<strong>Input:</strong> grid = [&quot;/\\&quot;,&quot;\\/&quot;]
<strong>Output:</strong> 5
<strong>Explanation: </strong>Recall that because \ characters are escaped, &quot;\\/&quot; refers to \/, and &quot;/\\&quot; refers to /\.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == grid.length == grid[i].length</code></li>
	<li><code>1 &lt;= n &lt;= 30</code></li>
	<li><code>grid[i][j]</code> is either <code>&#39;/&#39;</code>, <code>&#39;\&#39;</code>, or <code>&#39; &#39;</code>.</li>
</ul>

## My C++ Submissions

### `solution_2157429108.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0999-regions-cut-by-slashes/solution_2157429108.cpp)

```cpp
class Solution {
    int index(int n, int i, int j, int num){
        return (n*i + j) * 4 + num;
    }
    int find(vector<int>&parent , int x){
        if(parent[x]== -1){
            return x;
        }
        return parent[x] = find(parent, parent[x]);
    }
    int unite(vector<int>&parent, int x, int y){
        int px = find(parent, x);
        int py = find(parent, y);

        if(px != py){
            parent[px] = py;
            return 1;
        }

        return 0;
    }
public:
    int regionsBySlashes(vector<string>& grid) {

        int n = grid.size();
        
        int total = n*n*4;
        vector<int>parent(total, -1);

        int count = total;

        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(i > 0){
                    int c = unite(parent, index(n,i-1,j,2), index(n, i, j, 0));
                    count -= c;
                }
                if(j > 0){
                    int c = unite(parent, index(n,i,j-1,1), index(n, i, j, 3));
                    count -= c;
                }
                if(grid[i][j] != '/'){
                    int c = unite(parent, index(n, i, j, 0), index(n, i, j, 1));
                    count -= c;
                    c = unite(parent, index(n,i,j,2), index(n, i, j, 3));
                    count -=c;
                }
                if(grid[i][j] != '\\'){
                    int c = unite(parent, index(n, i, j, 0), index(n, i, j, 3));
                    count -= c;
                    c = unite(parent, index(n,i,j,2), index(n, i, j, 1));
                    count -=c;
                }


            }
        }
        return count;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
