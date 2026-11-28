# 20. Valid Parentheses

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0020-valid-parentheses)

## Problem

# Valid Parentheses

### Difficulty: Easy
### Topics: String, Stack, Bracket Sequences

<p>Given a string <code>s</code> containing just the characters <code>&#39;(&#39;</code>, <code>&#39;)&#39;</code>, <code>&#39;{&#39;</code>, <code>&#39;}&#39;</code>, <code>&#39;[&#39;</code> and <code>&#39;]&#39;</code>, determine if the input string is valid.</p>

<p>An input string is valid if:</p>

<ol>
	<li>Open brackets must be closed by the same type of brackets.</li>
	<li>Open brackets must be closed in the correct order.</li>
	<li>Every close bracket has a corresponding open bracket of the same type.</li>
</ol>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;()&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;()[]{}&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;(]&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">false</span></p>
</div>

<p><strong class="example">Example 4:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;([])&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>
</div>

<p><strong class="example">Example 5:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;([)]&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">false</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 10<sup>4</sup></code></li>
	<li><code>s</code> consists of parentheses only <code>&#39;()[]{}&#39;</code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0020-valid-parentheses/solution.cpp)

```cpp
class Solution {
public:
    bool isValid(string s) {
        
        int n = s.length();

        stack<char>st;

        int i = 0;

        while(i<n){

            char c = s[i];

            if(!st.empty()){
                char t = st.top();

                if(c == ')' && t == '('){
                    st.pop();
                }
                else if(c == '}' && t == '{'){
                    st.pop();
                }
                else if(c == ']' && t == '['){
                    st.pop();
                }
                else if( c == '(' || c == '[' || c == '{'){
                    st.push(c);
                }
                else{
                    return false;
                }
            }
            else{
                st.push(c);
            }
            i++;

        }
        if(!st.empty()) return false;
        return true;
    }
};
```

### `solution_2163270495.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0020-valid-parentheses/solution_2163270495.cpp)

```cpp
class Solution {
    bool check(char open, char close){
        if(open == '(' && close == ')') return true;
        else if(open == '[' && close == ']') return true;
        else if(open == '{' && close == '}') return true;
        return false;
    }
public:
    bool isValid(string s) {

        int n = s.size();
        stack<char>st;

        int i = 0;

        while( i < n){
            if(s[i] == '{' || s[i] == '[' || s[i] == '('){
                st.push(s[i]);
            }
            else{
                if(st.empty()){
                    return false;
                }
                else{
                    char c = st.top();
                    if(check(c, s[i])){
                        st.pop();
                    }
                    else{
                        return false;
                    }
                }
            }
            i++;
            
        }
        if(!st.empty()){
            return false;
        }
        return true;
        
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
