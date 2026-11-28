# 1813. Maximum Erasure Value

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1813-maximum-erasure-value)

## Problem

<p>You are given an array of positive integers <code>nums</code> and want to erase a subarray containing&nbsp;<strong>unique elements</strong>. The <strong>score</strong> you get by erasing the subarray is equal to the <strong>sum</strong> of its elements.</p>

<p>Return <em>the <strong>maximum score</strong> you can get by erasing <strong>exactly one</strong> subarray.</em></p>

<p>An array <code>b</code> is called to be a <span class="tex-font-style-it">subarray</span> of <code>a</code> if it forms a contiguous subsequence of <code>a</code>, that is, if it is equal to <code>a[l],a[l+1],...,a[r]</code> for some <code>(l,r)</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [4,2,4,5,6]
<strong>Output:</strong> 17
<strong>Explanation:</strong> The optimal subarray here is [2,4,5,6].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [5,2,1,2,5,2,1,2,5]
<strong>Output:</strong> 8
<strong>Explanation:</strong> The optimal subarray here is [5,2,1] or [1,2,5].
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1813-maximum-erasure-value/solution.cpp)

```cpp
class Solution {
public:
    int maximumUniqueSubarray(vector<int>& nums) {

        int n = nums.size();

        unordered_map<int,int>index;

        vector<int>prefix(n+1,0);

        for(int i=0; i<n; i++){
            prefix[i+1] = prefix[i]+nums[i];
        }

        int maxi = -1;
        int idx = 0;
        for(int i=0; i<n; i++){

            if(index.find(nums[i]) == index.end() || index[nums[i]] < idx){

                index[nums[i]] = i;
                int sum = prefix[i+1] - prefix[idx];
                maxi = max(sum, maxi);

            }
            else{
                int sum = prefix[i]-prefix[idx];
                idx = index[nums[i]]+1;
                index[nums[i]]=i;
                maxi = max(maxi, sum);
            }
        }

        return maxi;
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
