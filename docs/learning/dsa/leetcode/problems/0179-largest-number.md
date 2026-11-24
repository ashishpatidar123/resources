# 179. Largest Number

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0179-largest-number)

## Problem

<p>Given a list of non-negative integers <code>nums</code>, arrange them such that they form the largest number and return it.</p>

<p>Since the result may be very large, so you need to return a string instead of an integer.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [10,2]
<strong>Output:</strong> &quot;210&quot;
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,30,34,5,9]
<strong>Output:</strong> &quot;9534330&quot;
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 100</code></li>
	<li><code>0 &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/0179-largest-number/solution.cpp)

```cpp
#include <vector>
#include <string>
#include <algorithm>

class Solution {
private:
    class largerNumbercomparator {
    public:
        bool operator()(const std::string& a, const std::string& b) {
            std::string order1 = a + b;
            std::string order2 = b + a;
            return order2.compare(order1) < 0;
        }
    };

public:
    std::string largestNumber(std::vector<int> A) {
        std::vector<std::string> asString(A.size());
        for (int i = 0; i < A.size(); i++) {
            asString[i] = std::to_string(A[i]);
        }

        std::sort(asString.begin(), asString.end(), largerNumbercomparator());

        if (asString[0] == "0") {
            return "0";
        }

        std::string largestnumber = "";
        for (std::string str : asString) {
            largestnumber += str;
        }
        return largestnumber;
    }
};
```

---

[← Back to Medium](medium.md) · [All problems](index.md)
