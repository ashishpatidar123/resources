# 869. Similar String Groups

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0869-similar-string-groups)

## Problem

# Similar String Groups

### Difficulty: Hard
### Topics: Array, Hash Table, String, Depth-First Search, Breadth-First Search, Union-Find

<p>Two strings, <code>X</code> and <code>Y</code>, are considered similar if either they are identical or we can make them equivalent by swapping at most two letters (in distinct positions) within the string <code>X</code>.</p>

<p>For example, <code>&quot;tars&quot;</code>&nbsp;and <code>&quot;rats&quot;</code>&nbsp;are similar (swapping at positions <code>0</code> and <code>2</code>), and <code>&quot;rats&quot;</code> and <code>&quot;arts&quot;</code> are similar, but <code>&quot;star&quot;</code> is not similar to <code>&quot;tars&quot;</code>, <code>&quot;rats&quot;</code>, or <code>&quot;arts&quot;</code>.</p>

<p>Together, these form two connected groups by similarity: <code>{&quot;tars&quot;, &quot;rats&quot;, &quot;arts&quot;}</code> and <code>{&quot;star&quot;}</code>.&nbsp; Notice that <code>&quot;tars&quot;</code> and <code>&quot;arts&quot;</code> are in the same group even though they are not similar.&nbsp; Formally, each group is such that a word is in the group if and only if it is similar to at least one other word in the group.</p>

<p>We are given a list <code>strs</code> of strings where every string in <code>strs</code> is an anagram of every other string in <code>strs</code>. How many groups are there?</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;tars&quot;,&quot;rats&quot;,&quot;arts&quot;,&quot;star&quot;]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> strs = [&quot;omv&quot;,&quot;ovm&quot;]
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= strs.length &lt;= 300</code></li>
	<li><code>1 &lt;= strs[i].length &lt;= 300</code></li>
	<li><code>strs[i]</code> consists of lowercase letters only.</li>
	<li>All words in <code>strs</code> have the same length and are anagrams of each other.</li>
</ul>

## My C++ Submissions

### `solution_2153837244.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0869-similar-string-groups/solution_2153837244.cpp)

```cpp
class Solution {
    vector<int>parent;
    vector<int>rank;
    bool check(string s1, string s2){
        int count = 0;
        for(int i=0; i<s1.size(); i++){
            if(s1[i] != s2[i]) count++;
            if(count > 2) return false;
        }

        return true;
    }

    int find(int x){
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
    int numSimilarGroups(vector<string>& strs) {

        int n = strs.size();

        unordered_map<string, int> index;
        int idx = 0;
        for(int i=0; i<n; i++){
            if(index.find(strs[i]) == index.end()){
                index[strs[i]] = idx;
                idx++;
            }
        }
        parent.resize(idx); //parent array
        rank.resize(idx, 0); // rank array - height of the tree
        iota(parent.begin(), parent.end(),0);

        for(int i=0; i<n; i++){
            for(int j=i+1; j<n; j++){
                if(check(strs[i], strs[j])){
                    unite(index[strs[i]], index[strs[j]]);
                }
            }
        }

        set<int>s;

        for(int i=0; i<n; i++){
            int p = find(index[strs[i]]);
            s.insert(p);
        }

        return s.size();

        
    }
};
```

### `solution_2153840847.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0869-similar-string-groups/solution_2153840847.cpp)

```cpp
class Solution {
    vector<int>parent;
    vector<int>rank;
    bool check(const string& s1, const string& s2){
        int count = 0;
        for(int i=0; i<s1.size(); i++){
            if(s1[i] != s2[i]) count++;
            if(count > 2) return false;
        }

        return true;
    }

    int find(int x){
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
    int numSimilarGroups(vector<string>& strs) {

        int n = strs.size();

        // unordered_map<string, int> index;
        // int idx = 0;
        // for(int i=0; i<n; i++){
        //     if(index.find(strs[i]) == index.end()){
        //         index[strs[i]] = idx;
        //         idx++;
        //     }
        // }
        parent.resize(n); //parent array
        rank.resize(n, 0); // rank array - height of the tree
        iota(parent.begin(), parent.end(),0);
        int ans = n;
        for(int i=0; i<n; i++){
            for(int j=i+1; j<n; j++){
                if(find(i) == find(j)){
                    continue;
                }
                if(check(strs[i], strs[j])){
                    unite(i,j);
                    ans--;
                }
            }
        }

        // set<int>s;

        // for(int i=0; i<n; i++){
        //     int p = find(i);
        //     s.insert(p);
        // }

        // return s.size();

        return ans;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
