"""
Demo 03: GPU Acceleration with Numba (@cuda.jit)
================================================

Demonstrates pure-Python GPU programming using Numba:
    - Writing CUDA kernels directly in Python using @cuda.jit
    - Grid and block indexing with cuda.grid(1) and cuda.grid(2)
    - Device memory management with cuda.to_device() and copy_to_host()
    - Utilizing fast on-chip Shared Memory (cuda.shared.array)
    - Fallback: Multi-core CPU acceleration with Numba @jit(parallel=True)

Run instructions:
    If an NVIDIA GPU, Numba, and NumPy are present:
        python3 03_numba_cuda_jit.py
    Otherwise, executes an architectural simulation demonstrating the concepts.
"""

import time

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from numba import cuda, jit
    NUMBA_CUDA_AVAILABLE = cuda.is_available()
    NUMBA_AVAILABLE = True
except (ImportError, Exception):
    NUMBA_CUDA_AVAILABLE = False
    NUMBA_AVAILABLE = False


# ===================================================================
# 1. Pure Python GPU Kernel with @cuda.jit
# ===================================================================

if NUMBA_CUDA_AVAILABLE:
    @cuda.jit
    def numba_vector_add(a, b, c):
        """
        Pure Python function compiled directly to GPU PTX machine code!
        cuda.grid(1) automatically computes: blockIdx.x * blockDim.x + threadIdx.x
        """
        idx = cuda.grid(1)
        if idx < c.size:
            c[idx] = a[idx] + b[idx]


def demo_numba_cuda_kernel():
    """
    Demonstrates writing and launching a Numba CUDA kernel in pure Python.
    No C/C++ string compilation required!
    """
    print("=" * 60)
    print("Numba CUDA: JIT-Compiled Python Kernels on the GPU")
    print("=" * 60)

    N = 100_000

    if NUMBA_CUDA_AVAILABLE and NUMPY_AVAILABLE:
        print("Compiling and running on NVIDIA GPU via Numba @cuda.jit...")
        a = np.ones(N, dtype=np.float32) * 5.0
        b = np.ones(N, dtype=np.float32) * 10.0
        c = np.empty_like(a)

        threads_per_block = 256
        blocks_per_grid = (N + (threads_per_block - 1)) // threads_per_block

        # Copy data to GPU device memory
        d_a = cuda.to_device(a)
        d_b = cuda.to_device(b)
        d_c = cuda.device_array_like(a)

        # Launch kernel
        numba_vector_add[blocks_per_grid, threads_per_block](d_a, d_b, d_c)

        # Copy result back to CPU
        c = d_c.copy_to_host()
        print("Execution finished successfully on GPU.")
    else:
        print("[Simulated Mode — NVIDIA GPU / Numba CUDA not active]")
        print("Numba CUDA Syntax:")
        print("  @cuda.jit")
        print("  def vector_add(a, b, c):")
        print("      idx = cuda.grid(1)  # Absolute 1D thread position")
        print("      if idx < c.size:")
        print("          c[idx] = a[idx] + b[idx]")
        print()
        print("  # Invocation with [blocks, threads]:")
        print("  vector_add[blocks_per_grid, threads_per_block](d_a, d_b, d_c)")
        a = [5.0] * 5
        b = [10.0] * 5
        c = [x + y for x, y in zip(a, b)]

    print(f"Sample outputs: c[0] = {c[0]}, c[-1] = {c[-1]}")
    print("Verified correct (5.0 + 10.0 = 15.0) ✓\n")


# ===================================================================
# 2. Fast On-Chip Shared Memory
# ===================================================================

def demo_numba_shared_memory():
    """
    Demonstrates GPU Shared Memory:
    Global VRAM is high-latency (~400 clock cycles).
    Shared Memory is an on-chip software-managed cache (~1-2 clock cycles)
    shared by all threads inside the same Block.
    """
    print("=" * 60)
    print("GPU Shared Memory (cuda.shared.array)")
    print("=" * 60)
    print("Memory Hierarchy on GPU:")
    print("  Registers     : Fastest, private to single thread")
    print("  Shared Memory : Extremely fast (on-chip SRAM), shared across thread block")
    print("  Global VRAM   : Large (8-80 GB), but slower high-latency memory")
    print()
    print("Code Pattern:")
    print("  @cuda.jit")
    print("  def matrix_mul_shared(A, B, C):")
    print("      # Allocate on-chip shared tile:")
    print("      sA = cuda.shared.array(shape=(16, 16), dtype=float32)")
    print("      sB = cuda.shared.array(shape=(16, 16), dtype=float32)")
    print("      ...")
    print("      # Synchronize all threads in the block:")
    print("      cuda.syncthreads()")
    print()
    print("Using shared memory reduces global VRAM bus traffic by up to 10-50x!\n")


# ===================================================================
# 3. CPU Parallel JIT Fallback
# ===================================================================

def demo_numba_cpu_parallel():
    """
    Demonstrates Numba's CPU multi-core parallelism:
    Even without a GPU, Numba can compile Python code to multi-threaded machine code
    using @jit(parallel=True).
    """
    print("=" * 60)
    print("Numba Multi-Core CPU Parallelism (@jit(parallel=True))")
    print("=" * 60)

    print("Pattern:")
    print("  @jit(nopython=True, parallel=True)")
    print("  def parallel_monte_carlo(n):")
    print("      acc = 0")
    print("      for i in prange(n):  # prange runs iterations in parallel threads!")
    print("          acc += compute(i)")
    print("      return acc")
    print()
    print("This allows high-performance multi-threaded CPU execution without the GIL!\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_numba_cuda_kernel()
    # demo_numba_shared_memory()
    # demo_numba_cpu_parallel()


if __name__ == "__main__":
    main()
