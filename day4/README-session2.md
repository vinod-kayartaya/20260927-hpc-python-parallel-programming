# Day 4, Session 2: Remote Objects, RPC & Communicating Sequential Processes

> **Duration:** 2 hours (theory + live demonstrations)  
> **Prerequisites:** Days 1, 2, & 3 (OOP in Python, Networking, Sockets)  
> **Demos folder:** [`day4/demo/`](./demo/)

---

## Table of Contents

1. [The Remote Procedure Call (RPC) Paradigm](#1-the-remote-procedure-call-rpc-paradigm)
2. [Remote Method Invocation with Pyro4](#2-remote-method-invocation-with-pyro4)
   - [What is Pyro4?](#what-is-pyro4)
   - [The Name Server and Pyro Daemon](#the-name-server-and-pyro-daemon)
   - [Developing a Client-Server Application with Pyro4](#developing-a-client-server-application-with-pyro4)
   - [Chaining Remote Objects](#chaining-remote-objects)
3. [Transparent RPC with RPyC](#3-transparent-rpc-with-rpyc)
   - [Symmetric RPC Architecture](#symmetric-rpc-architecture)
   - [Exposing Services with RPyC](#exposing-services-with-rpyc)
4. [Communicating Sequential Processes (CSP) with PyCSP](#4-communicating-sequential-processes-csp-with-pycsp)
   - [The CSP Philosophy](#the-csp-philosophy)
   - [Channels, Read, and Write](#channels-read-and-write)
5. [Distributed MapReduce with Disco](#5-distributed-mapreduce-with-disco)
6. [Session 2 Summary & What's Next](#session-2-summary--whats-next)

---

## 1. The Remote Procedure Call (RPC) Paradigm

In standard Python code, when you instantiate an object and call a method:
```python
calc = Calculator()
res = calc.add(10, 20)
```
The method executes locally within the same process.

In **Distributed Systems**, we often want that object to live on a **remote machine** with specialized hardware (e.g. 512 GB RAM, high-end database, or GPUs), while the client calls methods **as if the object were local**:

```
┌──────────────────────┐                     ┌──────────────────────┐
│     Client Host      │                     │     Server Host      │
│                      │                     │                      │
│ proxy = Proxy(URI)   │   1. Serialize Call │ ┌──────────────────┐ │
│ res = proxy.add(5, 7)│ ──────────────────> │ │ Calculator Object│ │
│                      │                     │ │ add(5, 7) -> 12  │ │
│                      │   2. Return 12      │ └──────────────────┘ │
│ print(res)  # 12     │ <────────────────── │                      │
└──────────────────────┘                     └──────────────────────┘
```

The underlying network socket communication, serialization, and deserialization are handled automatically by the RPC framework.

---

## 2. Remote Method Invocation with Pyro4

**Pyro4** stands for **Python Remote Objects**:
- It allows you to expose ordinary Python classes over the network.
- It feels just like normal Python code (object-oriented RPC / RMI).
- Supports automatic network serialization, exception propagation, and security tokens.

---

### The Name Server and Pyro Daemon

To connect clients to servers without hardcoding IP addresses, Pyro uses a **Name Server**:

```
                       ┌──────────────────────┐
                       │   Pyro Name Server   │
                       │ "calc.service" -> URI│
                       └──────────▲───────────┘
                                  │ 2. Lookup URI
                     1. Register  │
┌──────────────────────┐          │          ┌──────────────────────┐
│     Pyro Server      ├──────────┘          │     Pyro Client      │
│  (Daemon publishes   │                     │  (Connects via URI   │
│   ComputeService)    │ <================== │   and calls methods) │
└──────────────────────┘   3. Direct TCP     └──────────────────────┘
```

1. **Start the Name Server**:
   ```bash
   pyro4-ns
   ```
2. **Server registers** its service under a human-friendly name (`"calc.service"`).
3. **Client queries Name Server** to locate the current IP/Port and connects directly.

---

### Developing a Client-Server Application with Pyro4

#### 1. The Server (`server.py`)
```python
import Pyro4

@Pyro4.expose  # Security: explicitly allow remote method calls
class CalculatorService:
    def add(self, a, b):
        return a + b

    def power(self, base, exp):
        return base ** exp

daemon = Pyro4.Daemon()                # Start the network listener
ns = Pyro4.locateNS()                  # Locate the Pyro Name Server
uri = daemon.register(CalculatorService) # Register the class
ns.register("service.calc", uri)       # Publish name to Name Server

print("Calculator service is running and ready for clients...")
daemon.requestLoop()
```

#### 2. The Client (`client.py`)
```python
import Pyro4

# Look up the remote object via the Name Server
calc = Pyro4.Proxy("PYRONAME:service.calc")

# Transparent remote method call!
result = calc.power(2, 10)
print("Result from remote server:", result)  # 1024
```

---

### Chaining Remote Objects

In distributed microservices, objects often interact with other remote services:
- **Service A (Auth)** verifies user identity.
- **Service B (Analytics)** queries the database.
- **Service C (Notifier)** sends notifications.

With Pyro4, remote proxies can be created inside another remote object. Service A can seamlessly forward data or chain calls to Service B and Service C without exposing internal cluster topology to the end client.

---

### 🖥️ Demo Time

> **Now, let's see these theoretical topics in action.**
>
> - [`03_pyro4_remote_objects.py`](./demo/03_pyro4_remote_objects.py) —
>   1. `demo_remote_method_invocation()` — Exposing remote objects, proxy calls, and stats
>   2. `demo_pyro_chaining()` — Chaining remote service objects across distributed microservices

---

## 3. Transparent RPC with RPyC

While Pyro4 focuses on object-oriented remote services, **RPyC** (Remote Python Call) provides **transparent, symmetrical RPC**:
- It allows you to directly manipulate remote variables, remote modules, and remote objects as if they were local.
- If an exception occurs on the remote server, RPyC reconstructs the full remote stack trace on your client!

```python
import rpyc

# Connect to remote RPyC server
conn = rpyc.connect("192.168.1.50", 18812)

# Directly execute operations on the remote server's Python interpreter:
print("Remote OS PID:", conn.modules.os.getpid())
remote_val = conn.modules.math.sqrt(144)
print("Evaluated remotely:", remote_val)  # 12.0
```

### Exposing Services with RPyC
For secure, controlled access, RPyC uses `Service` classes. Any method prefixed with `exposed_` is made available to clients:
```python
import rpyc

class MyService(rpyc.Service):
    def exposed_multiply(self, a, b):
        return a * b

# Client calls: conn.root.multiply(5, 6) -> 30
```

---

## 4. Communicating Sequential Processes (CSP) with PyCSP

### The CSP Philosophy

Formulated by computer scientist **C.A.R. Hoare** in 1978, **CSP** is a formal model for concurrency that powers modern languages like **Go** (Golang channels):

> *"Do not communicate by sharing memory; instead, share memory by communicating."*

Traditional multithreading shares memory and protects it with locks, leading to race conditions and deadlocks. In CSP:
- Threads or processes are **independent sequential entities**.
- They share **NO state**.
- They communicate exclusively through typed **Channels**.

```
┌──────────────────┐                            ┌──────────────────┐
│ Process A        │       Channel (FIFO)       │ Process B        │
│                  │ ─────────────────────────> │                  │
│ chan.write(data) │                            │ data = chan.read()
└──────────────────┘                            └──────────────────┘
```

### Channels, Read, and Write
- **Unbuffered Channel**: A write blocks until another process reads (rendezvous synchronization).
- **Buffered Channel**: Holds up to N messages before blocking the writer.
- In Python, the **`PyCSP`** library provides native CSP primitives (`@process`, `Channel`, `Sequence`, `Parallel`).

---

## 5. Distributed MapReduce with Disco

**Disco** is an open-source, lightweight distributed computing framework for big data processing based on the **MapReduce** paradigm:
- Developed by Nokia Research Center.
- Core written in Erlang (fault tolerance, concurrency) with jobs written in **pure Python**.
- Map tasks distribute data across nodes; Reduce tasks aggregate the mapped outputs into final insights.

---

### 🖥️ Demo Time

> **Now, let's see these theoretical topics in action.**
>
> - [`04_rpyc_and_csp.py`](./demo/04_rpyc_and_csp.py) —
>   1. `demo_rpyc()` — Remote procedure call and remote function execution
>   2. `demo_csp()` — Channel-based message passing following the Communicating Sequential Processes model

---

## Session 2 Summary & What's Next

| Framework | Paradigm | Key Concept | Use Case |
|---|---|---|---|
| **Pyro4** | Object-Oriented RMI | `@Pyro4.expose`, Name Server | Calling methods on remote Python objects |
| **RPyC** | Transparent RPC | `rpyc.connect()`, `exposed_` | Remote execution, remote scripting, testing |
| **PyCSP** | Sequential Processes | Channels (`read`/`write`) | Lock-free, message-passing concurrency |
| **Disco** | Distributed MapReduce | Map -> Shuffle -> Reduce | Big-data batch processing across clusters |

### What's Coming Tomorrow (Day 5)
Tomorrow is the grand finale: **GPU Programming with Python**!
- GPU hardware architecture: thousands of parallel ALUs, streaming multiprocessors.
- **PyCUDA**: Writing CUDA kernels in Python, GPU memory allocation, and grid/block threads hierarchy.
- **Numba / NumbaPro**: JIT compilation and `@cuda.jit` decorators.
- **PyOpenCL**: Cross-vendor GPU acceleration (NVIDIA, AMD, Intel, Apple Silicon).

---

> **End of Day 4**
