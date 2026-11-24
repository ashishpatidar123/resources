# 567. Permutation In String

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0567-permutation-in-string)

## Problem

<p>Given two strings <code>s1</code> and <code>s2</code>, return <code>true</code> if <code>s2</code> contains a <span data-keyword="permutation-string">permutation</span> of <code>s1</code>, or <code>false</code> otherwise.</p>

<p>In other words, return <code>true</code> if one of <code>s1</code>&#39;s permutations is the substring of <code>s2</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s1 = &quot;ab&quot;, s2 = &quot;eidbaooo&quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> s2 contains one permutation of s1 (&quot;ba&quot;).
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s1 = &quot;ab&quot;, s2 = &quot;eidboaoo&quot;
<strong>Output:</strong> false
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s1.length, s2.length &lt;= 10<sup>4</sup></code></li>
	<li><code>s1</code> and <code>s2</code> consist of lowercase English letters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0567-permutation-in-string/solution.cpp)

```cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        vector<int> count1(26,0);

        for(int i=0; i<s1.length(); i++){
            count1[s1[i]-'a']++;
        }
        int windowSize = s1.length();

        if(s1.length()>s2.length()){
            return false;
        }
        
        // vector<int> count2(26,0);
        for(int i=0; i<s2.length()-windowSize+1; i++){
            
            vector<int> count3(26,0);
            for(int j=i; j<i+windowSize; j++){
                // count2[s2[j]-'a']++;
                count3[s2[j]-'a']++;
            }
            if(count1 == count3){
                return true;
            }
            // count2[s2[i]-'a']--;
            continue;

        }

        // if(count1 == count2){
        //     return true;
        // }
        return false;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
