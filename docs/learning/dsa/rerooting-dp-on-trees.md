# Rerooting DP on Trees: Compute Answers for Every Root in Linear Time

**Domain:** Data Structures & Algorithms  
**Level:** Intermediate → Advanced  
**Prerequisites:** DFS/BFS, rooted trees, subtree sizes, bottom-up tree DP, prefix/suffix aggregates  
**Estimated study time:** 60–90 minutes

## Learning objectives

By the end, you should be able to:

- Recognize problems that ask for a tree-DP answer at every vertex, not just one fixed root.
- Derive the effect of moving a root across one edge.
- Implement the two-pass rerooting pattern iteratively in C++.
- Use prefix/suffix aggregates to exclude one child without division.
- Explain when rerooting is linear and when the state-combination cost makes it more expensive.

---

## 1. The problem pattern

A normal tree-DP solution temporarily chooses a root and computes information from leaves toward that root. This works when the question asks for one answer, such as:

- the size or sum of a subtree;
- the maximum independent set of the tree;
- the longest path passing through a vertex;
- a value associated with one chosen root.

Rerooting DP is useful when the question changes to:

> For every vertex u, what would the answer be if u were the root?

A brute-force approach is to run the ordinary tree DP once for each possible root. If one run costs O(N), doing it for all N roots costs O(N²). That is too slow for a tree with N = 2 × 10^5.

The key observation is that two neighboring roots describe almost the same tree. When the root moves across one edge, the tree splits into two components. We can reuse the information already computed for those components instead of recomputing the entire tree.

A tree has N - 1 edges, so a constant amount of work per edge gives an O(N) algorithm.

## 2. Start with the easiest rerooting transition: sum of distances

Consider this problem:

> For every vertex u, calculate the sum of its distances to all other vertices.

Running BFS from every vertex takes O(N²) on a tree. Instead, derive how the answer changes when moving from a parent p to its child c.

### 2.1 Fix one temporary root

Choose any root, say vertex 0. This root is only a bookkeeping device; it is not necessarily the final answer.

Compute:

- parent[u]: parent of u in this temporary rooting;
- depth[u]: distance from the temporary root;
- size[u]: number of vertices in u's subtree;
- ans[u]: sum of distances from u to all vertices.

The first answer is easy:

    ans[root] = sum(depth[u])

Then compute subtree sizes in post-order:

    size[u] = 1 + sum(size[child])

A reverse traversal order is enough: if parents are visited before children, reversing that order ensures children are processed before their parents.

### 2.2 Derive the transition instead of memorizing it

Suppose c is a child of p. Remove edge (p, c).

The tree is now split into:

- the component on c's side, containing size[c] vertices;
- the component on p's side, containing N - size[c] vertices.

Move the reference point from p to c:

- Every vertex in c's component becomes **one edge closer**.
- Every vertex in the other component becomes **one edge farther**.

Therefore:

    ans[c] = ans[p] - size[c] + (N - size[c])

So:

    ans[c] = ans[p] + N - 2 * size[c]

That is the entire transition. Once ans[p] and size[c] are known, the answer for c is available in constant time.

For an edge of weight w, every distance in the two components changes by w rather than 1:

    ans[c] = ans[p] + w * (N - 2 * size[c])

Use long long for distance sums. If input bounds can make the product exceed 64-bit range, use __int128 for intermediate arithmetic.

### 2.3 Worked example

Take this tree:

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

Root it at 1.

| Vertex | Subtree size | Sum of distances |
|---|---:|---:|
| 1 | 6 | 8 |
| 2 | 3 | 8 |
| 3 | 2 | 10 |
| 4 | 1 | 12 |
| 5 | 1 | 12 |
| 6 | 1 | 14 |

From vertex 1, the distances are 0, 1, 1, 2, 2, 2, so ans[1] = 8.

For vertex 2, its subtree has three vertices:

    ans[2] = 8 + 6 - 2 × 3 = 8

For vertex 3, its subtree has two vertices:

    ans[3] = 8 + 6 - 2 × 2 = 10

The same transition gives the remaining answers. We have replaced six traversals with two linear passes.

### 2.4 What this example teaches—and what it does not

The formula ans[child] = ans[parent] + N - 2 × size[child] is specific to the sum-of-distances problem. Do not copy it into an unrelated tree-DP problem.

The reusable idea is broader:

1. Compute the contribution from a node's own subtree.
2. Compute the contribution coming from outside that subtree.
3. Move the outside contribution from a parent to a child.
4. Reuse sibling information instead of recomputing it.

That leads to general rerooting DP.

---

## 3. General rerooting: inside and outside information

For a fixed root, ordinary tree DP naturally flows upward:

- children send information to their parent;
- the parent combines the children's contributions;
- the root produces the final answer.

For all-root answers, we also need information to flow downward. A child must learn what the rest of the tree contributes when viewed from that child.

A useful mental model is to cut an edge (u, v). The cut creates two components. Define a **directed message** for each direction:

- message[u -> v]: the information contributed by the component on u's side, as seen by v;
- message[v -> u]: the information contributed by the other component, as seen by u.

The two directions are not interchangeable. Their meanings depend on which side of the cut they summarize.

At a vertex u, combine the messages from all its neighbors to obtain the answer for u. To send a message from u to one neighbor v, combine every incoming contribution at u **except** the one from v, then transform that aggregate across edge (u, v).

This is the general pattern:

```text
                parent side
                    |
                    v
child side ---> [ vertex u ] <--- sibling side
                    |
                    v
               another child

First pass: children -> parent
Second pass: parent/siblings -> child
```

### 3.1 The three operations to define

Before writing code, explicitly define:

1. **State:** What exactly does one message represent?
2. **Merge:** How are independent neighbor contributions combined?
3. **Transfer:** How does the merged state change when it crosses an edge or includes the current vertex?

If the merge operation is associative, prefix/suffix aggregates can efficiently exclude one neighbor. If the merge is not associative, the order and grouping of contributions need more careful handling.

## 4. Why prefix and suffix aggregates matter

Suppose a vertex has children c[0 ... k-1]. Let each child's contribution be factor[i].

For child i, we need the aggregate of every sibling except child i.

If we recompute the aggregate for every child by scanning all siblings, a star-shaped tree can take O(N²) time: the center has N - 1 children.

If the merge is multiplication, define:

- prefix[i]: product of factors before i;
- suffix[i]: product of factors from i onward.

Then:

    product of all factors except i = prefix[i] * suffix[i + 1]

Both arrays are built in O(k), and each exclusion query takes O(1). Across the entire tree, the sum of all child counts is N - 1, so the total work remains O(N).

For a generic associative operation, replace multiplication with that operation and use its identity element. Examples:

| Aggregate | Identity | Excluding one child |
|---|---|---|
| Sum | 0 | prefix sum + suffix sum |
| Product | 1 | prefix product × suffix product |
| Minimum | +infinity | prefix minimum combined with suffix minimum |
| Maximum | -infinity | prefix maximum combined with suffix maximum |

For maximum-based transitions, keeping the largest two contributions is another common way to exclude one child in constant time.

**Do not use division as a shortcut unless the algebra and modulus guarantee it is safe.** A modular value may have no multiplicative inverse. Prefix/suffix products work even when the modulus is composite or a factor is zero modulo the modulus.

---

## 5. A full example: count connected black subsets containing each vertex

This is the core idea behind AtCoder Educational DP Contest, problem V — Subtree.

Given a tree, color each vertex either black or white. Count, for every vertex u, the number of colorings such that:

- u is black;
- all black vertices form one connected set.

Return each answer modulo M.

### 5.1 Define the state precisely

Temporarily root the tree at 0.

Let:

- down[u] = number of valid choices inside u's rooted subtree, assuming u is black and all selected black vertices in that subtree connect to u;
- outside[u] = number of compatible choices outside u's subtree, given that u is black.

The root has no outside component, so:

    outside[root] = 1

For a child c of u, the final answer is:

    answer[u] = down[u] * outside[u] mod M

The two regions are disjoint. Once u is black, a valid choice in the subtree and a valid choice outside the subtree can be combined independently.

### 5.2 Bottom-up transition

Consider a child c of u.

There are two possibilities for the branch rooted at c:

1. Make every vertex in that branch white. There is exactly one such choice.
2. Choose a connected black set containing c. There are down[c] choices.

Because u is black, any black vertices selected in a child branch must connect through that child. Different child branches are independent.

Therefore:

    down[u] = product over children c of (1 + down[c]) mod M

A leaf has no children, so its empty product is 1.

### 5.3 Top-down transition

Now calculate outside[c] for a child c of u.

There are two cases:

**Case A — u is white.**  
Since c is black and all black vertices must form one connected component, every vertex outside c's subtree must be white. There is exactly one choice.

**Case B — u is black.**  
The parent-side region contributes outside[u] choices. Every sibling branch s of c contributes either all white or a connected black set containing s, giving 1 + down[s] choices.

Thus:

    outside[c] = 1 + outside[u] * product over siblings s != c of (1 + down[s])

Take the result modulo M.

The sibling product is exactly the exclusion query from the previous section. Build prefix and suffix products over the children of u to calculate all child transitions in linear time.

### 5.4 Sanity check on a path

For path 1 — 2 — 3, root at 1:

- down[3] = 1
- down[2] = 1 + down[3] = 2
- down[1] = 1 + down[2] = 3

Outside values:

- outside[1] = 1
- outside[2] = 1 + outside[1] = 2
- outside[3] = 1 + outside[2] = 3

Therefore:

- answer[1] = 3 × 1 = 3
- answer[2] = 2 × 2 = 4
- answer[3] = 1 × 3 = 3

The result is 3, 4, 3, matching the sample.

For a star with one center and three leaves, the center's answer is 2 × 2 × 2 = 8. Each leaf's answer is 1 + 2 × 2 = 5.

---

## 6. C++17 implementation: iterative two-pass rerooting

This implementation solves the connected-black-subsets problem above. It uses an iterative traversal so a path-shaped tree with N vertices cannot overflow the call stack.

Input:

- N M
- N - 1 undirected edges, using 1-based vertex labels

Output: one answer per vertex, in input label order.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long mod;
    cin >> n >> mod;

    vector<vector<int>> graph(n);
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        --u;
        --v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    // Build a parent-before-child traversal order.
    vector<int> parent(n, -1);
    vector<int> order;
    order.reserve(n);
    order.push_back(0);

    for (int i = 0; i < (int)order.size(); ++i) {
        int u = order[i];

        for (int v : graph[u]) {
            if (v == parent[u]) continue;

            parent[v] = u;
            order.push_back(v);
        }
    }

    vector<long long> down(n, 1);
    vector<long long> outside(n, 1);
    vector<long long> answer(n, 0);

    // Pass 1: children -> parent.
    // Reverse order guarantees every child's down[] is ready.
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];

        for (int v : graph[u]) {
            if (parent[v] == u) {
                down[u] = down[u] * (1 + down[v]) % mod;
            }
        }
    }

    // The root has an empty outside component.
    outside[0] = 1 % mod;

    // Pass 2: parent -> children.
    // A parent's outside[] is ready before processing its children.
    for (int u : order) {
        vector<int> children;

        for (int v : graph[u]) {
            if (parent[v] == u) {
                children.push_back(v);
            }
        }

        int k = (int)children.size();

        vector<long long> prefix(k + 1, 1 % mod);
        vector<long long> suffix(k + 1, 1 % mod);

        for (int i = 0; i < k; ++i) {
            long long factor = (1 + down[children[i]]) % mod;
            prefix[i + 1] = prefix[i] * factor % mod;
        }

        for (int i = k - 1; i >= 0; --i) {
            long long factor = (1 + down[children[i]]) % mod;
            suffix[i] = factor * suffix[i + 1] % mod;
        }

        answer[u] = down[u] * outside[u] % mod;

        for (int i = 0; i < k; ++i) {
            int v = children[i];

            // Product of all sibling factors, excluding child i.
            long long siblings = prefix[i] * suffix[i + 1] % mod;

            outside[v] = (1 + outside[u] * siblings) % mod;
        }
    }

    for (int u = 0; u < n; ++u) {
        cout << answer[u] << '\n';
    }

    return 0;
}
```

### Complexity

- Building the parent/order arrays: O(N).
- Bottom-up pass: each edge is inspected a constant number of times, O(N).
- Top-down pass: each child contributes to one prefix and one suffix computation, O(N) total.
- Auxiliary memory: O(N) for the graph, traversal arrays, and DP states. The temporary prefix/suffix arrays use O(degree(u)) memory for the current vertex.

Overall: **O(N) time and O(N) space.**

### Implementation details worth noticing

- The first pass uses reverse order; the second uses forward order.
- outside[u] is an outside-region factor, not the same thing as down[u]. Naming and documenting state semantics prevents many rerooting bugs.
- No modular division is used. This matters because M is not guaranteed to be prime.
- The implementation assumes the input is a valid connected tree with N - 1 edges.
- For N = 1, the answer is 1: the only valid coloring with the single vertex black is the one containing that vertex.

---

## 7. How to recognize and design rerooting problems

Look for statements containing phrases such as:

- “For every vertex, find…”
- “If the tree were rooted at vertex u…”
- “For each node, calculate its contribution to all other nodes…”
- “What is the best value if we choose this vertex as the root?”
- “For each vertex, count connected configurations containing it…”

Then ask:

1. Can I solve the problem for one fixed root using tree DP?
2. What information does a child need from the part of the tree outside its subtree?
3. If I cross one edge, which component changes and which remains reusable?
4. Can I combine all sibling contributions efficiently?
5. Is the merge associative? Can prefix/suffix or top-two values exclude one child?
6. Is each message and transfer operation constant time?

If the answers support constant-time work per directed edge, an O(N) rerooting solution is likely.

## 8. Common mistakes and trade-offs

### Confusing the two directions

A child-to-parent message and a parent-to-child message often have different meanings. Write the exact state definition before deriving either transition.

### Recomputing sibling contributions

A nested loop over every child and every sibling can degrade to O(N²) on a star. Use prefix/suffix aggregates, or maintain the best two values for max-based transitions.

### Dividing modulo M

Computing total / factor modulo M is not generally valid. Modular division requires an inverse, which may not exist. Prefix/suffix avoids the issue.

### Using the wrong traversal order

Bottom-up states require children to be processed first. Outside states require the parent to be processed first. A single parent-before-child order and its reverse are usually enough.

### Recursive DFS on a deep tree

A path can have depth N - 1. In C++, recursion may overflow the process stack. Use an iterative parent/order traversal when constraints are large.

### Assuming every tree DP can be rerooted in O(N)

The two-pass structure is reusable, but the state merge may not be cheap. If merging child states costs O(k), the total may be larger than linear. Analyze the sum of merge costs, not just the number of DFS visits.

### Overgeneralizing a special transition

The distance-sum formula is not a universal rerooting formula. Each problem needs its own state, merge, and transfer derivation.

---

## 9. Engineering applications

- **Tree-shaped network placement:** Find the node minimizing total weighted distance to all machines or sites. The weighted distance-sum transition gives every candidate in linear time.
- **Hierarchy analysis:** Calculate a score for every possible root of an organizational or dependency tree without rebuilding the hierarchy each time.
- **Connected cluster counting:** Count connected selections containing each node, as in the AtCoder Subtree problem.
- **Tree-based optimization:** Compute eccentricities, best paths through each vertex, or the effect of excluding one neighboring branch.

The algorithm is especially valuable when the input is genuinely a tree. For general graphs with cycles, cutting one edge does not split the graph into two independent components, so the same reasoning does not apply directly.

## 10. Interview questions

1. **Why does running DFS from every vertex cost O(N²) on a tree?**  
   One traversal costs O(N) and there are N possible roots.

2. **Derive the distance-sum transition when moving from parent p to child c.**  
   size[c] vertices become one unit closer and N - size[c] become one unit farther, giving ans[c] = ans[p] + N - 2 × size[c].

3. **How does the transition change for a weighted edge?**  
   Multiply the net change by the edge weight: w × (N - 2 × size[c]).

4. **Why are prefix/suffix arrays useful in general rerooting?**  
   They combine all neighbor contributions except one in constant time after linear preprocessing.

5. **Why is modular division unsafe in the AtCoder Subtree problem?**  
   The modulus need not be prime, and a factor may not have a multiplicative inverse.

6. **What is the difference between down[u] and outside[u] in the implementation?**  
   down[u] summarizes valid configurations inside the rooted subtree; outside[u] summarizes compatible choices in the complement.

7. **When might rerooting fail to be linear?**  
   When the state merge or transfer is expensive, or when excluding one neighbor cannot be done efficiently.

## 11. Practice exercise

Implement rerooting for **Tree Distances II**:

> Given a tree, output the sum of distances from every vertex to all other vertices.

Constraints reach N = 2 × 10^5.

Try it in this order:

1. Write the brute-force solution using BFS from every vertex for small trees.
2. Build parent, depth, and order from root 0.
3. Compute ans[0] from the depths.
4. Compute subtree sizes in reverse order.
5. Propagate ans[child] = ans[parent] + N - 2 × size[child].
6. Compare the optimized result with brute force on randomly generated small trees.

**Extension:** Add positive edge weights and derive the weighted transition. Then solve for the vertex with minimum total weighted distance.

For a more challenging follow-up, solve AtCoder DP Contest V — Subtree using the connected-black-subsets recurrence from this lesson.

## 12. Key takeaways

- Rerooting DP computes a related answer for every possible root by reusing information across edges.
- The common structure is a bottom-up pass for subtree information and a top-down pass for outside information.
- The simple distance-sum transition is one special case; general rerooting needs explicit message semantics and transfer rules.
- Prefix/suffix aggregates make “all contributions except this child” efficient and avoid unsafe modular division.
- Iterative traversal is safer for deep trees.
- Always prove the state and transition before coding; the template does not replace problem-specific reasoning.

## References and further learning

1. [Rerooting DP in C++ — cppAcademy](https://cpp-academy.com/lessons/rerooting-dp) — A guided tutorial with the distance-sum derivation, C++ implementation, and common pitfalls.
2. [Tree Rerooting DP — Codeforces tutorial post](https://codeforces.com/blog/entry/96651) — A competitive-programming discussion focused on recognizing rerooting problems and implementing the technique.
3. [Tree Rerooting DP — video by codemastercpp](https://www.youtube.com/watch?v=7_huTWwl5jM) — Video linked from the Codeforces tutorial; useful for seeing the pattern explained visually.
4. [CSES: Tree Distances II](https://cses.fi/problemset/task/1133/) — A practical problem for the distance-sum transition.
5. [AtCoder Educational DP Contest V — Subtree](https://atcoder.jp/contests/dp/tasks/dp_v) — A more advanced problem that requires the general rerooting and sibling-exclusion technique.
