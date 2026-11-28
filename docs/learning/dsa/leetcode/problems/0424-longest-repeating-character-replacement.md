# 424. Longest Repeating Character Replacement

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0424-longest-repeating-character-replacement)

## Problem

<p>You are given a string <code>s</code> and an integer <code>k</code>. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most <code>k</code> times.</p>

<p>Return <em>the length of the longest substring containing the same letter you can get after performing the above operations</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;ABAB&quot;, k = 2
<strong>Output:</strong> 4
<strong>Explanation:</strong> Replace the two &#39;A&#39;s with two &#39;B&#39;s or vice versa.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;AABABBA&quot;, k = 1
<strong>Output:</strong> 4
<strong>Explanation:</strong> Replace the one &#39;A&#39; in the middle with &#39;B&#39; and form &quot;AABBBBA&quot;.
The substring &quot;BBBB&quot; has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 10<sup>5</sup></code></li>
	<li><code>s</code> consists of only uppercase English letters.</li>
	<li><code>0 &lt;= k &lt;= s.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0424-longest-repeating-character-replacement/solution.cpp)

```cpp
class Solution {
public:
    int characterReplacement(string s, int k) {

        int n = s.size();
        int ans = 0;
        set<char>st;
        for(int i=0; i<n; i++){
            st.insert(s[i]);
        }
        for(char c='A'; c<='Z'; c++){

            int count = 0;
            int l=0;
            int r=0;
            if(st.find(c) != st.end()){
                while(r<n){
                    if(s[r] != c){
                        count++;
                    }

                    if(count > k){
                        if(s[l]!=c){
                            count--;
                        }
                        l++;
                    }
                    int len = r-l+1;
                    ans = max(ans, len);
                    r++;
                }
            }

        }

        return ans;

        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
