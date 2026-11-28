# 4418. Number Of Intersecting Interval Pairs I

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/4418-number-of-intersecting-interval-pairs-i)

## Problem

# Number of Intersecting Interval Pairs I

### Difficulty: Easy
### Topics: 

<p>You are given a 2D integer array <code>intervals</code> of <code>n</code> elements, where <code>intervals[i] = [start<sub>i</sub>, end<sub>i</sub>]</code> represents the <strong>closed </strong>interval from <code>start<sub>i</sub></code> to <code>end<sub>i</sub></code>.</p>

<p>Return the number of pairs of indices <code>(i, j)</code> such that <code>0 &lt;= i &lt; j &lt; n</code> and <code>intervals[i]</code> and <code>intervals[j]</code> <strong>intersect</strong>.</p>

<p>Two intervals <strong>intersect</strong> if they have at least one point in common, including when they only share an endpoint.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">intervals = [[1,2],[2,3],[3,4]]</span></p>

<p><strong>Output:</strong> <span class="example-io">2</span></p>

<p><strong>Explanation:</strong></p>

<p>There are 2 intersecting interval pairs:</p>

<ul>
	<li>Intervals <code>[1, 2]</code> and <code>[2, 3]</code> intersect at the point 2.</li>
	<li>Intervals <code>[2, 3]</code> and <code>[3, 4]</code> intersect at the point 3.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">intervals = [[1,5],[2,4],[3,6]]</span></p>

<p><strong>Output:</strong> <span class="example-io">3</span></p>

<p><strong>Explanation:</strong></p>

<p>There are 3 intersecting interval pairs:</p>

<ul>
	<li>The intersection of <code>[1, 5]</code> and <code>[2, 4]</code> is <code>[2, 4]</code>.</li>
	<li>The intersection of <code>[1, 5]</code> and <code>[3, 6]</code> is <code>[3, 5]</code>.</li>
	<li>The intersection of <code>[2, 4]</code> and <code>[3, 6]</code> is <code>[3, 4]</code>.</li>
</ul>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">intervals = [[1,2],[3,4],[5,6]]</span></p>

<p><strong>Output:</strong> <span class="example-io">0</span></p>

<p><strong>Explanation:</strong></p>

<p>There are no intersecting interval pairs. Hence, the answer is 0.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= n == intervals.length &lt;= 100</code></li>
	<li><code>intervals[i] = [start<sub>i</sub>, end<sub>i</sub>]</code></li>
	<li><code>0 &lt;= start<sub>i</sub> &lt;= end<sub>i</sub> &lt;= 100</code></li>
</ul>

## My C++ Submissions

### `solution_2151147728.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/4418-number-of-intersecting-interval-pairs-i/solution_2151147728.cpp)

```cpp
class Solution {
public:
    int countIntersectingIntervals(vector<vector<int>>& intervals) {

        int count = 0;
        int n = intervals.size();
        sort(intervals.begin(), intervals.end());

        for(int i=0; i<n; i++){
            for(int j=i+1; j<n; j++){

                int start_1 = intervals[i][0];
                int end_1 = intervals[i][1];

                int start_2 = intervals[j][0];
                int end_2 = intervals[j][1];

                if(start_2 <= end_1){
                    count++;
                }

            }
            
        }

        return count;
        
    }
};
```

### `solution_2151180930.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/4418-number-of-intersecting-interval-pairs-i/solution_2151180930.cpp)

```cpp
class Solution {
public:
    int countIntersectingIntervals(vector<vector<int>>& intervals) {

        int count = 0;
        int n = intervals.size();
        sort(intervals.begin(), intervals.end());
        
        vector<int> starts;
        for(int i = 0; i < n; i++){
            starts.push_back(intervals[i][0]);
        }

        for(int i = 0; i < n; i++){
            int end_1 = intervals[i][1];
            auto it = upper_bound(starts.begin(), starts.end(), end_1);
            int temp = it - starts.begin(); // this will give the number of elements less than or equal to end_1, i.e. time intervals starting before end_1 so overlapping
            count += temp - i -1; // removing the intervals which are counted twice, i.e before i and i;
        }

        return count;
        
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
