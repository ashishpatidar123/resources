# 143. Reorder List

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0143-reorder-list)

## Problem

<p>You are given the head of a singly linked-list. The list can be represented as:</p>

<pre>
L<sub>0</sub> &rarr; L<sub>1</sub> &rarr; &hellip; &rarr; L<sub>n - 1</sub> &rarr; L<sub>n</sub>
</pre>

<p><em>Reorder the list to be on the following form:</em></p>

<pre>
L<sub>0</sub> &rarr; L<sub>n</sub> &rarr; L<sub>1</sub> &rarr; L<sub>n - 1</sub> &rarr; L<sub>2</sub> &rarr; L<sub>n - 2</sub> &rarr; &hellip;
</pre>

<p>You may not modify the values in the list&#39;s nodes. Only nodes themselves may be changed.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/03/04/reorder1linked-list.jpg" style="width: 422px; height: 222px;" />
<pre>
<strong>Input:</strong> head = [1,2,3,4]
<strong>Output:</strong> [1,4,2,3]
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/03/09/reorder2-linked-list.jpg" style="width: 542px; height: 222px;" />
<pre>
<strong>Input:</strong> head = [1,2,3,4,5]
<strong>Output:</strong> [1,5,2,4,3]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the list is in the range <code>[1, 5 * 10<sup>4</sup>]</code>.</li>
	<li><code>1 &lt;= Node.val &lt;= 1000</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0143-reorder-list/solution.cpp)

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
private:
    ListNode* reverse(ListNode* head){
        if(head==NULL || head->next==NULL){
            return head;
        }
        ListNode* curr = head;
        ListNode* prev = NULL;
        ListNode* next = NULL;

        while(curr!=NULL){
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        head = prev;
        return head;
    }
public:
    void reorderList(ListNode* head) {
        if(head==NULL || head->next==NULL){
            return;
        }
        // finding the length of the list
        int n = 0;
        ListNode* curr = head;
        while(curr!=NULL){
            curr = curr->next;
            n++;
        }
        // find middle
        if(n%2==0){
            n = n/2;
        }
        else{
            n = (n+1)/2;
        }
        // finding the middle node
        ListNode* newHead = new ListNode(-1);
        curr = head;
        ListNode* prev = NULL;
        while(n>0){
            prev = curr;
            curr = curr->next;
            n--;
        }
        // break the list from the middle
        prev->next = NULL;
        newHead = curr;
        // reverse the list after the middle
        newHead = reverse(newHead);
        // now we have two lists 
        // first -  the list till middle
        // second - the reversed list after middle
        ListNode* first = head;
        ListNode* second = newHead;
        // create a dummy node and add nodes as given in the question
        ListNode* dummy = new ListNode(-1);
        ListNode* temp = dummy;
        bool flag = true;
        while(first!=NULL || second!=NULL){
            if(flag){
                temp->next = first;
                temp = first;
                first = first->next;
            }
            else{
                temp->next = second;
                temp = second;
                second = second->next;
            }
            flag = !flag;
        }
        head = dummy->next;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
