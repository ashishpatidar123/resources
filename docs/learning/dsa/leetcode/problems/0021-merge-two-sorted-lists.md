# 21. Merge Two Sorted Lists

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0021-merge-two-sorted-lists)

## Problem

<p>You are given the heads of two sorted linked lists <code>list1</code> and <code>list2</code>.</p>

<p>Merge the two lists into one <strong>sorted</strong> list. The list should be made by splicing together the nodes of the first two lists.</p>

<p>Return <em>the head of the merged linked list</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg" style="width: 662px; height: 302px;" />
<pre>
<strong>Input:</strong> list1 = [1,2,4], list2 = [1,3,4]
<strong>Output:</strong> [1,1,2,3,4,4]
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> list1 = [], list2 = []
<strong>Output:</strong> []
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> list1 = [], list2 = [0]
<strong>Output:</strong> [0]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in both lists is in the range <code>[0, 50]</code>.</li>
	<li><code>-100 &lt;= Node.val &lt;= 100</code></li>
	<li>Both <code>list1</code> and <code>list2</code> are sorted in <strong>non-decreasing</strong> order.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0021-merge-two-sorted-lists/solution.cpp)

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
    ListNode* solve(ListNode*list1, ListNode*list2){
        // declare 4 pointers
        // current and next pointer for each list
        ListNode* curr1 = list1;
        ListNode* next1 = curr1->next;
        ListNode* curr2 = list2;
        ListNode* next2 = curr2->next;
        
        // traverse over the second list until it's current pointer become NULL and 
        // also check if the first list ends before the second list
        while(next1!=NULL && curr2!=NULL){
            // compare the value of curr2 with the values of curr1 and next1
            // if it lies between these two then add curr2 node in between of 
            // curr1 and next1
            if(curr2->val>=curr1->val && curr2->val<=next1->val){
                // adding the curr2 node
                curr1->next = curr2;
                next2 = curr2->next;
                curr2->next = next1;
                // update the pointers
                curr1 = curr2;
                curr2 = next2;
            }
            // else 
            else{
                // update the pointers
                curr1 = next1;
                next1 = next1->next;
                // check if we reaches at the end of the first list or not
                // if we reach then 
                if(next1==NULL){
                    // just points the last node of the first list to the current 
                    // pointer of the second list 
                    // and return the list1 pointer
                    curr1->next = curr2;
                    return list1;
                }
            }
        }
        return list1;
    }
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // check is list1 is empty of not
        // if it is empty then simply return list2 because there is nothing to merge
        if(list1==NULL){
            return list2;
        }
        //check is list2 is empty of not
        // if it is empty then simply return list1 because there is nothing to merge
        if(list2==NULL){
            return list1;
        }
        // now check which list has it's head value smaller
        // we will consider that list for putting values
        if(list1->val<=list2->val){
            // check if length of the first list is 1 
            // if it is then just points the next of the list1 to list2 
            // and return list1
            if(list1->next==NULL){
               list1->next=list2;
               return list1;
            }
            // else call the solve function
            return solve(list1,list2);
        }
        else{
            // check if length of the second list is 1 
            // if it is then just points the next of the list2 to list1
            // and return list2
            if(list2->next==NULL){
               list2->next=list1;
               return list2;
            }
            //else call the solve function
            return solve(list2,list1);
        }
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
