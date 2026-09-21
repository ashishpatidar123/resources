## 1. Multi-Level Indexing in Databases

Multi-level indexing is a technique for finding data efficiently when a dataset is too huge to perform a search operation directly.

> **The Basic Idea:** Instead of searching a huge index from the beginning, create an index for the index—a multi-level structure.

This produces several levels of progressively smaller indexes, similar to:

`Top Level Index` → `Middle Level Index` → `Leaf Level Index` → `Actual Data`

This is the main core and idea behind **B-trees** and **B+ trees**, which are the most important data structures used for database indexes.

---

## 2. The Problem: Finding Data on Storage

Let's assume a table containing around 1 billion records:

| user_id | name | email |
| :--- | :--- | :--- |
| 1 | Ram | ... |
| 2 | Laxman | ... |
| 3 | Sita | ... |
| ... | ... | ... |

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
`Letter D` → `Shelf 25`

You search the catalog instead of every book. This allows you to find the book much faster.

### Multi-Level Catalog

What if the catalog itself is huge? Then the library organizes it further:

1. `Letter D` → `Catalog Section 5`
2. `Catalog Section 5` → `Shelf 25`
3. `Shelf 25` → `Position 10`

This is **multi-level indexing**. The database equivalent of this is:
`Root Index Page` → `Internal Index Page` → `Leaf Index Page` → `Data Page` → `Row`

---

## 4. Storage Hierarchy: Where Data Sits

Let's go through how data is stored and where it can be stored. A database usually interacts with several layers:

`Application` → `Database Engine` → `OS` → `RAM/Buffer Cache` → `SSD/HDD` → `Physical Storage Media`

Each layer has different speed, cost, and persistence characteristics.

### CPU Cache

The CPU has very small but very fast memory caches:

1. CPU Registers
2. L1 Cache
3. L2 Cache
4. L3 Cache
5. RAM
6. SSD
7. HDD

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

The exact size depends on the specific database system. A table might be stored as:
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

### Buffer pool: the database's RAM cache

The database usually maintains a region of RAM called the buffer pool or buffer cache.

Suppose the database needs page 500.

#### Cache hit
```text
Database checks buffer cache
Page 500  is already there
Database uses it immediately
```
#### Cache miss
```text
Database checks buffer cache
Page 500  is not there
Database requests it from the disk
Storage returns page 500
Databases places it in RAM
Databases uses it
```
This is important because RAM access is much faster than storage access.

A query might perform:
```text
Root index page: cache hit
Internal page:   cache hit
Leaf page:       cache miss
Data page:       cache miss
```

If index pages remain cached, index lookups become much faster.
### Persistent storage
The database stores durable data on persistent storage usually:

* SSD
* HDD
* Network attached storage
* Cloud

Unlike RAM, persistent storage retains data after a restart.

A database may use several files. Modern database usually hides the physical device details behind the operating 
system and storage APIs, but the difference between SSD and HDD still affects performance.

#### HDD
An HDD contains rotating magnetic platters.
The disk has:

 * Platters
 * Tracks
 * Sectors
 * Read/Write heads

To read data the HDD may need to:

 1. Move the read head to the correct track.
 2. Wait for the platter to rotate to the correct sector.
 3. Transfer the data.

So these operations are mechanical in nature, thus contribute to the latency of the system.

Also in HDD sequential access is much better, because the heads are moves in one direction.
Random access is expensive because the head repeatedly moves around.

#### SSD
A SSD uses flash memory rather than spinning platters.

It has not moving heads and no rotating disks.

This makes random access much faster than HDD, but SSD still have important features:

 * Data is stored in pages
 * Data is erased in larger erase blocks
 * Writes may require internal housekeeping
 * Flash cells have limited write endurance
 * The SSD controller performs wear leveling and garbage collections.

A simplified SSD organisation looks like:
```text
Erase block:
  Flash page
  Flash page
  Flash page
```

The database normally does not manage these flash pages directly. The SSD controller translates logical addresses
into physical flash locations.

#### Important Distinction
A database page and a SSD flash page are not required to be of the same size or the same thing.
```Database page: 16KB``` and ``` SSD internal page: different size```.

### How a database reads from disk
Suppose the db needs the page 500.

The process is:

 1. Query asks for page 500
 2. Buffer pool checks whether the page 500 is present in cache
 3. If yes, then use it
 4. Otw, request logical block 500 from the operating system
 5. The OS sends a request to the storage device
 6. The device locates the data
 7. The data is moved to RAM
 8. The db places it in the buffer pool
 9. The query reads the page

## 5. Table storage layouts

The way table rows are stored affects indexing.

### Heap Organised table
A heap table stores rows wherever space is available.
```text
Page 10:
  Ram
  Laxman
Page 11:
  Seeta
  Hanuman
```
The rows are not necessarily sorted by a particular column.

An index may point to the physical disk location: ```user_id --> (page, slot)``` example ``` 42 --> (page 11, slot 2)```

### Clustered or index organised table
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
The index's leaf pages may contains the complete rows rather than pointers to seperate heap pages.

## 6. What is an INDEX ? 
An index is an auxillary data structure that helps locate table rows.

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

An index on id could contain:
```text
  id | row_location
  ---------
  1  | (10,1)
  2  | (10,2)
  3  | (11,1)
  4  | (11,2)
```

The index is smaller than the full table because it stores only the indexed key and a pointer or row locator.

The database searches the index first : ``` Find id = 3 ---> (row page 11, slot 1) ---> fetch row from page 11```

### Single-level indexing
A simple index might be a sorted list:

```text
Index:

1 -> page 10
2 -> page 10
3 -> page 11
4 -> page 11
```

If the index is small enough to fit in memory, then binary search can find a key efficiently.

But if the index itself is huge. Then searching the index itself becomes expensive. This leads to multi level indexing.

### Multi-level indexing

Suppose a leaf level index contains many entries:
```text
Leaf page 1:
 1 -> data page 10
 2 -> data page 10
 3 -> data page 10
 4 -> data page 11
Leaf page 2
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

So complete structure will look like this : 
```Root page ---> internal index pages ----> leaf index pages ----> table data pages```

Now understand why multi-level indexes are efficient. 

Assume 1 index page can store 100 entries. 

 * With one level : ``` 100 entries ```
 * With two level : ``` 100 x 100 = 10000 entries ```
 * With three level : ``` 100 x 100 x 100 = 1000000 entries ```
 * With four level : ``` 100 x 100 x 100 x 100 = 100000000 entries ```

