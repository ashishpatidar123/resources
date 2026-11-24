# 79. Word Search

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0079-word-search)

## Problem

<p>Given an <code>m x n</code> grid of characters <code>board</code> and a string <code>word</code>, return <code>true</code> <em>if</em> <code>word</code> <em>exists in the grid</em>.</p>

<p>The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/04/word2.jpg" style="width: 322px; height: 242px;" />
<pre>
<strong>Input:</strong> board = [[&quot;A&quot;,&quot;B&quot;,&quot;C&quot;,&quot;E&quot;],[&quot;S&quot;,&quot;F&quot;,&quot;C&quot;,&quot;S&quot;],[&quot;A&quot;,&quot;D&quot;,&quot;E&quot;,&quot;E&quot;]], word = &quot;ABCCED&quot;
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/04/word-1.jpg" style="width: 322px; height: 242px;" />
<pre>
<strong>Input:</strong> board = [[&quot;A&quot;,&quot;B&quot;,&quot;C&quot;,&quot;E&quot;],[&quot;S&quot;,&quot;F&quot;,&quot;C&quot;,&quot;S&quot;],[&quot;A&quot;,&quot;D&quot;,&quot;E&quot;,&quot;E&quot;]], word = &quot;SEE&quot;
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/10/15/word3.jpg" style="width: 322px; height: 242px;" />
<pre>
<strong>Input:</strong> board = [[&quot;A&quot;,&quot;B&quot;,&quot;C&quot;,&quot;E&quot;],[&quot;S&quot;,&quot;F&quot;,&quot;C&quot;,&quot;S&quot;],[&quot;A&quot;,&quot;D&quot;,&quot;E&quot;,&quot;E&quot;]], word = &quot;ABCB&quot;
<strong>Output:</strong> false
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>m == board.length</code></li>
	<li><code>n = board[i].length</code></li>
	<li><code>1 &lt;= m, n &lt;= 6</code></li>
	<li><code>1 &lt;= word.length &lt;= 15</code></li>
	<li><code>board</code> and <code>word</code> consists of only lowercase and uppercase English letters.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong> Could you use search pruning to make your solution faster with a larger <code>board</code>?</p>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0079-word-search/solution.cpp)

```cpp
class Solution {
    void dfs(int i, int j, int row, int col, string&word,string &path, vector<vector<char>>&board,
        vector<vector<bool>>&visited,bool &ans){
        // if the size of the path travesed till now is equal to word then check if the path is same as word or not
        // if it is then make ans true and return
        // else simply return
        if(path.size()==word.size()){
            if(path==word){
                ans = true;
            }
            return;
        }
        // if indexes are out of bound then return
        if(i<0 || i>=row || j<0 || j>=col){
            return;
        }
        // if we already found the path then return
        if(ans==true){
            return;
        }
        // if the cell was already visited earlier then return
        if(visited[i][j]==true){
            return;
        }
        // mark visited and add the letter to the path
        visited[i][j]=true;
        path.push_back(board[i][j]);
        dfs(i+1,j,row,col,word,path,board,visited,ans);
        dfs(i,j+1,row,col,word,path,board,visited,ans);
        dfs(i-1,j,row,col,word,path,board,visited,ans);
        dfs(i,j-1,row,col,word,path,board,visited,ans);
        // pop out the last added letter
        path.pop_back();
        // mark the cell unvisited so that we can check further
        visited[i][j]=false;
        return;
    }
public:
    bool exist(vector<vector<char>>& board, string word) {
        int row = board.size();
        int col = board[0].size();
        // creating a variable to store the path
        string path = "";
        //  a variable to store the ans
        bool ans = false;
        vector<vector<bool>>visited(row,vector<bool>(col,false));
        // traverse the grid
        for(int i=0; i<row; i++){
            for(int j=0; j<col; j++){
                dfs(i,j,row,col,word,path,board,visited,ans);
                // if ans is true which means we have found the word thus return true
                if(ans){
                    return true;
                }
                // else re initalise path and move to next cell
                path = "";
            }
        }
        return false;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
