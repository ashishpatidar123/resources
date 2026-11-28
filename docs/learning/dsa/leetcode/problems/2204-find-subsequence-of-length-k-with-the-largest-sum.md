# 2204. Find Subsequence Of Length K With The Largest Sum

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2204-find-subsequence-of-length-k-with-the-largest-sum)

## Problem

<p>You are given an integer array <code>nums</code> and an integer <code>k</code>. You want to find a <strong>subsequence </strong>of <code>nums</code> of length <code>k</code> that has the <strong>largest</strong> sum.</p>

<p>Return<em> </em><em><strong>any</strong> such subsequence as an integer array of length </em><code>k</code>.</p>

<p>A <strong>subsequence</strong> is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,1,3,3], k = 2
<strong>Output:</strong> [3,3]
<strong>Explanation:</strong>
The subsequence has the largest sum of 3 + 3 = 6.</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [-1,-2,3,4], k = 3
<strong>Output:</strong> [-1,3,4]
<strong>Explanation:</strong> 
The subsequence has the largest sum of -1 + 3 + 4 = 6.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,4,3,3], k = 2
<strong>Output:</strong> [3,4]
<strong>Explanation:</strong>
The subsequence has the largest sum of 3 + 4 = 7. 
Another possible subsequence is [4, 3].
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 1000</code></li>
	<li><code>-10<sup>5</sup>&nbsp;&lt;= nums[i] &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= k &lt;= nums.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2204-find-subsequence-of-length-k-with-the-largest-sum/solution.cpp)

```cpp
class Solution {
public:
    static bool comparator(pair<int,int>a, pair<int,int>b){
        return a.second < b.second;
    }
    vector<int> maxSubsequence(vector<int>& nums, int k) {

        int n = nums.size();

        priority_queue<pair<int,int>>pq;

        for(int i=0; i<n; i++){
            pq.push({nums[i],i});
            
        }

        
        vector<pair<int,int>>ans; 

        while(k > 0){
            pair<int,int> temp = pq.top();
            ans.push_back(temp);
            pq.pop();
            k--;
        }
        sort(ans.begin(),ans.end(),comparator);
        vector<int>temp;
        int l = ans.size();
        for(int i=0; i<l; i++){
            temp.push_back(ans[i].first);
        }

        return temp;
        
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
