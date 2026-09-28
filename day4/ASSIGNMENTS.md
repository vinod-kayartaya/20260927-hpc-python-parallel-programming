# Day 4: Lab Exercises — Distributed Python Computing

> **Duration:** 4 hours (self-paced hands-on practice)  
> **Reference:** [`day4/README.md`](./README.md), [`day4/README-session1.md`](./README-session1.md), and [`day4/README-session2.md`](./README-session2.md)  
> **Note:** These exercises are for personal practice to reinforce the concepts covered today. Start from Exercise 1 and work sequentially.

---

## Exercise 1: Asynchronous Distributed Tasks with Celery

**Topics:** Celery, Message Broker, Worker pool, `.delay()`, `AsyncResult`

### Problem Statement

Write a script `ex01_celery_task.py` that sets up and executes an asynchronous task queue:

1. Configure a Celery application instance:
   ```python
   from celery import Celery
   app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
   ```

2. Define a distributed task `@app.task` called `compute_factorial(n)`:
   - Computes $n!$ using an iterative loop.
   - Introduces a small artificial delay (`time.sleep(0.5)`) to simulate a heavy job.
   - Returns a dictionary: `{"n": n, "digits": len(str(result))}`.

3. In the client driver:
   - Submit 5 factorial calculations asynchronously using `.delay()`:
     ```python
     tasks = [compute_factorial.delay(x) for x in [1000, 2000, 3000, 4000, 5000]]
     ```
   - Print the generated task UUIDs immediately.
   - Poll each `AsyncResult` object in a loop until all tasks are marked as `READY`.
   - Retrieve and print the final dictionary results.

### Hints & Guidelines
- If Redis is installed locally, you can start the Celery worker in one terminal:
  `celery -A ex01_celery_task worker --loglevel=info`
- If Celery or Redis is not installed on your practice environment, write a self-contained simulation of the broker/worker architecture using `queue.Queue` and background threads as demonstrated in Demo 01.

### Best Practices
- Keep Celery tasks small and self-contained. Pass database IDs or file URLs instead of passing giant data structures through the broker.
- Always configure a Result Backend if the client code needs to read return values.

---

## Exercise 2: Celery Workflow Pipelines (Chains & Groups)

**Topics:** Celery Canvas, `chain()`, `group()`, workflow orchestration

### Problem Statement

Write a script `ex02_celery_canvas.py` implementing complex task workflows:

1. Define three discrete computational tasks:
   - `@app.task def fetch_numbers(count)`: Returns a list of random integers.
   - `@app.task def filter_evens(numbers)`: Returns only the even integers from the list.
   - `@app.task def compute_sum(numbers)`: Returns the sum of the filtered integers.

2. **Sequential Chain (Pipeline):**
   - Construct a sequential workflow using Celery's `chain`:
     ```python
     pipeline = chain(fetch_numbers.s(50) | filter_evens.s() | compute_sum.s())
     result = pipeline.apply_async()
     print("Pipeline result:", result.get())
     ```
   - Verify that the output of each stage automatically flows into the next stage.

3. **Parallel Group:**
   - Construct a parallel group that calculates squares for 10 numbers simultaneously:
     ```python
     job_group = group(compute_square.s(i) for i in range(10))
     group_result = job_group.apply_async()
     print("All squares computed:", group_result.get())
     ```

### Hints & Guidelines
- Use `.s()` (signature) to construct task templates without executing them immediately.
- The pipe operator `|` connects tasks in a chain.

### Best Practices
- Use `chain` for ETL (Extract-Transform-Load) sequential pipelines.
- Use `group` for parallel fan-out / fan-in map operations across multiple cluster machines.

---

## Exercise 3: Scientific Computing with SCOOP

**Topics:** SCOOP, ZeroMQ, `scoop.futures.map()`, cluster scaling

### Problem Statement

Write a script `ex03_scoop_monte_carlo.py` to distribute a scientific calculation across a network cluster using SCOOP:

1. Implement a numerical integration function `estimate_integral(bounds)`:
   - Evaluates a complex mathematical function (e.g. $\int \sin(x) e^{-x^2} dx$) across a sub-interval `[a, b]`.
   - Uses the trapezoidal rule or random Monte Carlo sampling with 500,000 evaluations per call.

2. In the main block:
   - Divide a large domain `[0, 100]` into 16 non-overlapping sub-intervals.
   - Distribute the intervals across all available cluster cores using `scoop.futures.map(estimate_integral, intervals)`.
   - Sum the returned sub-integrals to obtain the total area under the curve.

3. Execute the script:
   ```bash
   python3 -m scoop ex03_scoop_monte_carlo.py
   ```

### Hints & Guidelines
- SCOOP uses ZeroMQ under the hood and requires no central database setup.
- If SCOOP is not installed, you can simulate the cluster distribution locally using `multiprocessing.Pool.map()` with identical syntax.

### Best Practices
- SCOOP is especially popular for evolutionary algorithms (DEAP framework) where genetic populations must be evaluated across distributed workstations.
- Work stealing in SCOOP automatically balances workloads across fast and slow machines in heterogeneous clusters.

---

## Exercise 4: Remote Method Invocation with Pyro4

**Topics:** Pyro4, Remote objects, `@Pyro4.expose`, Name Server, remote proxies

### Problem Statement

Write a distributed client-server application `ex04_pyro_math.py` using Python Remote Objects (Pyro4):

1. **The Server Class:**
   - Define a class `MatrixService`:
     ```python
     import Pyro4
     @Pyro4.expose
     class MatrixService:
         def matrix_multiply(self, A, B):
             # Perform matrix multiplication
             return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

         def get_host_info(self):
             return {"os": os.name, "pid": os.getpid()}
     ```

2. **Publishing the Service:**
   - Register `MatrixService` with the Pyro Daemon.
   - Publish it to the Pyro Name Server under the name `"scientific.matrix"`.

3. **The Client:**
   - Connect to the remote service using `Pyro4.Proxy("PYRONAME:scientific.matrix")`.
   - Call `matrix_multiply()` with two $3 \times 3$ matrices as if the object were local!
   - Print the returned result and verify its accuracy.

### Hints & Guidelines
- Pyro4 handles all socket serialization and deserialization transparently.
- In simulated environments without Pyro4, implement the Proxy pattern using standard Python dynamic attribute delegation (`__getattr__`).

### Best Practices
- Always decorate classes or methods with `@Pyro4.expose` to prevent unauthorized remote execution of sensitive functions.
- Handle `Pyro4.errors.CommunicationError` in client applications to detect network disconnections.

---

## Exercise 5: Channel-Based Concurrency with CSP

**Topics:** Communicating Sequential Processes (CSP), channels, lock-free communication

### Problem Statement

Write a script `ex05_csp_pipeline.py` demonstrating the Communicating Sequential Processes concurrency model:

1. Implement a `Channel` class:
   - Uses an internal thread-safe queue.
   - Provides non-blocking/blocking `.write(value)` and `.read()` methods.

2. Build a three-stage sequential process pipeline:
   - **Data Generator Process:** Emits 10 sensor reading packets into `channel_1`.
   - **Analytics Process:** Reads packets from `channel_1`, converts temperatures from Celsius to Fahrenheit, and writes to `channel_2`.
   - **Alert Monitor Process:** Reads from `channel_2` and flags any readings exceeding a predefined safety threshold.

3. Run all three processes concurrently.
4. Verify that the processes **share no global variables and use no locks**, communicating exclusively via channel operations.

### Hints & Guidelines
- Send a sentinel value (e.g., `None` or a special `StopIteration` object) through each channel to signal completion.
- Notice how CSP simplifies reasoning about parallel code: each process is pure sequential code!

### Best Practices
- *"Do not communicate by sharing memory; instead, share memory by communicating."*
- Bounded channels apply backpressure automatically: fast producers will pause if slow consumers fall behind.
