import threading
import time
import random


class Node:
    """A node in the queue, storing a value and a pointer to the next node."""

    def __init__(self, value=None):
        self.value = value
        self.next = None


class ConcurrentQueue:
    """A thread-safe queue using mutex locks for head and tail."""

    def __init__(self):
        dummy = Node()
        self.head = dummy
        self.tail = dummy
        self.head_lock = threading.Lock()
        self.tail_lock = threading.Lock()

    def enqueue(self, value):
        """Enqueues a new value at the end of the queue."""
        new_node = Node(value)
        with self.tail_lock:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Dequeues the front value from the queue. Returns None if empty."""
        with self.head_lock:
            old_head = self.head
            new_head = old_head.next

            if new_head is None:
                return None

            self.head = new_head
            value = new_head.value

        del old_head
        return value


def worker_enqueue(queue, num_ops):
    """Worker thread for enqueueing items."""
    for _ in range(num_ops):
        queue.enqueue(random.randint(1, 100))


def worker_dequeue(queue, num_ops):
    """Worker thread for dequeueing items."""
    for _ in range(num_ops):
        queue.dequeue()


def benchmark(num_threads, num_operations):
    """Runs the benchmark for different thread configurations."""
    queue = ConcurrentQueue()
    threads = []

    start_time = time.time()

    # Creating enqueue and dequeue threads
    for _ in range(num_threads // 2):
        t1 = threading.Thread(target=worker_enqueue, args=(queue, num_operations))
        t2 = threading.Thread(target=worker_dequeue, args=(queue, num_operations))
        threads.append(t1)
        threads.append(t2)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Threads: {num_threads}, Operations per Thread: {num_operations}, Time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    # Run benchmarks with different workloads
    print("Benchmarking Mutex-Based Queue:")
    for threads_count in [2, 4, 8, 16]:  # Avoid shadowing function parameters
        for operations_count in [1000, 5000, 10000]:  # Avoid shadowing function parameters
            benchmark(threads_count, operations_count)
