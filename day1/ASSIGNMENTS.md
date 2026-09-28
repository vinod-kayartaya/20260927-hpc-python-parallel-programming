# Day 1: Lab Exercises — Foundations of Parallel Computing & Concurrency

> **Duration:** 4 hours (self-paced hands-on practice)  
> **Reference:** [`day1/README.md`](./README.md) and [`day1/demo/`](./demo/) programs  
> **Note:** These exercises are for personal practice to reinforce the concepts covered today. Start from Exercise 1 and work sequentially.

---

## Exercise 1: Configuration Management & Object Serialization (JSON & Pickle)

**Topics:** `json` module, `pickle` module, custom classes, serialization trade-offs

### Problem Statement

Write a Python script `ex01_serialization.py` that demonstrates both JSON and Pickle serialization for a parallel computing workflow:

1. **Part A (JSON Configuration):**
   - Create a dictionary representing job configuration parameters:
     ```python
     config = {
         "job_id": 101,
         "benchmark_name": "matrix_factorization",
         "num_workers": 4,
         "chunk_size": 2500,
         "tolerance": 1e-5,
         "active": True,
         "nodes": ["node-01", "node-02", "node-03", "node-04"]
     }
     ```
   - Serialize and save this configuration to `job_config.json` with an indentation of 4 spaces.
   - Read the configuration back from disk, update `"num_workers"` to 8, and write it back.

2. **Part B (Pickling Custom State):**
   - Define a class `ComputationTask`:
     ```python
     class ComputationTask:
         def __init__(self, task_id, matrix_dim):
             self.task_id = task_id
             self.matrix_dim = matrix_dim
             self.completed = False
             self.result_checksum = None

         def mark_done(self, checksum):
             self.completed = True
             self.result_checksum = checksum
     ```
   - Create 3 instances of `ComputationTask`, mark the first one as completed, and serialize all three into a binary file `tasks.pkl` using `pickle.dump()`.
   - Read the file back with `pickle.load()` and verify that the restored objects retain their exact class types, internal states, and method access.

### Hints & Guidelines
- Use context managers (`with open(...) as f:`) for all file operations.
- Open JSON files with mode `"w"` / `"r"` (text mode).
- Open Pickle files with mode `"wb"` / `"rb"` (binary mode).
- Notice that while JSON fails on custom class instances, Pickle serializes them seamlessly.

### Best Practices
- Never unpickle data received over an untrusted network connection.
- Use `json.dump()` with `indent=4` for human-readable configuration files.
- Always clean up temporary files using `os.remove()` when tests complete.

---

## Exercise 2: Data Parallelism with `multiprocessing.Pool`

**Topics:** `multiprocessing.Pool`, `pool.map()`, process isolation, speedup measurement

### Problem Statement

Write a script `ex02_parallel_primes.py` that compares sequential execution against parallel execution using a process pool:

1. Write a CPU-intensive worker function `count_primes_in_range(start, end)`:
   - Checks every odd number between `start` and `end` for primality using trial division.
   - Returns the total count of prime numbers found in that interval.

2. Create a list of 8 intervals of size 100,000 (e.g., `(1, 100000)`, `(100001, 200000)`, ..., `(700001, 800000)`).

3. **Sequential Run:**
   - Execute the 8 intervals sequentially in a standard `for` loop.
   - Record the start and end time using `time.perf_counter()`.

4. **Parallel Run:**
   - Use `multiprocessing.Pool()` to distribute the intervals across available CPU cores using `pool.starmap()`.
   - Record the elapsed time.

5. Compare the results:
   - Assert that the total prime count matches between sequential and parallel runs.
   - Calculate and print the Speedup ($S = T_{\text{seq}} / T_{\text{par}}$).

### Hints & Guidelines
- Use `multiprocessing.Pool.starmap()` when passing multiple arguments (tuples of `(start, end)`) to worker functions.
- Ensure `count_primes_in_range` is defined at the **module level** (not nested inside a function).
- Guard the execution entry point with `if __name__ == '__main__':`.

### Best Practices
- Parallelism has process creation overhead. Workloads must take at least 1–2 seconds total for parallel speedup to become visible.
- Always use `with multiprocessing.Pool() as pool:` to ensure worker processes terminate cleanly.

---

## Exercise 3: Multithreading & Shared Memory

**Topics:** `threading.Thread`, shared process memory, thread identifiers (`get_ident`)

### Problem Statement

Write a script `ex03_threaded_accumulator.py` that demonstrates how threads share memory within a single process:

1. Create a shared list `accumulator = []`.
2. Define a function `worker_task(thread_name, numbers_subset)`:
   - For each number in the subset, compute its cube ($n^3$).
   - Append a tuple `(thread_name, n, n**3)` to the shared `accumulator` list.
   - Print the thread's name, PID (`os.getpid()`), and thread ID (`threading.get_ident()`).

3. Split the numbers from 1 to 20 into 4 non-overlapping subsets:
   - Subset 1: 1 to 5
   - Subset 2: 6 to 10
   - Subset 3: 11 to 15
   - Subset 4: 16 to 20

4. Launch 4 threads, one for each subset. Start all threads, wait for them to finish with `.join()`, and print the final contents of `accumulator`.

### Hints & Guidelines
- Notice that all 4 threads share the exact same Process ID (PID), but have unique Thread Identifiers (TID).
- Because all threads share the process heap, they can append directly to `accumulator` without any inter-process communication.

### Best Practices
- While `list.append()` happens to be thread-safe in CPython due to the GIL, modifying shared complex objects across threads should always be synchronized using locks when multiple mutations occur.
- Never read final results from shared containers before calling `.join()` on all worker threads.

---

## Exercise 4: The GIL & Race Condition Detector

**Topics:** Global Interpreter Lock (GIL), CPU vs I/O bound tasks, race conditions, `threading.Lock`

### Problem Statement

Write a script `ex04_gil_and_locks.py` to examine the limits of threads and learn how to resolve race conditions:

1. **Part A (GIL Observation):**
   - Implement a CPU-bound function `compute_squares(n)` and an I/O-bound function `simulate_io(duration)`.
   - Run 4 iterations of each task sequentially, then with 4 threads.
   - Observe that threads provide no speedup for `compute_squares` (due to the GIL), but provide near $4\times$ speedup for `simulate_io`.

2. **Part B (Race Condition & Lock Fix):**
   - Create a shared counter `balance = 1000`.
   - Write a function `unsafe_withdraw(amount, times)` where each loop iteration reads `balance`, introduces a tiny delay (`time.sleep(0.0001)`), and writes `balance - amount`.
   - Run 5 threads withdrawing 100 times. Observe the final corrupted balance.
   - Fix the function by protecting the withdrawal logic with a `threading.Lock` using `with lock:`. Verify that the final balance is exactly $1000 - (5 \times 100) = 500$.

### Hints & Guidelines
- The `time.sleep(0.0001)` call widens the critical section window, forcing CPython to switch thread contexts between the read and write operations.
- Using `with lock:` ensures the lock is always released even if an exception occurs inside the critical section.

### Best Practices
- Keep critical sections (code enclosed by a Lock) as small and fast as possible to minimize thread contention.
- Never use threads for pure CPU-intensive Python calculations—use `multiprocessing` instead.

---

## Exercise 5: Parallel Speedup & Amdahl's Law Analyzer

**Topics:** Performance metrics, Speedup ($S$), Efficiency ($E$), Amdahl's Law, Gustafson's Law

### Problem Statement

Write a performance benchmarking tool `ex05_amdahl_analyzer.py` that evaluates parallel scaling:

1. Implement a CPU-bound workload:
   ```python
   def cpu_workload(iterations):
       return sum(i * i for i in range(iterations))
   ```

2. Establish a sequential baseline:
   - Measure the sequential time ($T_{\text{seq}}$) to compute 8,000,000 iterations.

3. Benchmark parallel execution across varying worker counts:
   - Test worker counts: $N = [1, 2, 4, 8]$ (or up to your machine's CPU core count).
   - Divide the 8,000,000 iterations evenly among $N$ workers using `multiprocessing.Pool(N).map()`.
   - Measure the parallel time ($T_{\text{par}}(N)$).

4. Calculate and display a formatted metrics table:
   - **Speedup**: $S(N) = \frac{T_{\text{seq}}}{T_{\text{par}}(N)}$
   - **Efficiency**: $E(N) = \frac{S(N)}{N} \times 100\%$
   - **Amdahl's Theoretical Speedup** (assume a 5% serial fraction $s = 0.05$):
     $$\text{Amdahl}(N) = \frac{1}{s + \frac{1 - s}{N}}$$
   - **Gustafson's Scaled Speedup**:
     $$\text{Gustafson}(N) = N - s \times (N - 1)$$

### Hints & Guidelines
- Use `multiprocessing.cpu_count()` to dynamically discover the number of logical cores on your machine.
- Format tabular outputs cleanly with header underlines and right-aligned numbers.

### Best Practices
- Run each test 3 times and take the average to eliminate noise caused by background operating system tasks.
- If $E(N) < 50\%$, communication overhead and process startup costs are dominating your workload.
