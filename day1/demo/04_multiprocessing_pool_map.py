"""
Demo 04: Parallel Execution with Pool and Map
==============================================

Demonstrates how to use `multiprocessing.Pool` to distribute work
across multiple worker processes using `pool.map()`.

Key concepts:
    - Pool(N)    → creates a pool of N worker processes.
    - pool.map() → splits an iterable across workers (like a parallel for-loop).
    - Results are returned in the same order as the input.
    - The Pool handles process creation, distribution, and collection.
"""

import multiprocessing
import os
import time


# ---------------------------------------------------------------------------
# Worker functions — must be at module level for macOS/Windows 'spawn' method
# ---------------------------------------------------------------------------

def is_prime(n):
    """
    Check if a number is prime (trial division).

    This is intentionally simple and CPU-bound — perfect for
    demonstrating parallel speedup.
    """
    if n < 2:
        return (n, False)
    if n == 2:
        return (n, True)
    if n % 2 == 0:
        return (n, False)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return (n, False)
    return (n, True)


def workload(n):
    """
    CPU-heavy workload: count primes up to n using trial division.
    Each call does substantial work, making parallelism worthwhile.
    """
    count = 0
    for i in range(2, n):
        if is_prime(i)[1]:
            count += 1
    return (n, count)


# ---------------------------------------------------------------------------
# Demo function: compare sequential vs pool-based parallel execution
# ---------------------------------------------------------------------------

def demo_pool_map():
    """Use Pool.map() to distribute prime counting across worker processes."""
    # Each task counts primes up to this limit — takes noticeable time per task
    tasks = [200_000] * 16  # 16 identical heavy tasks
    num_workers = multiprocessing.cpu_count()

    print(f"Task       : Count primes up to 200,000 — repeated 16 times")
    print(f"CPU cores  : {num_workers}")
    print()

    # --- Sequential execution ---
    start = time.time()
    sequential_results = [workload(n) for n in tasks]
    seq_time = time.time() - start

    print(f"Sequential : {seq_time:.3f}s")

    # --- Parallel execution using Pool.map ---
    start = time.time()
    with multiprocessing.Pool(processes=num_workers) as pool:
        parallel_results = pool.map(workload, tasks)
    par_time = time.time() - start

    print(f"Parallel   : {par_time:.3f}s  ({num_workers} workers)")

    # --- Verify correctness ---
    assert sequential_results == parallel_results, "Results mismatch!"
    print(f"Results    : each task found {sequential_results[0][1]} primes ✓")

    # --- Speedup ---
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"\nSpeedup    : {speedup:.2f}x")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_pool_map()


if __name__ == "__main__":
    main()
