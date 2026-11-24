# 989. Largest Component Size By Common Factor

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0989-largest-component-size-by-common-factor)

## Problem

# Largest Component Size by Common Factor

### Difficulty: Hard
### Topics: Array, Hash Table, Math, Union-Find, Number Theory, Prime Factorization

<p>You are given an integer array of unique positive integers <code>nums</code>. Consider the following graph:</p>

<ul>
	<li>There are <code>nums.length</code> nodes, labeled <code>nums[0]</code> to <code>nums[nums.length - 1]</code>,</li>
	<li>There is an undirected edge between <code>nums[i]</code> and <code>nums[j]</code> if <code>nums[i]</code> and <code>nums[j]</code> share a common factor greater than <code>1</code>.</li>
</ul>

<p>Return <em>the size of the largest connected component in the graph</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/01/ex1.png" style="width: 500px; height: 97px;" />
<pre>
<strong>Input:</strong> nums = [4,6,15,35]
<strong>Output:</strong> 4
</pre>

<p><strong class="example">Example 2:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/01/ex2.png" style="width: 500px; height: 85px;" />
<pre>
<strong>Input:</strong> nums = [20,50,9,63]
<strong>Output:</strong> 2
</pre>

<p><strong class="example">Example 3:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2018/12/01/ex3.png" style="width: 500px; height: 260px;" />
<pre>
<strong>Input:</strong> nums = [2,3,6,7,4,12,21,39]
<strong>Output:</strong> 8
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 2 * 10<sup>4</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>5</sup></code></li>
	<li>All the values of <code>nums</code> are <strong>unique</strong>.</li>
</ul>

## My C++ Submissions

### `solution_2153940293.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0989-largest-component-size-by-common-factor/solution_2153940293.cpp)

```cpp
class Solution {
    int parent[100005];
    int size[100005];

    int find(int x){
        if(parent[x] == x){
            return x;
        }
        return parent[x] = find(parent[x]);
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);

        if(px == py) return;

        if(size[px] >= size[py]){
            parent[py] = px;
            size[px] += size[py];
        }
        else{
            parent[px] = py;
            size[py] += size[px];
        }
    }
public:
    int largestComponentSize(vector<int>& nums) {
         
        int n = nums.size();
        
        for(int i=0; i<100000; i++){
            parent[i] = i;
            size[i] = 1;
        }

        // for(int i=0; i<n; i++){
        //     for(int j=i+1; j<n; j++){
        //         if(find(i) == find(j)){
        //             continue;
        //         }
        //         if(gcd(nums[i], nums[j]) > 1){
        //             unite(i, j);
        //         }
        //     }
            
        // }
        // int ans = 0;
        // for(int i=0; i<n; i++){
        //     ans = max(ans, size[i]);
        // }

        // return ans;

        for(int i=0; i<n; i++){
            int num = nums[i];
            // instead checking for each pair, we will 
            // check the factors of that number and unite all
            for(int j=2; j*j <= num; j++){
                if(num % j == 0){
                    unite(num, j);
                    unite(num, num / j);
                }
            }
        }

        unordered_map<int, int>count;

        int ans = 0;
        for(int i=0; i<n; i++){
            // calculating the count of the numbers sharing the same root
            int root = find(nums[i]);
            count[root]++;
            ans = max(ans, count[root]);
        }
        return ans;
    }
};
```

### `solution_2153943703.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/0989-largest-component-size-by-common-factor/solution_2153943703.cpp)

```cpp
class Solution {
    int parent[100005];
    int size[100005];

    int find(int x){
        if(parent[x] == x){
            return x;
        }
        return parent[x] = find(parent[x]);
    }

    void unite(int x, int y){
        int px = find(x);
        int py = find(y);

        if(px == py) return;

        if(size[px] >= size[py]){
            parent[py] = px;
            size[px] += size[py];
        }
        else{
            parent[px] = py;
            size[py] += size[px];
        }
    }
public:
    int largestComponentSize(vector<int>& nums) {
         
        int n = nums.size();
        int maxi = -2;
         for(int i=0; i<n; i++){
            maxi = max(maxi, nums[i]);
        }
        for(int i=0; i<=maxi; i++){
            parent[i] = i;
            size[i] = 1;
        }

        // for(int i=0; i<n; i++){
        //     for(int j=i+1; j<n; j++){
        //         if(find(i) == find(j)){
        //             continue;
        //         }
        //         if(gcd(nums[i], nums[j]) > 1){
        //             unite(i, j);
        //         }
        //     }
            
        // }
        // int ans = 0;
        // for(int i=0; i<n; i++){
        //     ans = max(ans, size[i]);
        // }

        // return ans;

        for(int i=0; i<n; i++){
            int num = nums[i];
            // instead checking for each pair, we will 
            // check the factors of that number and unite all
            for(int j=2; j*j <= num; j++){
                if(num % j == 0){
                    unite(num, j);
                    unite(num, num / j);
                }
            }
        }

        unordered_map<int, int>count;

        int ans = 0;
        for(int i=0; i<n; i++){
            // calculating the count of the numbers sharing the same root
            int root = find(nums[i]);
            count[root]++;
            ans = max(ans, count[root]);
        }
        return ans;
    }
};
```

---

[← Back to Hard](hard.md) · [All problems](index.md)
