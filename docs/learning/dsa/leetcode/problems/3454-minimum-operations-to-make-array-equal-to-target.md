# 3454. Minimum Operations To Make Array Equal To Target

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/3454-minimum-operations-to-make-array-equal-to-target)

## Problem

<p>You are given two positive integer arrays <code>nums</code> and <code>target</code>, of the same length.</p>

<p>In a single operation, you can select any subarray of <code>nums</code> and increment each element within that subarray by 1 or decrement each element within that subarray by 1.</p>

<p>Return the <strong>minimum</strong> number of operations required to make <code>nums</code> equal to the array <code>target</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [3,5,1,2], target = [4,6,2,4]</span></p>

<p><strong>Output:</strong> <span class="example-io">2</span></p>

<p><strong>Explanation:</strong></p>

<p>We will perform the following operations to make <code>nums</code> equal to <code>target</code>:<br />
- Increment&nbsp;<code>nums[0..3]</code> by 1, <code>nums = [4,6,2,3]</code>.<br />
- Increment&nbsp;<code>nums[3..3]</code> by 1, <code>nums = [4,6,2,4]</code>.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,3,2], target = [2,1,4]</span></p>

<p><strong>Output:</strong> <span class="example-io">5</span></p>

<p><strong>Explanation:</strong></p>

<p>We will perform the following operations to make <code>nums</code> equal to <code>target</code>:<br />
- Increment&nbsp;<code>nums[0..0]</code> by 1, <code>nums = [2,3,2]</code>.<br />
- Decrement&nbsp;<code>nums[1..1]</code> by 1, <code>nums = [2,2,2]</code>.<br />
- Decrement&nbsp;<code>nums[1..1]</code> by 1, <code>nums = [2,1,2]</code>.<br />
- Increment&nbsp;<code>nums[2..2]</code> by 1, <code>nums = [2,1,3]</code>.<br />
- Increment&nbsp;<code>nums[2..2]</code> by 1, <code>nums = [2,1,4]</code>.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length == target.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i], target[i] &lt;= 10<sup>8</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/3454-minimum-operations-to-make-array-equal-to-target/solution.cpp)

```cpp
class Solution {
public:
    long long minimumOperations(vector<int>& nums, vector<int>& target) {
        int n = nums.size();
        long long res = 0;
        int prev = 0;

        for (int i = 0; i < n; i++) {
            int curr = nums[i] - target[i];

            if (curr > 0 && prev < 0 || curr < 0 && prev > 0) {
                res += abs(curr);
            }
            else if (abs(curr) - abs(prev) > 0) {
                res += abs(curr - prev);
            }

            prev = curr;
        }

        return res;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
