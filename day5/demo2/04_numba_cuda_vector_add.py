"""
Example 04: Pure Python GPU Kernels with Numba (@cuda.jit)
Topic: Numba CUDA JIT Compilation, cuda.grid(1), [blocks, threads]
"""

import numpy as np
from numba import cuda


# 1. Define GPU kernel in pure Python syntax
@cuda.jit
def vector_add(a, b, c):
    # cuda.grid(1) automatically computes global thread index:
    # blockDim.x * blockIdx.x + threadIdx.x
    idx = cuda.grid(1)
    if idx < c.size:
        c[idx] = a[idx] + b[idx]


N = 100_000

# 2. Prepare data on Host (CPU)
a = np.ones(N, dtype=np.float32) * 10.0
b = np.ones(N, dtype=np.float32) * 25.0
c = np.empty_like(a)

# 3. Copy data to Device (GPU)
d_a = cuda.to_device(a)
d_b = cuda.to_device(b)
d_c = cuda.device_array_like(a)

# 4. Configure execution grid
threads_per_block = 256
blocks_per_grid = (N + (threads_per_block - 1)) // threads_per_block

# 5. Launch kernel
vector_add[blocks_per_grid, threads_per_block](d_a, d_b, d_c)

# 6. Copy result back to CPU
c = d_c.copy_to_host()

print("Executed on GPU via Numba @cuda.jit!")
print(f"Sample outputs: c[0] = {c[0]}, c[-1] = {c[-1]}")
assert np.allclose(c, a + b), "Verification failed!"
print("Verification: 10.0 + 25.0 = 35.0 -> Passed! ✓")
