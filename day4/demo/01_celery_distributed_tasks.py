"""
Demo 01: Distributed Task Queues with Celery
============================================

Demonstrates distributed task execution with Celery:
    - Architecture: Client -> Message Broker (Redis/RabbitMQ) -> Worker Pool -> Result Backend
    - Defining tasks with @app.task
    - Calling tasks asynchronously using task.delay() and task.apply_async()
    - Inspecting AsyncResult (status, result, error)
    - Workflow patterns: Chaining and grouping tasks

Run instructions:
    If Celery is installed and a Redis broker is running:
        celery -A 01_celery_distributed_tasks worker --loglevel=info
        python3 01_celery_distributed_tasks.py
    Otherwise, running with `python3` executes a self-contained simulation.
"""

import time
import os
import queue
import threading

# ---------------------------------------------------------------------------
# Celery setup with fallback simulation
# ---------------------------------------------------------------------------
try:
    from celery import Celery, chain, group
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False


if CELERY_AVAILABLE:
    # Standard Celery configuration with local Redis broker
    app = Celery(
        'hpc_tasks',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/1'
    )

    @app.task
    def add(x, y):
        """A simple computational task executed by worker."""
        return x + y

    @app.task
    def multiply(x, y):
        """Another task executed by worker."""
        return x * y

    @app.task
    def compute_heavy(n):
        """Simulates a heavy calculation."""
        time.sleep(0.5)
        return sum(i * i for i in range(n))


# ===================================================================
# Fallback Simulation: Demonstrating the Broker-Worker Architecture
# ===================================================================

class SimulatedBroker:
    """Simulates a message broker (like Redis or RabbitMQ) and worker."""

    def __init__(self):
        self.task_queue = queue.Queue()
        self.results = {}
        self._running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        while self._running:
            try:
                task_id, func, args = self.task_queue.get(timeout=0.1)
                print(f"  [Worker PID {os.getpid()}] Processing task {task_id}: {func.__name__}{args}...")
                res = func(*args)
                self.results[task_id] = ("SUCCESS", res)
                self.task_queue.task_done()
            except queue.Empty:
                continue

    def enqueue(self, task_id, func, args):
        self.results[task_id] = ("PENDING", None)
        self.task_queue.put((task_id, func, args))

    def get_result(self, task_id):
        return self.results.get(task_id, ("UNKNOWN", None))


# ===================================================================
# 1. Basic Task Definition and Asynchronous Invocation
# ===================================================================

def demo_celery_task_definition():
    """
    Demonstrates asynchronous task invocation:
    - task.delay(arg1, arg2) queues the task on the broker and returns an AsyncResult.
    - The client is non-blocking and can do other work.
    - result.get() waits for and retrieves the returned value.
    """
    print("=" * 60)
    print("Celery: Distributed Task Definition and .delay()")
    print("=" * 60)

    if CELERY_AVAILABLE:
        print("Using genuine Celery runtime:")
        print("Submitting add.delay(15, 27)...")
        async_res = add.delay(15, 27)
        print(f"  Task ID : {async_res.id}")
        print(f"  Status  : {async_res.status}")

        print("Waiting for result from worker...")
        final_val = async_res.get(timeout=5)
        print(f"  Result  : {final_val}")
    else:
        print("[Simulated Mode — Celery / Redis not installed]")
        print("Architecture: [Client] ---> [Broker (Redis)] ---> [Celery Worker]")
        broker = SimulatedBroker()

        def sim_add(a, b):
            time.sleep(0.3)
            return a + b

        task_id = "task-uuid-101"
        print(f"\n[Client] Submitting task {task_id} via simulated .delay(15, 27)...")
        broker.enqueue(task_id, sim_add, (15, 27))

        print("[Client] Task submitted. Checking status immediately:")
        status, val = broker.get_result(task_id)
        print(f"  Status: {status} (client is free to continue executing!)")

        print("[Client] Waiting for worker to finish...")
        time.sleep(0.6)
        status, val = broker.get_result(task_id)
        print(f"  Status: {status}, Result: {val}\n")


# ===================================================================
# 2. Workflow Orchestration: Chains and Groups
# ===================================================================

def demo_celery_workflows():
    """
    Demonstrates Celery workflow primitives:
    - chain: runs tasks sequentially, passing the output of task N to task N+1.
      Example: (add(2, 3) | multiply(10)) -> (2+3)*10 = 50
    - group: runs a list of independent tasks in parallel across worker nodes.
    """
    print("=" * 60)
    print("Celery Workflows: Chains and Groups")
    print("=" * 60)

    print("Pattern 1: Task Chaining (Sequential Pipeline)")
    print("  Syntax: chain(task1.s() | task2.s() | task3.s())")
    print("  Output of task 1 automatically becomes the first argument of task 2.")
    print("  Example: add(2, 3) -> 5, then multiply(5, 10) -> 50\n")

    print("Pattern 2: Task Grouping (Parallel Map across Workers)")
    print("  Syntax: group(task.s(i) for i in range(N))")
    print("  Executes tasks in parallel across available cluster nodes.")
    print("  Gathers all outputs into a single list once all tasks complete.\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_celery_task_definition()
    # demo_celery_workflows()


if __name__ == "__main__":
    main()
