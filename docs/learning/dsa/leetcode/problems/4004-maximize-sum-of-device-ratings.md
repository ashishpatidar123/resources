# 4004. Maximize Sum Of Device Ratings

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4004-maximize-sum-of-device-ratings)

## Problem

<p>You are given a 2D integer array <code>units</code> of size <code>m &times; n</code> where <code>units[i][j]</code> represents the capacity of the <code>j<sup>th</sup></code> unit in the <code>i<sup>th</sup></code> device. Each device contains <strong>exactly</strong> <code>n</code> units.</p>

<p>The <strong>rating</strong> of a device is the <strong>minimum</strong> capacity among all its units.</p>

<p>You may perform the following operation any number of times (including zero):</p>

<ul>
	<li>Choose a device <code>i</code> that has <strong>not been</strong> used as a source before.</li>
	<li>Remove <strong>exactly</strong> one unit from device <code>i</code> and add it to <strong>any</strong> different device.</li>
	<li>Then mark device <code>i</code> as used, so it cannot be chosen again as a source.</li>
</ul>

<p>Return the <strong>maximum</strong> possible sum of the ratings of all devices after any number of such operations.</p>

<p><strong>Note:</strong></p>

<ul>
	<li>Devices can receive units from multiple devices, regardless of whether they have been selected.</li>
	<li>The rating of an empty device is 0.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">units = [[1,3],[2,2]]</span></p>

<p><strong>Output:</strong> <span class="example-io">4</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>​​​​​​​​​​​​​​Select device <code>i = 0</code> and transfer <code>units[0][0] = 1</code> to device <code>i = 1</code>.</li>
	<li>After the transfer, the ratings are:
	<ul>
		<li>Device <code>0 = [3]</code>: <code>rating[0] = 3</code></li>
		<li>Device <code>1 = [2, 2, <u>1</u>]</code>: <code>rating[1] = 1</code></li>
	</ul>
	</li>
	<li>Thus, the sum of ratings is <code>3 + 1 = 4</code>.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">units = [[1,2,3],[4,5,6]]</span></p>

<p><strong>Output:</strong> <span class="example-io">6</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>Select device <code>i = 1</code> and transfer <code>units[1][0] = 4</code> to device <code>i = 0</code>.</li>
	<li>After the transfer, the ratings are:
	<ul>
		<li>Device <code>0 = [1, 2, 3, <u>4</u>]</code>: <code>rating[0] = 1</code></li>
		<li>Device <code>1 = [5, 6]</code>: <code>rating[1] = 5</code></li>
	</ul>
	</li>
	<li>Thus, the sum of ratings is <code>1 + 5 = 6</code>.</li>
</ul>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">units = [[5,5,5],[1,1,1]]</span></p>

<p><strong>Output:</strong> <span class="example-io">6</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>No transfers increase the sum of ratings. Thus, the sum of ratings is <code>5 + 1 = 6</code>.</li>
</ul>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= m == units.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= n == units[i].length &lt;= 10<sup>5</sup></code></li>
	<li><code>m * n &lt;= 2 * 10<sup>5</sup></code></li>
	<li><code>1 &lt;= units[i][j] &lt;= 10<sup>5</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4004-maximize-sum-of-device-ratings/solution.cpp)

```cpp
class Solution {
public:
    
    
    long long maxRatings(vector<vector<int>>& units) {
        int m = units.size();
        int n = units[0].size();
        
        if(n == 1){
            long long total = 0;
            for(int i=0; i<m; i++){
                total += units[i][0];
            }
            return total;
        }
        int globalMini = INT_MAX;
        int mini2Mini = INT_MAX;
        long long total = 0;

        for(int i=0; i<m; i++){
            int mini1 = INT_MAX;
            int mini2 = INT_MAX;

            for(int j=0; j<n; j++){
                if(units[i][j] < mini1){
                    mini2 = mini1;
                    mini1 = units[i][j];
                }
                else if(units[i][j] < mini2){
                    mini2  = units[i][j];
                }
            }
            total += mini2;
            mini2Mini = min(mini2Mini, mini2);
            globalMini = min(globalMini, mini1);

        }
        total = total - mini2Mini + globalMini;
        return total;

    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
