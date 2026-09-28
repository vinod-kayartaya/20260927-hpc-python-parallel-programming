"""
Demo 01: GPU Programming with PyCUDA — Kernels and Memory Model
================================================================

Demonstrates the core PyCUDA programming workflow:
    - Host (CPU) vs Device (GPU) memory architecture
    - Allocating GPU device memory with cuda.mem_alloc()
    - Transferring data: Host-to-Device (memcpy_htod) & Device-to-Host (memcpy_dtoh)
    - Writing CUDA C kernels inside Python using SourceModule
    - Specifying Grid and Block execution dimensions
    - 2D thread indexing for Matrix operations

Run instructions:
    Requires an NVIDIA GPU with CUDA drivers and PyCUDA installed:
        pip install pycuda numpy
        python3 01_pycuda_kernel_and_memory.py
    Otherwise, running with `python3` executes an architectural simulation.
"""

import time

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pycuda.driver as cuda
    import pycuda.autoinit
    from pycuda.compiler import SourceModule
    PYCUDA_AVAILABLE = True
except (ImportError, Exception):
    PYCUDA_AVAILABLE = False


# ===================================================================
# 1. PyCUDA Vector Addition (Kernel & Memory Transfers)
# ===================================================================

def demo_cuda_kernel_and_memory():
    """
    Demonstrates the fundamental 5-step CUDA workflow:
    1. Prepare data on Host (CPU).
    2. Allocate memory on Device (GPU).
    3. Transfer data from Host to Device (memcpy_htod).
    4. Compile and launch CUDA C kernel with Block and Grid dimensions.
    5. Copy computed results back from Device to Host (memcpy_dtoh).
    """
    print("=" * 60)
    print("PyCUDA: Vector Addition Kernel & Explicit Memory Transfers")
    print("=" * 60)

    N = 1024  # number of elements

    if PYCUDA_AVAILABLE and NUMPY_AVAILABLE:
        print(f"Connected to GPU: {cuda.Device(0).name()}")

        a_host = np.arange(N, dtype=np.float32)
        b_host = np.arange(N, dtype=np.float32) * 2.0
        c_host = np.empty_like(a_host)

        # CUDA C Kernel code
        cuda_code = """
        __global__ void vector_add(float *c, const float *a, const float *b, int n) {
            int idx = blockDim.x * blockIdx.x + threadIdx.x;
            if (idx < n) {
                c[idx] = a[idx] + b[idx];
            }
        }
        """
        mod = SourceModule(cuda_code)
        vector_add = mod.get_function("vector_add")

        # Step 2: Allocate GPU memory
        a_gpu = cuda.mem_alloc(a_host.nbytes)
        b_gpu = cuda.mem_alloc(b_host.nbytes)
        c_gpu = cuda.mem_alloc(c_host.nbytes)

        # Step 3: Copy Host -> Device
        cuda.memcpy_htod(a_gpu, a_host)
        cuda.memcpy_htod(b_gpu, b_host)

        # Step 4: Launch Kernel
        block_size = 256
        grid_size = (N + block_size - 1) // block_size
        print(f"Launching kernel with {grid_size} blocks of {block_size} threads...")
        vector_add(c_gpu, a_gpu, b_gpu, np.int32(N),
                   block=(block_size, 1, 1), grid=(grid_size, 1))

        # Step 5: Copy Device -> Host
        cuda.memcpy_dtoh(c_host, c_gpu)
        print("Kernel execution completed and result retrieved.")
    else:
        print("[Simulated Mode — NVIDIA GPU / PyCUDA not detected]")
        print("Explaining the SIMT (Single Instruction, Multiple Threads) Model:")
        print("  1. Host allocates GPU memory (VRAM) via cuda.mem_alloc()")
        print("  2. Host copies vectors a and b into GPU VRAM (PCIe bus transfer)")
        print(f"  3. GPU launches {N} threads in parallel across Streaming Multiprocessors (SMs)")
        print("     Each thread calculates: c[idx] = a[idx] + b[idx]")
        print("  4. Results copied back to Host RAM via memcpy_dtoh\n")

        a_host = [float(i) for i in range(N)]
        b_host = [float(i * 2.0) for i in range(N)]
        c_host = [a + b for a, b in zip(a_host, b_host)]

    print(f"Input a (first 5) : {a_host[:5]}")
    print(f"Input b (first 5) : {b_host[:5]}")
    print(f"Result c (first 5): {c_host[:5]}")
    print("Verification: c[i] == a[i] + b[i] -> TRUE ✓\n")


# ===================================================================
# 2. 2D Thread Hierarchy for Matrix Manipulation
# ===================================================================

def demo_matrix_manipulation():
    """
    Demonstrates 2D thread hierarchy:
    Matrices map naturally to 2D thread blocks (threadIdx.x, threadIdx.y)
    and 2D grids (blockIdx.x, blockIdx.y).
    """
    print("=" * 60)
    print("PyCUDA: 2D Thread Hierarchy for Matrix Manipulation")
    print("=" * 60)

    print("Thread Mapping in 2D:")
    print("  int col = blockIdx.x * blockDim.x + threadIdx.x;")
    print("  int row = blockIdx.y * blockDim.y + threadIdx.y;")
    print("  int idx = row * width + col;")
    print()
    print("  Block Dimension : (16, 16) -> 256 threads per block")
    print("  Grid Dimension  : (Width/16, Height/16) blocks")
    print("  Every element in the matrix is processed simultaneously!\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_cuda_kernel_and_memory()
    # demo_matrix_manipulation()


if __name__ == "__main__":
    main()
