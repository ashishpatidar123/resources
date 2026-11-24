# 66. Plus One

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0066-plus-one)

## Problem

<p>You are given a <strong>large integer</strong> represented as an integer array <code>digits</code>, where each <code>digits[i]</code> is the <code>i<sup>th</sup></code> digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading <code>0</code>&#39;s.</p>

<p>Increment the large integer by one and return <em>the resulting array of digits</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> digits = [1,2,3]
<strong>Output:</strong> [1,2,4]
<strong>Explanation:</strong> The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> digits = [4,3,2,1]
<strong>Output:</strong> [4,3,2,2]
<strong>Explanation:</strong> The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> digits = [9]
<strong>Output:</strong> [1,0]
<strong>Explanation:</strong> The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0].
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= digits.length &lt;= 100</code></li>
	<li><code>0 &lt;= digits[i] &lt;= 9</code></li>
	<li><code>digits</code> does not contain any leading <code>0</code>&#39;s.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0066-plus-one/solution.cpp)

```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        vector<int> ans;
        int sum = 0;
        int carry = 0;
        int n = digits.size();
        //traverse through the array
        for(int i=n-1; i>=0; i--){
            // for the last index add 1 to it
            if(i==n-1){
                sum = digits[i] + 1;
                // push sum%10 to ans vector
                ans.push_back(sum%10);
                // carry will be sum/10
                carry = sum/10;
            }
            // for other indexes simply add carry to the digits
            else{
                sum = digits[i]+carry;
                ans.push_back(sum%10);
                carry = sum/10;
            }
        }
        // if carry is not zero the push it to the ans vector
        if(carry!=0){
            ans.push_back(carry);
        }
        // reverse the ans vector
        reverse(ans.begin(),ans.end());
        // return ans
        return ans;
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
