"""
Demo 05: Basics of Multithreading and Thread Pools
====================================================

Demonstrates how to create and manage threads using the `threading` module
and how to build a simple worker pool pattern.

Key concepts:
    - threading.Thread(target=..., args=...) creates a thread.
    - All threads share the same process memory space and PID.
    - Each thread has a unique thread identifier (threading.get_ident()).
    - A worker pool processes a queue of tasks using a fixed number of threads.
"""

import threading
import queue
import os
import time


# ---------------------------------------------------------------------------
# 1. Creating and running basic threads
# ---------------------------------------------------------------------------

def greet(name, delay):
    """A simple function that each thread will execute."""
    tid = threading.get_ident()
    pid = os.getpid()
    print(f"  [Thread {tid}, PID {pid}] Hello from {name}! (sleeping {delay}s)")
    time.sleep(delay)
    print(f"  [Thread {tid}, PID {pid}] {name} done.")


def demo_basic_threads():
    """Create three threads and observe same PID, different thread IDs."""
    print("=" * 60)
    print("Part 1: Basic threads — same PID, different thread IDs")
    print("=" * 60)
    print(f"Main thread: PID={os.getpid()}, TID={threading.get_ident()}")
    print()

    threads = []
    for i, name in enumerate(["Alpha", "Beta", "Gamma"]):
        t = threading.Thread(target=greet, args=(name, 1.0))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\nAll basic threads completed.")


# ---------------------------------------------------------------------------
# 2. Communicating between threads using shared data
# ---------------------------------------------------------------------------

def demo_shared_memory():
    """Show that threads share the same memory (shared list)."""
    print("=" * 60)
    print("Part 2: Threads share the same memory (shared list)")
    print("=" * 60)

    shared_results = []  # all threads can access this list

    def compute_square(n):
        """Compute square and append to shared list."""
        result = n * n
        shared_results.append((n, result))
        print(f"  Thread computed: {n}² = {result}")

    threads = []
    for num in [2, 4, 6, 8, 10]:
        t = threading.Thread(target=compute_square, args=(num,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nShared results (from main thread): {shared_results}")


# ---------------------------------------------------------------------------
# 3. Creating a worker pool pattern
# ---------------------------------------------------------------------------

def demo_worker_pool():
    """Build a worker pool of 3 threads processing tasks from a queue."""
    print("=" * 60)
    print("Part 3: Worker pool pattern with 3 threads")
    print("=" * 60)

    # A thread-safe queue holds tasks to be processed
    task_queue = queue.Queue()

    def worker(worker_id):
        """
        Worker thread: pulls tasks from the queue until it receives None
        (the sentinel value indicating shutdown).
        """
        while True:
            task = task_queue.get()         # blocks until a task is available
            if task is None:                # sentinel → shut down
                print(f"  Worker-{worker_id}: shutting down")
                break
            print(f"  Worker-{worker_id}: processing task '{task}'")
            time.sleep(0.5)                 # simulate work
            task_queue.task_done()

    # Create 3 worker threads
    NUM_WORKERS = 3
    pool = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        pool.append(t)

    # Submit 8 tasks to the queue
    tasks = [f"task-{j}" for j in range(8)]
    for task in tasks:
        task_queue.put(task)

    # Wait for all tasks to be processed
    task_queue.join()

    # Send shutdown signal (one None per worker)
    for _ in range(NUM_WORKERS):
        task_queue.put(None)

    # Wait for worker threads to exit
    for t in pool:
        t.join()

    print("\nAll worker pool tasks completed.")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_basic_threads()
    # demo_shared_memory()
    # demo_worker_pool()


if __name__ == "__main__":
    main()
