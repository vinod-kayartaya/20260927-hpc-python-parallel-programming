"""
Example 03: High-Level PyCUDA with GPUArray
Topic: pycuda.gpuarray (NumPy-like syntax directly in GPU VRAM)
"""

import numpy as np
import pycuda.autoinit
import pycuda.gpuarray as gpuarray

N = 100_000

# 1. Create CPU arrays
a_cpu = np.arange(N, dtype=np.float32)
b_cpu = np.arange(N, dtype=np.float32) * 3.0

# 2. Transfer directly to GPU VRAM
a_gpu = gpuarray.to_gpu(a_cpu)
b_gpu = gpuarray.to_gpu(b_cpu)

# 3. Vector arithmetic executes automatically as parallel CUDA kernel
c_gpu = 2.0 * a_gpu + b_gpu

# 4. Transfer result back to CPU
c_cpu = c_gpu.get()

print(f"Executed on GPU using GPUArray across {N:,} elements!")
print(f"Result (first 5 elements): {c_cpu[:5]}")
assert np.allclose(c_cpu, 2.0 * a_cpu + b_cpu), "Verification failed!"
print("Verification passed! ✓")
print("Notice: No manual mem_alloc, pointer math, or C kernel strings required!")
