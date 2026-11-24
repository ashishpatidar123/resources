# 2. Add Two Numbers

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0002-add-two-numbers)

## Problem

<p>You are given two <strong>non-empty</strong> linked lists representing two non-negative integers. The digits are stored in <strong>reverse order</strong>, and each of their nodes contains a single digit. Add the two numbers and return the sum&nbsp;as a linked list.</p>

<p>You may assume the two numbers do not contain any leading zero, except the number 0 itself.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/10/02/addtwonumber1.jpg" style="width: 483px; height: 342px;" />
<pre>
<strong>Input:</strong> l1 = [2,4,3], l2 = [5,6,4]
<strong>Output:</strong> [7,0,8]
<strong>Explanation:</strong> 342 + 465 = 807.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> l1 = [0], l2 = [0]
<strong>Output:</strong> [0]
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
<strong>Output:</strong> [8,9,9,9,0,0,0,1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in each linked list is in the range <code>[1, 100]</code>.</li>
	<li><code>0 &lt;= Node.val &lt;= 9</code></li>
	<li>It is guaranteed that the list represents a number that does not have leading zeros.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0002-add-two-numbers/solution.cpp)

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
    ListNode* reverse(ListNode* temp){
        // create prev, curr and next pointers
        ListNode* prev = NULL;
        ListNode* curr = temp;
        ListNode* next2 = NULL;
        // traverse till curr not become null
        while(curr!=NULL){
            // update the next pointer
            next2 = curr->next;
            // make next of current to points to the previous node
            curr->next = prev;
            // now make the current pointer as the previous pointer
            prev = curr;
            // and next pointer as the current pointer
            curr = next2;
            
        }
        // return the prev pointer
        return prev;
    }
    void insert(ListNode* &head, ListNode* &tail, int value){
        ListNode* temp = new ListNode(value);
        // inserting a node in the list
        if(head==NULL){
            head = temp;
            tail = temp;
            return ;
        }
        else{
            tail->next = temp;
            tail = temp;
        }
    }
    ListNode* add(ListNode* first, ListNode* second){
        // intialise carry to 0;
        int carry = 0;
        // initialsie head and tail pointer to our answer list
        ListNode* ansHead = NULL;
        ListNode* ansTail = NULL;
        // traverse through both the list simultaneously
        // enter the loop if either of the list in non empty or even if both the lists
        // are empty check for the carry
        // if it is non zero the enter the loop 
        while(first!=NULL || second!=NULL || carry!=0){
            int val1 = 0;
            if(first!=NULL){
                val1 = first->val;
            }
            int val2 = 0;
            if(second!=NULL){
                val2 = second->val;
            }
            // find the sum of corresponding digits 
            int sum = val1 + val2 + carry;
            // digit will be equal to sum%10
            int digit =  sum%10;
            // add that digit in the ans list by creating a new node
            insert(ansHead,ansTail,digit);
            // find the carry
            carry = sum/10;
            // update the pointers
            if(first!=NULL){
                first = first->next;
            }
            if(second!=NULL){
                second = second->next;
            }
        }
        return ansHead;
    }
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        
        ListNode* first = l1;
        ListNode* second = l2;

        ListNode* ans = add(first,second);

        // ans = reverse(ans);   
        return ans;  
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
