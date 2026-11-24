# 1058. Lexicographically Smallest Equivalent String

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1058-lexicographically-smallest-equivalent-string)

## Problem

# Lexicographically Smallest Equivalent String

### Difficulty: Medium
### Topics: String, Union-Find

<p>You are given two strings of the same length <code>s1</code> and <code>s2</code> and a string <code>baseStr</code>.</p>

<p>We say <code>s1[i]</code> and <code>s2[i]</code> are equivalent characters.</p>

<ul>
	<li>For example, if <code>s1 = &quot;abc&quot;</code> and <code>s2 = &quot;cde&quot;</code>, then we have <code>&#39;a&#39; == &#39;c&#39;</code>, <code>&#39;b&#39; == &#39;d&#39;</code>, and <code>&#39;c&#39; == &#39;e&#39;</code>.</li>
</ul>

<p>Equivalent characters follow the usual rules of any equivalence relation:</p>

<ul>
	<li><strong>Reflexivity:</strong> <code>&#39;a&#39; == &#39;a&#39;</code>.</li>
	<li><strong>Symmetry:</strong> <code>&#39;a&#39; == &#39;b&#39;</code> implies <code>&#39;b&#39; == &#39;a&#39;</code>.</li>
	<li><strong>Transitivity:</strong> <code>&#39;a&#39; == &#39;b&#39;</code> and <code>&#39;b&#39; == &#39;c&#39;</code> implies <code>&#39;a&#39; == &#39;c&#39;</code>.</li>
</ul>

<p>For example, given the equivalency information from <code>s1 = &quot;abc&quot;</code> and <code>s2 = &quot;cde&quot;</code>, <code>&quot;acd&quot;</code> and <code>&quot;aab&quot;</code> are equivalent strings of <code>baseStr = &quot;eed&quot;</code>, and <code>&quot;aab&quot;</code> is the lexicographically smallest equivalent string of <code>baseStr</code>.</p>

<p>Return <em>the lexicographically smallest equivalent string of </em><code>baseStr</code><em> by using the equivalency information from </em><code>s1</code><em> and </em><code>s2</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s1 = &quot;parker&quot;, s2 = &quot;morris&quot;, baseStr = &quot;parser&quot;
<strong>Output:</strong> &quot;makkek&quot;
<strong>Explanation:</strong> Based on the equivalency information in s1 and s2, we can group their characters as [m,p], [a,o], [k,r,s], [e,i].
The characters in each group are equivalent and sorted in lexicographical order.
So the answer is &quot;makkek&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s1 = &quot;hello&quot;, s2 = &quot;world&quot;, baseStr = &quot;hold&quot;
<strong>Output:</strong> &quot;hdld&quot;
<strong>Explanation: </strong>Based on the equivalency information in s1 and s2, we can group their characters as [h,w], [d,e,o], [l,r].
So only the second letter &#39;o&#39; in baseStr is changed to &#39;d&#39;, the answer is &quot;hdld&quot;.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s1 = &quot;leetcode&quot;, s2 = &quot;programs&quot;, baseStr = &quot;sourcecode&quot;
<strong>Output:</strong> &quot;aauaaaaada&quot;
<strong>Explanation:</strong> We group the equivalent characters in s1 and s2 as [a,o,e,r,s,c], [l,p], [g,t] and [d,m], thus all letters in baseStr except &#39;u&#39; and &#39;d&#39; are transformed to &#39;a&#39;, the answer is &quot;aauaaaaada&quot;.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s1.length, s2.length, baseStr &lt;= 1000</code></li>
	<li><code>s1.length == s2.length</code></li>
	<li><code>s1</code>, <code>s2</code>, and <code>baseStr</code> consist of lowercase English letters.</li>
</ul>

## My C++ Submissions

### `solution_2153821776.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1058-lexicographically-smallest-equivalent-string/solution_2153821776.cpp)

```cpp
class Solution {
    vector<int> parent;
    vector<int> rank;

    int find(int x){
        // move up in the tree to reach the root node, because root node has parent equal to itself
        // also while doing this map each node to root only
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);
        // if both belongs to same set then no unite
        if(px == py) return;
        // check the height of the trees, we will add the smaller to larger one
        if(rank[px] < rank[py]){
            swap(px, py);
        }
        // now make the parent of smaller tree as large tree
        parent[py] = px;
        // if their current ranks are same then on addition rank (height increases by 1)
        if(rank[px] == rank[py]){
            rank[px]++;
        }
    }
public:
    string smallestEquivalentString(string s1, string s2, string baseStr) {

        int n = s1.size();
        int m = baseStr.size();

        parent.resize(26);
        for(int i=0; i<26; i++){
            parent[i] = i;
        }
        rank.assign(26, 0); // rank array - height of the tree

        for(int i=0; i<n; i++){
            unite(s1[i] - 'a', s2[i] - 'a'); 
        }

        unordered_map<int, vector<char>> roots;
        for(int i=0; i<26; i++){
            roots[find(i)].push_back(i + 'a');

        }
        for(auto& [id, list] :  roots){
            sort(list.begin(), list.end());
        }
        string ans = "";
        for(int i=0; i<m; i++){
            int indx = find(baseStr[i] - 'a');
            char c = roots[indx][0];
           
            ans += c;
        }

        return ans;


        
    }
};
```

### `solution_2153824186.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/1058-lexicographically-smallest-equivalent-string/solution_2153824186.cpp)

```cpp
class Solution {
    int parent[26];
    

    int find(int x){
        // move up in the tree to reach the root node, because root node has parent equal to itself
        // also while doing this map each node to root only
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);
        // if both belongs to same set then no unite
        if(px == py) return;
        if(px != py){
            // union by value because we need the smallest character at the root
            if(px < py){
                parent[py] = px;
            }
            else{
                parent[px] = py;
            }
        }
    }
public:
    string smallestEquivalentString(string s1, string s2, string baseStr) {

        int n = s1.size();
        int m = baseStr.size();

       
        for(int i=0; i<26; i++){
            parent[i] = i;
        }
      

        for(int i=0; i<n; i++){
            unite(s1[i] - 'a', s2[i] - 'a'); 
        }

        
        string ans = "";
        for(int i=0; i<m; i++){
            int indx = find(baseStr[i] - 'a');
            char c = indx + 'a';
           
            ans += c;
        }

        return ans;


        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
