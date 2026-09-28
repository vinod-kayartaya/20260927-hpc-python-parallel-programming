"""
Demo 02: Scientific Computing with SCOOP (Scalable Concurrent Operations in Python)
===================================================================================

Demonstrates parallel map over heterogeneous clusters with SCOOP:
    - How SCOOP extends Python's concurrent.futures interface over network nodes (ZeroMQ)
    - Distributing scientific computation using scoop.futures.map()
    - Difference between standard multiprocessing.Pool and SCOOP on clusters

Run instructions:
    If SCOOP is installed:
        python3 -m scoop 02_scoop_scientific_map.py
        # On a multi-node cluster:
        python3 -m scoop --hostfile hosts.txt 02_scoop_scientific_map.py
    Otherwise, running with `python3` executes a self-contained demonstration.
"""

import time
import math
import multiprocessing

try:
    from scoop import futures as scoop_futures
    SCOOP_AVAILABLE = True
except ImportError:
    SCOOP_AVAILABLE = False


# ===================================================================
# Worker functions (Module level)
# ===================================================================

def monte_carlo_pi_sample(samples):
    """
    Computes a portion of Monte Carlo Pi simulation.
    Ideal for scientific computing across distributed nodes.
    """
    import random
    inside = 0
    for _ in range(samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return inside


def scientific_task(n):
    """A CPU-heavy mathematical simulation."""
    return sum(math.sin(i) * math.cos(i) for i in range(n))


# ===================================================================
# 1. SCOOP Parallel Map
# ===================================================================

def demo_scoop_map():
    """
    Demonstrates scoop.futures.map():
    Similar syntax to multiprocessing.Pool.map(), but tasks can be executed
    across different physical computers in a scientific cluster via ZeroMQ.
    """
    print("=" * 60)
    print("SCOOP: Distributed Scientific Map across Cluster Nodes")
    print("=" * 60)

    workload = [1_000_000] * 8

    if SCOOP_AVAILABLE:
        print("Running with native SCOOP runtime...")
        start = time.time()
        results = list(scoop_futures.map(monte_carlo_pi_sample, workload))
        elapsed = time.time() - start

        total_inside = sum(results)
        total_samples = sum(workload)
        pi_approx = 4.0 * total_inside / total_samples
        print(f"Approximated Pi = {pi_approx:.6f} in {elapsed:.3f}s")
    else:
        print("[Simulated Mode — SCOOP not installed]")
        print("To install SCOOP: pip install scoop")
        print("To launch on cluster: python3 -m scoop --hosts node1,node2 script.py")
        print("\nExecuting comparable workload locally with multiprocessing.Pool:")
        start = time.time()
        with multiprocessing.Pool(processes=4) as pool:
            results = pool.map(monte_carlo_pi_sample, workload)
        elapsed = time.time() - start

        total_inside = sum(results)
        total_samples = sum(workload)
        pi_approx = 4.0 * total_inside / total_samples
        print(f"  Approximated Pi = {pi_approx:.6f}")
        print(f"  Execution time  = {elapsed:.3f}s\n")


# ===================================================================
# 2. SCOOP vs Multiprocessing Architecture
# ===================================================================

def demo_scoop_architecture():
    """Explains why SCOOP is favored for scientific and genetic algorithms."""
    print("=" * 60)
    print("Multiprocessing vs SCOOP Comparison")
    print("=" * 60)
    print("┌──────────────────┬─────────────────────────┬─────────────────────────┐")
    print("│ Feature          │ multiprocessing.Pool    │ SCOOP                   │")
    print("├──────────────────┼─────────────────────────┼─────────────────────────┤")
    print("│ Scope            │ Single computer only    │ Multi-node Cluster      │")
    print("│ Transport        │ OS Pipes / Semaphores   │ ZeroMQ sockets          │")
    print("│ Scalability      │ Limited to local cores  │ Thousands of cores      │")
    print("│ Host Management  │ None (local OS)         │ SSH hostfiles, SLURM    │")
    print("│ API Syntax       │ pool.map(func, data)    │ scoop.futures.map(...)  │")
    print("└──────────────────┴─────────────────────────┴─────────────────────────┘\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_scoop_map()
    # demo_scoop_architecture()


if __name__ == "__main__":
    main()
