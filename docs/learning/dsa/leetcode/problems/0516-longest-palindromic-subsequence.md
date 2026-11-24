# 516. Longest Palindromic Subsequence

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0516-longest-palindromic-subsequence)

## Problem

<p>Given a string <code>s</code>, find <em>the longest palindromic <strong>subsequence</strong>&#39;s length in</em> <code>s</code>.</p>

<p>A <strong>subsequence</strong> is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;bbbab&quot;
<strong>Output:</strong> 4
<strong>Explanation:</strong> One possible longest palindromic subsequence is &quot;bbbb&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;cbbd&quot;
<strong>Output:</strong> 2
<strong>Explanation:</strong> One possible longest palindromic subsequence is &quot;bb&quot;.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 1000</code></li>
	<li><code>s</code> consists only of lowercase English letters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0516-longest-palindromic-subsequence/solution.cpp)

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string s) {

        int n = s.size();

        vector<vector<int>>dp(n, vector<int>(n,0));

        for(int i=0; i<n; i++){
            dp[i][i] = 1;
        }

        for(int i=n-1; i>=0; i--){
            for(int j=i+1; j<n; j++){
                if(s[i]==s[j]){
                    dp[i][j] = dp[i+1][j-1] + 2;
                }
                else{
                    dp[i][j] = max(dp[i+1][j],dp[i][j-1]);
                }
            }
        }
        return dp[0][n-1];
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
