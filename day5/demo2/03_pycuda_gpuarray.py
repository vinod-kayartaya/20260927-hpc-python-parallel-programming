"""
Example 03: High-Level PyCUDA with GPUArray
Topic: pycuda.gpuarray (NumPy-like syntax directly in GPU VRAM)
"""

try:
    import numpy as np
    import pycuda.autoinit
    import pycuda.gpuarray as gpuarray
    PYCUDA_AVAILABLE = True
except (ImportError, Exception):
    PYCUDA_AVAILABLE = False


def main():
    N = 100_000

    if PYCUDA_AVAILABLE:
        # Create CPU arrays
        a_cpu = np.arange(N, dtype=np.float32)
        b_cpu = np.arange(N, dtype=np.float32) * 3.0

        # Transfer to GPU in one step:
        a_gpu = gpuarray.to_gpu(a_cpu)
        b_gpu = gpuarray.to_gpu(b_cpu)

        # Vector arithmetic automatically executes as parallel CUDA kernels on GPU:
        c_gpu = 2.0 * a_gpu + b_gpu

        # Transfer result back to CPU:
        c_cpu = c_gpu.get()
        print(f"Executed on GPU using GPUArray across {N:,} elements!")
    else:
        print("[Simulated Execution — PyCUDA / GPU not present]")
        a_cpu = [float(i) for i in range(5)]
        b_cpu = [float(i * 3.0) for i in range(5)]
        c_cpu = [2.0 * a + b for a, b in zip(a_cpu, b_cpu)]

    print(f"Result (first 5 elements): {c_cpu[:5]}")
    print("Notice: No manual mem_alloc, pointer math, or C kernel strings required!")


if __name__ == '__main__':
    main()
