# 126. Word Ladder Ii

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0126-word-ladder-ii)

## Problem

<p>A <strong>transformation sequence</strong> from word <code>beginWord</code> to word <code>endWord</code> using a dictionary <code>wordList</code> is a sequence of words <code>beginWord -&gt; s<sub>1</sub> -&gt; s<sub>2</sub> -&gt; ... -&gt; s<sub>k</sub></code> such that:</p>

<ul>
	<li>Every adjacent pair of words differs by a single letter.</li>
	<li>Every <code>s<sub>i</sub></code> for <code>1 &lt;= i &lt;= k</code> is in <code>wordList</code>. Note that <code>beginWord</code> does not need to be in <code>wordList</code>.</li>
	<li><code>s<sub>k</sub> == endWord</code></li>
</ul>

<p>Given two words, <code>beginWord</code> and <code>endWord</code>, and a dictionary <code>wordList</code>, return <em>all the <strong>shortest transformation sequences</strong> from</em> <code>beginWord</code> <em>to</em> <code>endWord</code><em>, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words </em><code>[beginWord, s<sub>1</sub>, s<sub>2</sub>, ..., s<sub>k</sub>]</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> beginWord = &quot;hit&quot;, endWord = &quot;cog&quot;, wordList = [&quot;hot&quot;,&quot;dot&quot;,&quot;dog&quot;,&quot;lot&quot;,&quot;log&quot;,&quot;cog&quot;]
<strong>Output:</strong> [[&quot;hit&quot;,&quot;hot&quot;,&quot;dot&quot;,&quot;dog&quot;,&quot;cog&quot;],[&quot;hit&quot;,&quot;hot&quot;,&quot;lot&quot;,&quot;log&quot;,&quot;cog&quot;]]
<strong>Explanation:</strong>&nbsp;There are 2 shortest transformation sequences:
&quot;hit&quot; -&gt; &quot;hot&quot; -&gt; &quot;dot&quot; -&gt; &quot;dog&quot; -&gt; &quot;cog&quot;
&quot;hit&quot; -&gt; &quot;hot&quot; -&gt; &quot;lot&quot; -&gt; &quot;log&quot; -&gt; &quot;cog&quot;
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> beginWord = &quot;hit&quot;, endWord = &quot;cog&quot;, wordList = [&quot;hot&quot;,&quot;dot&quot;,&quot;dog&quot;,&quot;lot&quot;,&quot;log&quot;]
<strong>Output:</strong> []
<strong>Explanation:</strong> The endWord &quot;cog&quot; is not in wordList, therefore there is no valid transformation sequence.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= beginWord.length &lt;= 5</code></li>
	<li><code>endWord.length == beginWord.length</code></li>
	<li><code>1 &lt;= wordList.length &lt;= 500</code></li>
	<li><code>wordList[i].length == beginWord.length</code></li>
	<li><code>beginWord</code>, <code>endWord</code>, and <code>wordList[i]</code> consist of lowercase English letters.</li>
	<li><code>beginWord != endWord</code></li>
	<li>All the words in <code>wordList</code> are <strong>unique</strong>.</li>
	<li>The <strong>sum</strong> of all shortest transformation sequences does not exceed <code>10<sup>5</sup></code>.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0126-word-ladder-ii/solution.cpp)

```cpp
class Solution {
private:

    void dfs(string& curr, string& beginWord, vector<string>&path, unordered_map<string, vector<string>>& parents, vector<vector<string>>& result){

        if(curr == beginWord){
            vector<string>currPath = path;
            reverse(currPath.begin(), currPath.end());
            result.push_back(currPath);
            return;
        }

        for(string& parent : parents[curr]){
            path.push_back(parent);
            dfs(parent, beginWord, path, parents, result);
            path.pop_back();
        }

    }
public:
    vector<vector<string>> findLadders(string beginWord, string endWord, vector<string>& wordList) {
        // unordered_set<string>wordCheck(wordList.begin(), wordList.end());

        // vector<vector<string>>result;

        // queue<vector<string>>q;
        // q.push({beginWord});
        // bool found = false;

        // while(!q.empty() && !found){
        //     int size = q.size();

        //     unordered_set<string>visited;

        //     for(int i=0; i<size; i++){
        //         vector<string>path = q.front();
        //         q.pop();

        //         string curr = path.back(); //last gene


        //         for(int j=0; j<curr.size(); j++){
        //             char original = curr[j];

        //             for(char c='a'; c<='z'; c++){
        //                 if(c == original) continue;

        //                 curr[j] = c;

        //                 if(wordCheck.count(curr)){
        //                     visited.insert(curr);

        //                     vector<string>newPath = path;

        //                     newPath.push_back(curr);

        //                     if(curr == endWord){
        //                         found = true;
        //                         result.push_back(newPath);
        //                     }
        //                     else{
        //                         q.push(newPath);
        //                     }
        //                 }
                      
        //             }
        //             curr[j] = original;
        //         }
        //     }
        //     for( auto c : visited){
        //         wordCheck.erase(c);
        //     }
        // }

        // return result;


        unordered_set<string>wordCheck(wordList.begin(), wordList.end());
        vector<vector<string>>result;

        if(wordCheck.find(endWord) == wordCheck.end()){
            return result;
        }

        unordered_map<string, vector<string>>parents;

        queue<string>q;
        q.push(beginWord);
        wordCheck.erase(beginWord);
        bool found = false;

        while(!q.empty() && !found){

            int size = q.size();

            unordered_set<string>visited;

            for(int i=0; i<size; i++){

                string curr = q.front();
                q.pop();
                string word = curr;

                for(int j=0; j<word.size(); j++){
                    char original  = word[j];

                    for(char c = 'a'; c<= 'z'; c++){
                        if(c == original ) continue;

                        word[j] = c;

                        if(wordCheck.count(word)){
                            visited.insert(word);
                            parents[word].push_back(curr);

                            if(word == endWord){
                                found = true;
                            }
                        }

                    }

                    word[j] = original;
                }

            }

            for(auto s : visited){
                wordCheck.erase(s);
                q.push(s);
            }

        }

        if(found){
            vector<string>path;
            path.push_back(endWord);
            dfs(endWord, beginWord, path, parents, result);
        }

        return result;

    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
