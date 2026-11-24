# 125. Valid Palindrome

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0125-valid-palindrome)

## Problem

<p>A phrase is a <strong>palindrome</strong> if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.</p>

<p>Given a string <code>s</code>, return <code>true</code><em> if it is a <strong>palindrome</strong>, or </em><code>false</code><em> otherwise</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;A man, a plan, a canal: Panama&quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> &quot;amanaplanacanalpanama&quot; is a palindrome.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;race a car&quot;
<strong>Output:</strong> false
<strong>Explanation:</strong> &quot;raceacar&quot; is not a palindrome.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot; &quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> s is an empty string &quot;&quot; after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 2 * 10<sup>5</sup></code></li>
	<li><code>s</code> consists only of printable ASCII characters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0125-valid-palindrome/solution.cpp)

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        
        int n = s.length();

        int start = 0;
        int end = n-1;

        while(end>start){
            
            char c1 = s[start];
            char c2 = s[end];
            if(((c1>= 'a' && c1 <= 'z') || (c1 >= 'A' && c1 <='Z') || (c1 >= '0' && c1<= '9')) && 
                ((c2>= 'a' && c2 <= 'z') || (c2 >= 'A' && c2 <='Z') || (c2 >= '0' && c2 <= '9'))){

                if(tolower(c1) != tolower(c2)){
                    return false;
                }
                else{
                    start++;
                    end--;
                }
            }
            if((c1 < 'a'  || c1 >'z') && (c1 < 'A' || c1 > 'Z') && (c1 < '0' || c1 > '9')){
                start++;
            }
            if((c2 < 'a' || c2 >'z') && (c2 < 'A' || c2 > 'Z') && (c2 < '0' || c2 > '9')){
                end--;
            }

        }
        return true;

    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
