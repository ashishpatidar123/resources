# 11. Container With Most Water

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0011-container-with-most-water)

## Problem

<p>You are given an integer array <code>height</code> of length <code>n</code>. There are <code>n</code> vertical lines drawn such that the two endpoints of the <code>i<sup>th</sup></code> line are <code>(i, 0)</code> and <code>(i, height[i])</code>.</p>

<p>Find two lines that together with the x-axis form a container, such that the container contains the most water.</p>

<p>Return <em>the maximum amount of water a container can store</em>.</p>

<p><strong>Notice</strong> that you may not slant the container.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://s3-lc-upload.s3.amazonaws.com/uploads/2018/07/17/question_11.jpg" style="width: 600px; height: 287px;" />
<pre>
<strong>Input:</strong> height = [1,8,6,2,5,4,8,3,7]
<strong>Output:</strong> 49
<strong>Explanation:</strong> The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> height = [1,1]
<strong>Output:</strong> 1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == height.length</code></li>
	<li><code>2 &lt;= n &lt;= 10<sup>5</sup></code></li>
	<li><code>0 &lt;= height[i] &lt;= 10<sup>4</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0011-container-with-most-water/solution.cpp)

```cpp
class Solution {
public:
    int maxArea(vector<int>& height) {
        
        // initialise two pointers 
        // one starting from start(0)
        // and other from the end(n-1)
        int start=0;
        int end=height.size()-1;
        // create a variable area to store the area of the container formed by the lines
        // start and end
        long long int area = 0;
        // define max area as 0
        int max_area = 0;
        // run the loop until both pointers meet
        while(start<end){
            
            // find the minimum of the two heights
            // that is - starting vertical line and ending vertical line
            long long int m = min(height[start],height[end]);
            // now find the area contained between this lines and the x-axis
            area = m*(end-start);
            // if area>max
            // then update max
            if(area>max_area){
                max_area = area;
            }
            // now update the pointer for which the height of the vertical line is smaller
            if(height[start]>height[end]){
                end--;
            }
            else{
                start++;
            }

        }
        // return maximum area
        return max_area;
        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
