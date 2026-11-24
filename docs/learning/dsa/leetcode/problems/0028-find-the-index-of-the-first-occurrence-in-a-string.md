# 28. Find The Index Of The First Occurrence In A String

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0028-find-the-index-of-the-first-occurrence-in-a-string)

## Problem

<p>Given two strings <code>needle</code> and <code>haystack</code>, return the index of the first occurrence of <code>needle</code> in <code>haystack</code>, or <code>-1</code> if <code>needle</code> is not part of <code>haystack</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> haystack = &quot;sadbutsad&quot;, needle = &quot;sad&quot;
<strong>Output:</strong> 0
<strong>Explanation:</strong> &quot;sad&quot; occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> haystack = &quot;leetcode&quot;, needle = &quot;leeto&quot;
<strong>Output:</strong> -1
<strong>Explanation:</strong> &quot;leeto&quot; did not occur in &quot;leetcode&quot;, so we return -1.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= haystack.length, needle.length &lt;= 10<sup>4</sup></code></li>
	<li><code>haystack</code> and <code>needle</code> consist of only lowercase English characters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0028-find-the-index-of-the-first-occurrence-in-a-string/solution.cpp)

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        // if length of both haystack and needle are equal then just compare the strings
        // if they are equal then return index 0
        // else return -1
        if(haystack.length()==needle.length()){
            if(haystack==needle){
                return 0;
            }
            else{
                return -1;
            }
        }
        // if length of the needle is greater than the length of the haystack
        // return -1 because it is impossible to fina needle in the haystack
        if(haystack.length()<needle.length()){
            return -1;
        }
        // traverse through the haystack
        for(int i=0; i<haystack.length()-needle.length()+1; i++){
            // declare a check variable
            bool check = true;
            // now for each index of haystack check if the next characters are forming
            // the string needle or not
            for(int j=i; j<needle.length()+i; j++){
                // if we get a nonmatching character then mark check as false and break
                // the loop
                if(haystack[j]!=needle[j-i]){
                    check = false;
                    break;
                }
            }
            // if we get check as true
            // which means we found needle in haystack
            // then return the index i
            if(check==true){
                return i;
            }
        }
        // return -1
        return -1;
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
