# 2589. Maximum Value Of A String In An Array

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2589-maximum-value-of-a-string-in-an-array)

## Problem

<p>The <strong>value</strong> of an alphanumeric string can be defined as:</p>

<ul>
	<li>The <strong>numeric</strong> representation of the string in base <code>10</code>, if it comprises of digits <strong>only</strong>.</li>
	<li>The <strong>length</strong> of the string, otherwise.</li>
</ul>

<p>Given an array <code>strs</code> of alphanumeric strings, return <em>the <strong>maximum value</strong> of any string in </em><code>strs</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;alic3&quot;,&quot;bob&quot;,&quot;3&quot;,&quot;4&quot;,&quot;00000&quot;]
<strong>Output:</strong> 5
<strong>Explanation:</strong> 
- &quot;alic3&quot; consists of both letters and digits, so its value is its length, i.e. 5.
- &quot;bob&quot; consists only of letters, so its value is also its length, i.e. 3.
- &quot;3&quot; consists only of digits, so its value is its numeric equivalent, i.e. 3.
- &quot;4&quot; also consists only of digits, so its value is 4.
- &quot;00000&quot; consists only of digits, so its value is 0.
Hence, the maximum value is 5, of &quot;alic3&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;1&quot;,&quot;01&quot;,&quot;001&quot;,&quot;0001&quot;]
<strong>Output:</strong> 1
<strong>Explanation:</strong> 
Each string in the array has value 1. Hence, we return 1.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= strs.length &lt;= 100</code></li>
	<li><code>1 &lt;= strs[i].length &lt;= 9</code></li>
	<li><code>strs[i]</code> consists of only lowercase English letters and digits.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2589-maximum-value-of-a-string-in-an-array/solution.cpp)

```cpp
class Solution {
public:
    int maximumValue(vector<string>& strs) {

        int n = strs.size();
        int maxi = -1;
        for(int i=0; i<n; i++){
            int len = strs[i].size();

            bool check = true;
            int sum = 0;
            int factor = 1;

            for(int j=0; j<len; j++){
                if(strs[i][j] >= 'a' && strs[i][j] <= 'z'){
                    maxi = max(maxi, len);
                    check = false;
                }
            }
            if(check){
                for(int j=len-1; j>=0; j--){
                    int dig = strs[i][j] - '0';
                    sum += dig*factor;
                    factor *= 10;
                }
                maxi = max(maxi, sum);
            }
       } 
       
       return maxi;
    }

};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
