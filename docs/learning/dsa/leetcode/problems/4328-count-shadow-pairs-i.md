# 4328. Count Shadow Pairs I

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4328-count-shadow-pairs-i)

## Problem

# Count Shadow Pairs I

### Difficulty: Medium
### Topics: 

<p>You are given an integer array <code>nums</code> of length <code>n</code>.</p>

<p>A pair of indices <code>(i, j)</code> is called a <strong>shadow pair</strong> if all of the following conditions are satisfied:</p>

<ul>
	<li><code>0 &lt;= i &lt; j &lt; n</code></li>
	<li><code>nums[i] &lt; nums[j]</code></li>
	<li>There <strong>does not exist</strong> an index <code>k</code> such that <code>i &lt; k &lt; j</code> and <code>nums[k] &lt; nums[i] &lt; nums[j]</code>.</li>
</ul>

<p>Return the total number of <strong>shadow pairs</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [3,1,4,1,5]</span></p>

<p><strong>Output:</strong> <span class="example-io">3</span></p>

<p><strong>Explanation:</strong></p>

<table style="border-collapse: collapse; text-align: center; width: 70%;">
	<thead>
		<tr>
			<th style="padding: 8px;"><code>(i, j)</code></th>
			<th style="padding: 8px;"><code>nums[i]</code></th>
			<th style="padding: 8px;"><code>nums[j]</code></th>
			<th style="padding: 8px;">Shadow Pair</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>(1, 2)</td>
			<td>1</td>
			<td>4</td>
			<td>No index <code>k</code> exists such that <code>1 &lt; k &lt; 2</code></td>
		</tr>
		<tr>
			<td>(1, 4)</td>
			<td>1</td>
			<td>5</td>
			<td><code>nums[2] = 4</code> and <code>nums[3] = 1</code> are not smaller than 1</td>
		</tr>
		<tr>
			<td>(3, 4)</td>
			<td>1</td>
			<td>5</td>
			<td>No index <code>k</code> exists such that <code>3 &lt; k &lt; 4</code></td>
		</tr>
	</tbody>
</table>

<p>Thus, the answer is 3.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [6,7,6,6,7]</span></p>

<p><strong>Output:</strong> <span class="example-io">4</span></p>

<p><strong>Explanation:</strong></p>

<table style="border-collapse: collapse; text-align: center; width: 70%;">
	<thead>
		<tr>
			<th style="padding: 8px;"><code>(i, j)</code></th>
			<th style="padding: 8px;"><code>nums[i]</code></th>
			<th style="padding: 8px;"><code>nums[j]</code></th>
			<th style="padding: 8px;">Shadow Pair</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>(0, 1)</td>
			<td>6</td>
			<td>7</td>
			<td>No index <code>k</code> exists such that <code>0 &lt; k &lt; 1</code></td>
		</tr>
		<tr>
			<td>(0, 4)</td>
			<td>6</td>
			<td>7</td>
			<td><code>nums[1] = 7</code>, <code>nums[2] = 6</code>, and <code>nums[3] = 6</code> are not smaller than 6</td>
		</tr>
		<tr>
			<td>(2, 4)</td>
			<td>6</td>
			<td>7</td>
			<td><code>nums[3] = 6</code> is not smaller than 6</td>
		</tr>
		<tr>
			<td>(3, 4)</td>
			<td>6</td>
			<td>7</td>
			<td>No index <code>k</code> exists such that <code>3 &lt; k &lt; 4</code></td>
		</tr>
	</tbody>
</table>

<p>Thus, the answer is 4.</p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,3,4]</span></p>

<p><strong>Output:</strong> <span class="example-io">6</span></p>

<p><strong>Explanation:</strong></p>

<table style="border-collapse: collapse; text-align: center; width: 70%;">
	<thead>
		<tr>
			<th style="padding: 8px;"><code>(i, j)</code></th>
			<th style="padding: 8px;"><code>nums[i]</code></th>
			<th style="padding: 8px;"><code>nums[j]</code></th>
			<th style="padding: 8px;">Shadow Pair</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>(0, 1)</td>
			<td>1</td>
			<td>2</td>
			<td>No index <code>k</code> exists such that <code>0 &lt; k &lt; 1</code></td>
		</tr>
		<tr>
			<td>(0, 2)</td>
			<td>1</td>
			<td>3</td>
			<td><code>nums[1] = 2</code> is not smaller than 1</td>
		</tr>
		<tr>
			<td>(0, 3)</td>
			<td>1</td>
			<td>4</td>
			<td><code>nums[1] = 2</code> and <code>nums[2] = 3</code> are not smaller than 1</td>
		</tr>
		<tr>
			<td>(1, 2)</td>
			<td>2</td>
			<td>3</td>
			<td>No index <code>k</code> exists such that <code>1 &lt; k &lt; 2</code></td>
		</tr>
		<tr>
			<td>(1, 3)</td>
			<td>2</td>
			<td>4</td>
			<td><code>nums[2] = 3</code> is not smaller than 2</td>
		</tr>
		<tr>
			<td>(2, 3)</td>
			<td>3</td>
			<td>4</td>
			<td>No index <code>k</code> exists such that <code>2 &lt; k &lt; 3</code></td>
		</tr>
	</tbody>
</table>

<p>Thus, the answer is 6.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>3 &lt;= n == nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution_2145149473.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4328-count-shadow-pairs-i/solution_2145149473.cpp)

```cpp
class Solution {
public:
    std::vector<int> findNextSmallerIndices(const std::vector<int>& arr) {
        int n = arr.size();
        std::vector<int> result(n, -1);
        std::stack<int> st;

        for (int i = n - 1; i >= 0; --i) {
            // Pop elements that are greater than or equal to the current element
            while (!st.empty() && arr[st.top()] >= arr[i]) {
                st.pop();
            }

            // If stack is not empty, the top element is the closest smaller index
            if (!st.empty()) {
                result[i] = st.top();
            }

            // Push the current index onto the stack
            st.push(i);
        }

        return result;
    }
    int count_occurrences_to_right(const std::unordered_map<int, std::vector<int>>& index_map, int val, int i, int k) {
        if (i >= k) return 0;
        
        auto it = index_map.find(val);
        if (it == index_map.end()) return 0;

        const auto& indices = it->second;
        auto lower = std::lower_bound(indices.begin(), indices.end(), i + 1);
        auto upper = std::upper_bound(indices.begin(), indices.end(), k);

        return std::distance(lower, upper);
    }

    long long shadowPairs(vector<int>& nums) {

        int n = nums.size();
        long long int ans = 0;
        vector<int> indexes = findNextSmallerIndices(nums);
        unordered_map<int, vector<int>> index_map;
        for (int i = 0; i < nums.size(); ++i) {
            index_map[nums[i]].push_back(i);
        }

        vector<long long int>temp(n, 0);
        temp[n-1] = 0;
        
        unordered_map<int, int> count;
        count[nums[n-1]]++;

        for(int i=n-2; i>=0; i--){
            if(nums[i] < nums[i+1]){
                int index = indexes[i];
                if(indexes[i] != -1){
                    temp[i] = index - i - 1;
                    
                    int c = count_occurrences_to_right(index_map, nums[i], i, index);
                    count[nums[i]] = c; 
                }
                else{
                    
                    temp[i] = n - i - 1;
                }
                
                if(count.find(nums[i]) != count.end()){
                    
                    temp[i] = temp[i] - count[nums[i]];
                }
            }
            if(nums[i] == nums[i+1]){
                temp[i] = temp[i+1];
            }
            count[nums[i]]++;
        }
        for(int i=0; i<n; i++){
            // cout<<temp[i]<<" ";
            ans += temp[i];
        }
        return ans;
    }
};
```

### `solution_2145153408.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4328-count-shadow-pairs-i/solution_2145153408.cpp)

```cpp
// class Solution {
// public:
//     std::vector<int> findNextSmallerIndices(const std::vector<int>& arr) {
//         int n = arr.size();
//         std::vector<int> result(n, -1);
//         std::stack<int> st;

//         for (int i = n - 1; i >= 0; --i) {
//             // Pop elements that are greater than or equal to the current element
//             while (!st.empty() && arr[st.top()] >= arr[i]) {
//                 st.pop();
//             }

//             // If stack is not empty, the top element is the closest smaller index
//             if (!st.empty()) {
//                 result[i] = st.top();
//             }

//             // Push the current index onto the stack
//             st.push(i);
//         }

//         return result;
//     }
//     int count_occurrences_to_right(const std::unordered_map<int, std::vector<int>>& index_map, int val, int i, int k) {
//         if (i >= k) return 0;
        
//         auto it = index_map.find(val);
//         if (it == index_map.end()) return 0;

//         const auto& indices = it->second;
//         auto lower = std::lower_bound(indices.begin(), indices.end(), i + 1);
//         auto upper = std::upper_bound(indices.begin(), indices.end(), k);

//         return std::distance(lower, upper);
//     }

//     long long shadowPairs(vector<int>& nums) {

//         int n = nums.size();
//         long long int ans = 0;
//         vector<int> indexes = findNextSmallerIndices(nums);
//         unordered_map<int, vector<int>> index_map;
//         for (int i = 0; i < nums.size(); ++i) {
//             index_map[nums[i]].push_back(i);
//         }

//         vector<long long int>temp(n, 0);
//         temp[n-1] = 0;
        
//         unordered_map<int, int> count;
//         count[nums[n-1]]++;

//         for(int i=n-2; i>=0; i--){
//             if(nums[i] < nums[i+1]){
//                 int index = indexes[i];
//                 if(indexes[i] != -1){
//                     temp[i] = index - i - 1;
                    
//                     int c = count_occurrences_to_right(index_map, nums[i], i, index);
//                     count[nums[i]] = c; 
//                 }
//                 else{
                    
//                     temp[i] = n - i - 1;
//                 }
                
//                 if(count.find(nums[i]) != count.end()){
                    
//                     temp[i] = temp[i] - count[nums[i]];
//                 }
//             }
//             if(nums[i] == nums[i+1]){
//                 temp[i] = temp[i+1];
//             }
//             count[nums[i]]++;
//         }
//         for(int i=0; i<n; i++){
//             // cout<<temp[i]<<" ";
//             ans += temp[i];
//         }
//         return ans;
//     }
// };
class Solution {
public:
    long long shadowPairs(vector<int>& nums) {
        int n = nums.size();
        long long int ans = 0;
        vector<long long int> temp(n, 0);
        stack<int> st; 

        for (int i = n - 1; i >= 0; --i) {
            
            while(!st.empty() && nums[st.top()] > nums[i]){
                st.pop();
            }

            int index = st.empty() ? n : st.top();

            if(index == n){
                temp[i] = n - i - 1;
            }
            else if(nums[index] == nums[i]){
                temp[i] = temp[index] + (index - i - 1);
            }
            else{
                temp[i] = index - i - 1;
            }

            ans += temp[i];
            st.push(i);
        }
        
        return ans;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
