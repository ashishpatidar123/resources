# 32. Longest Valid Parentheses

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0032-longest-valid-parentheses)

## Problem

<p>Given a string containing just the characters <code>&#39;(&#39;</code> and <code>&#39;)&#39;</code>, return <em>the length of the longest valid (well-formed) parentheses </em><span data-keyword="substring-nonempty"><em>substring</em></span>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;(()&quot;
<strong>Output:</strong> 2
<strong>Explanation:</strong> The longest valid parentheses substring is &quot;()&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;)()())&quot;
<strong>Output:</strong> 4
<strong>Explanation:</strong> The longest valid parentheses substring is &quot;()()&quot;.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;&quot;
<strong>Output:</strong> 0
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>0 &lt;= s.length &lt;= 3 * 10<sup>4</sup></code></li>
	<li><code>s[i]</code> is <code>&#39;(&#39;</code>, or <code>&#39;)&#39;</code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0032-longest-valid-parentheses/solution.cpp)

```cpp
class Solution {
public:
    int longestValidParentheses(string s) {
        
        int n = s.length();

        int left = 0;
        int right = 0;
        int maxi = 0;

        for(int i=0; i<n; i++){
            if(s[i] == '('){
                left++;
            }
            else{
                right++;
            }

            if(left == right){
                maxi = max(maxi, 2*right);
            }
            else if(right > left){
                left = 0;
                right = 0;
            }

        }
        left = 0;
        right = 0;
        for(int i=n-1; i>=0; i--){
            if(s[i] == '('){
                left++;
            }
            else{
                right++;
            }
            if(left == right){
                maxi = max(maxi, 2*left);
            }
            else if(left > right){
                left = 0;
                right= 0;
            }
        }
        return maxi;

    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
