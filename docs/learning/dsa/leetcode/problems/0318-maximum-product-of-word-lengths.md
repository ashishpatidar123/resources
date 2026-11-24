# 318. Maximum Product Of Word Lengths

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0318-maximum-product-of-word-lengths)

## Problem

<p>Given a string array <code>words</code>, return <em>the maximum value of</em> <code>length(word[i]) * length(word[j])</code> <em>where the two words do not share common letters</em>. If no such two words exist, return <code>0</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> words = [&quot;abcw&quot;,&quot;baz&quot;,&quot;foo&quot;,&quot;bar&quot;,&quot;xtfn&quot;,&quot;abcdef&quot;]
<strong>Output:</strong> 16
<strong>Explanation:</strong> The two words can be &quot;abcw&quot;, &quot;xtfn&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> words = [&quot;a&quot;,&quot;ab&quot;,&quot;abc&quot;,&quot;d&quot;,&quot;cd&quot;,&quot;bcd&quot;,&quot;abcd&quot;]
<strong>Output:</strong> 4
<strong>Explanation:</strong> The two words can be &quot;ab&quot;, &quot;cd&quot;.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> words = [&quot;a&quot;,&quot;aa&quot;,&quot;aaa&quot;,&quot;aaaa&quot;]
<strong>Output:</strong> 0
<strong>Explanation:</strong> No such pair of words.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= words.length &lt;= 1000</code></li>
	<li><code>1 &lt;= words[i].length &lt;= 1000</code></li>
	<li><code>words[i]</code> consists only of lowercase English letters.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0318-maximum-product-of-word-lengths/solution.cpp)

```cpp
class Solution {
public:
    int maxProduct(vector<string>& words) {

        int n = words.size();
        // vector<vector<int>>mask(n, vector<int>(26,0));
        // for(int i=0; i<n; i++){
        //     string s = words[i];
            
        //     for(int j=0; j<s.size(); j++){
        //         mask[i][s[j]-'a'] = 1;
        //     }

        // }

        // int ans = 0;

        // for(int i=0; i<n; i++){
        //     for(int j=i+1; j<n; j++){

        //         bool check = true;
        //         for(int l=0; l<26; l++){
        //             if((mask[i][l] & mask[j][l]) == 1){
        //                 check = false;
        //                 break;
        //             }
        //         }
        //         if(check){
        //             int len1 = words[i].size();
        //             int len2 = words[j].size();

        //             ans = max(ans, len1*len2);
        //         }
        //     }
        // }

        // return ans;

        // creating bitmask for letters
        vector<int>mask(n,0);
        int ans = 0;
        for(int i=0; i<n; i++){
            for(char c:words[i]){
                // setting the bit corresponding to that letter
                mask[i] = mask[i] | (1 << (c - 'a')); 
            }
        }
        for(int i=0; i<n; i++){
            for(int j=i+1; j<n; j++){
                if((mask[i]&mask[j]) == 0){
                    int len1 = words[i].size();
                    int len2 = words[j].size();

                    ans = max(ans, len1*len2);
                }
            }
        }
        return ans;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
