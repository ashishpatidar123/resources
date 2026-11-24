# 433. Minimum Genetic Mutation

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0433-minimum-genetic-mutation)

## Problem

<p>A gene string can be represented by an 8-character long string, with choices from <code>&#39;A&#39;</code>, <code>&#39;C&#39;</code>, <code>&#39;G&#39;</code>, and <code>&#39;T&#39;</code>.</p>

<p>Suppose we need to investigate a mutation from a gene string <code>startGene</code> to a gene string <code>endGene</code> where one mutation is defined as one single character changed in the gene string.</p>

<ul>
	<li>For example, <code>&quot;AACCGGTT&quot; --&gt; &quot;AACCGGTA&quot;</code> is one mutation.</li>
</ul>

<p>There is also a gene bank <code>bank</code> that records all the valid gene mutations. A gene must be in <code>bank</code> to make it a valid gene string.</p>

<p>Given the two gene strings <code>startGene</code> and <code>endGene</code> and the gene bank <code>bank</code>, return <em>the minimum number of mutations needed to mutate from </em><code>startGene</code><em> to </em><code>endGene</code>. If there is no such a mutation, return <code>-1</code>.</p>

<p>Note that the starting point is assumed to be valid, so it might not be included in the bank.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> startGene = &quot;AACCGGTT&quot;, endGene = &quot;AACCGGTA&quot;, bank = [&quot;AACCGGTA&quot;]
<strong>Output:</strong> 1
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> startGene = &quot;AACCGGTT&quot;, endGene = &quot;AAACGGTA&quot;, bank = [&quot;AACCGGTA&quot;,&quot;AACCGCTA&quot;,&quot;AAACGGTA&quot;]
<strong>Output:</strong> 2
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>0 &lt;= bank.length &lt;= 10</code></li>
	<li><code>startGene.length == endGene.length == bank[i].length == 8</code></li>
	<li><code>startGene</code>, <code>endGene</code>, and <code>bank[i]</code> consist of only the characters <code>[&#39;A&#39;, &#39;C&#39;, &#39;G&#39;, &#39;T&#39;]</code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0433-minimum-genetic-mutation/solution.cpp)

```cpp
class Solution {
public:
    bool diff(string& first, string& second){
        int n = 8;
        int count = 0;
        for(int i=0; i<n; i++){
            if(first[i] != second[i]){
                count++;
            }
        }
        if(count == 1){
            return true;
        }
        return false;
    }
    int minMutation(string startGene, string endGene, vector<string>& bank) {
        
        // int n = bank.size();

        // unordered_map<string, vector<string>>graph;

        // for(int i=0; i<n; i++){
        //     if(bank[i] == startGene) continue;
        //     if(diff(startGene, bank[i])){
        //         graph[startGene].push_back(bank[i]);
        //         graph[bank[i]].push_back(startGene);
        //     }
        // }
        // for(int i=0; i<n; i++){
        //     for(int j=i+1; j<n; j++){
        //         if(bank[i] == startGene || bank[j] == startGene) continue;
        //         if(diff(bank[i], bank[j])){
        //             graph[bank[i]].push_back(bank[j]);
        //             graph[bank[j]].push_back(bank[i]);
        //         }
        //     }
        // }

        // unordered_map<string, bool>visited;
        // queue<pair<string, int>>q;
        // int step = 0;

        // q.push({startGene,0});
        // visited[startGene] = true;

        // while(!q.empty()){
        //     auto entry = q.front();
        //     q.pop();
        //     string gene = entry.first;
        //     int step = entry.second;
        //     if(gene == endGene){
        //         return step;
        //     }

        //     for(string nbr : graph[gene]){
        //         if(visited.find(nbr) == visited.end()){
        //             visited[nbr] = true;
        //             q.push({nbr, step+1});
        //         }
        //     }
        // }

        // return -1;

        unordered_set<string>bankCheck(bank.begin(),bank.end()); // this if for checking valid genes in O(1)

        if(bankCheck.find(endGene) == bankCheck.end()) return -1; // if the endGene is not valid then we can mutate to it

        queue<string>q;
        q.push(startGene);

        int count = 0;
        char choices[] = {'A', 'C', 'G', 'T'};

        while(!q.empty()){
            int size = q.size();

            for(int i=0; i<size; i++){
                string curr = q.front();
                q.pop();

                if(curr == endGene){
                    return count;
                }

                for(int j=0; j<8; j++){
                    char original = curr[j];

                    for(auto c : choices){
                        if(c == original) continue;

                        curr[j] = c;

                        if(bankCheck.count(curr)){
                            q.push(curr);
                            bankCheck.erase(curr); //removing so that it is marked as visited
                        }
                    }

                    curr[j] = original;
                }

               
            }
             count++;
        }

        return -1;
    }

};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
