# 42. Trapping Rain Water

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0042-trapping-rain-water)

## Problem

<p>Given <code>n</code> non-negative integers representing an elevation map where the width of each bar is <code>1</code>, compute how much water it can trap after raining.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img src="https://assets.leetcode.com/uploads/2018/10/22/rainwatertrap.png" style="width: 412px; height: 161px;" />
<pre>
<strong>Input:</strong> height = [0,1,0,2,1,0,1,3,2,1,2,1]
<strong>Output:</strong> 6
<strong>Explanation:</strong> The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> height = [4,2,0,3,2,5]
<strong>Output:</strong> 9
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == height.length</code></li>
	<li><code>1 &lt;= n &lt;= 2 * 10<sup>4</sup></code></li>
	<li><code>0 &lt;= height[i] &lt;= 10<sup>5</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0042-trapping-rain-water/solution.cpp)

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        
        int n = height.size();
        vector<int>left(n,0);
        vector<int>right(n,0);

        left[0] = 0;
        right[n-1] = 0;

        for(int i=1; i<n; i++){
            left[i] = max(left[i-1],height[i-1]);
        }
        for(int i=n-2; i>=0; i--){
            right[i] = max(right[i+1],height[i+1]); 
        }

        int sum = 0;

        for(int i=0; i<n; i++){
            
            int mini = min(left[i],right[i]);
            int water = 0;
            if(mini - height[i] > 0){
                water = mini - height[i];
            }
            sum += water;
        }
        return sum;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
