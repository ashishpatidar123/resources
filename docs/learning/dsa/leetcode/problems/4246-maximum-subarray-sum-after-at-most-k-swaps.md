# 4246. Maximum Subarray Sum After At Most K Swaps

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/4246-maximum-subarray-sum-after-at-most-k-swaps)

## Problem

<p>You are given an integer array <code>nums</code> and an integer <code>k</code>.</p>

<p>You are allowed to perform <strong>at most</strong> <code>k</code> swap operations on the array.</p>

<p>In one swap operation, you may choose any two indices <code>i</code> and <code>j</code> and swap <code>nums[i]</code> and <code>nums[j]</code>.</p>

<p>Return an integer denoting the <strong>maximum possible <span data-keyword="subarray-nonempty">subarray</span> sum</strong> after performing the swaps.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,-1,0,2], k = 1</span></p>

<p><strong>Output:</strong> <span class="example-io">3</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>We can swap on indices 1 and 3, resulting in the array <code>[1, 2, 0, -1]</code>.</li>
	<li>The subarray <code>[1, 2]</code> has a sum of 3, which is the maximum possible subarray sum after at most <code>k = 1</code>​​​​​​​ swap.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [4,3,2,4], k = 2</span></p>

<p><strong>Output:</strong> <span class="example-io">13</span></p>

<p><strong>Explanation:</strong></p>

<p>The maximum possible subarray sum after at most <code>k = 2</code> swaps is the sum of the entire array, which is 13.</p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [-1,-2], k = 0</span></p>

<p><strong>Output:</strong> <span class="example-io">-1</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li><code>k = 0</code> swaps are allowed.</li>
	<li>The possible subarrays are <code>[-1]</code>, <code>[-2]</code>, and <code>[-1, -2]</code>, with sums -1, -2, and -3 respectively.</li>
	<li>Among these sums, the maximum is -1.</li>
</ul>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 1500</code></li>
	<li><code>-10<sup>5</sup> &lt;= nums[i] &lt;= 10<sup>5</sup></code></li>
	<li><code>0 &lt;= k &lt;= nums.length</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/4246-maximum-subarray-sum-after-at-most-k-swaps/solution.cpp)

```cpp
class SegmentTree{
private:
    int V; // number of unique values
    vector<int>cnt; // tracks how many numbers are in this range
    vector<long long> sum; //tracks the total sum of numbers in this range
    const vector<int>& unique_vals; //reference to the compressed mapping array


    void update_tree(int node, int start, int end, int id, int val, int freq){
        if(start == end){
            cnt[node] += freq;
            sum[node] += (1LL * val * freq);
            return;
        }   

        int mid = start + (end - start)/2;

        if(id <= mid){
            update_tree(2*node, start, mid, id, val, freq);
        }
        else{
            update_tree(2*node + 1, mid+1, end, id, val, freq);
        }

        cnt[node] = cnt[node*2] + cnt[node*2 + 1];
        sum[node] = sum[node*2] + sum[node*2 + 1];
    }
    // Recursive query for the K-th smallest exact value
    int query_kth_smallest(int node, int start, int end, int k) {
        if (start == end) return unique_vals[start]; // Found the leaf!
        
        int mid = start + (end - start) / 2;
        int left_count = cnt[2 * node];
        
        if (left_count >= k) {
            return query_kth_smallest(2 * node, start, mid, k);
        } else {
            return query_kth_smallest(2 * node + 1, mid + 1, end, k - left_count);
        }
    }

    // Recursive query for the K-th largest exact value
    int query_kth_largest(int node, int start, int end, int k) {
        if (start == end) return unique_vals[start];
        
        int mid = start + (end - start) / 2;
        int right_count = cnt[2 * node + 1]; // Look at right child first!
        
        if (right_count >= k) {
            return query_kth_largest(2 * node + 1, mid + 1, end, k);
        } else {
            return query_kth_largest(2 * node, start, mid, k - right_count);
        }
    }
    // Recursive query for the sum of the K smallest elements
    long long query_sum_smallest(int node, int start, int end, int k) {
        if (k == 0) return 0;
        if (cnt[node] <= k) return sum[node]; // Take the whole node if it fits
        if (start == end) return 1LL * k * unique_vals[start]; // Take partial leaf
        
        int mid = start + (end - start) / 2;
        int left_count = cnt[2 * node];
        
        if (left_count >= k) {
            return query_sum_smallest(2 * node, start, mid, k);
        } else {
            return sum[2 * node] + query_sum_smallest(2 * node + 1, mid + 1, end, k - left_count);
        }
    }

    // Recursive query for the sum of the K largest elements
    long long query_sum_largest(int node, int start, int end, int k) {
        if (k == 0) return 0;
        if (cnt[node] <= k) return sum[node];
        if (start == end) return 1LL * k * unique_vals[start];
        
        int mid = start + (end - start) / 2;
        int right_count = cnt[2 * node + 1]; // Pull from the right first!
        
        if (right_count >= k) {
            return query_sum_largest(2 * node + 1, mid + 1, end, k);
        } else {
            return sum[2 * node + 1] + query_sum_largest(2 * node, start, mid, k - right_count);
        }
    }

public:
    // Constructor
    SegmentTree(int size, const vector<int>& mapped_vals) 
        : V(size), unique_vals(mapped_vals) {
        // 1-indexed segment tree (size 4*N is standard safe size)
        cnt.assign(4 * V + 1, 0);
        sum.assign(4 * V + 1, 0);
    }

    // Public API for our outer loop
    void add(int id, int val) { update_tree(1, 0, V - 1, id, val, 1); }
    void remove(int id, int val) { update_tree(1, 0, V - 1, id, val, -1); }
    
    int get_kth_smallest(int k) { return query_kth_smallest(1, 0, V - 1, k); }
    int get_kth_largest(int k) { return query_kth_largest(1, 0, V - 1, k); }
    
    long long get_sum_smallest(int k) { return query_sum_smallest(1, 0, V - 1, k); }
    long long get_sum_largest(int k) { return query_sum_largest(1, 0, V - 1, k); }

};



class Solution {
public:
    long long maxSum(vector<int>& nums, int k) {
        int n = nums.size();
        
        // Coordinate Compression
        vector<int> unique_vals = nums;
        sort(unique_vals.begin(), unique_vals.end());
        auto remove_ptr = unique(unique_vals.begin(), unique_vals.end());
        unique_vals.erase(remove_ptr, unique_vals.end());

        int V = unique_vals.size();

        auto get_id = [&](int val){
            return lower_bound(unique_vals.begin(), unique_vals.end(), val) - unique_vals.begin();
        };

        long long global_max = -1e18;

        // 1. Instantiate the trees ONLY ONCE outside the loops
        SegmentTree FullTree(V, unique_vals);
        for (int num : nums) {
            FullTree.add(get_id(num), num);
        }
        
        SegmentTree InsideTree(V, unique_vals);
        SegmentTree OutsideTree = FullTree;

        for(int i = 0; i < n; i++){
            long long curr_sum = 0;

            // 1. Declare best_t OUTSIDE the 'j' loop so it carries over!
            int best_t = 0;

            for(int j = i; j < n; j++) {
                int val = nums[j];
                int id = get_id(val);

                // Expand window
                OutsideTree.remove(id, val);
                InsideTree.add(id, val);
                curr_sum += val;

                int max_swaps = min({k, j - i + 1, n - (j - i + 1)});
                
                // --- NO MORE BINARY SEARCH ---
                
                // 2. Cap best_t just in case our window size restricts it
                best_t = min(best_t, max_swaps);

                // 3. Adjust best_t DOWNWARDS if the current swaps are no longer profitable
                while (best_t > 0) {
                    long long outside_val = OutsideTree.get_kth_largest(best_t);
                    long long inside_val = InsideTree.get_kth_smallest(best_t);
                    
                    if (outside_val > inside_val) {
                        break; // Still profitable, stop adjusting downwards!
                    }
                    best_t--;
                }

                // 4. Adjust best_t UPWARDS if we can get away with MORE profitable swaps
                while (best_t < max_swaps) {
                    long long outside_val = OutsideTree.get_kth_largest(best_t + 1);
                    long long inside_val = InsideTree.get_kth_smallest(best_t + 1);
                    
                    if (outside_val > inside_val) {
                        best_t++;
                    } else {
                        break; // Not profitable, stop adjusting upwards!
                    }
                }

                // --- END OPTIMIZATION ---

                long long max_gain = 0;
                if(best_t > 0){
                    long long gained_from_outside = OutsideTree.get_sum_largest(best_t);
                    long long lost_from_inside = InsideTree.get_sum_smallest(best_t);
                    max_gain = gained_from_outside - lost_from_inside;
                }

                global_max = max(global_max, curr_sum + max_gain);
            }
            
            // 2. THE ROLLBACK TRICK: 
            // Undo all the moves we made in the inner loop so the trees are completely 
            // reset for the next starting position 'i + 1', without copying vectors!
            for(int j = i; j < n; j++) {
                int val = nums[j];
                int id = get_id(val);
                InsideTree.remove(id, val);
                OutsideTree.add(id, val);
            }
        }

        return global_max;
    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
