# 2134. Maximize The Confusion Of An Exam

**Difficulty:** Medium  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2134-maximize-the-confusion-of-an-exam)

## Problem

<p>A teacher is writing a test with <code>n</code> true/false questions, with <code>&#39;T&#39;</code> denoting true and <code>&#39;F&#39;</code> denoting false. He wants to confuse the students by <strong>maximizing</strong> the number of <strong>consecutive</strong> questions with the <strong>same</strong> answer (multiple trues or multiple falses in a row).</p>

<p>You are given a string <code>answerKey</code>, where <code>answerKey[i]</code> is the original answer to the <code>i<sup>th</sup></code> question. In addition, you are given an integer <code>k</code>, the maximum number of times you may perform the following operation:</p>

<ul>
	<li>Change the answer key for any question to <code>&#39;T&#39;</code> or <code>&#39;F&#39;</code> (i.e., set <code>answerKey[i]</code> to <code>&#39;T&#39;</code> or <code>&#39;F&#39;</code>).</li>
</ul>

<p>Return <em>the <strong>maximum</strong> number of consecutive</em> <code>&#39;T&#39;</code>s or <code>&#39;F&#39;</code>s <em>in the answer key after performing the operation at most</em> <code>k</code> <em>times</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> answerKey = &quot;TTFF&quot;, k = 2
<strong>Output:</strong> 4
<strong>Explanation:</strong> We can replace both the &#39;F&#39;s with &#39;T&#39;s to make answerKey = &quot;<u>TTTT</u>&quot;.
There are four consecutive &#39;T&#39;s.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> answerKey = &quot;TFFT&quot;, k = 1
<strong>Output:</strong> 3
<strong>Explanation:</strong> We can replace the first &#39;T&#39; with an &#39;F&#39; to make answerKey = &quot;<u>FFF</u>T&quot;.
Alternatively, we can replace the second &#39;T&#39; with an &#39;F&#39; to make answerKey = &quot;T<u>FFF</u>&quot;.
In both cases, there are three consecutive &#39;F&#39;s.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> answerKey = &quot;TTFTTFTT&quot;, k = 1
<strong>Output:</strong> 5
<strong>Explanation:</strong> We can replace the first &#39;F&#39; to make answerKey = &quot;<u>TTTTT</u>FTT&quot;
Alternatively, we can replace the second &#39;F&#39; to make answerKey = &quot;TTF<u>TTTTT</u>&quot;. 
In both cases, there are five consecutive &#39;T&#39;s.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>n == answerKey.length</code></li>
	<li><code>1 &lt;= n &lt;= 5 * 10<sup>4</sup></code></li>
	<li><code>answerKey[i]</code> is either <code>&#39;T&#39;</code> or <code>&#39;F&#39;</code></li>
	<li><code>1 &lt;= k &lt;= n</code></li>
</ul>

## My C++ Submissions

### `solution.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Medium/2134-maximize-the-confusion-of-an-exam/solution.cpp)

```cpp
class Solution {
public:
    int maxConsecutiveAnswers(string answerKey, int k) {

        int n = answerKey.size();

        int count = 0;
        int ans1 = 0;

        int l=0;
        int l2=0;
        int count2=0;
        int ans2=0;

        for(int r=0; r<n; r++){

            if(answerKey[r] == 'F'){
                count++;
            }

            while(count > k){
                if(answerKey[l] == 'F'){
                    count--;
                }

                l++;
            }

            ans1 = max(ans1, r-l+1);

            if(answerKey[r] == 'T'){
                count2++;
            }

            while(count2 > k){
                if(answerKey[l2] == 'T'){
                    count2--;
                }

                l2++;
            }

            ans2 = max(ans2, r-l2+1);



        }
        // l=0;
        // count=0;
        // int ans2 = 0;
        // for(int r=0; r<n; r++){

        //     if(answerKey[r] == 'T'){
        //         count++;
        //     }

        //     while(count > k){
        //         if(answerKey[l] == 'T'){
        //             count--;
        //         }

        //         l++;
        //     }

        //     ans2 = max(ans2, r-l+1);

        // }

        return max(ans1, ans2);
        

        
    }
};
```

---

[← Back to Medium Problems](../medium.md) · [All LeetCode Problems](../index.md)
