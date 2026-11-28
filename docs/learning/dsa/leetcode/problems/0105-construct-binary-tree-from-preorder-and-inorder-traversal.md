# 105. Construct Binary Tree From Preorder And Inorder Traversal

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0105-construct-binary-tree-from-preorder-and-inorder-traversal)

## Problem

<p>Given two integer arrays <code>preorder</code> and <code>inorder</code> where <code>preorder</code> is the preorder traversal of a binary tree and <code>inorder</code> is the inorder traversal of the same tree, construct and return <em>the binary tree</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/02/19/tree.jpg" style="width: 277px; height: 302px;" />
<pre>
<strong>Input:</strong> preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
<strong>Output:</strong> [3,9,20,null,null,15,7]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> preorder = [-1], inorder = [-1]
<strong>Output:</strong> [-1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= preorder.length &lt;= 3000</code></li>
	<li><code>inorder.length == preorder.length</code></li>
	<li><code>-3000 &lt;= preorder[i], inorder[i] &lt;= 3000</code></li>
	<li><code>preorder</code> and <code>inorder</code> consist of <strong>unique</strong> values.</li>
	<li>Each value of <code>inorder</code> also appears in <code>preorder</code>.</li>
	<li><code>preorder</code> is <strong>guaranteed</strong> to be the preorder traversal of the tree.</li>
	<li><code>inorder</code> is <strong>guaranteed</strong> to be the inorder traversal of the tree.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0105-construct-binary-tree-from-preorder-and-inorder-traversal/solution.cpp)

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
    TreeNode* func2(vector<int>&preorder, vector<int>&inorder, int &pre, unordered_map<int,int>&m, int start, int end){

            if(start>end) return NULL;

            int val = preorder[pre];
            pre++;

            TreeNode* root = new TreeNode(val);
            int index = m[val];

            root->left = func2(preorder, inorder, pre, m, start, index-1);
            root->right = func2(preorder, inorder, pre, m , index+1, end);
            return root;

    }
    TreeNode* func1(vector<int>& preorder, vector<int>& inorder, int &size){

        unordered_map<int,int>m;
        for(int i=0; i<size; i++){
            int t = inorder[i];
            m[t] = i;
        }
        int pre = 0;
        int start = 0;
        int end = size-1;
        return func2(preorder, inorder, pre, m, start, end );

    }
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        
        int size = sizeof(preorder)/sizeof(preorder[0]);
        size = inorder.size();
        if(size==0) return NULL;
        TreeNode* root = func1(preorder, inorder, size);

        return root;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
