"""
Demo 02: High-Level PyCUDA — GPUArray, ElementwiseKernel & MapReduce
====================================================================

Demonstrates high-level abstractions in PyCUDA:
    - GPUArray: NumPy-like ndarray living entirely in GPU memory
    - ElementwiseKernel: Writing one-line parallel expressions without boilerplate C
    - ReductionKernel: GPU-accelerated MapReduce (Sum, Min, Dot Product)

Run instructions:
    Requires an NVIDIA GPU with PyCUDA and NumPy installed.
    Otherwise, executes an architectural simulation demonstrating the concepts.
"""

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import pycuda.autoinit
    import pycuda.gpuarray as gpuarray
    from pycuda.elementwise import ElementwiseKernel
    from pycuda.reduction import ReductionKernel
    PYCUDA_AVAILABLE = True
except (ImportError, Exception):
    PYCUDA_AVAILABLE = False


# ===================================================================
# 1. GPUArray: NumPy on the GPU
# ===================================================================

def demo_gpuarray_vector_ops():
    """
    Demonstrates pycuda.gpuarray:
    Instead of manual mem_alloc and memcpy, GPUArray behaves like a NumPy array
    where every arithmetic operation (+, -, *, sin, cos) automatically executes
    as a parallel CUDA kernel on the GPU!
    """
    print("=" * 60)
    print("PyCUDA GPUArray: NumPy-like Syntax on the GPU")
    print("=" * 60)

    N = 1_000_000

    if PYCUDA_AVAILABLE and NUMPY_AVAILABLE:
        a_host = np.linspace(0, 10, N, dtype=np.float32)
        b_host = np.linspace(10, 20, N, dtype=np.float32)

        # Transfer NumPy array to GPU memory in one call:
        a_gpu = gpuarray.to_gpu(a_host)
        b_gpu = gpuarray.to_gpu(b_host)

        # Automatic parallel GPU kernel launch:
        c_gpu = 2.0 * a_gpu + b_gpu ** 2

        # Fetch result back to Host RAM:
        c_host = c_gpu.get()
        print(f"Calculated 2*a + b^2 for {N:,} elements directly on GPU!")
    else:
        print("[Simulated Mode — PyCUDA / NumPy not installed]")
        print("GPUArray Architecture:")
        print("  1. a_gpu = gpuarray.to_gpu(a_host)   # Allocates & copies in 1 step")
        print("  2. c_gpu = 2.0 * a_gpu + b_gpu ** 2  # Launches optimized CUDA kernel")
        print("  3. c_host = c_gpu.get()              # Transfers back to CPU NumPy array")
        print()
        a_host = [float(i * 10 / N) for i in range(5)]
        b_host = [float(10 + i * 10 / N) for i in range(5)]
        c_host = [2.0 * a + (b ** 2) for a, b in zip(a_host, b_host)]

    print(f"Result (first 5 elements): {c_host[:5]}\n")


# ===================================================================
# 2. ElementwiseKernel: Custom Fast Expressions
# ===================================================================

def demo_elementwise_kernel():
    """
    Demonstrates ElementwiseKernel:
    Generates, compiles, and caches an optimized CUDA kernel from a single C expression.
    No need to write grid/block loops or threadIdx math!
    """
    print("=" * 60)
    print("PyCUDA ElementwiseKernel: Inline Expressions")
    print("=" * 60)

    print("Pattern:")
    print('  linear_comb = ElementwiseKernel(')
    print('      "float a, float *x, float *y, float *z",')
    print('      "z[i] = a * x[i] + y[i]",')
    print('      "saxpy_kernel"')
    print('  )')
    print('  linear_comb(2.5, x_gpu, y_gpu, z_gpu)')
    print()
    print("PyCUDA dynamically compiles the C expression and executes it across all GPU cores.\n")


# ===================================================================
# 3. GPU MapReduce (ReductionKernel)
# ===================================================================

def demo_map_reduce_gpu():
    """
    Demonstrates ReductionKernel:
    Performs high-performance parallel reductions on the GPU (e.g. Dot Product, Sum).
    """
    print("=" * 60)
    print("GPU MapReduce with ReductionKernel")
    print("=" * 60)

    print("Pattern for Vector Dot Product (sum(x[i] * y[i])):")
    print('  dot_prod = ReductionKernel(')
    print('      np.float32,')
    print('      neutral="0",')
    print('      reduce_expr="a + b",')
    print('      map_expr="x[i] * y[i]",')
    print('      arguments="float *x, float *y"')
    print('  )')
    print()
    print("The GPU computes the Map step (multiplication) in parallel across thousands of cores,")
    print("then performs a parallel tree Reduction (addition) down to a single scalar result.\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_gpuarray_vector_ops()
    # demo_elementwise_kernel()
    # demo_map_reduce_gpu()


if __name__ == "__main__":
    main()
