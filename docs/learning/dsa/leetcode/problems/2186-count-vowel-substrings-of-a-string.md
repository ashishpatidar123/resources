# 2186. Count Vowel Substrings Of A String

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2186-count-vowel-substrings-of-a-string)

## Problem

<p>A <strong>substring</strong> is a contiguous (non-empty) sequence of characters within a string.</p>

<p>A <strong>vowel substring</strong> is a substring that <strong>only</strong> consists of vowels (<code>&#39;a&#39;</code>, <code>&#39;e&#39;</code>, <code>&#39;i&#39;</code>, <code>&#39;o&#39;</code>, and <code>&#39;u&#39;</code>) and has <strong>all five</strong> vowels present in it.</p>

<p>Given a string <code>word</code>, return <em>the number of <strong>vowel substrings</strong> in</em> <code>word</code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> word = &quot;aeiouu&quot;
<strong>Output:</strong> 2
<strong>Explanation:</strong> The vowel substrings of word are as follows (underlined):
- &quot;<strong><u>aeiou</u></strong>u&quot;
- &quot;<strong><u>aeiouu</u></strong>&quot;
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> word = &quot;unicornarihan&quot;
<strong>Output:</strong> 0
<strong>Explanation:</strong> Not all 5 vowels are present, so there are no vowel substrings.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> word = &quot;cuaieuouac&quot;
<strong>Output:</strong> 7
<strong>Explanation:</strong> The vowel substrings of word are as follows (underlined):
- &quot;c<strong><u>uaieuo</u></strong>uac&quot;
- &quot;c<strong><u>uaieuou</u></strong>ac&quot;
- &quot;c<strong><u>uaieuoua</u></strong>c&quot;
- &quot;cu<strong><u>aieuo</u></strong>uac&quot;
- &quot;cu<strong><u>aieuou</u></strong>ac&quot;
- &quot;cu<strong><u>aieuoua</u></strong>c&quot;
- &quot;cua<strong><u>ieuoua</u></strong>c&quot;
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= word.length &lt;= 100</code></li>
	<li><code>word</code> consists of lowercase English letters only.</li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/2186-count-vowel-substrings-of-a-string/solution.cpp)

```cpp
class Solution {
public:
    bool check(char c){
        if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'){
            return true;   
        }
        return false;
    }
    int solve(string word, int k){

        int n = word.size();
        unordered_map<char, int>freq;
        int l = 0;
        int ans = 0;
        int distinct = 0;

        for(int r=0; r<n; r++){

            char c = word[r];

            if(!check(c)){
                freq.clear();
                distinct = 0;
                l = r+1;
                continue;
            }

            freq[c]++;

            if(freq[c] == 1){
                distinct++;
            }

            while(distinct > k){

                freq[word[l]]--;

                if(freq[word[l]] == 0){
                    distinct--;
                }

                l++;

            }
            ans += r - l+1;

        }
        return ans;

    }
    int countVowelSubstrings(string word) {

        return solve(word, 5) - solve(word, 4);
        
        
    }
};
```

---

[← Back to Easy](easy.md) · [All problems](index.md)
