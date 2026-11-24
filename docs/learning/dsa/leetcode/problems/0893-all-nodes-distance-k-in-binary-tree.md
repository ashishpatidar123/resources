# 893. All Nodes Distance K In Binary Tree

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0893-all-nodes-distance-k-in-binary-tree)

## Problem

<p>Given the <code>root</code> of a binary tree, the value of a target node <code>target</code>, and an integer <code>k</code>, return <em>an array of the values of all nodes that have a distance </em><code>k</code><em> from the target node.</em></p>

<p>You can return the answer in <strong>any order</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://s3-lc-upload.s3.amazonaws.com/uploads/2018/06/28/sketch0.png" style="width: 500px; height: 429px;" />
<pre>
<strong>Input:</strong> root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
<strong>Output:</strong> [7,4,1]
Explanation: The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> root = [1], target = 1, k = 3
<strong>Output:</strong> []
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the tree is in the range <code>[1, 500]</code>.</li>
	<li><code>0 &lt;= Node.val &lt;= 500</code></li>
	<li>All the values <code>Node.val</code> are <strong>unique</strong>.</li>
	<li><code>target</code> is the value of one of the nodes in the tree.</li>
	<li><code>0 &lt;= k &lt;= 1000</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0893-all-nodes-distance-k-in-binary-tree/solution.cpp)

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    vector<int>result;

    void findDownwards(TreeNode* node, int distance){

        if(!node || distance < 0){
            return ;
        }

        if(distance == 0){
            result.push_back(node->val);
            return;
        }

        findDownwards(node->left, distance - 1);
        findDownwards(node->right, distance -1);
    }

    int dfs(TreeNode* node, TreeNode* target, int k){

        if(!node) return -1;

        if(node == target){
            findDownwards(node, k);
            return 1;
        }

        int left_dist = dfs(node->left, target, k);

        if(left_dist != -1){
            if(left_dist == k){
                result.push_back(node->val);
            }
            else{
                findDownwards(node->right, k - left_dist - 1);
            }

            return left_dist + 1;
        }

        int right_dist = dfs(node->right, target, k);

        if(right_dist != -1){
            if(right_dist == k){
                result.push_back(node->val);
            }
            else{
                findDownwards(node->left, k-right_dist -1);
            }
            return right_dist + 1;
        }

        return -1;
    }
    vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {

        dfs(root, target, k);
        return result;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
