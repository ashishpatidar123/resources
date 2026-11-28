# 4322. Frequency Balance Subarray

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4322-frequency-balance-subarray)

## Problem

<p>You are given an integer array ​​​​​​​<code>nums</code>.</p>

<p>Define a <strong>frequency balance <span data-keyword="subarray-nonempty">subarray</span></strong> as follows:</p>

<ul>
	<li>If the subarray contains only one distinct value, it is frequency balanced.</li>
	<li>Otherwise, there must exist a positive integer <code>f</code> such that every distinct value in the subarray occurs either <code>f</code> or <code>2 * f</code> times, and both <span data-keyword="frequency-array">frequencies</span> occur among the distinct values.</li>
</ul>

<p>Return an integer denoting the length of the <strong>longest</strong> frequency balance subarray.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,2,1,2,3,3,3]</span></p>

<p><strong>Output:</strong> <span class="example-io">5</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>The longest frequency balance subarray is <code>[2, 1, 2, 3, 3]</code>.</li>
	<li>The elements that appear most frequently are 2 and 3, both appearing twice.</li>
	<li>The remaining element 1 appears once, meeting the requirements.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [5,5,5,5]</span></p>

<p><strong>Output:</strong> <span class="example-io">4</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>The longest frequency balance subarray is <code>[5, 5, 5, 5]</code>.</li>
	<li>The element that appears most frequently is 5.</li>
	<li>There are no other elements meeting the requirements.</li>
</ul>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,3,4]</span></p>

<p><strong>Output:</strong> <span class="example-io">1</span></p>

<p><strong>Explanation:</strong></p>

<p>Since all elements appear only once, the length of the longest frequency balance subarray is 1.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>​​​​​​​3</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>​​​​​​​9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4322-frequency-balance-subarray/solution.cpp)

```cpp
class Solution {
public:
    int getLength(vector<int>& arr) {
        
        int n = arr.size();
        int maxi = 1;

        

        for(int i=0; i<n; i++){
            int distinct = 0;
            unordered_map<int, int>count;

            unordered_map<int, int>freq;
            for(int j=i; j<n; j++){
                int currFreq = count[arr[j]];
                
                if(freq.find(currFreq) != freq.end()){
                    freq[currFreq]--;
                    if(freq[currFreq] == 0){
                        freq.erase(currFreq);
                    }
                }
                count[arr[j]]++;
                int newFreq = count[arr[j]];
                freq[newFreq]++;
                if(newFreq == 1){
                    distinct++;
                }


                if(distinct == 1){
                    maxi = max(maxi, j-i+1);
                }
                else{
                    if(freq.size() == 2){
                        vector<int>temp;
                        for(auto t:freq){
                            temp.push_back(t.first);
                        }

                        if(temp[0] == 2*temp[1] || temp[1] == 2*temp[0]){
                            maxi = max(maxi, j-i + 1);
                        }
                    }
                }
            }
        }
        return maxi;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
