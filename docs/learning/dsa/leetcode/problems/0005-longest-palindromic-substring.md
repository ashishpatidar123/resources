# 5. Longest Palindromic Substring

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0005-longest-palindromic-substring)

## Problem

<p>Given a string <code>s</code>, return <em>the longest</em> <span data-keyword="palindromic-string"><em>palindromic</em></span> <span data-keyword="substring-nonempty"><em>substring</em></span> in <code>s</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;babad&quot;
<strong>Output:</strong> &quot;bab&quot;
<strong>Explanation:</strong> &quot;aba&quot; is also a valid answer.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;cbbd&quot;
<strong>Output:</strong> &quot;bb&quot;
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 1000</code></li>
	<li><code>s</code> consist of only digits and English letters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0005-longest-palindromic-substring/solution.cpp)

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int n = s.size();
        
        int left = 0;
        int right = n-1;
        int max_len = 0;
        for(int c = 0; c < 2*n-1; c++){
            int l = c/2;
            int r = l + c%2;

            while(l>=0 && r<n && s[l]==s[r]){
                int len = r-l+1;
                if(len > max_len){
                    max_len = len;
                    left = l;
                    right = r;
                }
                r++;
                l--;
            }
        }
        string ans = "";
        for(int i=left; i<=right; i++){
            ans += s[i];
        }
        return ans;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
