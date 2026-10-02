"""
Example 02: PyCUDA Vector Addition (Explicit Memory & Kernel)
Topic: SourceModule, cuda.mem_alloc, memcpy_htod, memcpy_dtoh
"""

import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

N = 1024  # Size of vectors

# 1. Define CUDA C Kernel
kernel_code = """
__global__ void vector_add(float *c, const float *a, const float *b, int n) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
"""

# 2. Prepare Host (CPU) Data
a_host = np.arange(N, dtype=np.float32)
b_host = np.arange(N, dtype=np.float32) * 2.0
c_host = np.empty_like(a_host)

# 3. Compile Kernel with SourceModule
mod = SourceModule(kernel_code)
vector_add = mod.get_function("vector_add")

# 4. Allocate Device (GPU) Memory
a_gpu = cuda.mem_alloc(a_host.nbytes)
b_gpu = cuda.mem_alloc(b_host.nbytes)
c_gpu = cuda.mem_alloc(c_host.nbytes)

# 5. Copy Data: Host -> Device
cuda.memcpy_htod(a_gpu, a_host)
cuda.memcpy_htod(b_gpu, b_host)

# 6. Launch Kernel (block = 256 threads, grid = N/256 blocks)
block_size = 256
grid_size = (N + block_size - 1) // block_size
vector_add(c_gpu, a_gpu, b_gpu, np.int32(N), block=(block_size, 1, 1), grid=(grid_size, 1))

# 7. Copy Result: Device -> Host
cuda.memcpy_dtoh(c_host, c_gpu)

print("Kernel executed successfully on NVIDIA GPU!")
print(f"Sample Input  a (first 5) : {a_host[:5]}")
print(f"Sample Input  b (first 5) : {b_host[:5]}")
print(f"Sample Output c (first 5) : {c_host[:5]}")
assert np.allclose(c_host, a_host + b_host), "Verification failed!"
print("Verification: c[i] == a[i] + b[i] -> Passed! ✓")
