# DSA Interview Practice Log

A compact, cumulative log for daily LeetCode interview practice. Keep only these fields for each question: **Question, Topic, LeetCode link, Trick to solve, and 2 Similar Questions.** Similar questions are optional follow-up practice, not part of the daily 4-question quota.

## 2026-11-23

### House Robber II
- **Topic:** Dynamic Programming — circular array
- **LeetCode:** https://leetcode.com/problems/house-robber-ii/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [House Robber](https://leetcode.com/problems/house-robber/) — foundational linear DP version.
  2. [House Robber III](https://leetcode.com/problems/house-robber-iii/) — extend the adjacent-selection constraint to a tree.

### Network Delay Time
- **Topic:** Graph — shortest paths
- **LeetCode:** https://leetcode.com/problems/network-delay-time/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) — shortest path with a constraint on edges/stops.
  2. [Path with Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) — shortest-path-style minimax cost.

### Gas Station
- **Topic:** Greedy — circular traversal
- **LeetCode:** https://leetcode.com/problems/gas-station/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [Candy](https://leetcode.com/problems/candy/) — greedy constraints and local/global reasoning.
  2. [Jump Game](https://leetcode.com/problems/jump-game/) — greedy reachability.

### Kth Largest Element in an Array
- **Topic:** Heap / Priority Queue — selection
- **LeetCode:** https://leetcode.com/problems/kth-largest-element-in-an-array/
- **Trick to solve:** Maintain a min-heap of size k; its top is the kth-largest among the processed values. (User's discussed approach.)
- **Similar questions (2):**
  1. [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — bounded heap for top-k selection.
  2. [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — maintain a bounded heap by a ranking metric.

## 2026-11-24

### Edit Distance
- **Topic:** Dynamic Programming — string DP
- **LeetCode:** https://leetcode.com/problems/edit-distance/
- **Trick to solve:** Define `dp(i,j)` for converting the remaining suffixes. If characters match, advance both; otherwise take 1 + min(insert, delete, replace). Memoize states; when one suffix is exhausted, the remaining length is the answer.
- **Similar questions (2):**
  1. [Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) — related string transformation DP.
  2. [Minimum ASCII Delete Sum for Two Strings](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/) — weighted deletion variant.

### Is Graph Bipartite?
- **Topic:** Graph — graph coloring / BFS-DFS
- **LeetCode:** https://leetcode.com/problems/is-graph-bipartite/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) — apply bipartite checking to dislike constraints.
  2. [Flower Planting With No Adjacent](https://leetcode.com/problems/flower-planting-with-no-adjacent/) — graph coloring with limited colors.

### Jump Game II
- **Topic:** Greedy — reachability ranges
- **LeetCode:** https://leetcode.com/problems/jump-game-ii/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [Jump Game](https://leetcode.com/problems/jump-game/) — reachability before optimizing jump count.
  2. [Minimum Number of Taps to Open to Water a Garden](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/) — greedy range coverage.

### Trapping Rain Water
- **Topic:** Two Pointers / Monotonic reasoning — boundary heights
- **LeetCode:** https://leetcode.com/problems/trapping-rain-water/
- **Trick to solve:** To be recorded from the user's approach and coaching discussion.
- **Similar questions (2):**
  1. [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) — two-pointer boundary reasoning.
  2. [Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/) — extend water trapping to a 2D elevation map.

## 2026-11-27 — Carryover (no new assignments)

All four problems from 2026-11-24 remain pending and are carried forward; no new problems were added to respect the four-problem daily cap.

- [Edit Distance](https://leetcode.com/problems/edit-distance/) — Dynamic Programming — pending
- [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) — Graph — pending
- [Jump Game II](https://leetcode.com/problems/jump-game-ii/) — Greedy — pending
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — Two Pointers / Monotonic Structures — pending
