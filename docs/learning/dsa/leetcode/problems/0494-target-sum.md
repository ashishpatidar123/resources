# 494. Target Sum

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0494-target-sum)

## Problem

<p>You are given an integer array <code>nums</code> and an integer <code>target</code>.</p>

<p>You want to build an <strong>expression</strong> out of nums by adding one of the symbols <code>&#39;+&#39;</code> and <code>&#39;-&#39;</code> before each integer in nums and then concatenate all the integers.</p>

<ul>
	<li>For example, if <code>nums = [2, 1]</code>, you can add a <code>&#39;+&#39;</code> before <code>2</code> and a <code>&#39;-&#39;</code> before <code>1</code> and concatenate them to build the expression <code>&quot;+2-1&quot;</code>.</li>
</ul>

<p>Return the number of different <strong>expressions</strong> that you can build, which evaluates to <code>target</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,1,1,1,1], target = 3
<strong>Output:</strong> 5
<strong>Explanation:</strong> There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1], target = 1
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 20</code></li>
	<li><code>0 &lt;= nums[i] &lt;= 1000</code></li>
	<li><code>0 &lt;= sum(nums[i]) &lt;= 1000</code></li>
	<li><code>-1000 &lt;= target &lt;= 1000</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0494-target-sum/solution.cpp)

```cpp
class Solution {
public:
    int ans = 0;
    void func(vector<int>&nums, int sum,  int n, int i, int target){
        if(i == n){
            if(sum == target){
                ans++;
               
            }
            return;
        }
        func(nums, sum + nums[i], n, i+1, target);
        func(nums, sum-nums[i], n, i+1, target);
    }
    int findTargetSumWays(vector<int>& nums, int target) {
        
        int n = nums.size();
        // func(nums, 0, n, 0, target);
        // return ans;
        int total = 0;
        for(int i=0; i<n; i++){
            total += nums[i];
        }
        if(abs(target) > total) return 0;
        // vector<vector<int>>dp(n+1, vector<int>(2*total+1,0));

        // dp[0][total] = 1;

        // for(int i=0; i<n; i++){
        //     for(int s=0; s<=2*total; s++){
        //         if(dp[i][s] > 0){
        //             dp[i+1][s + nums[i]] += dp[i][s];
        //             dp[i+1][s - nums[i]] += dp[i][s];
        //         }
        //     }
            

        // }

        // return dp[n][target + total];

        vector<int>dp(2*total+1,0);
        dp[total]=1;

        for(int i = 0; i < n; i++) {
        vector<int> next(2 * total + 1, 0); // Temporary storage for current element
        for(int s = 0; s <= 2 * total; s++) {
            if(dp[s] > 0) {
                next[s + nums[i]] += dp[s];
                next[s - nums[i]] += dp[s];
            }
        }
        dp = next; // Update the main DP table for the next iteration
    }
        return dp[total+target];

    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
