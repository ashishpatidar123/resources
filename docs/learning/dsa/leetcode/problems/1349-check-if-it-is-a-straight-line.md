# 1349. Check If It Is A Straight Line

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1349-check-if-it-is-a-straight-line)

## Problem

<p>You are given an integer array&nbsp;<code>coordinates</code>, <code>coordinates[i] = [x, y]</code>, where <code>[x, y]</code> represents the coordinate of a point. Check if these points&nbsp;make a straight line in the XY plane.</p>

<p>&nbsp;</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<p><img alt="" src="https://assets.leetcode.com/uploads/2019/10/15/untitled-diagram-2.jpg" style="width: 336px; height: 336px;" /></p>

<pre>
<strong>Input:</strong> coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 2:</strong></p>

<p><strong><img alt="" src="https://assets.leetcode.com/uploads/2019/10/09/untitled-diagram-1.jpg" style="width: 348px; height: 336px;" /></strong></p>

<pre>
<strong>Input:</strong> coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]
<strong>Output:</strong> false
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;=&nbsp;coordinates.length &lt;= 1000</code></li>
	<li><code>coordinates[i].length == 2</code></li>
	<li><code>-10^4 &lt;=&nbsp;coordinates[i][0],&nbsp;coordinates[i][1] &lt;= 10^4</code></li>
	<li><code>coordinates</code>&nbsp;contains no duplicate point.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/1349-check-if-it-is-a-straight-line/solution.cpp)

```cpp
class Solution {
public:
    bool checkStraightLine(vector<vector<int>>& p) {
        int n = p.size();
        int flag = 0;
        if(n==2){
            flag=1;
        }
        else if(p[0][0]-p[1][0]==0){
            for(int i=2; i<n; i++){
                if(p[i][0]==p[1][0]){
                    flag = 1;
                }
                else {
                    flag = 0;
                    break;
                }
            }
        }
        else {
            float m = float((p[0][1]-p[1][1]))/(p[0][0]-p[1][0]);
            cout<<m;
            float c = p[0][1] - m*p[0][0];
            cout<<c;
            for(int i=2; i<n; i++){
                if(c==0){
                    if(float(p[1][1])/p[1][0]==float(p[i][1])/p[i][0]){
                        flag=1;
                    }
                    else {
                        flag=0;
                        break;
                    }
                }
                else if(p[i][1]==m*p[i][0]+c){
                    flag=1;
                }
                else {
                    flag=0;
                    break;
                }
            }
        }
        
        if(flag){
            return true;
        } 
        else return false;
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
