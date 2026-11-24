# 1046. Max Consecutive Ones Iii

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1046-max-consecutive-ones-iii)

## Problem

<p>Given a binary array <code>nums</code> and an integer <code>k</code>, return <em>the maximum number of consecutive </em><code>1</code><em>&#39;s in the array if you can flip at most</em> <code>k</code> <code>0</code>&#39;s.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
<strong>Output:</strong> 6
<strong>Explanation:</strong> [1,1,1,0,0,<u><strong>1</strong>,1,1,1,1,<strong>1</strong></u>]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
<strong>Output:</strong> 10
<strong>Explanation:</strong> [0,0,<u>1,1,<strong>1</strong>,<strong>1</strong>,1,1,1,<strong>1</strong>,1,1</u>,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>nums[i]</code> is either 0 or 1.</li>
	<li><code>0 &lt;= k &lt;= nums.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1046-max-consecutive-ones-iii/solution.cpp)

```cpp
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        
        int n = nums.size();

        vector<int>prefix(n+1,0);

        for(int i=0; i<n; i++){
            prefix[i+1] = prefix[i] + (abs(1-nums[i]));
        }
        int l=0;
        int r=0;
        int ans = 0;
        while(l <= r && r<n){
            if(prefix[r+1]-prefix[l] <= k){
                ans = max(ans, r+1-l);
                r++;
            }
            else{
                l++;
                r++;
            }
        }
        return max(ans, n-l);
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
