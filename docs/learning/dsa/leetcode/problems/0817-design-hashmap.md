# 817. Design Hashmap

**Difficulty:** Easy  
**Source folder:** [View on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0817-design-hashmap)

## Problem

# Design HashMap

### Difficulty: Easy
### Topics: Array, Hash Table, Linked List, Design, Hash Function

<p>Design a HashMap without using any built-in hash table libraries.</p>

<p>Implement the <code>MyHashMap</code> class:</p>

<ul>
	<li><code>MyHashMap()</code> initializes the object with an empty map.</li>
	<li><code>void put(int key, int value)</code> inserts a <code>(key, value)</code> pair into the HashMap. If the <code>key</code> already exists in the map, update the corresponding <code>value</code>.</li>
	<li><code>int get(int key)</code> returns the <code>value</code> to which the specified <code>key</code> is mapped, or <code>-1</code> if this map contains no mapping for the <code>key</code>.</li>
	<li><code>void remove(key)</code> removes the <code>key</code> and its corresponding <code>value</code> if the map contains the mapping for the <code>key</code>.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input</strong>
[&quot;MyHashMap&quot;, &quot;put&quot;, &quot;put&quot;, &quot;get&quot;, &quot;get&quot;, &quot;put&quot;, &quot;get&quot;, &quot;remove&quot;, &quot;get&quot;]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
<strong>Output</strong>
[null, null, null, 1, -1, null, 1, null, -1]

<strong>Explanation</strong>
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // The map is now [[1,1]]
myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>0 &lt;= key, value &lt;= 10<sup>6</sup></code></li>
	<li>At most <code>10<sup>4</sup></code> calls will be made to <code>put</code>, <code>get</code>, and <code>remove</code>.</li>
</ul>

## My C++ Submissions

### `solution_2165103696.cpp`

[View source on GitHub](https://github.com/ashishpatidar123/Coding-Questions-Solutions/tree/main/my-solutions/Easy/0817-design-hashmap/solution_2165103696.cpp)

```cpp
class MyHashMap {
private:
    struct Node {
        int key;
        int value;
        Node* next;

        Node(int k, int v) : key(k), value(v), next(nullptr) {}
    };

    vector<Node*> buckets;
    int capacity;
    int size;

    double loadFactor = 0.75;

    int getIndex(int key) {
        return key % capacity;
    }

    void resize() {
        int oldCapacity = capacity;
        capacity *= 2;

        vector<Node*> newBuckets(capacity, nullptr);

        for (int i = 0; i < oldCapacity; i++) {
            Node* curr = buckets[i];

            while (curr != nullptr) {
                Node* next = curr->next;

                int newIndex = curr->key % capacity;

                curr->next = newBuckets[newIndex];
                newBuckets[newIndex] = curr;

                curr = next;
            }
        }

        buckets = move(newBuckets);
    }

public:
    MyHashMap() {
        capacity = 16;
        size = 0;
        buckets.resize(capacity, nullptr);
    }

    void put(int key, int value) {
        int index = getIndex(key);

        Node* curr = buckets[index];

        // Key already exists → update value
        while (curr != nullptr) {
            if (curr->key == key) {
                curr->value = value;
                return;
            }
            curr = curr->next;
        }

        // Insert new key-value pair
        Node* newNode = new Node(key, value);
        newNode->next = buckets[index];
        buckets[index] = newNode;

        size++;

        // Resize if load factor becomes too high
        if ((double)size / capacity > loadFactor) {
            resize();
        }
    }

    int get(int key) {
        int index = getIndex(key);

        Node* curr = buckets[index];

        while (curr != nullptr) {
            if (curr->key == key) {
                return curr->value;
            }

            curr = curr->next;
        }

        return -1;
    }

    void remove(int key) {
        int index = getIndex(key);

        Node* curr = buckets[index];
        Node* prev = nullptr;

        while (curr != nullptr) {

            if (curr->key == key) {

                // Removing head
                if (prev == nullptr) {
                    buckets[index] = curr->next;
                }
                // Removing middle/tail
                else {
                    prev->next = curr->next;
                }

                delete curr;
                size--;
                return;
            }

            prev = curr;
            curr = curr->next;
        }
    }

    ~MyHashMap() {
        for (int i = 0; i < capacity; i++) {
            Node* curr = buckets[i];

            while (curr != nullptr) {
                Node* next = curr->next;
                delete curr;
                curr = next;
            }
        }
    }
};
```

---

[← Back to Easy Problems](../easy.md) · [All LeetCode Problems](../index.md)
