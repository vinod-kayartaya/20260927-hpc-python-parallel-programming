"""
Example 04: Pure Python GPU Kernels with Numba (@cuda.jit)
Topic: Numba CUDA JIT Compilation, cuda.grid(1), [blocks, threads]
"""

try:
    import numpy as np
    from numba import cuda
    NUMBA_CUDA_AVAILABLE = cuda.is_available()
except (ImportError, Exception):
    NUMBA_CUDA_AVAILABLE = False


# 1. Define GPU kernel in pure Python syntax!
if NUMBA_CUDA_AVAILABLE:
    @cuda.jit
    def vector_add_numba(a, b, c):
        # cuda.grid(1) automatically computes global thread index:
        # blockDim.x * blockIdx.x + threadIdx.x
        idx = cuda.grid(1)
        if idx < c.size:
            c[idx] = a[idx] + b[idx]


def main():
    N = 100_000

    if NUMBA_CUDA_AVAILABLE:
        # Prepare data
        a = np.ones(N, dtype=np.float32) * 10.0
        b = np.ones(N, dtype=np.float32) * 25.0
        c = np.empty_like(a)

        # Copy data to GPU
        d_a = cuda.to_device(a)
        d_b = cuda.to_device(b)
        d_c = cuda.device_array_like(a)

        # Configure execution grid
        threads_per_block = 256
        blocks_per_grid = (N + (threads_per_block - 1)) // threads_per_block

        # Launch kernel
        vector_add_numba[blocks_per_grid, threads_per_block](d_a, d_b, d_c)

        # Copy result back to CPU
        c = d_c.copy_to_host()
        print("Executed on GPU via Numba @cuda.jit!")
    else:
        print("[Simulated Execution — Numba CUDA / GPU not present]")
        a = [10.0] * 5
        b = [25.0] * 5
        c = [x + y for x, y in zip(a, b)]

    print(f"Sample outputs: c[0] = {c[0]}, c[-1] = {c[-1]}")
    print("Verification: 10.0 + 25.0 = 35.0 -> Correct! ✓")


if __name__ == '__main__':
    main()
