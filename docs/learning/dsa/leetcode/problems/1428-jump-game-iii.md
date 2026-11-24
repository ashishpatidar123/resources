# 1428. Jump Game Iii

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1428-jump-game-iii)

## Problem

<p>Given an array of non-negative integers <code>arr</code>, you are initially positioned at <code>start</code>&nbsp;index of the array. When you are at index <code>i</code>, you can jump&nbsp;to <code>i + arr[i]</code> or <code>i - arr[i]</code>, check if you can reach&nbsp;<strong>any</strong> index with value 0.</p>

<p>Notice that you can not jump outside of the array at any time.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> arr = [4,2,3,0,3,1,2], start = 5
<strong>Output:</strong> true
<strong>Explanation:</strong> 
All possible ways to reach at index 3 with value 0 are: 
index 5 -&gt; index 4 -&gt; index 1 -&gt; index 3 
index 5 -&gt; index 6 -&gt; index 4 -&gt; index 1 -&gt; index 3 
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> arr = [4,2,3,0,3,1,2], start = 0
<strong>Output:</strong> true 
<strong>Explanation: 
</strong>One possible way to reach at index 3 with value 0 is: 
index 0 -&gt; index 4 -&gt; index 1 -&gt; index 3
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> arr = [3,0,2,1,2], start = 2
<strong>Output:</strong> false
<strong>Explanation: </strong>There is no way to reach at index 1 with value 0.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= arr.length &lt;= 5 * 10<sup>4</sup></code></li>
	<li><code>0 &lt;= arr[i] &lt;&nbsp;arr.length</code></li>
	<li><code>0 &lt;= start &lt; arr.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1428-jump-game-iii/solution.cpp)

```cpp
class Solution {
public:
    bool canReach(vector<int>& arr, int start) {
        int n =  arr.size();
        queue<int>q;
        q.push(start);
        vector<bool>visited(n, false);
        visited[start] = true;
        while(!q.empty()){

            int size = q.size();

            for(int i=0; i<size; i++){
                int index = q.front();
                q.pop();

                if(arr[index] == 0){
                    return true;
                }
                int first = index + arr[index];

                if(first < n && !visited[first]){
                    q.push(first);
                    visited[first] = true;
                }

                first = index - arr[index];

                if(first >=0 && !visited[first]){
                    q.push(first);
                    visited[first] = true;
                }
            }

        }

        return false;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
