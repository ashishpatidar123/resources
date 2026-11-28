# 1047. Maximize Sum Of Array After K Negations

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1047-maximize-sum-of-array-after-k-negations)

## Problem

<p>Given an integer array <code>nums</code> and an integer <code>k</code>, modify the array in the following way:</p>

<ul>
	<li>choose an index <code>i</code> and replace <code>nums[i]</code> with <code>-nums[i]</code>.</li>
</ul>

<p>You should apply this process exactly <code>k</code> times. You may choose the same index <code>i</code> multiple times.</p>

<p>Return <em>the largest possible sum of the array after modifying it in this way</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [4,2,3], k = 1
<strong>Output:</strong> 5
<strong>Explanation:</strong> Choose index 1 and nums becomes [4,-2,3].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,-1,0,2], k = 3
<strong>Output:</strong> 6
<strong>Explanation:</strong> Choose indices (1, 2, 2) and nums becomes [3,1,0,2].
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,-3,-1,5,-4], k = 2
<strong>Output:</strong> 13
<strong>Explanation:</strong> Choose indices (1, 4) and nums becomes [2,3,-1,5,4].
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-100 &lt;= nums[i] &lt;= 100</code></li>
	<li><code>1 &lt;= k &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1047-maximize-sum-of-array-after-k-negations/solution.cpp)

```cpp
class Solution {
public:
    int largestSumAfterKNegations(vector<int>& nums, int k) {
        

        int n = nums.size();

        
        
        vector<int>neg;
        vector<int>pos;

        int index = -1;
        bool check = false;

        for(int i=0; i<n; i++){
            if(nums[i] >=0){
                pos.push_back(nums[i]);
            }
            else{
                neg.push_back(nums[i]);
            }
        }

        sort(neg.begin(),neg.end());
        sort(pos.begin(),pos.end());

        int m = pos.size();
        int l = neg.size();

        for(int i=0; i<l; i++){
            if(k > 0){
                neg[i] = -1 * neg[i];
                k--;
            }
        }
        int sum = 0;
        int mini = 0;
        if(k%2!=0){
            if( l >=1 && m > 0){
                mini = min(neg[l-1],pos[0]);
            }
            else if(l==0){
                mini = pos[0];
            }
            else if(m == 0){
                mini = neg[l-1];
            }
        }
        for(int i=0; i<l; i++){
            sum += neg[i];
        }
        for(int j=0; j<m; j++){
            sum += pos[j];
        }
        if(k%2!=0){
            sum -= 2 * mini;
        }
        
        return sum;
        
        
       

    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
