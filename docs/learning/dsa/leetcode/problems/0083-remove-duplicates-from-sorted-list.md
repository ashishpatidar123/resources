# 83. Remove Duplicates From Sorted List

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0083-remove-duplicates-from-sorted-list)

## Problem

<p>Given the <code>head</code> of a sorted linked list, <em>delete all duplicates such that each element appears only once</em>. Return <em>the linked list <strong>sorted</strong> as well</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/01/04/list1.jpg" style="width: 302px; height: 242px;" />
<pre>
<strong>Input:</strong> head = [1,1,2]
<strong>Output:</strong> [1,2]
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/01/04/list2.jpg" style="width: 542px; height: 222px;" />
<pre>
<strong>Input:</strong> head = [1,1,2,3,3]
<strong>Output:</strong> [1,2,3]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the list is in the range <code>[0, 300]</code>.</li>
	<li><code>-100 &lt;= Node.val &lt;= 100</code></li>
	<li>The list is guaranteed to be <strong>sorted</strong> in ascending order.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0083-remove-duplicates-from-sorted-list/solution.cpp)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {

        // check for empty list
        if(head==NULL){
            return head;
        }
        // check is there is only node in the list then just return head because there 
        // won't be any duplicates
        if(head->next==NULL){
            return head;
        }
        // initialise a curr pointer to head
        ListNode*curr = head;
        // traverse through the list until the curr node is NULL
        while(curr!=NULL){
            // check for whether curr is the last node or not 
            // if it's not last then check for the value of the curr
            // and the next node
            if((curr->next!=NULL) && (curr->val==curr->next->val)){
                // if the values are equal then create a next to next node
                // and a node to be deleted
                ListNode*next_next = curr->next->next;
                ListNode*todelete = curr->next;
                // making the next of the node to be delete NULL
                todelete->next = NULL;
                // deleting the duplicate node
                delete(todelete);
                //pointing the next of the current node to the next to next node
                curr->next = next_next;

            }
            // if values are not equal then simply increase the curr pointer to 
            // the next node
            else{
                curr = curr->next;
            }
        }
        return head;
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
