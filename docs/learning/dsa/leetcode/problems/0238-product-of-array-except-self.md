# 238. Product Of Array Except Self

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0238-product-of-array-except-self)

## Problem

<p>Given an integer array <code>nums</code>, return <em>an array</em> <code>answer</code> <em>such that</em> <code>answer[i]</code> <em>is equal to the product of all the elements of</em> <code>nums</code> <em>except</em> <code>nums[i]</code>.</p>

<p>The product of any prefix or suffix of <code>nums</code> is <strong>guaranteed</strong> to fit in a <strong>32-bit</strong> integer.</p>

<p>You must write an algorithm that runs in&nbsp;<code>O(n)</code>&nbsp;time and without using the division operation.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> nums = [1,2,3,4]
<strong>Output:</strong> [24,12,8,6]
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> nums = [-1,1,0,-3,3]
<strong>Output:</strong> [0,0,9,0,0]
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-30 &lt;= nums[i] &lt;= 30</code></li>
	<li>The input is generated such that <code>answer[i]</code> is <strong>guaranteed</strong> to fit in a <strong>32-bit</strong> integer.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong>&nbsp;Can you solve the problem in <code>O(1)</code>&nbsp;extra&nbsp;space complexity? (The output array <strong>does not</strong> count as extra space for space complexity analysis.)</p>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0238-product-of-array-except-self/solution.cpp)

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        
        int n = nums.size();

        // vector<long long int>prefix(n+1,1);
        // vector<long long int>suffix(n+1,1);

        // for(int i=1; i<n; i++){
        //     prefix[i] = prefix[i-1] * nums[i-1];
        // }
        // for(int i=n-2; i>=0; i--){
        //     suffix[i] = suffix[i+1] * nums[i+1];
        // }
        int prefix = 1;
        int suffix = 1;

        
        vector<int>ans(n,0);
        ans[0] = 1;
        for(int i=1; i<n; i++){
            ans[i] = prefix*nums[i-1];
            prefix = prefix*nums[i-1];
        }
        for(int i=n-2; i>=0; i--){
            ans[i] = ans[i] * suffix * nums[i+1];
            suffix = suffix * nums[i+1];
        }
        // for(int i=0; i<n; i++){
        //     ans[i] = prefix[i] * suffix[i];
        // }
        
        return ans;

    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
