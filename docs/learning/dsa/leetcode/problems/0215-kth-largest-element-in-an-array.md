# 215. Kth Largest Element In An Array

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0215-kth-largest-element-in-an-array)

## Problem

# Kth Largest Element in an Array

### Difficulty: Medium
### Topics: Array, Divide and Conquer, Sorting, Heap (Priority Queue), Quickselect

<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return <em>the</em> <code>k<sup>th</sup></code> <em>largest element in the array</em>.</p>

<p>Note that it is the <code>k<sup>th</sup></code> largest element in the sorted order, not the <code>k<sup>th</sup></code> distinct element.</p>

<p>Can you solve it without sorting?</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> nums = [3,2,1,5,6,4], k = 2
<strong>Output:</strong> 5
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> nums = [3,2,3,1,2,4,5,5,6], k = 4
<strong>Output:</strong> 4
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= k &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-10<sup>4</sup> &lt;= nums[i] &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0215-kth-largest-element-in-an-array/solution.cpp)

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        
        int n = nums.size();
        priority_queue<int> pq;

        for(int i=0; i<n; i++){
            pq.push(nums[i]);
        }

        
        int ans = 0;
        while(k > 0){

            ans = pq.top();
            pq.pop();
            k--;
        }

        return ans;
    }
};
```

### `solution_2202177085.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0215-kth-largest-element-in-an-array/solution_2202177085.cpp)

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int n = nums.size();

        priority_queue<int, vector<int>, greater<>> pq;

        for(int i=0; i<n; i++){
            if(pq.size() == k){
                if(pq.top() < nums[i]){
                    pq.pop();
                    pq.push(nums[i]);
                }
            }
            else{
                pq.push(nums[i]);
            }
        }

        return pq.top();
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
