# Day 2: Thread-Based & Process-Based Parallelism

> **Total Duration:** 4 hours (divided into two 2-hour sessions)  
> **Prerequisites:** Day 1 (Serialization, Multiprocessing/Threading basics, GIL, Amdahl's Law)  
> **Demos Folder:** [`day2/demo/`](./demo/)

---

## Session Overview

Day 2 dives into shared-memory parallelism within a single machine across two dedicated 2-hour sessions:

---

### [Session 1: Thread-Based Parallelism](./README-session1.md)
*Duration: 2 hours*

- **Thread Definition & Introspection**: Inspecting threads with `current_thread()`, `enumerate()`, `active_count()`.
- **Subclassing `threading.Thread`**: Encapsulating stateful tasks within custom thread classes.
- **Synchronization Primitives**:
  - `Lock`: Mutual exclusion to protect shared variables.
  - `RLock`: Reentrant locks for recursive and nested calls.
  - `Semaphore`: Controlling pools of limited resources (e.g. max connections).
- **Thread Coordination Primitives**:
  - `Condition`: State-change notification with `wait()`, `notify()`, `notify_all()`.
  - `Event`: One-shot signaling for synchronized startup or cancellation.
  - `Barrier`: Phased execution checkpoints across fixed thread sets.
- **Thread-Safe Data Structures**: `queue.Queue`, `queue.LifoQueue`, and `queue.PriorityQueue`.

**Session 1 Demos:**
- [`day2/demo/01_thread_sync_primitives.py`](./demo/01_thread_sync_primitives.py)
- [`day2/demo/02_thread_coordination.py`](./demo/02_thread_coordination.py)

---

### [Session 2: Process-Based Parallelism](./README-session2.md)
*Duration: 2 hours*

- **Process Lifecycle**:
  - Spawning processes with `multiprocessing.Process`.
  - Assigning process names for debugging.
  - Daemon processes for background tasks.
  - Process termination and cleanup (`terminate()`, `kill()`, `is_alive()`).
- **Subclassing `multiprocessing.Process`**: Creating custom process classes.
- **Inter-Process Communication (IPC)**:
  - `multiprocessing.Queue`: Process-safe multi-producer / multi-consumer FIFOs.
  - `multiprocessing.Pipe`: Fast bidirectional point-to-point connections.
- **Process Synchronization & Shared State**:
  - Process-safe `Lock`, `Event`, `Semaphore`, `Barrier`.
  - Shared memory with `Value`, `Array`, and proxy managers with `Manager`.
- **Process Pools**:
  - Batch data execution with `Pool.map()` and `Pool.starmap()`.
  - Non-blocking task submission with `Pool.apply_async()` and completion callbacks.

**Session 2 Demos:**
- [`day2/demo/03_process_lifecycle.py`](./demo/03_process_lifecycle.py)
- [`day2/demo/04_process_communication_pool.py`](./demo/04_process_communication_pool.py)

---

## Quick Demo Reference

| Demo File | Topic | Key Primitives / Functions |
|---|---|---|
| [`01_thread_sync_primitives.py`](./demo/01_thread_sync_primitives.py) | Synchronization | `threading.Lock`, `threading.RLock`, `threading.Semaphore` |
| [`02_thread_coordination.py`](./demo/02_thread_coordination.py) | Coordination & Queues | `threading.Condition`, `threading.Event`, `threading.Barrier`, `queue.PriorityQueue` |
| [`03_process_lifecycle.py`](./demo/03_process_lifecycle.py) | Process Management | `Process`, `daemon=True`, `terminate()`, subclassing `Process` |
| [`04_process_communication_pool.py`](./demo/04_process_communication_pool.py) | IPC & Process Pools | `multiprocessing.Queue`, `multiprocessing.Pipe`, `Pool.map`, `Pool.apply_async` |

---

> **Ready to begin? Start with [Session 1: Thread-Based Parallelism](./README-session1.md)**
