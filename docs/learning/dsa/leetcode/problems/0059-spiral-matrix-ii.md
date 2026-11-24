# 59. Spiral Matrix Ii

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0059-spiral-matrix-ii)

## Problem

<p>Given a positive integer <code>n</code>, generate an <code>n x n</code> <code>matrix</code> filled with elements from <code>1</code> to <code>n<sup>2</sup></code> in spiral order.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/13/spiraln.jpg" style="width: 242px; height: 242px;" />
<pre>
<strong>Input:</strong> n = 3
<strong>Output:</strong> [[1,2,3],[8,9,4],[7,6,5]]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> n = 1
<strong>Output:</strong> [[1]]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 20</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0059-spiral-matrix-ii/solution.cpp)

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>>ans(n,vector<int>(n));
        int count = 1;
        for(int i=0; i<(n+1)/2; i++){
            for(int j=i; j<n-i; j++){
                ans[i][j] = count++;
            }
            for(int j = i+1; j<n-i; j++){
                ans[j][n-i-1] = count++;
            }
            for(int j = n-i-2; j>=i; j--){
                ans[n-i-1][j] = count++;
            }
            for(int j = n-i-2; j>i; j--){
                ans[j][i] = count++;
            }
        }

        return ans;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
