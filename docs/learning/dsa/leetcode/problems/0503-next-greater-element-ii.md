# 503. Next Greater Element Ii

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0503-next-greater-element-ii)

## Problem

<p>Given a circular integer array <code>nums</code> (i.e., the next element of <code>nums[nums.length - 1]</code> is <code>nums[0]</code>), return <em>the <strong>next greater number</strong> for every element in</em> <code>nums</code>.</p>

<p>The <strong>next greater number</strong> of a number <code>x</code> is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn&#39;t exist, return <code>-1</code> for this number.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,1]
<strong>Output:</strong> [2,-1,2]
Explanation: The first 1&#39;s next greater number is 2; 
The number 2 can&#39;t find next greater number. 
The second 1&#39;s next greater number needs to search circularly, which is also 2.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [1,2,3,4,3]
<strong>Output:</strong> [2,3,4,-1,4]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0503-next-greater-element-ii/solution.cpp)

```cpp
class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {

        // declare a vector ans
        vector<int> ans;
        // declare a vector temp of double the size than nums
        vector<int> temp(2*nums.size(),0);
        

        int n = nums.size();
        
        // fill the temp with nums two times
        // so that we can form a circular loop
        for(int i=0; i<nums.size(); i++){
            temp[i] = nums[i];
            temp[nums.size()+i] = nums[i];
        }
        
        // declare a stack
        stack<int> st;
        
        // traverse from the back
        // since we added nums two times in temp
        // so we only put answer to our ans vector for values of i less than i
        // because we don't want to waste memory two times
        for(int i = 2*n-1; i>=0; i--){
            
            // if the stack is empty 
            // push the index inside the stack
            // and push -1 into the answer array because stack is empty(if i is less
            // than n)
            if(st.empty()){
                st.push(i);
                if(i<n){
                    ans.push_back(-1);
                }
            }

            // check for the empty stack and if the element at the top of the stack
            // is smaller or equal to the current element
            // if yes then pop it out
            while(!st.empty() && temp[i]>=temp[st.top()]){
                st.pop();
            }
            
            // if the stack is empty then push -1 (if i is less than n)
            // push the index into the stack
            if(st.empty()){
                if(i<n){
                    ans.push_back(-1);
                }
                st.push(i);
            }

            // else push element at the top index to the array(if it is less than n)
            // push the index into the stack
            else{
                if(i<n){
                    ans.push_back(temp[st.top()]);
                }
                
                st.push(i);
            }
        }
        // reverse the answer array
        reverse(ans.begin(),ans.end());
        return ans;

    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
