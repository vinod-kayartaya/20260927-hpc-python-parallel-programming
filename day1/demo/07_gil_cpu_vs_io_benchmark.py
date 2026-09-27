"""
Demo 07: Global Interpreter Lock (GIL) — CPU-Bound vs I/O-Bound
=================================================================

Demonstrates the impact of Python's GIL on multithreaded performance.

Key concepts:
    - The GIL allows only ONE thread to execute Python bytecode at a time.
    - CPU-bound tasks get NO speedup from threads (they contend for the GIL).
    - I/O-bound tasks DO benefit from threads (GIL is released during I/O waits).
    - Processes bypass the GIL entirely (each has its own interpreter).

Experiment:
    We run the same workload four ways and compare execution times:
      1. Sequential           (baseline)
      2. Multithreaded        (limited by GIL for CPU tasks)
      3. Multiprocess         (true parallelism)
    … for both CPU-bound and I/O-bound workloads.
"""

import threading
import multiprocessing
import time
import os

NUM_WORKERS = 4


# ---------------------------------------------------------------------------
# Worker functions — must be at module level for macOS/Windows 'spawn' method
# ---------------------------------------------------------------------------

def cpu_task(n=5_000_000):
    """Perform a CPU-intensive calculation."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def io_task(duration=1.0):
    """Simulate an I/O operation (e.g., network request, file read)."""
    time.sleep(duration)


# ---------------------------------------------------------------------------
# Helper functions for running tasks in different modes
# ---------------------------------------------------------------------------

def run_sequential(task, num_tasks):
    """Run the task sequentially `num_tasks` times."""
    for _ in range(num_tasks):
        task()


def run_threaded(task, num_tasks):
    """Run the task using threads."""
    threads = [threading.Thread(target=task) for _ in range(num_tasks)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run_multiprocess(task, num_tasks):
    """Run the task using processes."""
    processes = [multiprocessing.Process(target=task) for _ in range(num_tasks)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


def benchmark(label, task, num_tasks):
    """Run all three modes and print timings."""
    print(f"\n{'─' * 55}")
    print(f"  {label}  ({num_tasks} tasks)")
    print(f"{'─' * 55}")

    # Sequential
    start = time.time()
    run_sequential(task, num_tasks)
    seq = time.time() - start
    print(f"  Sequential    : {seq:.3f}s")

    # Threaded
    start = time.time()
    run_threaded(task, num_tasks)
    thr = time.time() - start
    speedup_t = seq / thr if thr > 0 else 0
    print(f"  Threaded      : {thr:.3f}s  (speedup: {speedup_t:.2f}x)")

    # Multiprocess
    start = time.time()
    run_multiprocess(task, num_tasks)
    proc = time.time() - start
    speedup_p = seq / proc if proc > 0 else 0
    print(f"  Multiprocess  : {proc:.3f}s  (speedup: {speedup_p:.2f}x)")


# ---------------------------------------------------------------------------
# Demo functions
# ---------------------------------------------------------------------------

def demo_cpu_bound():
    """Benchmark CPU-bound task: threads will NOT help (GIL contention)."""
    print("GIL Benchmark: CPU-Bound")
    print(f"Workers/tasks: {NUM_WORKERS}, CPU cores: {multiprocessing.cpu_count()}")
    benchmark("CPU-BOUND (sum of squares)", cpu_task, NUM_WORKERS)

    print(f"\n{'═' * 55}")
    print("TAKEAWAY:")
    print("  • CPU-bound → use multiprocessing (threads ~= sequential)")
    print(f"{'═' * 55}")


def demo_io_bound():
    """Benchmark I/O-bound task: threads WILL help (GIL released during I/O)."""
    print("GIL Benchmark: I/O-Bound")
    print(f"Workers/tasks: {NUM_WORKERS}, CPU cores: {multiprocessing.cpu_count()}")
    benchmark("I/O-BOUND (simulated network call)", io_task, NUM_WORKERS)

    print(f"\n{'═' * 55}")
    print("TAKEAWAY:")
    print("  • I/O-bound → threads work well    (and are lighter weight)")
    print(f"{'═' * 55}")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_cpu_bound()
    # demo_io_bound()


if __name__ == "__main__":
    main()
