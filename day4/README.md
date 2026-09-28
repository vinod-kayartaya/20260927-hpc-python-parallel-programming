# Day 4: Distributed Python Computing

> **Total Duration:** 4 hours (divided into two 2-hour sessions)  
> **Prerequisites:** Days 1, 2, & 3 (Concurrency, Networking, Multi-core & MPI basics)  
> **Demos Folder:** [`day4/demo/`](./demo/)

---

## Session Overview

Day 4 explores how Python scales across heterogeneous networks, clouds, and clusters using high-level distributed architectures, task queues, and remote object models:

---

### [Session 1: Distributed Task Queues & Scientific Computing](./README-session1.md)
*Duration: 2 hours*

- **Distributed Task Queues with Celery**:
  - The 4-component architecture: Client, Message Broker (RabbitMQ/Redis), Workers, and Result Backend.
  - Creating and registering tasks with `@app.task`.
  - Non-blocking asynchronous task execution with `.delay()` and `.apply_async()`.
  - Monitoring task lifecycles and retrieving values with `AsyncResult`.
  - Complex multi-task workflows: **Chains** (pipelines) and **Groups** (parallel maps).
- **Scientific Computing with SCOOP**:
  - Purpose-built scientific computing on heterogeneous workstations.
  - ZeroMQ brokerless communication topology.
  - Distributed `map()` operations via `scoop.futures.map()`.
  - Dynamic load balancing and comparisons against standard `multiprocessing.Pool`.

**Session 1 Demos:**
- [`day4/demo/01_celery_distributed_tasks.py`](./demo/01_celery_distributed_tasks.py)
- [`day4/demo/02_scoop_scientific_map.py`](./demo/02_scoop_scientific_map.py)

---

### [Session 2: Remote Objects, RPC & Communicating Sequential Processes](./README-session2.md)
*Duration: 2 hours*

- **Remote Method Invocation (RMI) with Pyro4**:
  - Exposing Python classes over the network with `@Pyro4.expose`.
  - The Pyro Daemon and Name Server (`pyro4-ns`).
  - Transparent remote method calls through client proxies.
  - Microservice-style distributed workflows via object chaining.
- **Transparent Remote Procedure Calls (RPyC)**:
  - Symmetric RPC model and remote Python execution.
  - Exposing services via `rpyc.Service` and `exposed_` methods.
- **Communicating Sequential Processes (CSP) with PyCSP**:
  - Tony Hoare's CSP philosophy: *"Do not communicate by sharing memory; instead, share memory by communicating."*
  - Lock-free synchronization using synchronous and buffered Channels.
- **Big Data Processing with Disco**:
  - Erlang-backed distributed MapReduce in Python.

**Session 2 Demos:**
- [`day4/demo/03_pyro4_remote_objects.py`](./demo/03_pyro4_remote_objects.py)
- [`day4/demo/04_rpyc_and_csp.py`](./demo/04_rpyc_and_csp.py)

---

## Quick Demo Reference

| Demo File | Topic | Key Primitives / Technologies |
|---|---|---|
| [`01_celery_distributed_tasks.py`](./demo/01_celery_distributed_tasks.py) | Task Queues | `@app.task`, `delay()`, `AsyncResult`, `chain`, `group` |
| [`02_scoop_scientific_map.py`](./demo/02_scoop_scientific_map.py) | Scientific Map | `scoop.futures.map()`, ZeroMQ cluster scaling |
| [`03_pyro4_remote_objects.py`](./demo/03_pyro4_remote_objects.py) | Remote Objects | `@Pyro4.expose`, `Pyro4.Daemon`, Name Server, Proxies |
| [`04_rpyc_and_csp.py`](./demo/04_rpyc_and_csp.py) | RPC & Channels | `rpyc.Service`, `exposed_`, CSP `Channel` (`write`/`read`) |

---

> **Ready to begin? Start with [Session 1: Distributed Task Queues & Scientific Computing](./README-session1.md)**
