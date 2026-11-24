# 1034. Subarrays With K Different Integers

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/1034-subarrays-with-k-different-integers)

## Problem

<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return <em>the number of <strong>good subarrays</strong> of </em><code>nums</code>.</p>

<p>A <strong>good array</strong> is an array where the number of different integers in that array is exactly <code>k</code>.</p>

<ul>
	<li>For example, <code>[1,2,3,1,2]</code> has <code>3</code> different integers: <code>1</code>, <code>2</code>, and <code>3</code>.</li>
</ul>

<p>A <strong>subarray</strong> is a <strong>contiguous</strong> part of an array.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,1,2,3], k = 2
<strong>Output:</strong> 7
<strong>Explanation:</strong> Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,1,3,4], k = 3
<strong>Output:</strong> 3
<strong>Explanation:</strong> Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 2 * 10<sup>4</sup></code></li>
	<li><code>1 &lt;= nums[i], k &lt;= nums.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/1034-subarrays-with-k-different-integers/solution.cpp)

```cpp
class Solution {
public:
// counting the subarrays with distict elements equal to K or less
    int solve(vector<int>&nums, int k){
        int n = nums.size();
        int count = k;
        int ans = 0;
        
        unordered_map<int,int>freq;

        int l = 0;
        int distinct = 0;

        for(int r = 0; r<n; r++){
            freq[nums[r]]++;
            if(freq[nums[r]] == 1){
                distinct++;
            }

            while(distinct > count){

                freq[nums[l]]--;

                if(freq[nums[l]] == 0){
                    distinct--;
                
                }
                l++;
    
            }
            ans += r - l + 1;
        }
        return ans;
    }
    int subarraysWithKDistinct(vector<int>& nums, int k) {

        int ans = solve(nums, k) - solve(nums, k-1);
        return ans;
        
    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
