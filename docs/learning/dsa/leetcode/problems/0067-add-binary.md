# 67. Add Binary

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0067-add-binary)

## Problem

<p>Given two binary strings <code>a</code> and <code>b</code>, return <em>their sum as a binary string</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> a = "11", b = "1"
<strong>Output:</strong> "100"
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> a = "1010", b = "1011"
<strong>Output:</strong> "10101"
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= a.length, b.length &lt;= 10<sup>4</sup></code></li>
	<li><code>a</code> and <code>b</code> consist&nbsp;only of <code>&#39;0&#39;</code> or <code>&#39;1&#39;</code> characters.</li>
	<li>Each string does not contain leading zeros except for the zero itself.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0067-add-binary/solution.cpp)

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        
        char carry = '0';

        int n = a.length();
        int m = b.length();
        int i = n-1;
        int j = m-1;

        string s = "";

        while(i>=0 && j>=0){

            if(a[i]=='0' && b[j] == '0'){

                if(carry=='0'){
                    s = s + '0';
                }
                else if(carry=='1'){
                    s = s + '1';
                    carry = '0';
                }
            }
            else if(a[i]=='0' && b[j] == '1'){

                if(carry=='0'){
                    s = s + '1';
                }
                else if(carry=='1'){
                    s = s + '0';
                    carry = '1';
                } 
            }
            else if(a[i]=='1' && b[j] == '0'){

                if(carry=='0'){
                    s = s + '1';
                }
                else if(carry=='1'){
                    s = s + '0';
                    carry = '1';
                }    
            }
            else {

                if(carry=='0'){
                    s = s + '0';
                    carry = '1';
                }
                else if(carry=='1'){
                    s = s + '1';
                    carry = '1';
                } 
            }
            i--;
            j--;

        }
        while(i>=0){
            if(a[i]=='0'){
                
                if(carry == '0'){
                    s = s + '0';
                    carry = '0';
                }
                else{
                    s = s + '1';
                    carry = '0';
                }
            }
            else{

                if(carry == '0'){
                    s = s + '1';
                    carry = '0';
                }
                else{
                    s = s + '0';
                    carry = '1';
                }
            }
            i--;
        }
        while(j>=0)
        {
            if(b[j]=='0'){
                
                if(carry == '0'){
                    s = s + '0';
                    carry = '0';
                }
                else{
                    s = s + '1';
                    carry = '0';
                }
            }
            else{

                if(carry == '0'){
                    s = s + '1';
                    carry = '0';
                }
                else{
                    s = s + '0';
                    carry = '1';
                }
            }
            j--;
        }
        if(carry == '1'){
            s = s + '1';
        }
        reverse(s.begin(),s.end());
        return s;

    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
