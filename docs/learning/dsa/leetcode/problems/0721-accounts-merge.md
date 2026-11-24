# 721. Accounts Merge

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0721-accounts-merge)

## Problem

# Accounts Merge

### Difficulty: Medium
### Topics: Array, Hash Table, String, Depth-First Search, Breadth-First Search, Union-Find, Sorting

<p>Given a list of <code>accounts</code> where each element <code>accounts[i]</code> is a list of strings, where the first element <code>accounts[i][0]</code> is a name, and the rest of the elements are <strong>emails</strong> representing emails of the account.</p>

<p>Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.</p>

<p>After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails <strong>in sorted order</strong>. The accounts themselves can be returned in <strong>any order</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> accounts = [[&quot;John&quot;,&quot;johnsmith@mail.com&quot;,&quot;john_newyork@mail.com&quot;],[&quot;John&quot;,&quot;johnsmith@mail.com&quot;,&quot;john00@mail.com&quot;],[&quot;Mary&quot;,&quot;mary@mail.com&quot;],[&quot;John&quot;,&quot;johnnybravo@mail.com&quot;]]
<strong>Output:</strong> [[&quot;John&quot;,&quot;john00@mail.com&quot;,&quot;john_newyork@mail.com&quot;,&quot;johnsmith@mail.com&quot;],[&quot;Mary&quot;,&quot;mary@mail.com&quot;],[&quot;John&quot;,&quot;johnnybravo@mail.com&quot;]]
<strong>Explanation:</strong>
The first and second John&#39;s are the same person as they have the common email &quot;johnsmith@mail.com&quot;.
The third John and Mary are different people as none of their email addresses are used by other accounts.
We could return these lists in any order, for example the answer [[&#39;Mary&#39;, &#39;mary@mail.com&#39;], [&#39;John&#39;, &#39;johnnybravo@mail.com&#39;], 
[&#39;John&#39;, &#39;john00@mail.com&#39;, &#39;john_newyork@mail.com&#39;, &#39;johnsmith@mail.com&#39;]] would still be accepted.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> accounts = [[&quot;Gabe&quot;,&quot;Gabe0@m.co&quot;,&quot;Gabe3@m.co&quot;,&quot;Gabe1@m.co&quot;],[&quot;Kevin&quot;,&quot;Kevin3@m.co&quot;,&quot;Kevin5@m.co&quot;,&quot;Kevin0@m.co&quot;],[&quot;Ethan&quot;,&quot;Ethan5@m.co&quot;,&quot;Ethan4@m.co&quot;,&quot;Ethan0@m.co&quot;],[&quot;Hanzo&quot;,&quot;Hanzo3@m.co&quot;,&quot;Hanzo1@m.co&quot;,&quot;Hanzo0@m.co&quot;],[&quot;Fern&quot;,&quot;Fern5@m.co&quot;,&quot;Fern1@m.co&quot;,&quot;Fern0@m.co&quot;]]
<strong>Output:</strong> [[&quot;Ethan&quot;,&quot;Ethan0@m.co&quot;,&quot;Ethan4@m.co&quot;,&quot;Ethan5@m.co&quot;],[&quot;Gabe&quot;,&quot;Gabe0@m.co&quot;,&quot;Gabe1@m.co&quot;,&quot;Gabe3@m.co&quot;],[&quot;Hanzo&quot;,&quot;Hanzo0@m.co&quot;,&quot;Hanzo1@m.co&quot;,&quot;Hanzo3@m.co&quot;],[&quot;Kevin&quot;,&quot;Kevin0@m.co&quot;,&quot;Kevin3@m.co&quot;,&quot;Kevin5@m.co&quot;],[&quot;Fern&quot;,&quot;Fern0@m.co&quot;,&quot;Fern1@m.co&quot;,&quot;Fern5@m.co&quot;]]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= accounts.length &lt;= 1000</code></li>
	<li><code>2 &lt;= accounts[i].length &lt;= 10</code></li>
	<li><code>1 &lt;= accounts[i][j].length &lt;= 30</code></li>
	<li><code>accounts[i][0]</code> consists of English letters.</li>
	<li><code>accounts[i][j] (for j &gt; 0)</code> is a valid email.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0721-accounts-merge/solution.cpp)

```cpp
class Solution {
    vector<int> parent;
    vector<int> rank;

    int find(int x){
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);

        if(px == py) return;

        if(rank[px] < rank[py]){
            swap(px, py);
        }
        parent[py] = px;

        if(rank[px] == rank[py]){
            rank[px]++;
        }
    }
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {

        unordered_map<string, int> index;
        unordered_map<string, string>names;

        int id = 0;

        for(auto& acc:accounts){
            string name = acc[0];
            for(int i=1; i<acc.size(); i++){
                if(index.find(acc[i]) == index.end()){
                    index[acc[i]] = id++;
                }
                names[acc[i]] = name;
            }
        }


        parent.resize(id);
        rank.resize(id, 0);
        iota(parent.begin(), parent.end(),0);

        for(auto& acc:accounts){
            int first = index[acc[1]];

            for(int i=2; i<acc.size(); i++){
                unite(first, index[acc[i]]);
            }
        }

        unordered_map<int, vector<string>> roots;
        for(auto& [email, id] :  index){
            roots[find(id)].push_back(email);

        }

        vector<vector<string>> result;
        for(auto& [root, emails] : roots){
            sort(emails.begin(), emails.end());
            string name = names[emails[0]];
            emails.insert(emails.begin(), name);
            result.push_back(emails);
        }

        return result;

        

        

        
        
    }
};
```

### `solution_2152416293.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0721-accounts-merge/solution_2152416293.cpp)

```cpp
class Solution {
    vector<int> parent;
    vector<int> rank;

    int find(int x){
        // if(parent[x] != x){
        //     parent[x] = find(parent[x]);
        // }
        // return parent[x];
        if(x == parent[x]){
            return x;
        }
        return find(parent[x]);
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);

        if(px == py) return;

        if(rank[px] < rank[py]){
            swap(px, py);
        }
        parent[py] = px;

        if(rank[px] == rank[py]){
            rank[px]++;
        }
    }
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {

        unordered_map<string, int> index;
        unordered_map<string, string>names;

        int id = 0;

        for(auto& acc:accounts){
            string name = acc[0];
            for(int i=1; i<acc.size(); i++){
                if(index.find(acc[i]) == index.end()){
                    index[acc[i]] = id++;
                }
                names[acc[i]] = name;
            }
        }


        parent.resize(id);
        rank.resize(id, 0);
        iota(parent.begin(), parent.end(),0);

        for(auto& acc:accounts){
            int first = index[acc[1]];

            for(int i=2; i<acc.size(); i++){
                unite(first, index[acc[i]]);
            }
        }

        unordered_map<int, vector<string>> roots;
        for(auto& [email, id] :  index){
            roots[find(id)].push_back(email);

        }

        vector<vector<string>> result;
        for(auto& [root, emails] : roots){
            sort(emails.begin(), emails.end());
            string name = names[emails[0]];
            emails.insert(emails.begin(), name);
            result.push_back(emails);
        }

        return result;

        

        

        
        
    }
};
```

### `solution_2152422859.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0721-accounts-merge/solution_2152422859.cpp)

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
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {

        unordered_map<string, int> index; // mapping each email to an index value
        unordered_map<string, string>names; // mapping each email to it's owner name

        int id = 0;

        for(auto& acc:accounts){
            string name = acc[0];
            for(int i=1; i<acc.size(); i++){
                if(index.find(acc[i]) == index.end()){
                    index[acc[i]] = id++;
                }
                names[acc[i]] = name;
            }
        }


        parent.resize(id); //parent array
        rank.resize(id, 0); // rank array - height of the tree
        iota(parent.begin(), parent.end(),0); // setting parent to all indexes to 0 so currently each
        // email belongs to a seperate set

        for(auto& acc:accounts){
            int first = index[acc[1]];
            // taking the first email's index from each list
            for(int i=2; i<acc.size(); i++){
                // adding all other emails to this first email set, because they all belong
                // to the same person
                unite(first, index[acc[i]]);
            }
        }

        unordered_map<int, vector<string>> roots;
        // now we will mow find all these new sets
        for(auto& [email, id] :  index){
            // for each email, id pair, we will store them in the common vector based on parent's index
            // they share same parent
            roots[find(id)].push_back(email);

        }

        vector<vector<string>> result; // result creation
        for(auto& [root, emails] : roots){
            // sort emails first
            sort(emails.begin(), emails.end());
            // now use the names mapping to find the name of the owner - can use any email 
            string name = names[emails[0]];
            // add that name to the first position to frame the output
            emails.insert(emails.begin(), name);
            // push it into the result
            result.push_back(emails);
        }

        return result;

        

        

        
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
