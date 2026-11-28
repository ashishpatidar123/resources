# 414. Third Maximum Number

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0414-third-maximum-number)

## Problem

<p>Given an integer array <code>nums</code>, return <em>the <strong>third distinct maximum</strong> number in this array. If the third maximum does not exist, return the <strong>maximum</strong> number</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,2,1]
<strong>Output:</strong> 1
<strong>Explanation:</strong>
The first distinct maximum is 3.
The second distinct maximum is 2.
The third distinct maximum is 1.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2]
<strong>Output:</strong> 2
<strong>Explanation:</strong>
The first distinct maximum is 2.
The second distinct maximum is 1.
The third distinct maximum does not exist, so the maximum (2) is returned instead.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,2,3,1]
<strong>Output:</strong> 1
<strong>Explanation:</strong>
The first distinct maximum is 3.
The second distinct maximum is 2 (both 2&#39;s are counted together since they have the same value).
The third distinct maximum is 1.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-2<sup>31</sup> &lt;= nums[i] &lt;= 2<sup>31</sup> - 1</code></li>
</ul>

<p>&nbsp;</p>
<strong>Follow up:</strong> Can you find an <code>O(n)</code> solution?

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0414-third-maximum-number/solution.cpp)

```cpp
class Solution {
public:
    int thirdMax(vector<int>& nums) {

        int n = nums.size();

        int max1 = INT_MIN;
        int max2 = INT_MIN;
        int max3 = INT_MIN;
        bool check = false;

        for(int i=0; i<n; i++){
            int x = nums[i];
            if(x == INT_MIN){
                check = true;
            }
            if(x > max1){
                max3 = max2;
                max2 = max1;
                max1 = x;
            }
            else if(x == max1){
                continue;
            }
            else if(x > max2){
                max3 = max2;
                max2 = x;
            }
            else if(x == max2){
                continue;
            }
            else if(x > max3){
                max3 = x;
            }
            else if(x ==  max3){
                continue;
            }
            
        }

        if(max3 == INT_MIN && check == false){

            return max1;
            
        }
        else if(max2 == INT_MIN && check == true && max1 != INT_MIN){
            return max1;
        }
        
        return max3;
        
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
