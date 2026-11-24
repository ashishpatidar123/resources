# 242. Valid Anagram

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0242-valid-anagram)

## Problem

<p>Given two strings <code>s</code> and <code>t</code>, return <code>true</code> if <code>t</code> is an <span data-keyword="anagram">anagram</span> of <code>s</code>, and <code>false</code> otherwise.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;anagram&quot;, t = &quot;nagaram&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;rat&quot;, t = &quot;car&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">false</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length, t.length &lt;= 5 * 10<sup>4</sup></code></li>
	<li><code>s</code> and <code>t</code> consist of lowercase English letters.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong> What if the inputs contain Unicode characters? How would you adapt your solution to such a case?</p>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0242-valid-anagram/solution.cpp)

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        
        int n = s.length();
        int m = t.length();

        if(n != m){
            return false;
        }

        vector<int>count1(26,0);
        vector<int>count2(26,0);

        for(int i=0; i<n; i++){
            count1[s[i]-'a']++;
        }
        for(int i=0; i<m; i++){
            count2[t[i]-'a']++;
        }
        for(int i=0; i<26; i++){
            if(count1[i] != count2[i]){
                return false;
            }
        }
        return true;
        
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
