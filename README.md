# OS-HW4
# Design
The main design of the code was to compare two different types of concurrent queue implementations under
different thread workloads. I used a Mutex-Lock queue and a Lock-Free queue. The Mutex is where access 
to the shared structure is being controlled using mutex locks while the Lock-Free queue using compare and swap to avoid using locks. The benchmarking I used measured the execution time of the queue under different work loads. The libraries used were threading, time, random, atomic, and queue.
# Instructions
To run the code I used PyCharm but any Python IDE can be used. You then would run the Mutex.py and record the measurements of performance afterwards and then run the Lock-Free.py and record the results of that and then compare.
# Analysis
The Mutex queue seemed to run just a little faster than the lock-free queue after running both on PyCharm
but the lock-free could handle more threads without slowing down. Makes sense why the Mutex would start to slow down since lock contention forces only one thread can be accessed at a time. This also correlates to Michael and Scott's paper saying how the mutex has more latency and is slower while lock-free is more scalable.
