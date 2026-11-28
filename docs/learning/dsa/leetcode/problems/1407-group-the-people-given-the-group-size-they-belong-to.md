# 1407. Group The People Given The Group Size They Belong To

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1407-group-the-people-given-the-group-size-they-belong-to)

## Problem

<p>There are <code>n</code> people&nbsp;that are split into some unknown number of groups. Each person is labeled with a&nbsp;<strong>unique ID</strong>&nbsp;from&nbsp;<code>0</code>&nbsp;to&nbsp;<code>n - 1</code>.</p>

<p>You are given an integer array&nbsp;<code>groupSizes</code>, where <code>groupSizes[i]</code>&nbsp;is the size of the group that person&nbsp;<code>i</code>&nbsp;is in. For example, if&nbsp;<code>groupSizes[1] = 3</code>, then&nbsp;person&nbsp;<code>1</code>&nbsp;must be in a&nbsp;group of size&nbsp;<code>3</code>.</p>

<p>Return&nbsp;<em>a list of groups&nbsp;such that&nbsp;each person&nbsp;<code>i</code>&nbsp;is in a group of size&nbsp;<code>groupSizes[i]</code></em>.</p>

<p>Each person should&nbsp;appear in&nbsp;<strong>exactly one group</strong>,&nbsp;and every person must be in a group. If there are&nbsp;multiple answers, <strong>return any of them</strong>. It is <strong>guaranteed</strong> that there will be <strong>at least one</strong> valid solution for the given input.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> groupSizes = [3,3,3,3,3,1,3]
<strong>Output:</strong> [[5],[0,1,2],[3,4,6]]
<b>Explanation:</b> 
The first group is [5]. The size is 1, and groupSizes[5] = 1.
The second group is [0,1,2]. The size is 3, and groupSizes[0] = groupSizes[1] = groupSizes[2] = 3.
The third group is [3,4,6]. The size is 3, and groupSizes[3] = groupSizes[4] = groupSizes[6] = 3.
Other possible solutions are [[2,1,6],[5],[0,4,3]] and [[5],[0,6,2],[4,3,1]].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> groupSizes = [2,1,3,3,3,2]
<strong>Output:</strong> [[1],[0,5],[2,3,4]]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>groupSizes.length == n</code></li>
	<li><code>1 &lt;= n&nbsp;&lt;= 500</code></li>
	<li><code>1 &lt;=&nbsp;groupSizes[i] &lt;= n</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1407-group-the-people-given-the-group-size-they-belong-to/solution.cpp)

```cpp
class Solution {
public:
    vector<vector<int>> groupThePeople(vector<int>& groupSizes) {
        int n = groupSizes.size();
        vector<vector<int>>group(n+1);
        for(int i=0; i<n; i++){
            group[groupSizes[i]].push_back(i);
        }
        vector<vector<int>>ans;

        for(int i=1; i<=n; i++){
            if(group[i].size()!=0){
                int s = group[i].size();
                vector<int>temp;
                for(int j=0; j<s; j++){
                    temp.push_back(group[i][j]);
                    if(temp.size()==i){
                        ans.push_back(temp);
                        temp.clear();
                    }
                }
            }
        }
        return ans;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
