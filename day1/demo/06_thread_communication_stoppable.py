"""
Demo 06: Thread Communication and Graceful Shutdown
=====================================================

Demonstrates two essential multithreading patterns:
  (a) Passing data between threads using `queue.Queue`.
  (b) Gracefully stopping a running thread using `threading.Event`.

Key concepts:
    - queue.Queue is thread-safe (no external locking needed).
    - A producer thread generates data; a consumer thread processes it.
    - threading.Event provides a simple flag that threads can wait on
      or check, enabling cooperative shutdown.
"""

import threading
import queue
import time
import random


# ---------------------------------------------------------------------------
# 1. Producer–Consumer communication using queue.Queue
# ---------------------------------------------------------------------------

def producer(q, count):
    """Produce `count` items and put them on the queue."""
    for i in range(count):
        item = f"item-{i}"
        q.put(item)                  # blocks if queue is full
        print(f"  [Producer] put '{item}' (queue size: {q.qsize()})")
        time.sleep(random.uniform(0.1, 0.3))
    q.put(None)                      # sentinel to signal "done"
    print("  [Producer] finished — sent sentinel")


def consumer(q):
    """Consume items from the queue until sentinel (None) is received."""
    while True:
        item = q.get()               # blocks if queue is empty
        if item is None:             # sentinel → stop
            print("  [Consumer] received sentinel — stopping")
            break
        print(f"  [Consumer] processing '{item}'")
        time.sleep(0.2)              # simulate processing
        q.task_done()


def demo_producer_consumer():
    """Launch a producer and consumer thread communicating via a Queue."""
    print("=" * 60)
    print("Part 1: Producer–Consumer with queue.Queue")
    print("=" * 60)

    data_queue = queue.Queue(maxsize=5)  # bounded queue (max 5 items)

    # Launch producer and consumer threads
    prod = threading.Thread(target=producer, args=(data_queue, 8))
    cons = threading.Thread(target=consumer, args=(data_queue,))

    prod.start()
    cons.start()

    prod.join()
    cons.join()
    print("Part 1 complete.")


# ---------------------------------------------------------------------------
# 2. Stoppable thread using threading.Event
# ---------------------------------------------------------------------------

def sensor_reader(stop_event, interval=0.5):
    """
    Simulates a sensor that reads data at regular intervals.
    The thread keeps running until `stop_event` is set.

    This pattern is common in monitoring, logging, and
    real-time data acquisition systems.
    """
    reading_num = 0
    while not stop_event.is_set():
        reading_num += 1
        value = round(random.uniform(20.0, 30.0), 2)
        print(f"  [Sensor] reading #{reading_num}: {value}°C")
        # Use event.wait() instead of time.sleep() so the thread
        # responds to the stop signal without waiting for the
        # full interval to elapse.
        stop_event.wait(timeout=interval)
    print("  [Sensor] stop_event detected — shutting down gracefully")


def demo_stoppable_thread():
    """Start a sensor thread and gracefully stop it after 3 seconds."""
    print("=" * 60)
    print("Part 2: Stoppable thread with threading.Event")
    print("=" * 60)

    # Create the stop event (initially unset / False)
    stop_event = threading.Event()

    # Start the sensor thread
    sensor_thread = threading.Thread(target=sensor_reader, args=(stop_event,))
    sensor_thread.start()

    # Let it run for 3 seconds, then signal it to stop
    time.sleep(3)
    print("\n  [Main] Setting stop_event...")
    stop_event.set()

    # Wait for the sensor thread to finish
    sensor_thread.join()
    print("  [Main] Sensor thread has exited cleanly.")
    print("\nPart 2 complete.")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_producer_consumer()
    # demo_stoppable_thread()


if __name__ == "__main__":
    main()
