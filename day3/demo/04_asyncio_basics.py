"""
Demo 04: Asynchronous Programming with `asyncio`
================================================

Demonstrates cooperative multitasking using Python's `asyncio`:
    - Defining coroutines (async def / await) and running tasks concurrently (asyncio.gather)
    - Task manipulation (asyncio.create_task, cancellation, status checking)
    - Bridging asyncio with blocking / CPU-bound code using run_in_executor

Uncomment one function at a time in main() to demonstrate progressively.
"""

import asyncio
import time
import os

# ===================================================================
# 1. Coroutines and asyncio.gather()
# ===================================================================

async def fetch_data(name, delay):
    """An asynchronous coroutine that simulates waiting for I/O."""
    print(f"  [{name}] Request started... (will take {delay}s)")
    await asyncio.sleep(delay)  # non-blocking sleep yields control to event loop
    print(f"  [{name}] Data received!")
    return f"Result-{name}"


async def coroutine_gather_demo():
    """Run multiple coroutines concurrently using asyncio.gather()."""
    print("=" * 60)
    print("Coroutines with asyncio.gather() — Cooperative Multitasking")
    print("=" * 60)

    start = time.time()

    # Launch all 3 coroutines concurrently on the single-threaded event loop
    results = await asyncio.gather(
        fetch_data("Service-A", 1.0),
        fetch_data("Service-B", 0.5),
        fetch_data("Service-C", 0.8),
    )

    elapsed = time.time() - start
    print(f"\nAll results: {results}")
    print(f"Total time: {elapsed:.2f}s (Sequential would take 1.0 + 0.5 + 0.8 = 2.3s)")
    print("Notice how Service-B (0.5s) finished before Service-A (1.0s)!\n")


def demo_coroutines_and_gather():
    asyncio.run(coroutine_gather_demo())


# ===================================================================
# 2. Task Manipulation (create_task & cancellation)
# ===================================================================

async def periodic_worker(name):
    """A task that runs in a loop until cancelled."""
    count = 1
    try:
        while True:
            print(f"  [Heartbeat {name}] Ping #{count}")
            await asyncio.sleep(0.3)
            count += 1
    except asyncio.CancelledError:
        print(f"  [Heartbeat {name}] Cancellation requested. Cleaning up...")
        raise


async def task_manipulation_demo():
    """Demonstrates scheduling background tasks and cooperative cancellation."""
    print("=" * 60)
    print("Task Manipulation: create_task, status, and cancel")
    print("=" * 60)

    # Schedule periodic_worker to run immediately in the background
    task = asyncio.create_task(periodic_worker("Monitor"))

    print(f"Task created. Is done? {task.done()}")

    # Let the background task run for 1 second
    await asyncio.sleep(1.0)

    # Cancel the task
    print("\nCancelling the background task...")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Task confirmed cancelled.")

    print(f"Is done after cancel? {task.done()}\n")


def demo_task_manipulation():
    asyncio.run(task_manipulation_demo())


# ===================================================================
# 3. Bridging Asyncio with Blocking / CPU Code (run_in_executor)
# ===================================================================

def blocking_cpu_task(n):
    """
    A traditional synchronous, blocking CPU calculation.
    If called with regular 'await', it would freeze the entire asyncio event loop!
    """
    print(f"  [Sync Worker, PID {os.getpid()}] Calculating sum of squares up to {n:,}...")
    total = sum(i * i for i in range(n))
    return total


async def run_in_executor_demo():
    """
    Demonstrates run_in_executor to execute blocking code in a background thread pool,
    preventing the event loop from freezing.
    """
    print("=" * 60)
    print("Bridging Asyncio & Blocking Code: run_in_executor")
    print("=" * 60)

    loop = asyncio.get_running_loop()

    # Simultaneously run an async task AND offload a blocking task to a thread pool
    async def async_ticker():
        for i in range(4):
            print(f"    [Async Event Loop] Tick {i + 1} (event loop is not blocked!)")
            await asyncio.sleep(0.2)

    ticker_coro = async_ticker()

    # Offload the blocking CPU function to default thread pool executor
    executor_future = loop.run_in_executor(None, blocking_cpu_task, 10_000_000)

    # Await both concurrently
    _, result = await asyncio.gather(ticker_coro, executor_future)

    print(f"\nResult from blocking task: {result}")
    print("Notice the async ticks continued running while the CPU task executed!\n")


def demo_asyncio_with_futures():
    asyncio.run(run_in_executor_demo())


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_coroutines_and_gather()
    # demo_task_manipulation()
    # demo_asyncio_with_futures()


if __name__ == "__main__":
    main()
