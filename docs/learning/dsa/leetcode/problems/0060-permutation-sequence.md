# 60. Permutation Sequence

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0060-permutation-sequence)

## Problem

<p>The set <code>[1, 2, 3, ...,&nbsp;n]</code> contains a total of <code>n!</code> unique permutations.</p>

<p>By listing and labeling all of the permutations in order, we get the following sequence for <code>n = 3</code>:</p>

<ol>
	<li><code>&quot;123&quot;</code></li>
	<li><code>&quot;132&quot;</code></li>
	<li><code>&quot;213&quot;</code></li>
	<li><code>&quot;231&quot;</code></li>
	<li><code>&quot;312&quot;</code></li>
	<li><code>&quot;321&quot;</code></li>
</ol>

<p>Given <code>n</code> and <code>k</code>, return the <code>k<sup>th</sup></code> permutation sequence.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> n = 3, k = 3
<strong>Output:</strong> "213"
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> n = 4, k = 9
<strong>Output:</strong> "2314"
</pre><p><strong class="example">Example 3:</strong></p>
<pre><strong>Input:</strong> n = 3, k = 1
<strong>Output:</strong> "123"
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 9</code></li>
	<li><code>1 &lt;= k &lt;= n!</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0060-permutation-sequence/solution.cpp)

```cpp
class Solution {
    void generate(string &s, vector<string> &ans, int index){
        if(index>=s.length()){
            ans.push_back(s);
            return ;
        }
        for(int i=index; i<s.length(); i++){
            swap(s[index],s[i]);
            generate(s,ans,index+1);
            swap(s[index],s[i]);
        }
        
    }
public:
    string getPermutation(int n, int k) {
        string s ="";
        while(n>0){
            char c = n + '0';
            s.push_back(c);
            n--;
        }
        
        // vector<string> ans;
        // int index = 0;
        // generate(s,ans,index);
        // string temp ;
        // sort(ans.begin(),ans.end());
        // temp = ans[k-1];
        // return temp;
        while(k>0){
            next_permutation(s.begin(),s.begin()+s.length());
            k--;
        }
        return s;
    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
