# Day 5: GPU Programming with Python

> **Total Duration:** 4 hours (divided into two 2-hour sessions)  
> **Prerequisites:** Days 1, 2, 3, & 4 (Process parallelism, vectorization, arrays)  
> **Demos Folder:** [`day5/demo/`](./demo/)

---

## Session Overview

Day 5 unlocks massive hardware acceleration by tapping into **Graphics Processing Units (GPUs)** with thousands of parallel cores, exploring both NVIDIA CUDA and cross-platform OpenCL:

---

### [Session 1: GPU Architecture & PyCUDA Programming](./README-session1.md)
*Duration: 2 hours*

- **GPU Hardware Foundations**:
  - CPU (low-latency cores) vs GPU (thousands of parallel high-throughput ALUs).
  - The Heterogeneous Host-Device Computing Model.
  - SIMT (Single Instruction, Multiple Threads).
- **The CUDA Execution & Memory Hierarchy**:
  - Grids, Blocks, Warps, and Thread indexing formulas.
  - Registers, on-chip Shared Memory, and Global VRAM.
- **PyCUDA Programming**:
  - The 5-step CUDA lifecycle: Alloc -> Memcpy HtoD -> Launch -> Memcpy DtoH -> Free.
  - Compiling CUDA C kernels using `SourceModule`.
  - 2D thread indexing for Matrix operations.
- **High-Level Abstractions**:
  - `gpuarray.GPUArray` (NumPy arrays living in VRAM).
  - `ElementwiseKernel` for one-line custom parallel expressions.
  - `ReductionKernel` for parallel tree reductions (dot products, sums).

**Session 1 Demos:**
- [`day5/demo/01_pycuda_kernel_and_memory.py`](./demo/01_pycuda_kernel_and_memory.py)
- [`day5/demo/02_pycuda_gpuarray_elementwise.py`](./demo/02_pycuda_gpuarray_elementwise.py)

---

### [Session 2: JIT GPU Acceleration (Numba) & OpenCL (PyOpenCL)](./README-session2.md)
*Duration: 2 hours*

- **Numba & NumbaPro CUDA**:
  - Just-In-Time (JIT) compilation from pure Python syntax without writing C strings.
  - The `@cuda.jit` decorator.
  - Thread positioning with `cuda.grid(1)` and `cuda.grid(2)`.
  - On-chip Shared Memory optimization (`cuda.shared.array()`) and synchronization (`cuda.syncthreads()`).
  - Multi-core CPU parallel JIT fallback (`@jit(parallel=True)`).
- **Cross-Platform Heterogeneous Computing with PyOpenCL**:
  - OpenCL architecture: Vendor independence across NVIDIA, AMD, Intel, and Apple Silicon.
  - Platforms, Devices, Contexts, Command Queues, and Memory Buffers.
  - Dynamic compilation and execution of OpenCL C kernels.
- **5-Day Masterclass Grand Wrap-Up**:
  - The Complete Parallel Python Stack: From single-core serialization to 10,000-core supercomputing.

**Session 2 Demos:**
- [`day5/demo/03_numba_cuda_jit.py`](./demo/03_numba_cuda_jit.py)
- [`day5/demo/04_pyopencl_basics.py`](./demo/04_pyopencl_basics.py)

---

## Quick Demo Reference

| Demo File | Topic | Key Primitives / Technologies |
|---|---|---|
| [`01_pycuda_kernel_and_memory.py`](./demo/01_pycuda_kernel_and_memory.py) | PyCUDA Basics | `SourceModule`, `mem_alloc`, `memcpy_htod`, `memcpy_dtoh`, Block/Grid |
| [`02_pycuda_gpuarray_elementwise.py`](./demo/02_pycuda_gpuarray_elementwise.py) | High-Level PyCUDA | `gpuarray.to_gpu()`, `ElementwiseKernel`, `ReductionKernel` |
| [`03_numba_cuda_jit.py`](./demo/03_numba_cuda_jit.py) | Numba CUDA JIT | `@cuda.jit`, `cuda.grid(1)`, `cuda.shared.array`, `cuda.syncthreads` |
| [`04_pyopencl_basics.py`](./demo/04_pyopencl_basics.py) | PyOpenCL | `cl.create_some_context()`, `CommandQueue`, `Program.build()`, Buffers |

---

> **Ready to begin? Start with [Session 1: GPU Architecture & PyCUDA Programming](./README-session1.md)**
