# 1849. Maximum Absolute Sum Of Any Subarray

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1849-maximum-absolute-sum-of-any-subarray)

## Problem

<p>You are given an integer array <code>nums</code>. The <strong>absolute sum</strong> of a subarray <code>[nums<sub>l</sub>, nums<sub>l+1</sub>, ..., nums<sub>r-1</sub>, nums<sub>r</sub>]</code> is <code>abs(nums<sub>l</sub> + nums<sub>l+1</sub> + ... + nums<sub>r-1</sub> + nums<sub>r</sub>)</code>.</p>

<p>Return <em>the <strong>maximum</strong> absolute sum of any <strong>(possibly empty)</strong> subarray of </em><code>nums</code>.</p>

<p>Note that <code>abs(x)</code> is defined as follows:</p>

<ul>
	<li>If <code>x</code> is a negative integer, then <code>abs(x) = -x</code>.</li>
	<li>If <code>x</code> is a non-negative integer, then <code>abs(x) = x</code>.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,-3,2,3,-4]
<strong>Output:</strong> 5
<strong>Explanation:</strong> The subarray [2,3] has absolute sum = abs(2+3) = abs(5) = 5.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,-5,1,-4,3,-2]
<strong>Output:</strong> 8
<strong>Explanation:</strong> The subarray [-5,1,-4] has absolute sum = abs(-5+1-4) = abs(-8) = 8.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-10<sup>4</sup> &lt;= nums[i] &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1849-maximum-absolute-sum-of-any-subarray/solution.cpp)

```cpp
class Solution {
public:
    int maxAbsoluteSum(vector<int>& nums) {
        
        int n = nums.size();
        if(n==0) return 0;

        vector<int>dp(n+1,0);
        vector<int>dp2(n+1,20000);
        int curr_max = 0;
        int curr_min = 20000;
        int maxi = 0;
        int mini = 20000;

        for(int i=0; i<n; i++){
            curr_max = max(nums[i], nums[i] + curr_max);
            curr_min = min(nums[i], nums[i] + curr_min);
            maxi = max(maxi, curr_max);
            mini = min(mini, curr_min);

        }

        // int ans = INT_MIN;
        // int ans2 = INT_MAX;
        // for(int i=0; i<n+1; i++){
        //     ans = max(ans, dp[i]);
        //     ans2 = min(ans2, dp2[i]);
        // }
        return max(abs(maxi), abs(mini));



    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
