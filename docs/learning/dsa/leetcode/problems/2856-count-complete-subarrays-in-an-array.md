# 2856. Count Complete Subarrays In An Array

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2856-count-complete-subarrays-in-an-array)

## Problem

<p>You are given an array <code>nums</code> consisting of <strong>positive</strong> integers.</p>

<p>We call a subarray of an array <strong>complete</strong> if the following condition is satisfied:</p>

<ul>
	<li>The number of <strong>distinct</strong> elements in the subarray is equal to the number of distinct elements in the whole array.</li>
</ul>

<p>Return <em>the number of <strong>complete</strong> subarrays</em>.</p>

<p>A <strong>subarray</strong> is a contiguous non-empty part of an array.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,3,1,2,2]
<strong>Output:</strong> 4
<strong>Explanation:</strong> The complete subarrays are the following: [1,3,1,2], [1,3,1,2,2], [3,1,2] and [3,1,2,2].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [5,5,5,5]
<strong>Output:</strong> 10
<strong>Explanation:</strong> The array consists only of the integer 5, so any subarray is complete. The number of subarrays that we can choose is 10.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 1000</code></li>
	<li><code>1 &lt;= nums[i] &lt;= 2000</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2856-count-complete-subarrays-in-an-array/solution.cpp)

```cpp
class Solution {
public:
    int countCompleteSubarrays(vector<int>& nums) {
        
        int n = nums.size();
        set<int>s;

        for(int i=0; i<n; i++){
            s.insert(nums[i]);
        }
        int count = s.size();
        int ans = 0;
        
        // for(int i=0; i<n; i++){
        //     set<int>t;
        //     for(int j=i; j<n; j++){
        //         t.insert(nums[j]);
        //         if(t.size() == count){
        //             ans += n-j;
        //             break;
        //         }
        //     }
        // }
        unordered_map<int,int>freq;

        int l = 0;
        int distinct = 0;

        for(int r = 0; r<n; r++){
            freq[nums[r]]++;
            if(freq[nums[r]] == 1){
                distinct++;
            }

            while(distinct == count){

                ans += n-r;

                freq[nums[l]]--;

                if(freq[nums[l]] == 0){
                    distinct--;
                }
                l++;

            }
        }
        return ans;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
