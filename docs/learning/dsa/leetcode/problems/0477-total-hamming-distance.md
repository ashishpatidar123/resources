# 477. Total Hamming Distance

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0477-total-hamming-distance)

## Problem

<p>The <a href="https://en.wikipedia.org/wiki/Hamming_distance" target="_blank">Hamming distance</a> between two integers is the number of positions at which the corresponding bits are different.</p>

<p>Given an integer array <code>nums</code>, return <em>the sum of <strong>Hamming distances</strong> between all the pairs of the integers in</em> <code>nums</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [4,14,2]
<strong>Output:</strong> 6
<strong>Explanation:</strong> In binary representation, the 4 is 0100, 14 is 1110, and 2 is 0010 (just
showing the four bits relevant in this case).
The answer will be:
HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2) = 2 + 2 + 2 = 6.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [4,14,4]
<strong>Output:</strong> 4
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>0 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
	<li>The answer for the given input will fit in a <strong>32-bit</strong> integer.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0477-total-hamming-distance/solution.cpp)

```cpp
class Solution {
public:
    // unsigned int countSetBits(int n){
    //     unsigned int count = 0;
    //     while (n) {
    //         n &= (n - 1);
    //         count++;
    //     }
    //     return count;
    // }
    int BitsSetTable256[256];
    void initialize() 
    { 

        // To initially generate the 
        // table algorithmically 
        BitsSetTable256[0] = 0; 
        for (int i = 0; i < 256; i++)
        { 
            BitsSetTable256[i] = (i & 1) + 
            BitsSetTable256[i / 2]; 
        } 
    } 
 
    int countSetBits(int n) 
    { 
        return (BitsSetTable256[n & 0xff] + 
                BitsSetTable256[(n >> 8) & 0xff] + 
                BitsSetTable256[(n >> 16) & 0xff] + 
                BitsSetTable256[n >> 24]); 
    }   
    int totalHammingDistance(vector<int>& nums) {
        
        int n = nums.size();
        long long int ans = 0;
        // initialize();
        // for(int i=0; i<n; i++){
        //     for(int j=i+1; j<n; j++){
        //         int temp = nums[i]^nums[j];
        //         ans += countSetBits(temp);
        //     }
        // }
        // return ans;

        for(int b=0; b<32; b++){
            int count1 = 0;

            for(int x:nums){
                if(x&(1 << b)){
                    count1++;
                }
            }
            int count0 = n - count1;

            ans = ans + (long long int)count1*count0;
        }
        return ans;

    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
