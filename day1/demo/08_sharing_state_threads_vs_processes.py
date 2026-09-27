"""
Demo 08: Sharing State — Threads vs Processes
===============================================

Demonstrates the fundamental memory difference between threads and processes:
    - Threads SHARE memory → can access the same variables (but risk race conditions).
    - Processes have ISOLATED memory → changes in one process are invisible to another.

Key concepts:
    - Race condition: when multiple threads modify shared data without synchronization.
    - threading.Lock: prevents race conditions by allowing only one thread at a time.
    - multiprocessing.Value / multiprocessing.Array: explicit shared memory for processes.
"""

import threading
import multiprocessing
import time

INCREMENTS = 100_000


# ---------------------------------------------------------------------------
# Functions used by child processes — MUST be at module level on macOS/Windows
# (the 'spawn' start method needs to pickle/import them).
# ---------------------------------------------------------------------------

def try_modify_global(amount):
    """Attempt to modify a global variable from a child process."""
    global global_var
    global_var += amount
    print(f"  [Child PID {multiprocessing.current_process().pid}] "
          f"global_var inside child = {global_var}")


def increment_shared(counter, n):
    """Safely increment a shared counter using its built-in lock."""
    for _ in range(n):
        with counter.get_lock():
            counter.value += 1


# This global is used in Part 2 — each child gets its own copy (starts at 0)
global_var = 0


# ---------------------------------------------------------------------------
# Demo functions
# ---------------------------------------------------------------------------

def demo_race_condition():
    """Show that threads without locks cause race conditions on shared data."""
    print("=" * 60)
    print("Part 1a: Threads share memory — race condition (WITHOUT Lock)")
    print("=" * 60)

    counter_unsafe = 0

    def increment_unsafe(n):
        """Increment a shared counter n times WITHOUT a lock."""
        nonlocal counter_unsafe
        for _ in range(n):
            # This is NOT atomic: read → modify → write can be interleaved
            counter_unsafe += 1

    threads = []
    for _ in range(5):
        t = threading.Thread(target=increment_unsafe, args=(INCREMENTS,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = 5 * INCREMENTS
    print(f"  Without Lock: counter = {counter_unsafe}  (expected {expected})")
    print(f"  {'✓ Correct' if counter_unsafe == expected else '✗ RACE CONDITION — value is wrong!'}")


def demo_thread_lock():
    """Show that using a Lock fixes the race condition."""
    print("=" * 60)
    print("Part 1b: Threads share memory — fixed with Lock")
    print("=" * 60)

    counter_safe = 0
    lock = threading.Lock()

    def increment_safe(n):
        """Increment a shared counter n times WITH a lock."""
        nonlocal counter_safe
        for _ in range(n):
            with lock:                   # acquire lock before modifying
                counter_safe += 1

    threads = []
    for _ in range(5):
        t = threading.Thread(target=increment_safe, args=(INCREMENTS,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = 5 * INCREMENTS
    print(f"  With Lock   : counter = {counter_safe}  (expected {expected})")
    print(f"  {'✓ Correct!' if counter_safe == expected else '✗ Still wrong?!'}")


def demo_process_isolation():
    """Show that processes have isolated memory — parent doesn't see child changes."""
    print("=" * 60)
    print("Part 2: Processes have isolated memory")
    print("=" * 60)

    p1 = multiprocessing.Process(target=try_modify_global, args=(100,))
    p2 = multiprocessing.Process(target=try_modify_global, args=(200,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"\n  [Parent] global_var in parent = {global_var}")
    print("  → Children's changes are NOT visible to the parent!")
    print("    Each process has its own copy of memory.")


def demo_shared_value():
    """Use multiprocessing.Value for explicit shared state between processes."""
    print("=" * 60)
    print("Part 3: Shared memory for processes (multiprocessing.Value)")
    print("=" * 60)

    expected = 5 * INCREMENTS

    # multiprocessing.Value creates a shared memory variable
    # 'i' = signed integer, initial value = 0
    shared_counter = multiprocessing.Value('i', 0)

    processes = []
    for _ in range(5):
        p = multiprocessing.Process(
            target=increment_shared,
            args=(shared_counter, INCREMENTS)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"  Shared counter = {shared_counter.value}  (expected {expected})")
    print(f"  {'✓ Correct!' if shared_counter.value == expected else '✗ Wrong!'}")
    print()
    print("SUMMARY:")
    print("  • Threads → shared memory (fast but needs locks)")
    print("  • Processes → isolated memory (safe but needs explicit sharing)")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_race_condition()
    # demo_thread_lock()
    # demo_process_isolation()
    # demo_shared_value()


if __name__ == "__main__":
    main()
