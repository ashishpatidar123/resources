# 322. Coin Change

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0322-coin-change)

## Problem

# Coin Change

### Difficulty: Medium
### Topics: Array, Dynamic Programming, Breadth-First Search, Knapsack Problem, Complete Knapsack

<p>You are given an integer array <code>coins</code> representing coins of different denominations and an integer <code>amount</code> representing a total amount of money.</p>

<p>Return the <strong>fewest</strong> number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.</p>

<p>You may assume that you have an infinite number of each kind of coin.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> coins = [1,2,5], amount = 11
<strong>Output:</strong> 3
<strong>Explanation:</strong> 11 = 5 + 5 + 1
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> coins = [2], amount = 3
<strong>Output:</strong> -1
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> coins = [1], amount = 0
<strong>Output:</strong> 0
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= coins.length &lt;= 12</code></li>
	<li><code>1 &lt;= coins[i] &lt;= 2<sup>31</sup> - 1</code></li>
	<li><code>0 &lt;= amount &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0322-coin-change/solution.cpp)

```cpp
class Solution {
private:
    int solve(vector<int>&coins,int amount,vector<int>&dp){
        if(amount==0){
            return 0;
        }
        if(dp[amount]!=-1){
            return dp[amount];
        }
        int ans = INT_MAX;

        for(int i=0; i<coins.size(); i++){
            if(coins[i]<=amount){
                int temp = solve(coins,amount-coins[i],dp);
                if(temp!=INT_MAX){
                    ans = min(ans,temp+1);
                }
                else{
                    ans = ans;
                }
                
            }
        }
        dp[amount] = ans;
        return ans;
    }
public:
    int coinChange(vector<int>& coins, int amount) {
        int n = coins.size();
        vector<int>dp(amount+1,-1);
        int ans = solve(coins,amount,dp);
        if(ans==INT_MAX){
            return -1;
        }
        return ans;
    }
};
```

### `solution_2165055203.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0322-coin-change/solution_2165055203.cpp)

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {

        int n = coins.size();
        vector<int>dp(amount+1,INT_MAX-1 );
        dp[0] = 0;

        for(int i=0; i<n; i++){
            for(int x=coins[i]; x<=amount; x++){
                dp[x] = min(dp[x], 1 + dp[x-coins[i]]);
            }
        }
        if(dp[amount] == INT_MAX-1) return -1;
        return dp[amount];
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
