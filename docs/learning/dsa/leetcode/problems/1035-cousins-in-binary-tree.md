# 1035. Cousins In Binary Tree

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1035-cousins-in-binary-tree)

## Problem

<p>Given the <code>root</code> of a binary tree with unique values and the values of two different nodes of the tree <code>x</code> and <code>y</code>, return <code>true</code> <em>if the nodes corresponding to the values </em><code>x</code><em> and </em><code>y</code><em> in the tree are <strong>cousins</strong>, or </em><code>false</code><em> otherwise.</em></p>

<p>Two nodes of a binary tree are <strong>cousins</strong> if they have the same depth with different parents.</p>

<p>Note that in a binary tree, the root node is at the depth <code>0</code>, and children of each depth <code>k</code> node are at the depth <code>k + 1</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/02/12/q1248-01.png" style="width: 304px; height: 270px;" />
<pre>
<strong>Input:</strong> root = [1,2,3,4], x = 4, y = 3
<strong>Output:</strong> false
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/02/12/q1248-02.png" style="width: 334px; height: 266px;" />
<pre>
<strong>Input:</strong> root = [1,2,3,null,4,null,5], x = 5, y = 4
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/02/13/q1248-03.png" style="width: 267px; height: 258px;" />
<pre>
<strong>Input:</strong> root = [1,2,3,null,4], x = 2, y = 3
<strong>Output:</strong> false
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the tree is in the range <code>[2, 100]</code>.</li>
	<li><code>1 &lt;= Node.val &lt;= 100</code></li>
	<li>Each node has a <strong>unique</strong> value.</li>
	<li><code>x != y</code></li>
	<li><code>x</code> and <code>y</code> are exist in the tree.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1035-cousins-in-binary-tree/solution.cpp)

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
private:
    int level(TreeNode* root, int temp , int lev){

        if(root==NULL){
            return 0;
        }
        if(root->val==temp){
            return lev;
        }
        int l = level(root->left,temp,lev+1);
        if(l!=0){
            return l;
        }
        return level(root->right,temp,lev+1);

    }
    bool isSiblings(TreeNode* root, int x, int y) {
        if (root == nullptr) {
            return false;
        }
        
        bool foundX = false;
        bool foundY = false;
        
        if (root->left != nullptr && root->right != nullptr) {
            foundX = (root->left->val == x || root->right->val == x);
            foundY = (root->left->val == y || root->right->val == y);
        }
        
        return foundX && foundY ||
            isSiblings(root->left, x, y) ||
            isSiblings(root->right, x, y);
    }
public:
    bool isCousins(TreeNode* root, int x, int y) {

        
        
        return (level(root,x,1)==level(root,y,1) &&
                !isSiblings(root,x,y));

        
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
