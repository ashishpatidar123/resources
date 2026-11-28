# 4344. Minimum Operations To Make Every Element Palindromic

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4344-minimum-operations-to-make-every-element-palindromic)

## Problem

# Minimum Operations to Make Every Element Palindromic

### Difficulty: Medium
### Topics: 

<p>You are given an integer array <code>nums</code>.</p>

<p>In one <strong>operation</strong>, you may choose an index <code>i</code> and either increment or decrement <code>nums[i]</code> by 2.</p>

<p>Return the <strong>minimum</strong> number of operations required to make every element in <code>nums</code> a <strong>positive</strong> <span data-keyword="palindrome-integer">palindrome</span>. Different elements may be changed into different palindromic integers.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [10,12,14,16]</span></p>

<p><strong>Output:</strong> <span class="example-io">9</span></p>

<p><strong>Explanation:</strong></p>

<p>One optimal sequence of operations is:</p>

<ul>
	<li>Decrement <code>nums[0]</code> by 2 once to change it from 10 to 8.</li>
	<li>Decrement <code>nums[1]</code> by 2 twice to change it from 12 to 8.</li>
	<li>Decrement <code>nums[2]</code> by 2 three times to change it from 14 to 8.</li>
	<li>Increment <code>nums[3]</code> by 2 three times to change it from 16 to 22.</li>
</ul>

<p>After <code>1 + 2 + 3 + 3 = 9</code> operations, <code>nums = [8, 8, 8, 22]</code>, and every element is a positive palindromic integer.</p>

<p>It can be shown that fewer than 9 operations cannot achieve this.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [9,10,11,10]</span></p>

<p><strong>Output:</strong> <span class="example-io">2</span></p>

<p><strong>Explanation:</strong></p>

<p>Decrement <code>nums[1]</code> and <code>nums[3]</code> by 2 once each.</p>

<p>After 2 operations, <code>nums = [9, 8, 11, 8]</code>, and every element is a positive palindromic integer.</p>

<p>At least one operation is needed for each of these two elements, so the minimum number of operations is 2.</p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [125]</span></p>

<p><strong>Output:</strong> <span class="example-io">2</span></p>

<p><strong>Explanation:</strong></p>

<p>Decrement <code>nums[0]</code> by 2 twice to change it from 125 to 121, which is a positive palindromic integer.</p>

<p>A single operation would change it to 123 or 127, neither of which is palindromic. Thus, the minimum number of operations is 2.</p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>1 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution_2144681112.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/4344-minimum-operations-to-make-every-element-palindromic/solution_2144681112.cpp)

```cpp
vector<long long int> even;
vector<long long int> odd;
bool created = false;

void compute(){
    if(created){
        return;
    }

    created = true;

    for(int i=1; i<=100000; i++){
        string s = to_string(i);
        string s2 = s;
        reverse(s2.begin(), s2.end());

        string s_even = s + s2;
        long long int p_even  = stoll(s_even);
        if(p_even % 2 == 0){
            even.push_back(p_even);
        }
        else{
            odd.push_back(p_even);
        }

        string s_odd = s + s2.substr(1);
        long long int p_odd  = stoll(s_odd);
        if(p_odd % 2 == 0){
            even.push_back(p_odd);
        }
        else{
            odd.push_back(p_odd);
        }
    }

    sort(even.begin(), even.end());
    sort(odd.begin(), odd.end());
}
class Solution {
public:
    bool check(long long int n){

        string s = to_string(n);

        if(s.length() == 1) return true;

        int i=0;
        int j=s.length()-1;

        while(j>i && s[i] == s[j]){
            i++;
            j--;
        }

        if(j>i) return false;
        return true;

    }
    long long minOperations(vector<int>& nums) {

        // int n = nums.size();

        // long long int ans = 0;

        // for(int i=0; i<n; i++){
        //     long long temp = nums[i];

        //     long long int count1 = 0;

        //     while(!check(temp)){
        //         temp += 2;
        //         count1++;
        //     }

        //     temp = nums[i];
        //     long long int count2=0;
        //     while(temp >=0 && !check(temp)){
        //         temp -= 2;
        //         count2++;
        //     } 

        //     ans += min(count1, count2);
        // }

        // return ans;

        compute();

        long long int ans = 0;
        int n = nums.size();

        for(int i=0; i<n; i++){
            long long int x = nums[i];

            const vector<long long int>* temp;

            if(x%2 == 0){
                temp = &even;
            }
            else{
                temp = &odd;
            }

            auto it = lower_bound(temp->begin(), temp->end(), x);

            long long int min_diff = 2e18;

            if(it != temp->end()){
                min_diff = min(min_diff, abs(*it - x));
            }
            if(it != temp->begin()){
                min_diff = min(min_diff, abs(*(it-1) - x));
            }

            ans += (min_diff/2);
        }

        return ans;
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
