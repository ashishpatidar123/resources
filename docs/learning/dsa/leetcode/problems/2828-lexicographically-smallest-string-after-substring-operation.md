# 2828. Lexicographically Smallest String After Substring Operation

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2828-lexicographically-smallest-string-after-substring-operation)

## Problem

<p>Given a string <code>s</code> consisting of lowercase English letters. Perform the following operation:</p>

<ul>
	<li>Select any non-empty <span data-keyword="substring-nonempty">substring</span> then replace every letter of the substring with the preceding letter of the English alphabet. For example, &#39;b&#39; is converted to &#39;a&#39;, and &#39;a&#39; is converted to &#39;z&#39;.</li>
</ul>

<p>Return the <span data-keyword="lexicographically-smaller-string"><strong>lexicographically smallest</strong></span> string <strong>after performing the operation</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;cbabc&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">&quot;baabc&quot;</span></p>

<p><strong>Explanation:</strong></p>

<p>Perform the operation on the substring starting at index 0, and ending at index 1 inclusive.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;aa&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">&quot;az&quot;</span></p>

<p><strong>Explanation:</strong></p>

<p>Perform the operation on the last letter.</p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;acbbc&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">&quot;abaab&quot;</span></p>

<p><strong>Explanation:</strong></p>

<p>Perform the operation on the substring starting at index 1, and ending at index 4 inclusive.</p>
</div>

<p><strong class="example">Example 4:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">s = &quot;leetcode&quot;</span></p>

<p><strong>Output:</strong> <span class="example-io">&quot;kddsbncd&quot;</span></p>

<p><strong>Explanation:</strong></p>

<p>Perform the operation on the entire string.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 3 * 10<sup>5</sup></code></li>
	<li><code>s</code> consists of lowercase English letters</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2828-lexicographically-smallest-string-after-substring-operation/solution.cpp)

```cpp
class Solution {
public:
    string smallestString(string s) {
        int index1 = s.length();
        int index2 = 0;

        for(int i=0; i<s.length(); i++){
            if(s[i]!='a'){
                index1 = i;
                break;
            }
        }
        if(index1==s.length()){
            s[index1-1] = 'z';
        }
        int i = index1+1;
        while(i<s.length() && s[i]!='a'){
            i++;
        }
        index2 = i-1;
        for(int i=index1; i<=index2; i++){
            s[i] = s[i]-1;
        }
        return s;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
