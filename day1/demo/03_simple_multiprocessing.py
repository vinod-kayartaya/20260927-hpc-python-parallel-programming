"""
Demo 03: Running Simple Processes
==================================

Demonstrates how to create and run independent worker processes using
the `multiprocessing.Process` class.

Key concepts:
    - Each process gets its own Python interpreter and memory space.
    - Processes run truly in parallel on multi-core CPUs.
    - `os.getpid()` shows each process has a unique process ID (PID).
    - `process.start()` launches the process.
    - `process.join()` waits for it to finish.
"""

import multiprocessing
import os
import time


# ---------------------------------------------------------------------------
# Worker functions — must be at module level for macOS/Windows 'spawn' method
# ---------------------------------------------------------------------------

def compute_squares(numbers):
    """Compute squares of a list of numbers."""
    pid = os.getpid()
    print(f"  [PID {pid}] compute_squares started")
    results = []
    for n in numbers:
        results.append(n * n)
        time.sleep(0.3)  # simulate some work
    print(f"  [PID {pid}] compute_squares finished → {results}")


def compute_cubes(numbers):
    """Compute cubes of a list of numbers."""
    pid = os.getpid()
    print(f"  [PID {pid}] compute_cubes started")
    results = []
    for n in numbers:
        results.append(n * n * n)
        time.sleep(0.3)  # simulate some work
    print(f"  [PID {pid}] compute_cubes finished → {results}")


# ---------------------------------------------------------------------------
# Demo function: spawn two processes
# ---------------------------------------------------------------------------

def demo_spawn_two_processes():
    """Spawn two processes that compute squares and cubes concurrently."""
    numbers = [1, 2, 3, 4, 5]

    print(f"Main process PID: {os.getpid()}")
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
    print()

    # Create two process objects
    p1 = multiprocessing.Process(target=compute_squares, args=(numbers,))
    p2 = multiprocessing.Process(target=compute_cubes,   args=(numbers,))

    # Start both processes (they run concurrently)
    start_time = time.time()
    print("Starting both processes...")
    p1.start()
    p2.start()

    # Wait for both to finish
    p1.join()
    p2.join()
    elapsed = time.time() - start_time

    print()
    print(f"Both processes completed in {elapsed:.2f} seconds")
    print(f"(Sequential would take ~{0.3 * len(numbers) * 2:.2f}s, "
          f"parallel takes ~{0.3 * len(numbers):.2f}s)")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_spawn_two_processes()


if __name__ == "__main__":
    main()
