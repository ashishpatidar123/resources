# 1020. Longest Turbulent Subarray

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1020-longest-turbulent-subarray)

## Problem

<p>Given an integer array <code>arr</code>, return <em>the length of a maximum size turbulent subarray of</em> <code>arr</code>.</p>

<p>A subarray is <strong>turbulent</strong> if the comparison sign flips between each adjacent pair of elements in the subarray.</p>

<p>More formally, a subarray <code>[arr[i], arr[i + 1], ..., arr[j]]</code> of <code>arr</code> is said to be turbulent if and only if:</p>

<ul>
	<li>For <code>i &lt;= k &lt; j</code>:

	<ul>
		<li><code>arr[k] &gt; arr[k + 1]</code> when <code>k</code> is odd, and</li>
		<li><code>arr[k] &lt; arr[k + 1]</code> when <code>k</code> is even.</li>
	</ul>
	</li>
	<li>Or, for <code>i &lt;= k &lt; j</code>:
	<ul>
		<li><code>arr[k] &gt; arr[k + 1]</code> when <code>k</code> is even, and</li>
		<li><code>arr[k] &lt; arr[k + 1]</code> when <code>k</code> is odd.</li>
	</ul>
	</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> arr = [9,4,2,10,7,8,8,1,9]
<strong>Output:</strong> 5
<strong>Explanation:</strong> arr[1] &gt; arr[2] &lt; arr[3] &gt; arr[4] &lt; arr[5]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> arr = [4,8,12,16]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> arr = [100]
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= arr.length &lt;= 4 * 10<sup>4</sup></code></li>
	<li><code>0 &lt;= arr[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1020-longest-turbulent-subarray/solution.cpp)

```cpp
class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        
        
        int n = arr.size();
        int max_len = -1;
        if(n==1){
            return 1;
        }
        if(n==2){
            if(arr[0]==arr[1]){
                return 1;
            }
            else{
                return 2;
            }
        }
        bool sign = true; 

        int curr = 0;
        
        for(int i=1; i<n; i++){
            
            bool temp = sign;

            if(arr[i]>arr[i-1]){
                temp = true;
                if(temp == sign){
                    max_len = max(max_len, curr);
                    curr = 1;

                }
                else{
                    curr += 1;
                    max_len = max(max_len, curr);
                    sign = temp;
                }
            }
            else if(arr[i] < arr[i-1]){
                temp = false;
                    if(temp == sign){
                    max_len = max(max_len, curr);
                    curr = 1;

                }
                else{
                    curr += 1;
                    max_len = max(max_len, curr);
                    sign = temp;
                }
            }
            else if(arr[i]==arr[i-1]){
                curr = 0;
                max_len = max(max_len, curr);
                sign = false;
            }


        }
        return max_len+1;

    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
