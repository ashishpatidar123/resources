# 106. Construct Binary Tree From Inorder And Postorder Traversal

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0106-construct-binary-tree-from-inorder-and-postorder-traversal)

## Problem

<p>Given two integer arrays <code>inorder</code> and <code>postorder</code> where <code>inorder</code> is the inorder traversal of a binary tree and <code>postorder</code> is the postorder traversal of the same tree, construct and return <em>the binary tree</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/02/19/tree.jpg" style="width: 277px; height: 302px;" />
<pre>
<strong>Input:</strong> inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
<strong>Output:</strong> [3,9,20,null,null,15,7]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> inorder = [-1], postorder = [-1]
<strong>Output:</strong> [-1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= inorder.length &lt;= 3000</code></li>
	<li><code>postorder.length == inorder.length</code></li>
	<li><code>-3000 &lt;= inorder[i], postorder[i] &lt;= 3000</code></li>
	<li><code>inorder</code> and <code>postorder</code> consist of <strong>unique</strong> values.</li>
	<li>Each value of <code>postorder</code> also appears in <code>inorder</code>.</li>
	<li><code>inorder</code> is <strong>guaranteed</strong> to be the inorder traversal of the tree.</li>
	<li><code>postorder</code> is <strong>guaranteed</strong> to be the postorder traversal of the tree.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0106-construct-binary-tree-from-inorder-and-postorder-traversal/solution.cpp)

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    TreeNode* func2(vector<int>&inorder, vector<int> &postorder, int& post, int start, int end, unordered_map<int,int>&m){

        if(start>end) return NULL;

        int val = postorder[post];
        post--;
        int index = m[val];
        TreeNode* root = new TreeNode(val);
        
        root->right = func2(inorder, postorder, post, index+1, end, m);
        root->left = func2(inorder,postorder, post, start, index-1, m);
        
        return root;
    }
    TreeNode* func1(vector<int>& inorder, vector<int> &postorder, int size){
        unordered_map<int,int>m;

        for(int i=0; i<size; i++){
            m[inorder[i]] = i;
        }

        int post = size-1;
        int start = 0;
        int end = size-1;

        return func2(inorder, postorder, post, start, end, m);
    }
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        
        int size = inorder.size();
        if(size==0) return NULL;
        TreeNode* root = func1(inorder, postorder, size);
        return root;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
