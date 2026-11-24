# 278. First Bad Version

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0278-first-bad-version)

## Problem

<p>You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.</p>

<p>Suppose you have <code>n</code> versions <code>[1, 2, ..., n]</code> and you want to find out the first bad one, which causes all the following ones to be bad.</p>

<p>You are given an API <code>bool isBadVersion(version)</code> which returns whether <code>version</code> is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> n = 5, bad = 4
<strong>Output:</strong> 4
<strong>Explanation:</strong>
call isBadVersion(3) -&gt; false
call isBadVersion(5)&nbsp;-&gt; true
call isBadVersion(4)&nbsp;-&gt; true
Then 4 is the first bad version.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> n = 1, bad = 1
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= bad &lt;= n &lt;= 2<sup>31</sup> - 1</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0278-first-bad-version/solution.cpp)

```cpp
// The API isBadVersion is defined for you.
// bool isBadVersion(int version);

class Solution {
public:
    int firstBadVersion(int n) {

        
        long long int left = 0;
        long long int right = pow(2,31)-1;

        while(right>left+1){

            long long int m = left + (right-left)/2;

            if(isBadVersion(m)){
                right = m;
            }
            else{
                left = m;
            }

        }

        return right;
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
