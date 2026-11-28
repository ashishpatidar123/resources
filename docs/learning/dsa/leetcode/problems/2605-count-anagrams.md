# 2605. Count Anagrams

**Difficulty:** Hard  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/2605-count-anagrams)

## Problem

<p>You are given a string <code>s</code> containing one or more words. Every consecutive pair of words is separated by a single space <code>&#39; &#39;</code>.</p>

<p>A string <code>t</code> is an <strong>anagram</strong> of string <code>s</code> if the <code>i<sup>th</sup></code> word of <code>t</code> is a <strong>permutation</strong> of the <code>i<sup>th</sup></code> word of <code>s</code>.</p>

<ul>
	<li>For example, <code>&quot;acb dfe&quot;</code> is an anagram of <code>&quot;abc def&quot;</code>, but <code>&quot;def cab&quot;</code>&nbsp;and <code>&quot;adc bef&quot;</code> are not.</li>
</ul>

<p>Return <em>the number of <strong>distinct anagrams</strong> of </em><code>s</code>. Since the answer may be very large, return it <strong>modulo</strong> <code>10<sup>9</sup> + 7</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;too hot&quot;
<strong>Output:</strong> 18
<strong>Explanation:</strong> Some of the anagrams of the given string are &quot;too hot&quot;, &quot;oot hot&quot;, &quot;oto toh&quot;, &quot;too toh&quot;, and &quot;too oht&quot;.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;aa&quot;
<strong>Output:</strong> 1
<strong>Explanation:</strong> There is only one anagram possible for the given string.</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 10<sup>5</sup></code></li>
	<li><code>s</code> consists of lowercase English letters and spaces <code>&#39; &#39;</code>.</li>
	<li>There is single space between consecutive words.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Hard/2605-count-anagrams/solution.cpp)

```cpp
class Solution {
public:
    int mod = 1e9 + 7;
    int fact[100002]; // to store the factorial results, to reduce over computations

    int multiply(int a, int b){

        long long int ans = ((long long) (a%mod)*(b%mod))%mod; // only works if both a and b are smaller than mod 
        // if larger then can't use this. In that case multiply first and then take mod
        return ans;
    }

    void factorial(){
        fact[0] = 1;
        for(int i=1; i<=100001; i++){
            fact[i] = multiply(fact[i-1],i);
        }
    }
    int binaryExponentiation(int a, int b){
        if(!b){
            return 1;
        }
        int result = binaryExponentiation(a, b/2);

        if(b&1){
            int res = multiply(a, multiply(result, result));
            return res;
        }
        else{
            int res = multiply(result, result);
            return res;

        }
    }
    int moduloInverse(int a){
        int ans = binaryExponentiation(a, mod-2);
        return ans;
    }

    int count(string str){
        vector<int>freq(26,0);
        int n = str.length();

        for(int i=0; i<n; i++){
            freq[str[i]-'a']++;
        }

        int ans = fact[n];

        int res = 1;

        for(int i=0; i<26; i++){
            res = multiply(res, fact[freq[i]]);
        }

        return multiply(ans, moduloInverse(res));

    }
    int countAnagrams(string s) {
        
        factorial();

        istringstream ss(s);

        string word;
        int ans = 1;

        while(ss >> word){
            ans = multiply(ans, count(word));
        }
        return ans;

    }
};
```

---

[← Back to Hard Problems](../hard.md) · [All LeetCode Problems](../index.md)
