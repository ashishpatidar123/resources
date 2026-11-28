# 4412. Count Good Cyclic Rotations

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4412-count-good-cyclic-rotations)

## Problem

# Count Good Cyclic Rotations

### Difficulty: Medium
### Topics: 

<p>You are given an integer array <code>nums</code> of even length <code>n</code>.</p>

<p>A <strong>cyclic rotation</strong> of <code>nums</code> is obtained by choosing a <span data-keyword="array-prefix">prefix</span> of <code>nums</code> whose length is between 0 and <code>n - 1</code> (inclusive), and moving it to the end of the array while preserving the order of all elements.</p>

<p>A cyclic rotation is <strong>good</strong> if the sum of its first <code>n / 2</code> elements is <strong>strictly greater</strong> than the sum of its last <code>n / 2</code> elements.</p>

<p>Return the number of cyclic rotations of <code>nums</code> that are good.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,3,4,5,6]</span></p>

<p><strong>Output:</strong> <span class="example-io">3</span></p>

<p><strong>Explanation:</strong></p>

<p>The cyclic rotations of <code>nums</code> are:</p>

<table>
	<thead>
		<tr>
			<th style="text-align: center; padding: 6px 12px;">Cyclic rotation</th>
			<th style="text-align: center; padding: 6px 12px;">Sum of first <code>n / 2</code> elements</th>
			<th style="text-align: center; padding: 6px 12px;">Sum of last <code>n / 2</code> elements</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[1, 2, 3, 4, 5, 6]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 + 3 = 6</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>4 + 5 + 6 = 15</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[2, 3, 4, 5, 6, 1]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 3 + 4 = 9</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>5 + 6 + 1 = 12</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[3, 4, 5, 6, 1, 2]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>3 + 4 + 5 = 12</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>6 + 1 + 2 = 9</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[4, 5, 6, 1, 2, 3]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>4 + 5 + 6 = 15</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 + 3 = 6</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[5, 6, 1, 2, 3, 4]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>5 + 6 + 1 = 12</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 3 + 4 = 9</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[6, 1, 2, 3, 4, 5]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>6 + 1 + 2 = 9</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>3 + 4 + 5 = 12</code></td>
		</tr>
	</tbody>
</table>

<p>The first half has a greater sum than the second half for 3 rotations. Thus, the answer is 3.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,1,2]</span></p>

<p><strong>Output:</strong> <span class="example-io">0</span></p>

<p><strong>Explanation:</strong></p>

<p>The cyclic rotations of <code>nums</code> are:</p>

<table>
	<thead>
		<tr>
			<th style="text-align: center; padding: 6px 12px;">Cyclic rotation</th>
			<th style="text-align: center; padding: 6px 12px;">Sum of first <code>n / 2</code> elements</th>
			<th style="text-align: center; padding: 6px 12px;">Sum of last <code>n / 2</code> elements</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[1, 2, 1, 2]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 = 3</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 = 3</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[2, 1, 2, 1]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 1 = 3</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 1 = 3</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[1, 2, 1, 2]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 = 3</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>1 + 2 = 3</code></td>
		</tr>
		<tr>
			<td style="text-align: center; padding: 6px 12px;"><code>[2, 1, 2, 1]</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 1 = 3</code></td>
			<td style="text-align: center; padding: 6px 12px;"><code>2 + 1 = 3</code></td>
		</tr>
	</tbody>
</table>

<p>No cyclic rotation is good because the two sums are equal for every rotation. Thus, the answer is 0.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= n == nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
	<li><code>n</code> is even.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4412-count-good-cyclic-rotations/solution.cpp)

```cpp
class Solution {
public:
    int countGoodRotations(vector<int>& nums) {
        int n = nums.size();
        int count = 0;
        vector<long long int>prefix(2*n+1, 0);
        for(int i=0; i<2*n; i++){
            prefix[i+1] = prefix[i] + nums[i%n];
        }
        for(int l=0; l<n; l++){
            int m = n + l;
            long long int last = prefix[m] - prefix[m -n/2];
            long long int first = prefix[m - n/2] - prefix[l];

            if(first > last) count++;
        }
        return count;
    }
};
```

### `solution_2137879884.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4412-count-good-cyclic-rotations/solution_2137879884.cpp)

```cpp
class Solution {
public:
    int countGoodRotations(vector<int>& nums) {
        int n = nums.size();
        int count = 0;
        long long int total = 0;

        
        for(int i=0; i<n; i++){
            total += nums[i];
        }
        
        int k = n - n/2;
        long long int windowTotal = 0;

        for(int i=0; i<k; i++){
            windowTotal += nums[i];
        }

        for(int l=0; l<n; l++){
            if(2*windowTotal > total){
                count++;
            }
            windowTotal -= nums[l];
            windowTotal += nums[(l+k)%n];
        }
        return count;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
