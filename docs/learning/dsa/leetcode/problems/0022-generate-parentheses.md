# 22. Generate Parentheses

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0022-generate-parentheses)

## Problem

<p>Given <code>n</code> pairs of parentheses, write a function to <em>generate all combinations of well-formed parentheses</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> n = 3
<strong>Output:</strong> ["((()))","(()())","(())()","()(())","()()()"]
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> n = 1
<strong>Output:</strong> ["()"]
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 8</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0022-generate-parentheses/solution.cpp)

```cpp
class Solution {
public:
    vector<string>ans;
    void solve(string s, int open, int close, int n){

        if(s.length() == 2*n){
            ans.push_back(s);
            return;
        }

        if(open < n){
            solve(s + '(' , open+1, close, n);
        }
        if(close < open){
            solve(s + ')', open, close+1, n);
        }

    }
    vector<string> generateParenthesis(int n) {
        
        solve("", 0, 0, n);
        return ans;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
