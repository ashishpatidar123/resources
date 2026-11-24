# 61. Rotate List

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0061-rotate-list)

## Problem

<p>Given the <code>head</code> of a linked&nbsp;list, rotate the list to the right by <code>k</code> places.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/13/rotate1.jpg" style="width: 450px; height: 191px;" />
<pre>
<strong>Input:</strong> head = [1,2,3,4,5], k = 2
<strong>Output:</strong> [4,5,1,2,3]
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/13/roate2.jpg" style="width: 305px; height: 350px;" />
<pre>
<strong>Input:</strong> head = [0,1,2], k = 4
<strong>Output:</strong> [2,0,1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the list is in the range <code>[0, 500]</code>.</li>
	<li><code>-100 &lt;= Node.val &lt;= 100</code></li>
	<li><code>0 &lt;= k &lt;= 2 * 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0061-rotate-list/solution.cpp)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), +1next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        // if(head==NULL || head->next==NULL){
        //     return head;
        // }
        // ListNode* curr = head;
        // int count = 0;
        // while(curr!=NULL){
        //     count++;
        //     curr = curr->next;
        // }
        // curr = head;
        // int n = count;
        // if(k==0 || k%n==0){
        //     return head;
        // }
        // vector<int>values(n);
        // int i = 0;
        // while(curr!=NULL){
        //     int val = curr->val;
        //     curr = curr->next;
        //     values[i++] = val;
        // }
        // k = k%n;
        // vector<int>nums(n);
        // for(int i=0; i<n; i++){
        //     if(i+k<n){
        //         nums[i+k] = values[i];
        //     }
        //     else{
        //         nums[i+k-n] = values[i];
        //     }
            
        // }
        // i = 0;
        // curr = head;
        // while(curr!=NULL){
        //     curr->val = nums[i++];
        //     curr = curr->next;
        // }
        // return head;
        //if head is null or the list has only one node then return head
        if(head==NULL || head->next==NULL){
            return head;
        }
        // find the last node and the count of nodes
        ListNode* curr = head;
        int count = 0;
        while(curr->next!=NULL){
            curr = curr->next;
            count++;
        }
        ListNode* last = curr;
        // number of nodes is count+1 because the above loop runs till we reach last node
        int n = count+1;
        // update k by taking modulo with n
        k = k%n;
        curr = head;
        // find the n-k th node from start 
        // this node will be our new head
        // all keep track of just prev node
        // so that we can make it's next pointer null
        int x = n-k;
        if(k==0){
            return head;
        }
        ListNode* prev = NULL;
        while(x--){
            prev = curr;
            curr = curr->next;
        }
        prev->next = NULL;
        // mark newhead
        ListNode* newHead = curr;
        // make the next of last node to point to the current head
        // and update head
        last->next = head;
        head = newHead;
        return newHead;
        
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
