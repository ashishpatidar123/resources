# 438. Find All Anagrams In A String

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0438-find-all-anagrams-in-a-string)

## Problem

# Find All Anagrams in a String

### Difficulty: Medium
### Topics: Hash Table, String, Sliding Window

<p>Given two strings <code>s</code> and <code>p</code>, return an array of all the start indices of <code>p</code>&#39;s <span data-keyword="anagram">anagrams</span> in <code>s</code>. You may return the answer in <strong>any order</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;cbaebabacd&quot;, p = &quot;abc&quot;
<strong>Output:</strong> [0,6]
<strong>Explanation:</strong>
The substring with start index = 0 is &quot;cba&quot;, which is an anagram of &quot;abc&quot;.
The substring with start index = 6 is &quot;bac&quot;, which is an anagram of &quot;abc&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;abab&quot;, p = &quot;ab&quot;
<strong>Output:</strong> [0,1,2]
<strong>Explanation:</strong>
The substring with start index = 0 is &quot;ab&quot;, which is an anagram of &quot;ab&quot;.
The substring with start index = 1 is &quot;ba&quot;, which is an anagram of &quot;ab&quot;.
The substring with start index = 2 is &quot;ab&quot;, which is an anagram of &quot;ab&quot;.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length, p.length &lt;= 3 * 10<sup>4</sup></code></li>
	<li><code>s</code> and <code>p</code> consist of lowercase English letters.</li>
</ul>

## My C++ Submissions

### `solution_2163534585.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0438-find-all-anagrams-in-a-string/solution_2163534585.cpp)

```cpp
class Solution {
    bool check(vector<int>& freq, vector<int>& window){
        for(int i=0; i<26; i++){
            if(freq[i] != window[i]) return false;
        }
        return true;
    }
public:
    vector<int> findAnagrams(string s, string p) {

        int m = s.length();
        int n = p.length();

        vector<int>freq(26,0);
        vector<int>window(26,0);
        if( n > m) return {}; 
        for(int i=0; i<n; i++){
            freq[p[i] - 'a']++;
            window[s[i] - 'a']++;
        }

        vector<int>ans;

        for(int i=0; i<=m-n; i++){
            
            if(i >= 1 ){
                window[s[i-1] - 'a']--;
                window[s[i+n-1] - 'a']++;
            }
            if(check(freq, window)){
                ans.push_back(i);
            }

        }
        return ans;
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
