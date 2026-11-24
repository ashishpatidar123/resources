# 86. Partition List

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0086-partition-list)

## Problem

<p>Given the <code>head</code> of a linked list and a value <code>x</code>, partition it such that all nodes <strong>less than</strong> <code>x</code> come before nodes <strong>greater than or equal</strong> to <code>x</code>.</p>

<p>You should <strong>preserve</strong> the original relative order of the nodes in each of the two partitions.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/01/04/partition.jpg" style="width: 662px; height: 222px;" />
<pre>
<strong>Input:</strong> head = [1,4,3,2,5,2], x = 3
<strong>Output:</strong> [1,2,2,4,3,5]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> head = [2,1], x = 2
<strong>Output:</strong> [1,2]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the list is in the range <code>[0, 200]</code>.</li>
	<li><code>-100 &lt;= Node.val &lt;= 100</code></li>
	<li><code>-200 &lt;= x &lt;= 200</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0086-partition-list/solution.cpp)

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
    ListNode* partition(ListNode* head, int x) {
        if(head==NULL){
            return head;
        }
        if(head->next==NULL){
            return head;
        }
        ListNode* curr = head;
        ListNode* dummy = new ListNode();
        ListNode* temp = dummy;
        // finding pivot
        while(curr!=NULL && curr->val!=x){
            curr = curr->next;
        }
        ListNode* pivot = curr;
        // first adding all the smaller elements
        curr = head;
        while(curr!=NULL){
            if(curr->val < x){
                ListNode* temp2 = new ListNode(curr->val);
                temp->next = temp2;
                temp = temp2;
            }
            curr = curr->next;
        }
        // now adding all the greater elements which are before the pivot
        curr = head;
        while(curr!=pivot){
            if(curr->val>x){
                ListNode* temp2 = new ListNode(curr->val);
                temp->next = temp2;
                temp = temp2;
            }
            curr = curr->next;
        }
        // adding elements which are greater than or equal to pivot and are in the right side of the pivot
        curr = pivot;
        while(curr!=NULL){
            if(curr->val>=x){
                ListNode* temp2 = new ListNode(curr->val);
                temp->next = temp2;
                temp = temp2;
            }
            curr = curr->next;
        }
        return dummy->next;

    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
