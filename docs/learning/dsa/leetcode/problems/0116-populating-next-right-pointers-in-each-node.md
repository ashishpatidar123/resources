# 116. Populating Next Right Pointers In Each Node

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0116-populating-next-right-pointers-in-each-node)

## Problem

<p>You are given a <strong>perfect binary tree</strong> where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:</p>

<pre>
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
</pre>

<p>Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to <code>NULL</code>.</p>

<p>Initially, all next pointers are set to <code>NULL</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2019/02/14/116_sample.png" style="width: 500px; height: 171px;" />
<pre>
<strong>Input:</strong> root = [1,2,3,4,5,6,7]
<strong>Output:</strong> [1,#,2,3,#,4,5,6,7,#]
<strong>Explanation: </strong>Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with &#39;#&#39; signifying the end of each level.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> root = []
<strong>Output:</strong> []
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the tree is in the range <code>[0, 2<sup>12</sup> - 1]</code>.</li>
	<li><code>-1000 &lt;= Node.val &lt;= 1000</code></li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow-up:</strong></p>

<ul>
	<li>You may only use constant extra space.</li>
	<li>The recursive approach is fine. You may assume implicit stack space does not count as extra space for this problem.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0116-populating-next-right-pointers-in-each-node/solution.cpp)

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        // if the tree is empty then return null
        if(root==NULL){
            return NULL;
        }
        // start from the root node
        Node* curr = root;
        // since the tree is a perfect binary tree 
        // so we can easily check if the next level exist or not by simply checking 
        // the current nodes left pointer if it's null it means no more levels are
        // present in the tree
        while(curr->left!=NULL){
            // start from the current node of the level
            // i.e. the first node of the level
            // and traverse all the nodes of that level
            Node* temp = curr;
            while(temp!=NULL){
                // add the next pointers 
                temp->left->next = temp->right;
                if(temp->next!=NULL){
                    temp->right->next = temp->next->left;
                }
                // if we reach at the end of the level then make it's pointer NULL
                else{
                    temp->right->next = NULL;
                }
                // move to the next node
                temp = temp->next;
            }
            // move to the next levele
            curr = curr->left;
        }
        return root;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
