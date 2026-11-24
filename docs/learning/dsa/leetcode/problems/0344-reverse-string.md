# 344. Reverse String

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0344-reverse-string)

## Problem

<p>Write a function that reverses a string. The input string is given as an array of characters <code>s</code>.</p>

<p>You must do this by modifying the input array <a href="https://en.wikipedia.org/wiki/In-place_algorithm" target="_blank">in-place</a> with <code>O(1)</code> extra memory.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> s = ["h","e","l","l","o"]
<strong>Output:</strong> ["o","l","l","e","h"]
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> s = ["H","a","n","n","a","h"]
<strong>Output:</strong> ["h","a","n","n","a","H"]
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 10<sup>5</sup></code></li>
	<li><code>s[i]</code> is a <a href="https://en.wikipedia.org/wiki/ASCII#Printable_characters" target="_blank">printable ascii character</a>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0344-reverse-string/solution.cpp)

```cpp
class Solution {
    void reverse(vector<char>& s, int i, int j){
        if(i>j){
            return;
        }
        swap(s[i],s[j]);
        i++;
        j--;
        return reverse(s,i,j);
    }
public:
    void reverseString(vector<char>& s) {
        // int start = 0;
        // int end = s.size()-1;

        // while(start<end){
        //     swap(s[start++],s[end--]);
        // }
        int i = 0;
        int j = s.size()-1;
        reverse(s,i,j);

    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
