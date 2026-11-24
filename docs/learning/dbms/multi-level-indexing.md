# Multi-Level Indexing in Databases

## 1. Introduction

Multi-level indexing is a technique for finding data efficiently when a dataset is too huge to perform a search operation directly.

!!! note "The Basic Idea"
    Instead of searching a huge index from the beginning, create an index for the index—a multi-level structure.

This produces several levels of progressively smaller indexes, similar to:

`Top Level Index` → `Middle Level Index` → `Leaf Level Index` → `Actual Data`

This is the main core and idea behind **B-trees** and **B+ trees**, which are the most widely used data structures for database indexes.

---

## 2. The Problem: Finding Data on Storage

Let's assume a table containing around 1 billion records:

| user_id | name   | email |
| :------ | :----- | :---- |
| 1       | Ram    | ...   |
| 2       | Laxman | ...   |
| 3       | Sita   | ...   |
| ...     | ...    | ...   |

Now, if we execute the following query:

```sql
SELECT * FROM users WHERE user_id = 700000000;
```

The database needs to find the row where `user_id = 700000000`. Without an index, the database may need to look at every single row and check for this particular condition.

This is called a **table scan** or **sequential scan**. For a table with huge records, this will be extremely expensive.

So, we use indexes here. An index provides a shortcut:

`user_id 700000000` → `location of the row`

Instead of searching all the rows, the database searches an organized structure that points directly to the row.

---

## 3. The Library Analogy

We can understand this with the example of how we get books in a library. Imagine a library with millions of books.

### Without an Index

To find a book titled *System Design*, you have to walk through every shelf and check every book:

```text
Shelf 1
Shelf 2
Shelf 3
....
Shelf 100000
```

This is equivalent to a table scan.

### With a Catalog

If the library has a catalog:

`Letter S` → `Shelf 25`

You search the catalog instead of every book. This allows you to find the book much faster.

### Multi-Level Catalog

What if the catalog itself is huge? Then the library organizes it further:

1. `Letter S` → `Catalog Section 5`
2. `Catalog Section 5` → `Shelf 25`
3. `Shelf 25` → `Position 10`

This is **multi-level indexing**. The database equivalent of this is:

`Root Index Page` → `Internal Index Page` → `Leaf Index Page` → `Data Page` → `Row`

---

## 4. Storage Hierarchy: Where Data Sits

Let's go through how data is stored and where it can be stored. A database usually interacts with several layers:

`Application` → `Database Engine` → `Buffer Pool (RAM)` → `Operating System / File System` → `SSD / HDD`

Each layer has different speed, cost, and persistence characteristics.

### Memory and Storage Layers

From fastest (and smallest) to slowest (and largest):

1. CPU Registers
2. L1 Cache
3. L2 Cache
4. L3 Cache
5. RAM
6. SSD
7. HDD

### CPU Cache

The CPU has very small but very fast memory caches (L1, L2 and L3).

The CPU cache stores recently used instructions and data. For example, if a database repeatedly examines the same B-tree root page, then that root page may remain in the CPU cache or RAM.

You normally do not design database indexes around CPU cache, but locality still matters:

* **Sequential access** is generally efficient.
* **Repeatedly accessed pages** stay cached.
* **Random access** is generally more expensive.

### RAM

RAM is fast but volatile. It is temporary, meaning data is lost when power is removed.

A database uses RAM for:

* The buffer pool
* Cached table pages
* Cached index pages
* Active transactions
* Sort operations
* Hash tables
* Memtables (in LSM trees)
* Query execution state

A database does not usually read individual rows directly from the disk every time. It reads larger units called **pages** into RAM.

**For example:**

`Disk Page 100` → `Read` → `Buffer Pool in RAM`

If the page is already in RAM, the database will reuse it without accessing the disk again.

### Database Pages

A database typically divides its files into fixed-size pages.

Common page sizes include:

* 4KB
* 8KB
* 16KB
* 32KB

The exact size depends on the specific database system (for example, PostgreSQL uses 8KB by default and MySQL InnoDB uses 16KB). A table might be stored as:

```text
Page 0
Page 1
Page 2
...
```

Each page contains records or index entries. For example:

```text
Page 100:

  Row A
  Row B
  Row C
```

The database identifies a row using a coordinate system similar to `(page_number, slot_number)`.

**For example:** `(100, 3)` means the row is in page 100, slot 3.

Some systems call this a **Row Identifier (RID)** or a **Physical Record Pointer**.

#### Why use pages?

Reading an individual byte from storage is not usually practical, as storage devices transfer chunks of data at once. A page is the database's convenient unit for:

* Reading
* Writing
* Caching
* Locking
* Indexing

### Buffer Pool: The Database's RAM Cache

The database usually maintains a region of RAM called the buffer pool or buffer cache.

Suppose the database needs page 500.

#### Cache hit

```text
Database checks buffer cache
Page 500 is already there
Database uses it immediately
```

#### Cache miss

```text
Database checks buffer cache
Page 500 is not there
Database requests it from the disk
Storage returns page 500
Database places it in RAM
Database uses it
```

This is important because RAM access is much faster than storage access.

A query might perform:

```text
Root index page: cache hit
Internal page:   cache hit
Leaf page:       cache hit
Data page:       cache miss
```

If index pages remain cached, index lookups become much faster.

!!! tip
    The upper levels of an index (root and internal pages) are accessed by almost every query, so they almost always stay in the buffer pool. Most cache misses happen at the leaf and data pages.

### Persistent Storage

The database stores durable data on persistent storage, usually:

* SSD
* HDD
* Network attached storage
* Cloud

Unlike RAM, persistent storage retains data after a restart.

A database may use several files. Modern databases usually hide the physical device details behind the operating system and storage APIs, but the difference between SSD and HDD still affects performance.

#### HDD

An HDD contains rotating magnetic platters.

The disk has:

* Platters
* Tracks
* Sectors
* Read/Write heads

To read data the HDD may need to:

1. Move the read head to the correct track (seek).
2. Wait for the platter to rotate to the correct sector.
3. Transfer the data.

These operations are mechanical in nature, so they add to the latency of the system.

Also in HDD, sequential access is much better, because the data sits in adjacent sectors and the head does not need to move again and again.
Random access is expensive because the head repeatedly moves around to different tracks.

#### SSD

An SSD uses flash memory rather than spinning platters.

It has no moving heads and no rotating disks.

This makes random access much faster than HDD, but SSDs still have important features:

* Data is read and written in flash pages
* Data is erased in larger erase blocks
* Writes may require internal housekeeping
* Flash cells have limited write endurance
* The SSD controller performs wear leveling and garbage collection

A simplified SSD organisation looks like:

```text
Erase block:
  Flash page
  Flash page
  Flash page
```

The database normally does not manage these flash pages directly. The SSD controller translates logical addresses into physical flash locations.

#### Important Distinction

A database page and an SSD flash page are not required to be of the same size or the same thing.

```text
Database page: 16KB
SSD internal page: different size
```

### Sequential vs Random Access

Sequential access means accessing in order like 1, 2, 3... while random access means accessing completely random locations like 1, 100, 5000, 2...

Generally sequential access is efficient, especially on HDDs, while random access is expensive, particularly on HDDs.

### How a Database Locates a Page

It uses a logical page identifier:

```text
Page ID = 200
```

It maps that to a file offset:

```text
file offset = page_id x page_size
```

For example, with an 8KB page:

```text
offset of page 200 = 200 x 8192 bytes = 1,638,400 bytes
```

The OS then maps the database file offset to a logical block on the storage device. The SSD or HDD maps the logical block to its physical storage.

### How a Database Reads from Disk

Suppose the database needs page 500.

The process is:

1. Query asks for page 500.
2. Buffer pool checks whether page 500 is present in cache.
3. If yes, then use it.
4. Otherwise, request the page from the operating system (using its file offset, as shown above).
5. The OS sends a request to the storage device (it may also serve it from its own file system cache).
6. The device locates the data.
7. The data is moved to RAM.
8. The database places it in the buffer pool.
9. The query reads the page.

---

## 5. Table Storage Layouts

The way table rows are stored affects indexing.

### Heap Organised Table

A heap table stores rows wherever space is available.

```text
Page 10:
  Ram
  Laxman
Page 11:
  Sita
  Hanuman
```

The rows are not necessarily sorted by a particular column.

An index may point to the physical disk location:

`user_id` → `(page, slot)`

**For example:** `42` → `(page 11, slot 2)`

### Clustered or Index Organised Table

A clustered table stores the actual rows in index order.

For example:

```text
Page 10:
  id 1
  id 2
  id 3
Page 11:
  id 4
  id 5
```

The index's leaf pages contain the complete rows rather than pointers to separate heap pages.

---

## 6. What is an Index?

An index is an auxiliary data structure that helps locate table rows.

Suppose the table is:

```text
Page 10:
  id | name
  ---------
  1  | Ram
  2  | Laxman

Page 11:
  3  | Sita
  4  | Hanuman
```

An index on `id` could contain:

```text
id | row_location
---------
1  | (10,1)
2  | (10,2)
3  | (11,1)
4  | (11,2)
```

The index is smaller than the full table because it stores only the indexed key and a pointer or row locator.

The database searches the index first:

`Find id = 3` → `(page 11, slot 1)` → `fetch row from page 11`

### Single-Level Indexing

A simple index might be a sorted list:

```text
Index:

1 -> page 10
2 -> page 10
3 -> page 11
4 -> page 11
```

If the index is small enough to fit in memory, then binary search can find a key efficiently.

But if the index itself is huge, then searching the index itself becomes expensive. This leads to multi-level indexing.

### Multi-Level Indexing

Suppose a leaf level index contains many entries:

```text
Leaf page 1:
 1 -> data page 10
 2 -> data page 10
 3 -> data page 10
 4 -> data page 11
Leaf page 2:
 5 -> data page 11
 6 -> data page 12
 7 -> data page 12
 8 -> data page 13
....
```

Now create an index over those leaf pages:

```text
Internal index:

1 -> leaf page 1
5 -> leaf page 2
...
```

and if even this becomes large we can extend it further.

So the complete structure will look like this:

`Root page` → `Internal index pages` → `Leaf index pages` → `Table data pages`

### Why Multi-Level Indexes are Efficient

Assume 1 index page can store 100 entries.

| Levels      | Entries you can reach                 |
| :---------- | :------------------------------------ |
| One level   | `100`                                 |
| Two levels  | `100 x 100 = 10,000`                  |
| Three levels| `100 x 100 x 100 = 1,000,000`         |
| Four levels | `100 x 100 x 100 x 100 = 100,000,000` |

Each level costs us roughly one page read, so finding a key among 100 million entries needs only about 4 page reads.

!!! info
    In real databases an index page (8KB or 16KB) holds several hundred entries, not just 100. That is why even a table with billions of rows usually needs only 3 to 4 index levels.

---

## 7. Different Types of Indexes

### Clustered Index

A clustered index determines the physical or logical order of table rows.

```text
Clustered order by id:

Page 10:
  id 1
  id 2
  id 3
Page 11:
  id 4
  id 5
```

The leaf level contains the full rows.

**Advantages:**

* Efficient range scans on the clustering key
* Related rows may be stored near one another
* Fewer extra lookups for queries using the clustered key

Usually a table can have only one clustered index.

### Non-Clustered Index

A non-clustered index is a separate structure:

```text
For example:

Index:
   email -> row pointer

ap@gmail.com -> (page 20, slot 3)
```

The database first searches the index and then fetches the actual table row.

**Advantages:**

* Multiple non-clustered indexes can exist
* Useful for different query patterns

**Disadvantages:**

* An additional lookup may be required to retrieve the complete row

!!! note
    In databases that use clustered tables (like MySQL InnoDB), a non-clustered index usually stores the clustering key (primary key) instead of the `(page, slot)` location. The database then searches the clustered index again to get the row.

### Covering Indexes

Suppose the query is:

```sql
SELECT name FROM users WHERE email = 'ap@gmail.com';
```

An index containing only `email` may find the row but the database must fetch the table row to retrieve `name`.

A covering index contains all needed columns:

```text
Index:
  email -> name
```

Then the database can answer the query directly from the index:

```text
ap@gmail.com  ashish
```

No separate table lookup is necessary.

This is called an index-only scan or covering index scan.

### Composite Index

A composite index uses multiple columns.

Example:

```sql
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

The index is ordered approximately like:

```text
customer_id | order_date
------------------------
1           | 2026-01-01
1           | 2026-01-05
1           | 2026-01-06
2           | 2026-01-07
2           | 2026-01-08
```

This efficiently supports:

* `WHERE customer_id = 1`
* `WHERE customer_id = 1 AND order_date >= '2026-01-01';`

The order of columns matters. An index on `(customer_id, order_date)` is generally useful for queries with `customer_id`, but it is generally not efficient for queries that filter only on `order_date`. This is because the index is sorted by `customer_id` first (also known as the leftmost prefix rule).

### Hash Indexes

A hash index applies a hash function to a key: `hash(key)` → `bucket`.

Example: `hash('ap@gmail.com')` → `bucket 42`

The database looks directly in bucket 42.

They are good for equality queries like `WHERE email = 'ap@gmail.com'` but generally poor for range queries like `WHERE id BETWEEN 1 AND 50`.

This is because hash order does not preserve key order. They may also require bucket expansion or collision handling.

### Bitmap Indexes

A bitmap index is useful for columns with a small number of distinct values.

```text
id | dept
---------
1  | CSE
2  | EE
3  | ME
4  | EE
5  | CSE
```

The bitmap for each value might be:

```text
id positions: 1 2 3 4 5
EE:           0 1 0 1 0
CSE:          1 0 0 0 1
ME:           0 0 1 0 0
```

A query like `WHERE dept = 'EE'` uses the EE bitmap. They are more suitable when the cardinality of the column is low.

### Inverted Indexes

An inverted index maps a value to all records containing that value. Search engines use inverted indexes for text.

```text
Doc 1: ds and algo
Doc 2: algo code
Doc 3: ds and code

So an inverted index might be:

ds   -> [Doc 1, Doc 3]
algo -> [Doc 1, Doc 2]
code -> [Doc 2, Doc 3]
```

For a query like `ds and code`, it will intersect `[Doc 1, Doc 3]` and `[Doc 2, Doc 3]` and return `Doc 3`.

They are used for full-text search, token search, tags, arrays, JSON fields, Elasticsearch and OpenSearch.

### Spatial Index

Spatial indexes support locations and geometric objects. For example: find restaurants within 2 km.

Common structures include: **R-trees**, **Quadtrees**, **Geohashes**.

---

## 8. More About Pages

### Write Ahead Log (WAL)

A database usually does not rely only on writing table pages directly to storage. Instead it uses a **Write Ahead Log (WAL)**. So whenever a database updates a page, it first writes the change to the log and only then modifies the page. If a system crash happens, the database can replay the log on restart and recover to a consistent state.

### Dirty Pages

When a database modifies a page in RAM, the page becomes **dirty**, because the RAM version is different from the disk page. Eventually the database flushes this RAM page back to the disk. This is called **write-back caching**.

### Page Splits

When a page is full, a new entry may require a **split**. So the new page may not be adjacent to the current page on the disk. This is acceptable because generally indexes like B+ trees store pointers or page identifiers.

---

## 9. Things to Keep in Mind About Indexes

### Storage and Write Cost

An index is also a data structure, it is not free. The index consumes disk and RAM cache space since it stores the key and the pointer (or value).

Indexes also slow down writes, because every `INSERT`, `UPDATE` (on indexed columns) and `DELETE` has to update the indexes too.

### Index Selectivity

An index is useful when it narrows the search space. So for B-tree indexes, we should prefer columns which have mostly unique (high cardinality) values, like `user_id` or `email`. A column like `gender` has only a few distinct values, so a normal index on it will not narrow down much.
