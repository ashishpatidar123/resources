# 14. Longest Common Prefix

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0014-longest-common-prefix)

## Problem

<p>Write a function to find the longest common prefix string amongst an array of strings.</p>

<p>If there is no common prefix, return an empty string <code>&quot;&quot;</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;flower&quot;,&quot;flow&quot;,&quot;flight&quot;]
<strong>Output:</strong> &quot;fl&quot;
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;dog&quot;,&quot;racecar&quot;,&quot;car&quot;]
<strong>Output:</strong> &quot;&quot;
<strong>Explanation:</strong> There is no common prefix among the input strings.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= strs.length &lt;= 200</code></li>
	<li><code>0 &lt;= strs[i].length &lt;= 200</code></li>
	<li><code>strs[i]</code> consists of only lowercase English letters if it is non-empty.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0014-longest-common-prefix/solution.cpp)

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        
        string ans = "";

        int n = strs.size();
        if(n==1){
            return strs[0];
        }
        // sort(strs.begin(),strs.end());

        string first = strs[0];
        int l = first.size();
       
        bool flag = true;
        for(int i=0; i<l; i++){

            char c = first[i];

            for(int j=1; j<n; j++){

                if(strs[j].size() > i){
                    if(strs[j][i] != c){
                        flag = false;
                        break;
                    }
                    
                }
                else{
                    return ans;
                }

            }
            if(flag){
                ans += c;
            }
            else{
                return ans;
            }

        }
        
        return ans;
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
