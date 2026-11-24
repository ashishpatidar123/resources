# 2706. Minimum Score By Changing Two Elements

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2706-minimum-score-by-changing-two-elements)

## Problem

<p>You are given an integer array <code>nums</code>.</p>

<ul>
	<li>The <strong>low</strong> score of <code>nums</code> is the <strong>minimum</strong> absolute difference between any two integers.</li>
	<li>The <strong>high</strong> score of <code>nums</code> is the <strong>maximum</strong> absolute difference between any two integers.</li>
	<li>The <strong>score</strong> of <code>nums</code> is the sum of the <strong>high</strong> and <strong>low</strong> scores.</li>
</ul>

<p>Return the <strong>minimum score</strong> after <strong>changing two elements</strong> of <code>nums</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,4,7,8,5]</span></p>

<p><strong>Output:</strong> <span class="example-io">3</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>Change <code>nums[0]</code> and <code>nums[1]</code> to be 6 so that <code>nums</code> becomes [6,6,7,8,5].</li>
	<li>The low score is the minimum absolute difference: |6 - 6| = 0.</li>
	<li>The high score is the maximum absolute difference: |8 - 5| = 3.</li>
	<li>The sum of high and low score is 3.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,4,3]</span></p>

<p><strong>Output:</strong> <span class="example-io">0</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>Change <code>nums[1]</code> and <code>nums[2]</code> to 1 so that <code>nums</code> becomes [1,1,1].</li>
	<li>The sum of maximum absolute difference and minimum absolute difference is 0.</li>
</ul>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>3 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2706-minimum-score-by-changing-two-elements/solution.cpp)

```cpp
class Solution {
public:
    int minimizeSum(vector<int>& a) {
        int n = a.size();
        if(n==3){
            return 0;
        }
        sort(a.begin(),a.end());
        int one = a[n-1] - a[2];
        int two = a[n-3] - a[0];
        int three = a[n-2] - a[1];
        return min({one,two,three});
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
