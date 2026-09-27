"""
Demo 09: Evaluating Performance — Speedup, Efficiency & Amdahl's Law
======================================================================

Demonstrates how to measure and evaluate parallel performance using:
    - Speedup       = T_sequential / T_parallel
    - Efficiency    = Speedup / N   (where N = number of workers)
    - Amdahl's Law  = 1 / (S + (1 - S) / N)
      where S is the serial fraction of the program.

Experiment:
    We run a CPU-bound workload with varying numbers of worker processes
    (1, 2, 4, ..., max cores), measure actual speedup/efficiency,
    and compare against the theoretical Amdahl's Law upper bound.
"""

import multiprocessing
import time


# ---------------------------------------------------------------------------
# Worker functions — must be at module level for macOS/Windows 'spawn' method
# ---------------------------------------------------------------------------

def cpu_work(iterations):
    """Pure CPU work: sum of squares."""
    total = 0
    for i in range(iterations):
        total += i * i
    return total


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parallel_workload(num_workers, total_iterations):
    """
    Run the workload across `num_workers` processes.

    The total work is divided equally among workers.
    """
    chunk_size = total_iterations // num_workers

    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(cpu_work, [chunk_size] * num_workers)

    return sum(results)


def amdahl_speedup(serial_fraction, num_processors):
    """
    Calculate theoretical maximum speedup using Amdahl's Law.

    Parameters:
        serial_fraction  : fraction of work that is strictly serial (0 to 1)
        num_processors   : number of parallel processors

    Returns:
        Theoretical speedup bound.

    Formula:
        Speedup = 1 / (S + (1 - S) / N)
    """
    return 1.0 / (serial_fraction + (1.0 - serial_fraction) / num_processors)


def get_worker_counts(max_cores):
    """Build list of worker counts to test: 1, 2, 4, ... up to max_cores."""
    worker_counts = []
    n = 1
    while n <= max_cores:
        worker_counts.append(n)
        n *= 2
    if worker_counts[-1] != max_cores:
        worker_counts.append(max_cores)
    return worker_counts


# ---------------------------------------------------------------------------
# Demo functions
# ---------------------------------------------------------------------------

def demo_speedup_efficiency():
    """Measure actual Speedup and Efficiency across varying core counts."""
    TOTAL_ITERATIONS = 10_000_000
    max_cores = multiprocessing.cpu_count()
    worker_counts = get_worker_counts(max_cores)

    print("Performance Benchmark: Speedup & Efficiency")
    print(f"Total work     : {TOTAL_ITERATIONS:,} iterations")
    print(f"Available cores: {max_cores}")
    print()

    # --- Sequential baseline ---
    start = time.time()
    cpu_work(TOTAL_ITERATIONS)
    t_sequential = time.time() - start
    print(f"Sequential time: {t_sequential:.3f}s")
    print()

    # --- Parallel runs ---
    header = f"{'Workers':>8} {'Time(s)':>8} {'Speedup':>8} {'Efficiency':>10}"
    print(header)
    print("─" * len(header))

    for num_workers in worker_counts:
        start = time.time()
        parallel_workload(num_workers, TOTAL_ITERATIONS)
        t_parallel = time.time() - start

        speedup = t_sequential / t_parallel
        efficiency = speedup / num_workers

        print(f"{num_workers:>8} {t_parallel:>8.3f} {speedup:>8.2f} "
              f"{efficiency:>10.1%}")

    print()
    print("KEY DEFINITIONS:")
    print(f"  Speedup(N)    = T_seq / T_par(N)")
    print(f"  Efficiency(N) = Speedup(N) / N        (ideal = 100%)")


def demo_amdahls_law():
    """Compare actual speedup against Amdahl's Law theoretical bound."""
    TOTAL_ITERATIONS = 10_000_000
    max_cores = multiprocessing.cpu_count()
    worker_counts = get_worker_counts(max_cores)
    serial_fraction = 0.05  # assume ~5% serial overhead

    print("Amdahl's Law: Theoretical vs Actual Speedup")
    print(f"Total work      : {TOTAL_ITERATIONS:,} iterations")
    print(f"Serial fraction : {serial_fraction:.0%}")
    print(f"Max theoretical : {1.0 / serial_fraction:.1f}x (even with ∞ processors)")
    print()

    # --- Sequential baseline ---
    start = time.time()
    cpu_work(TOTAL_ITERATIONS)
    t_sequential = time.time() - start
    print(f"Sequential time : {t_sequential:.3f}s")
    print()

    # --- Parallel runs with Amdahl comparison ---
    header = f"{'Workers':>8} {'Time(s)':>8} {'Actual':>8} {'Amdahl':>8}"
    print(header)
    print("─" * len(header))

    for num_workers in worker_counts:
        start = time.time()
        parallel_workload(num_workers, TOTAL_ITERATIONS)
        t_parallel = time.time() - start

        speedup = t_sequential / t_parallel
        theoretical = amdahl_speedup(serial_fraction, num_workers)

        print(f"{num_workers:>8} {t_parallel:>8.3f} {speedup:>8.2f} "
              f"{theoretical:>8.2f}")

    print()
    print("  Amdahl's Law  = 1 / (S + (1-S)/N)     (S = serial fraction)")


def demo_gustafsons_law():
    """Show Gustafson's scaled speedup — the optimistic counterpart to Amdahl."""
    max_cores = multiprocessing.cpu_count()
    worker_counts = get_worker_counts(max_cores)
    serial_fraction = 0.05

    print("GUSTAFSON'S LAW (complementary view):")
    print("  Instead of fixing problem size, Gustafson argues that as we add")
    print("  more processors, we increase the problem size proportionally.")
    print(f"  Serial fraction: {serial_fraction:.0%}")
    print()
    print("  Scaled Speedup = N - S × (N - 1)")
    print()

    header = f"{'Workers':>8} {'Gustafson':>10}"
    print(header)
    print("─" * len(header))

    for n in worker_counts:
        gustafson = n - serial_fraction * (n - 1)
        print(f"{n:>8} {gustafson:>10.2f}")

    print()
    print("  Gustafson is more optimistic: speedup grows nearly linearly with N")
    print("  when we scale the problem size along with the processor count.")


# ---------------------------------------------------------------------------
# Main: uncomment functions one by one to demonstrate each concept
# ---------------------------------------------------------------------------

def main():
    demo_speedup_efficiency()
    # demo_amdahls_law()
    # demo_gustafsons_law()


if __name__ == "__main__":
    main()
