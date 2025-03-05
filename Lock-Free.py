import threading
import time
import random

class Node:
    """A node for the lock-free queue, storing a value and a pointer to the next node."""
    def __init__(self, value=None):
        self.value = value
        self.next = None

class LockFreeQueue:
    """A lock-free queue using atomic compare-and-swap (CAS) operations."""
    def __init__(self):
        dummy = Node()
        self.head = dummy
        self.tail = dummy
        self.lock = threading.Lock()  # Needed for atomic CAS simulation

    def compare_and_swap(self, obj, attr, expected, new_value):
        """Atomic compare-and-swap (CAS) using Python's threading lock to simulate atomicity."""
        with self.lock:
            if getattr(obj, attr) is expected:
                setattr(obj, attr, new_value)
                return True
            return False

    def enqueue(self, value):
        """Lock-free enqueue operation."""
        new_node = Node(value)
        while True:
            tail = self.tail  # Snapshot of tail
            next_node = tail.next  # Check the next node

            if tail == self.tail:  # Ensure tail is still valid
                if next_node is None:  # Queue is in a stable state
                    if self.compare_and_swap(tail, 'next', None, new_node):
                        self.compare_and_swap(self, 'tail', tail, new_node)  # Move tail forward
                        return
                else:  # Tail is lagging, move it forward
                    self.compare_and_swap(self, 'tail', tail, next_node)

    def dequeue(self):
        """Lock-free dequeue operation."""
        while True:
            head = self.head  # Snapshot of head
            first_node = head.next  # First real node in the queue

            if head == self.head:  # Ensure head is still valid
                if first_node is None:
                    return None  # Queue is empty

                value = first_node.value
                if self.compare_and_swap(self, 'head', head, first_node):
                    return value

def worker_enqueue(queue, num_ops):
    """Worker thread for enqueueing items."""
    for _ in range(num_ops):
        queue.enqueue(random.randint(1, 100))

def worker_dequeue(queue, num_ops):
    """Worker thread for dequeueing items."""
    for _ in range(num_ops):
        queue.dequeue()

def benchmark(queue_class, num_threads, num_operations):
    """Runs the benchmark for different thread configurations."""
    queue = queue_class()
    threads = []

    queue_name = getattr(queue_class, '__name__', str(queue_class))  # Fix for PyCharm warning

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
    print(f"{queue_name} - Threads: {num_threads}, Operations per Thread: {num_operations}, Time: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    # Run benchmarks for lock-free queue
    print("Benchmarking Lock-Free Queue:")

    for threads_count in [2, 4, 8, 16]:
        for operations_count in [1000, 5000, 10000]:
            benchmark(LockFreeQueue, threads_count, operations_count)
