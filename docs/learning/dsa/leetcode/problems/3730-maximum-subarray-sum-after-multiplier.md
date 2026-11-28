# 3730. Maximum Subarray Sum After Multiplier

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/3730-maximum-subarray-sum-after-multiplier)

## Problem

<p>You are given an integer array <code>nums</code> and a positive integer <code>k</code>.</p>

<p>You must choose <strong>exactly</strong> one <span data-keyword="subarray-nonempty">subarray</span> of <code>nums</code> and perform <strong>exactly</strong> one of the following operations:</p>

<ol>
	<li>Multiply each number in the chosen subarray by <code>k</code>.</li>
	<li>Divide each number in the chosen subarray by <code>k</code>.
	<ul>
		<li>When dividing a positive number by <code>k</code>, use the <strong>floor</strong> value of the division result.</li>
		<li>When dividing a negative number by <code>k</code>, use the <strong>ceiling</strong> value of the division result.</li>
	</ul>
	</li>
</ol>

<p>Return the <strong>maximum</strong> possible sum of a <strong>non-empty</strong> subarray in the resulting array.</p>

<p>Note that the subarray chosen for the operation and the subarray chosen for the sum may be <strong>different</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,-2,3,4,-5], k = 2</span></p>

<p><strong>Output:</strong> <span class="example-io">14</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>Multiply each number in the subarray <code>[3, 4]</code> by 2.</li>
	<li>This results in <code>nums = [1, -2, 6, 8, -5]</code>.</li>
	<li>The subarray with the largest sum is <code>[6, 8]</code>, so the output is <code>6 + 8 = 14</code>.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [-5,-4,-3], k = 2</span></p>

<p><strong>Output:</strong> <span class="example-io">-1</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>Divide each number in the subarray <code>[-3]</code> by 2.</li>
	<li>This results in <code>nums = [-5, -4, -1]</code>.</li>
	<li>The subarray with the largest sum is <code>[-1]</code>, so the output is -1.</li>
</ul>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-10<sup>5</sup> &lt;= nums[i] &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= k &lt;= 10<sup>5</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/3730-maximum-subarray-sum-after-multiplier/solution.cpp)

```cpp
class Solution {
public:
    long long maxSubarraySum(vector<int>& nums, int k) {
        int n = nums.size();

        long long mini = -1e15;

        long long dp0 = mini;
        long long dp1 = mini;
        long long dp2 = mini;
        long long dp3 = mini;

        long long maxi = mini;

        for(int i=0; i<n; i++){
            long long val = (long long) nums[i];

            long long mul = val * k;
            long long div = val/k;


            long long dp0_prev = dp0;
            long long dp1_prev = dp1;
            long long dp2_prev = dp2;
            long long dp3_prev = dp3;


            dp0 = max(val, dp0_prev + val);

            dp1 = max({mul, dp0_prev + mul, dp1_prev + mul});

            dp2 = max({div, dp0_prev + div, dp2_prev + div});

            dp3 = max({dp3_prev + val, dp1_prev + val, dp2_prev + val});
            
            maxi = max({maxi, dp1, dp2, dp3});

        }
        return maxi;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
