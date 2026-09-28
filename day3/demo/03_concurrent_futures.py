"""
Demo 03: High-Level Parallelism with `concurrent.futures`
=========================================================

Demonstrates high-level thread and process pools via `concurrent.futures`:
    - ThreadPoolExecutor for I/O tasks
    - ProcessPoolExecutor for CPU-bound tasks
    - Managing Future objects with `as_completed()`, timeouts, and callbacks

Uncomment one function at a time in main() to demonstrate progressively.
"""

from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
    TimeoutError
)
import time
import os

# ===================================================================
# Worker functions (Module level for macOS 'spawn' multiprocessing)
# ===================================================================

def download_mock(url):
    """Simulates downloading a resource (I/O-bound)."""
    pid = os.getpid()
    print(f"  [PID {pid}] Downloading: {url}...")
    time.sleep(0.5)
    return f"Content of {url} (size: {len(url) * 42} bytes)"


def cpu_factorial(n):
    """Computes factorial (CPU-bound calculation)."""
    pid = os.getpid()
    print(f"  [PID {pid}] Computing factorial of {n}...")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return n, len(str(result))  # return n and digit count


def task_with_error(val):
    """Worker that demonstrates handling errors within a Future."""
    if val < 0:
        raise ValueError(f"Negative value ({val}) is not supported!")
    return val * 10


# ===================================================================
# 1. ThreadPoolExecutor (I/O-bound Concurrency)
# ===================================================================

def demo_thread_pool():
    """
    Using ThreadPoolExecutor for I/O tasks:
    - submit() returns a Future object representing pending execution.
    - as_completed() yields futures as soon as they finish.
    """
    print("=" * 60)
    print("ThreadPoolExecutor — I/O-Bound Tasks with as_completed()")
    print("=" * 60)

    urls = [
        "https://api.example.org/users",
        "https://api.example.org/posts",
        "https://api.example.org/comments",
        "https://api.example.org/photos",
    ]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks; returns a dictionary mapping future -> url
        future_to_url = {executor.submit(download_mock, url): url for url in urls}

        # Retrieve results as soon as each finishes
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(f"  ✓ Finished {url} -> {data}")
            except Exception as e:
                print(f"  ✗ {url} generated an exception: {e}")

    elapsed = time.time() - start_time
    print(f"\nAll 4 downloads finished in {elapsed:.2f}s (sequential would be ~2.0s)\n")


# ===================================================================
# 2. ProcessPoolExecutor (CPU-bound Parallelism)
# ===================================================================

def demo_process_pool():
    """
    Using ProcessPoolExecutor to bypass the GIL for heavy CPU math.
    executor.map() works like built-in map, preserving input order.
    """
    print("=" * 60)
    print("ProcessPoolExecutor — CPU-Bound Parallelism with executor.map()")
    print("=" * 60)

    numbers = [5000, 7000, 9000, 11000]

    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        # executor.map preserves the order of inputs
        results = executor.map(cpu_factorial, numbers)

        for n, digit_count in results:
            print(f"  ✓ {n}! has {digit_count} digits")

    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.2f}s\n")


# ===================================================================
# 3. Future Callbacks, Timeouts, and Exception Handling
# ===================================================================

def demo_future_lifecycle():
    """
    Demonstrates features of Future objects:
    - add_done_callback(): triggers automatically when finished
    - future.result(timeout=...): prevents hanging indefinitely
    - Exception propagation from workers
    """
    print("=" * 60)
    print("Future Lifecycle: Callbacks, Exceptions & Timeouts")
    print("=" * 60)

    def on_complete(future):
        print(f"  [Callback] Task has finished! Result = {future.result()}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        # 1. Callback demonstration
        print("1. Attaching a callback to a future:")
        f1 = executor.submit(lambda x: x ** 3, 5)
        f1.add_done_callback(on_complete)
        f1.result()  # wait

        # 2. Exception handling
        print("\n2. Handling exceptions raised inside a worker:")
        f2 = executor.submit(task_with_error, -5)
        try:
            f2.result()
        except ValueError as err:
            print(f"  Caught expected error from future: {err}")

        # 3. Timeout handling
        print("\n3. Handling timeouts:")
        f3 = executor.submit(time.sleep, 2.0)
        try:
            f3.result(timeout=0.3)
        except TimeoutError:
            print("  TimeoutError caught: Task took longer than 0.3s!")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_thread_pool()
    # demo_process_pool()
    # demo_future_lifecycle()


if __name__ == "__main__":
    main()
