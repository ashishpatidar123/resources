# 84. Largest Rectangle In Histogram

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0084-largest-rectangle-in-histogram)

## Problem

<p>Given an array of integers <code>heights</code> representing the histogram&#39;s bar height where the width of each bar is <code>1</code>, return <em>the area of the largest rectangle in the histogram</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg" style="width: 522px; height: 242px;" />
<pre>
<strong>Input:</strong> heights = [2,1,5,6,2,3]
<strong>Output:</strong> 10
<strong>Explanation:</strong> The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg" style="width: 202px; height: 362px;" />
<pre>
<strong>Input:</strong> heights = [2,4]
<strong>Output:</strong> 4
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= heights.length &lt;= 10<sup>5</sup></code></li>
	<li><code>0 &lt;= heights[i] &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0084-largest-rectangle-in-histogram/solution.cpp)

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& A) {
        
        //create two vectors for storing index of the nearest smaller element to the 
        // left and right of every element
        int n = A.size();
        vector<int>leftsmall;
        vector<int>rightsmall;
        
        stack<int> st;
        // finding left small
        // for the explanation look the code for the nearest smaller number problem
        leftsmall.push_back(-1);
        st.push(0);
        
        for(int i=1; i<n; i++){
            if(st.empty()){
                st.push(i);
                leftsmall.push_back(-1);
            }
            while(!st.empty() && A[st.top()]>=A[i]){
                st.pop();
            }
            if(st.empty()){
                st.push(i);
                leftsmall.push_back(-1);
            }
            else{
                leftsmall.push_back(st.top());
                st.push(i);
            }
            
        }
        while(!st.empty()){
            st.pop();
        }
        //right small
        // for the explanation look out the code for the help classmates problem
        rightsmall.push_back(n);
        st.push(n-1);
        
        for(int i=n-2; i>=0; i--){
            if(st.empty()){
                st.push(i);
                rightsmall.push_back(n);
            }
            while(!st.empty() && A[st.top()]>=A[i]){
                st.pop();
            }
            if(st.empty()){
                st.push(i);
                rightsmall.push_back(n);
            }
            else{
                rightsmall.push_back(st.top());
                st.push(i);
            }
            
        }
        reverse(rightsmall.begin(),rightsmall.end());

        int max = 0;
        int area = 0;
         // now finding area by just multiplying the height with the range over which 
         // we can move either side of the element without getting a smaller element than
         // the given element
        for(int i=0; i<n; i++){
            area = A[i]*(rightsmall[i]-leftsmall[i]-1);
            if(area>max){
                max = area;
            }
            
        }
        return max;
        
    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
