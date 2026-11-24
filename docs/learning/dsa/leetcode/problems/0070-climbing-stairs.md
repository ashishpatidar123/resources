# 70. Climbing Stairs

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0070-climbing-stairs)

## Problem

<p>You are climbing a staircase. It takes <code>n</code> steps to reach the top.</p>

<p>Each time you can either climb <code>1</code> or <code>2</code> steps. In how many distinct ways can you climb to the top?</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> n = 2
<strong>Output:</strong> 2
<strong>Explanation:</strong> There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> n = 3
<strong>Output:</strong> 3
<strong>Explanation:</strong> There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= n &lt;= 45</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0070-climbing-stairs/solution.cpp)

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if(n==0){
            return 1;
        }
        else if(n==2 || n==1){
            return n;
        }
        int a = 1;
        int b = 1;
        int c = 0;

        for(int i=2; i<=n; i++){
            c = a+b;
            a = b;
            b = c;
        }
        return b;
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
