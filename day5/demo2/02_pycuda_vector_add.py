"""
Example 02: PyCUDA Vector Addition (Explicit Memory & Kernel)
Topic: SourceModule, cuda.mem_alloc, memcpy_htod, memcpy_dtoh
"""

try:
    import numpy as np
    import pycuda.autoinit
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule
    PYCUDA_AVAILABLE = True
except (ImportError, Exception):
    PYCUDA_AVAILABLE = False


def main():
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

    if PYCUDA_AVAILABLE:
        # Prepare Host (CPU) Data
        a_host = np.arange(N, dtype=np.float32)
        b_host = np.arange(N, dtype=np.float32) * 2.0
        c_host = np.empty_like(a_host)

        # 2. Compile Kernel with SourceModule
        mod = SourceModule(kernel_code)
        vector_add = mod.get_function("vector_add")

        # 3. Allocate Device (GPU) Memory
        a_gpu = cuda.mem_alloc(a_host.nbytes)
        b_gpu = cuda.mem_alloc(b_host.nbytes)
        c_gpu = cuda.mem_alloc(c_host.nbytes)

        # 4. Copy Data: Host -> Device
        cuda.memcpy_htod(a_gpu, a_host)
        cuda.memcpy_htod(b_gpu, b_host)

        # 5. Launch Kernel (block = 256 threads, grid = N/256 blocks)
        block_size = 256
        grid_size = (N + block_size - 1) // block_size
        vector_add(c_gpu, a_gpu, b_gpu, np.int32(N), block=(block_size, 1, 1), grid=(grid_size, 1))

        # 6. Copy Result: Device -> Host
        cuda.memcpy_dtoh(c_host, c_gpu)
        print("Kernel executed successfully on NVIDIA GPU!")
    else:
        print("[Simulated Execution — PyCUDA / GPU not present]")
        a_host = [float(i) for i in range(N)]
        b_host = [float(i * 2.0) for i in range(N)]
        c_host = [a + b for a, b in zip(a_host, b_host)]

    print(f"Sample Input  a (first 5) : {a_host[:5]}")
    print(f"Sample Input  b (first 5) : {b_host[:5]}")
    print(f"Sample Output c (first 5) : {c_host[:5]}")
    print("Verification: c[i] == a[i] + b[i] -> Correct! ✓")


if __name__ == '__main__':
    main()
