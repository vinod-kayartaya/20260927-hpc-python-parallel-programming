# Day 3: Distributed Computing (MPI) & Asynchronous Programming

> **Total Duration:** 4 hours (divided into two 2-hour sessions)  
> **Prerequisites:** Days 1 & 2 (Processes, Threads, Concurrency, Serialization)  
> **Demos Folder:** [`day3/demo/`](./demo/)

---

## Session Overview

Day 3 takes our parallel programming capabilities to the next level: scaling out to **distributed multi-node clusters** with MPI, and mastering modern **asynchronous concurrent programming** with `concurrent.futures` and `asyncio`.

---

### [Session 1: Distributed Computing with MPI (`mpi4py`)](./README-session1.md)
*Duration: 2 hours*

- **Distributed Memory Model**: How clusters communicate without shared RAM.
- **MPI Fundamentals**: Communicators (`MPI.COMM_WORLD`), Rank, and Size.
- **Point-to-Point Communication**: Blocking `send`/`recv` vs non-blocking `isend`/`irecv`.
- **Deadlock Avoidance**: Using `comm.sendrecv()` to safely swap data.
- **Collective Operations**: Broadcast (`bcast`), Scatter, Gather, Reductions (`reduce`/`allreduce`), and All-to-all (`alltoall`).
- **Performance Optimization**: Zero-copy array transfers with NumPy buffer protocols (`Send`/`Recv`).

**Session 1 Demos:**
- [`day3/demo/01_mpi_point_to_point.py`](./demo/01_mpi_point_to_point.py)
- [`day3/demo/02_mpi_collective.py`](./demo/02_mpi_collective.py)

---

### [Session 2: Asynchronous Programming (`concurrent.futures` & `asyncio`)](./README-session2.md)
*Duration: 2 hours*

- **High-Level Pool Abstractions**: `ThreadPoolExecutor` and `ProcessPoolExecutor`.
- **Working with Futures**: `submit()`, `as_completed()`, timeouts, exception handling, and callbacks.
- **The Event Loop Model**: Single-threaded cooperative multitasking.
- **Async & Await**: Writing coroutines and coordinating concurrent execution with `asyncio.gather()`.
- **Task Management**: Creating, monitoring, and cancelling background tasks with `create_task()`.
- **Bridging Worlds**: Offloading blocking I/O and heavy CPU computations with `loop.run_in_executor()`.
- **Architectural Comparison**: When to use Threads vs Processes vs Asyncio vs MPI.

**Session 2 Demos:**
- [`day3/demo/03_concurrent_futures.py`](./demo/03_concurrent_futures.py)
- [`day3/demo/04_asyncio_basics.py`](./demo/04_asyncio_basics.py)

---

## Quick Demo Reference

| Demo File | Topic | Key Primitives / Functions |
|---|---|---|
| [`01_mpi_point_to_point.py`](./demo/01_mpi_point_to_point.py) | MPI Point-to-Point | `comm.send`, `comm.recv`, `comm.isend`, `comm.sendrecv` |
| [`02_mpi_collective.py`](./demo/02_mpi_collective.py) | MPI Collectives | `comm.bcast`, `comm.scatter`, `comm.gather`, `comm.reduce`, `comm.alltoall` |
| [`03_concurrent_futures.py`](./demo/03_concurrent_futures.py) | Executor Pools | `ThreadPoolExecutor`, `ProcessPoolExecutor`, `submit`, `as_completed` |
| [`04_asyncio_basics.py`](./demo/04_asyncio_basics.py) | Asyncio Event Loop | `async def`, `await`, `asyncio.gather`, `create_task`, `run_in_executor` |

---

> **Ready to begin? Start with [Session 1: Distributed Computing with MPI](./README-session1.md)**
