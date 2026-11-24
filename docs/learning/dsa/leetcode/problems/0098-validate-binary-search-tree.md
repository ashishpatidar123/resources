# 98. Validate Binary Search Tree

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0098-validate-binary-search-tree)

## Problem

# Validate Binary Search Tree

### Difficulty: Medium
### Topics: Tree, Depth-First Search, Binary Search Tree, Binary Tree

<p>Given the <code>root</code> of a binary tree, <em>determine if it is a valid binary search tree (BST)</em>.</p>

<p>A <strong>valid BST</strong> is defined as follows:</p>

<ul>
	<li>The left <span data-keyword="subtree">subtree</span> of a node contains only nodes with keys&nbsp;<strong>strictly less than</strong> the node&#39;s key.</li>
	<li>The right subtree of a node contains only nodes with keys <strong>strictly greater than</strong> the node&#39;s key.</li>
	<li>Both the left and right subtrees must also be binary search trees.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/12/01/tree1.jpg" style="width: 302px; height: 182px;" />
<pre>
<strong>Input:</strong> root = [2,1,3]
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/12/01/tree2.jpg" style="width: 422px; height: 292px;" />
<pre>
<strong>Input:</strong> root = [5,1,4,null,null,3,6]
<strong>Output:</strong> false
<strong>Explanation:</strong> The root node&#39;s value is 5 but its right child&#39;s value is 4.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the tree is in the range <code>[1, 10<sup>4</sup>]</code>.</li>
	<li><code>-2<sup>31</sup> &lt;= Node.val &lt;= 2<sup>31</sup> - 1</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0098-validate-binary-search-tree/solution.cpp)

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
    int min(TreeNode*root){
        while(root->left!=NULL){
            root = root->left;
        }
        return root->val;
    }
    int max(TreeNode*root){
        while(root->right!=NULL){
            root = root->right;
        }
        return root->val;
    }
public:
    bool isValidBST(TreeNode* root) {

        if(root==NULL){
            return true;
        }
        
        if(root->left!=NULL){
            if(root->left->val >= root->val||max(root->left)>=root->val)
            {
                return false;
            }
        }
        if(root->right!=NULL){
            if(root->right->val <= root->val
                ||min(root->right)<=root->val)
            {
                return false;
            }
        }
        return isValidBST(root->left)&&isValidBST(root->right);
        
    }
};
```

### `solution_2163504430.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0098-validate-binary-search-tree/solution_2163504430.cpp)

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
    bool dfs(TreeNode* node, long long mini, long long maxi){
        if(node == NULL) return true;
        if(node->val <= mini || node->val >= maxi){
            return false;
        }
        
        bool check1 = dfs(node->left, mini, node->val);

        bool check2 = dfs(node->right, node->val, maxi);

        return check1 & check2;
    }
public:
    bool isValidBST(TreeNode* root) {

        return dfs(root, LLONG_MIN, LLONG_MAX);
        
    }
};
```

### `solution_2163505736.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0098-validate-binary-search-tree/solution_2163505736.cpp)

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
    bool dfs(TreeNode* node, long long mini, long long maxi){
        if(node == NULL) return true;
        if(node->val <= mini || node->val >= maxi){
            return false;
        }
        
        bool check1 = dfs(node->left, mini, node->val);

        bool check2 = dfs(node->right, node->val, maxi);

        return check1 && check2;
    }
public:
    bool isValidBST(TreeNode* root) {

        return dfs(root, LLONG_MIN, LLONG_MAX);
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
