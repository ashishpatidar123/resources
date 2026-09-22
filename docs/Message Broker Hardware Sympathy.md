# Message Broker Hardware Sympathy: Sequential I/O and Zero-Copy

## 1. Introduction

If you are building a system that needs to process millions of events per second, like tracking every click on a website or every GPS ping from a fleet of delivery vehicles, a traditional database or a standard message queue will fall over. This is the same hardware-level idea we've seen before (like how LSM-trees flush data to disk to avoid random I/O), now applied to building a massive event streaming platform like Apache Kafka.

!!! note "The Basic Idea"
    Don't update individual records on disk for every message. Only ever append to the end of a file, and let the *consumer* keep track of how far it has read.

---

## 2. The Problem: Traditional Message Queues

### The Architecture

Think of traditional message brokers (like older versions of RabbitMQ or ActiveMQ) as very anxious librarians. When a publisher sends a message, the broker saves it. When a consumer reads the message, the broker updates that message's state to "read", or deletes it.

### The Flaw (Random I/O)

To track the state of every single message, for every single consumer, the broker has to constantly update rows or index entries on the disk.

### The Hardware Reality

Updating individual records scattered across a file means the disk has to keep jumping between different locations to find the right blocks. This is called **Random I/O**. Even on modern SSDs, random writes are noticeably slower than sequential writes. If you try to push 100,000 messages a second through this kind of system, the disk will thrash, latency goes through the roof, and the whole system bottlenecks.

!!! warning
    Traditional queues couple the storage of the message with the state of the consumer. This creates lock contention in memory and forces random disk access every time a message is acknowledged.

---

## 3. The Solution: The Append-Only Log

Instead of acting like a librarian crossing things off a list, Kafka acts like a receipt printer. It doesn't care if you've read the receipt; it just keeps printing new items at the bottom.

### Sequential I/O

Kafka stores messages in a flat, append-only file called a **Log**. When a new message arrives, it is simply appended to the end of the file.

### The Speed

Because the disk is only writing sequentially, without ever jumping around, even a plain spinning hard drive (HDD) can write data at over 100 MB/s. It is close to the physical speed limit of the hardware.

### The Analogy

Think of a VHS tape versus a DVD. Skipping to a random scene on a VHS tape means fast-forwarding through everything in between, which is slow. But just hitting "record" and letting the tape run is fast and efficient, because it never has to jump around.

!!! info
    Because Kafka never deletes or updates individual messages when they are read, the broker doesn't have to track "has this specific message been read" for every consumer. Instead, each *consumer* tracks its own place in the log using an integer called an **Offset**. This removes the read-write lock contention that a traditional queue has.

    Modern Kafka does still store committed offsets on the broker (so a consumer can resume after a restart), but even that is done by appending to an internal log topic (`__consumer_offsets`) rather than updating a row in place, so it doesn't bring back the random I/O problem.

---

## 4. The Secret Sauce: Zero-Copy

Writing data fast is only half the battle. When a consumer asks for data, the broker has to read it from disk and push it out over the network.

### The Standard (Slow) Way

Normally, sending a file over a network involves four steps:

1. **DMA copies** data from Disk to Kernel Space (the OS Page Cache). This step doesn't need the CPU: DMA (Direct Memory Access) lets the disk controller move data into RAM on its own.
2. **CPU copies** data from Kernel Space to User Space (your JVM/Application memory).
3. **CPU copies** data from User Space back down to Kernel Space (the Socket Buffer).
4. **DMA copies** it from the Socket Buffer to the Network Interface Card (NIC).

### The Problem

That is 4 memory copies and 4 context switches between user mode and kernel mode (the switch into the kernel for the read, back out to the application, into the kernel again for the write, and back out). Two of the four copies (steps 2 and 3) burn CPU cycles just moving bytes around for no real reason, since the application usually doesn't need to look at the bytes; it's just forwarding them. Materializing that data as a byte array in the JVM also adds pressure on the Garbage Collector.

### Zero-Copy (The Kafka Way)

Kafka uses a low-level OS system call called `sendfile()`. This tells the operating system to copy data directly from the OS Page Cache to the Network Card, skipping steps 2 and 3 entirely.

### The Result

The data never touches User Space, and it never enters the JVM. On a NIC that supports scatter-gather DMA, only the two DMA copies (disk → page cache, page cache → NIC) remain, and the CPU does almost no work at all. Kafka is essentially just a routing tube connecting the disk directly to the network cable.

!!! note
    Without scatter-gather DMA support in the NIC, `sendfile()` still needs one CPU copy inside the kernel, from the page cache into the socket buffer. Even then, it skips both trips through user space, so it still cuts the copies from 4 down to 3, and the context switches from 4 down to 2. Most modern Linux servers do have this NIC support, which is what gets you the full "2 copies, 2 context switches" zero-copy path.

---

## 5. Practical Code Example: Zero-Copy in Java

Here is how you can implement a Zero-Copy network transfer in Java using the NIO (New I/O) package. This `transferTo` method is what Kafka calls under the hood, and on Linux it maps directly to the `sendfile()` system call.

```java
import java.io.IOException;
import java.io.RandomAccessFile;
import java.net.InetSocketAddress;
import java.nio.channels.FileChannel;
import java.nio.channels.SocketChannel;

public class ZeroCopyExample {

    public void sendDataZeroCopy(String filePath, String destIp, int destPort) throws IOException {
        // try-with-resources ensures everything is closed even if transferTo() throws
        try (RandomAccessFile file = new RandomAccessFile(filePath, "r");
             FileChannel fileChannel = file.getChannel();
             SocketChannel socketChannel = SocketChannel.open()) {

            socketChannel.connect(new InetSocketAddress(destIp, destPort));

            // The Magic Call: transferTo()
            // This invokes the OS 'sendfile()' system call.
            // Data goes straight from the disk cache to the socket buffer via DMA.
            // It never enters the Java heap.
            long totalBytes = fileChannel.size();
            long position = 0;

            // transferTo() is not guaranteed to send everything in one call,
            // especially for large files, so we loop until it's all sent.
            while (position < totalBytes) {
                position += fileChannel.transferTo(position, totalBytes - position, socketChannel);
            }
        }
    }
}
```

!!! tip
    The original single-call version (`fileChannel.transferTo(0, totalBytes, socketChannel)`) works for small files, but `transferTo()` can transfer fewer bytes than requested in one call, particularly for large log segments. The loop above makes sure the whole file is actually sent.

---

## 6. Architecture Trade-offs

You can't get this kind of speed without giving something up.

### No Querying

Because data is written as a raw sequential byte stream, you lose the ability to query it. You cannot ask Kafka, "give me the event where `userId == 123`." Kafka only understands offsets. You have to say, "give me all the bytes starting at offset 4500," and do the filtering yourself on the consumer side.

### Latency vs Throughput

Kafka batches messages together before writing them to disk, which is what makes the sequential writes so efficient. This is great for throughput, but it means a single message can sit in a batch for a few milliseconds before being flushed, which is a small trade-off against the absolute lowest possible per-message latency.

---

## 7. Summary

When scaling backend systems to handle millions of events per second, traditional message queues bottleneck because they rely on random disk I/O and heavy CPU usage to track the state of every message. Kafka solves this by treating storage as a simple, append-only log, which lets it make the most of cheap sequential disk write speeds.

To serve that data back to consumers, Kafka uses the OS-level `sendfile()` system call (zero-copy), letting the hardware's DMA controller move data straight from the disk cache to the network card. This bypasses the application layer almost entirely, saving CPU cycles and memory, in exchange for giving up the ability to query the data directly.

---

## Resources for Further Deep Diving

* **Guide:** [Why is Kafka Fast? (ByteByteGo)](https://bytebytego.com/guides/why-is-kafka-fast/) - A visual walkthrough of Sequential I/O and the Zero-Copy data path, step by step.
* **Article:** [The Log: What every software engineer should know about real-time data's unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) - Written by Jay Kreps, co-creator of Kafka. The canonical piece on why append-only logs are central to distributed systems.
