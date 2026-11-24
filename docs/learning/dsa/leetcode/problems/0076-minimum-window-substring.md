# 76. Minimum Window Substring

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0076-minimum-window-substring)

## Problem

# Minimum Window Substring

### Difficulty: Hard
### Topics: Hash Table, String, Sliding Window

<p>Given two strings <code>s</code> and <code>t</code> of lengths <code>m</code> and <code>n</code> respectively, return <em>the <strong>minimum window</strong></em> <span data-keyword="substring-nonempty"><strong><em>substring</em></strong></span><em> of </em><code>s</code><em> such that every character in </em><code>t</code><em> (<strong>including duplicates</strong>) is included in the window</em>. If there is no such substring, return <em>the empty string </em><code>&quot;&quot;</code>.</p>

<p>The testcases will be generated such that the answer is <strong>unique</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;ADOBECODEBANC&quot;, t = &quot;ABC&quot;
<strong>Output:</strong> &quot;BANC&quot;
<strong>Explanation:</strong> The minimum window substring &quot;BANC&quot; includes &#39;A&#39;, &#39;B&#39;, and &#39;C&#39; from string t.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;a&quot;, t = &quot;a&quot;
<strong>Output:</strong> &quot;a&quot;
<strong>Explanation:</strong> The entire string s is the minimum window.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;a&quot;, t = &quot;aa&quot;
<strong>Output:</strong> &quot;&quot;
<strong>Explanation:</strong> Both &#39;a&#39;s from t must be included in the window.
Since the largest window of s only has one &#39;a&#39;, return empty string.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>m == s.length</code></li>
	<li><code>n == t.length</code></li>
	<li><code>1 &lt;= m, n &lt;= 10<sup>5</sup></code></li>
	<li><code>s</code> and <code>t</code> consist of uppercase and lowercase English letters.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong> Could you find an algorithm that runs in <code>O(m + n)</code> time?</p>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0076-minimum-window-substring/solution.cpp)

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        int m = s.size();
        int n = t.size();

        

        unordered_map<char,int>val;

        for(int i=0; i<n; i++){
            val[t[i]]++;
        }

        int l=0;
        int r=0;

        int len = INT_MAX;
        unordered_map<char,int>count;
        int formed = 0;
        int required = val.size();
        int start = 0;

        while(r < m){

            count[s[r]]++;

            if((val.find(s[r])!=val.end()) &&( count[s[r]] == val[s[r]])){
                formed++;
            }

            while((l <= r) && (formed==required)){
                if(r-l+1 < len){
                    len = r-l+1;
                    start = l;
                }

                count[s[l]]--;
                if((val.find(s[l])!=val.end()) && (count[s[l]] < val[s[l]])){
                    formed--;
                }

                l++;
            }
            r++;


        }
        
        if(len == INT_MAX){
            return "";
        }
        return s.substr(start, len);

    }
};
```

### `solution_2163552488.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0076-minimum-window-substring/solution_2163552488.cpp)

```cpp
class Solution {
public:
    string minWindow(string s, string t) {

        int m = s.size();
        int n = t.size();

        unordered_map<char,int> need;
        unordered_map<char,int> window;

        if( n > m) return "";

        for(int i=0; i<n; i++){
            need[t[i]]++;
        }

        int left = 0;
        int formed = 0;
        int required = need.size();

        string ans = "";
        int mini = INT_MAX;
        int start = 0;
        for(int right=0; right<m; right++){
            window[s[right]]++;

            if(need.find(s[right]) !=  need.end() && window[s[right]] == need[s[right]]){
                formed++;
            }

            while(formed == required){
                

                if(right - left + 1 < mini){
                    mini = right - left + 1;
                    start = left;
                }
                window[s[left]]--;
                if(need.find(s[left]) !=  need.end() && window[s[left]] < need[s[left]]){
                    formed--;
                }
                left++;
            }
        }
        ans = s.substr(start, mini);
        if(mini == INT_MAX) return "";
        return ans;


        
    }
};
```

### `solution_2163552856.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0076-minimum-window-substring/solution_2163552856.cpp)

```cpp
class Solution {
public:
    string minWindow(string s, string t) {

        int m = s.size();
        int n = t.size();

        unordered_map<char,int> need;
        unordered_map<char,int> window;

        if( n > m) return "";

        for(int i=0; i<n; i++){
            need[t[i]]++;
        }

        int left = 0;
        int formed = 0;
        int required = need.size();

        string ans = "";
        int mini = INT_MAX;
        int start = 0;
        for(int right=0; right<m; right++){
            window[s[right]]++;

            if(need.find(s[right]) !=  need.end() && window[s[right]] == need[s[right]]){
                formed++;
            }

            while(formed == required){
                

                if(right - left + 1 < mini){
                    mini = right - left + 1;
                    start = left;
                }
                window[s[left]]--;
                if(need.find(s[left]) !=  need.end() && window[s[left]] < need[s[left]]){
                    formed--;
                }
                left++;
            }
        }
        
        if(mini == INT_MAX) return "";
        ans = s.substr(start, mini);
        return ans;


        
    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
