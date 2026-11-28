# 416. Partition Equal Subset Sum

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0416-partition-equal-subset-sum)

## Problem

<p>Given an integer array <code>nums</code>, return <code>true</code> <em>if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or </em><code>false</code><em> otherwise</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,5,11,5]
<strong>Output:</strong> true
<strong>Explanation:</strong> The array can be partitioned as [1, 5, 5] and [11].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,3,5]
<strong>Output:</strong> false
<strong>Explanation:</strong> The array cannot be partitioned into equal sum subsets.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 200</code></li>
	<li><code>1 &lt;= nums[i] &lt;= 100</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0416-partition-equal-subset-sum/solution.cpp)

```cpp
class Solution {
    int solve(vector<int>&nums,int n, int sum, vector<vector<int>>&dp){
        // base case 
        // if sum is 0 then we can always have a empty subset
        if(sum==0){
            return 1;
        }
        // if n is 0 and sum is not zero
        // then we cannot have a subset with some nonzero sum 
        if(n==0){
            return 0;
        }
        // if we already calculated a value then return it
        if(dp[n][sum]!=-1){
            return dp[n][sum];
        }
        // else check if the element is less than or equal to sum 
        if(nums[n-1]<=sum){
            // if it is then either we can include it or exclude it
            return dp[n][sum] = solve(nums,n-1,sum-nums[n-1],dp)||solve(nums,n-1,sum,dp);
        }
        // else we can't include it so we have to exclude it
        else{
            return dp[n][sum] = solve(nums,n-1,sum,dp);
        }

    }
public:
    bool canPartition(vector<int>& nums) {
        int n = nums.size();
        int sum = 0;
        for(int i=0; i<n; i++){
            sum += nums[i];
        }
        
        if(sum%2!=0){
            return false;
        }
        sum = sum/2;
        vector<vector<int>> dp(n+1,vector<int>(sum+1,-1));

        if(solve(nums,n,sum,dp)){
            return true;
        }
        return false;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
