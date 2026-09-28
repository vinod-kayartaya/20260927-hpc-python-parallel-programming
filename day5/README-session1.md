# Day 5, Session 1: GPU Architecture & PyCUDA Programming

> **Duration:** 2 hours (theory + live demonstrations)  
> **Prerequisites:** Days 1, 2, 3, & 4 (Process parallelism, vectorization concepts)  
> **Demos folder:** [`day5/demo/`](./demo/)

---

## Table of Contents

1. [Why GPUs for High-Performance Computing?](#1-why-gpus-for-high-performance-computing)
2. [CPU vs GPU Hardware Architecture](#2-cpu-vs-gpu-hardware-architecture)
3. [The CUDA Execution & Thread Hierarchy](#3-the-cuda-execution--thread-hierarchy)
   - [Grids, Blocks, Warps, and Threads](#grids-blocks-warps-and-threads)
   - [Memory Hierarchy: Registers, Shared Memory, and Global VRAM](#memory-hierarchy)
4. [PyCUDA Programming Model](#4-pycuda-programming-model)
   - [The 5-Step CUDA Lifecycle](#the-5-step-cuda-lifecycle)
   - [Writing CUDA C Kernels with `SourceModule`](#writing-cuda-c-kernels-with-sourcemodule)
   - [Explicit Memory Management: Alloc, Memcpy](#explicit-memory-management)
5. [High-Level PyCUDA: GPUArray & ElementwiseKernel](#5-high-level-pycuda-gpuarray--elementwisekernel)
   - [NumPy on the GPU: `gpuarray.GPUArray`](#numpy-on-the-gpu)
   - [Custom Fast Expressions: `ElementwiseKernel`](#custom-fast-expressions)
   - [GPU MapReduce with `ReductionKernel`](#gpu-mapreduce-with-reductionkernel)
6. [Session 1 Summary](#session-1-summary)

---

## 1. Why GPUs for High-Performance Computing?

Modern CPUs have 4 to 128 large, powerful cores optimized for **low-latency sequential execution**:
- Deep pipeline stages
- Massive caches (L1, L2, L3)
- Sophisticated branch predictors and speculative execution hardware

In contrast, GPUs (Graphics Processing Units) are massively parallel processors with **thousands of small, energy-efficient ALUs (Arithmetic Logic Units)** designed for **high-throughput compute**:

```text
          CPU (Low Latency)                         GPU (High Throughput)
┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │   │ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ │
│ │Core0 │ │Core1 │ │Core2 │ │Core3 │ │   │ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ │
│ └──────┘ └──────┘ └──────┘ └──────┘ │   │ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ │
│ ┌─────────────────────────────────┐ │   │ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ │
│ │         L3 Cache Memory         │ │   │        Thousands of Tiny ALUs       │
│ └─────────────────────────────────┘ │   │ ┌─────────────────────────────────┐ │
│ ┌───────────────┐ ┌───────────────┐ │   │ │    L2 Cache & High-Bandwidth    │ │
│ │ Control Unit  │ │   DRAM (RAM)  │ │   │ │       VRAM (GDDR6 / HBM)        │ │
│ └───────────────┘ └───────────────┘ │   │ └─────────────────────────────────┘ │
└─────────────────────────────────────┘   └─────────────────────────────────────┘
```

GPUs achieve **10x to 100x speedups** on data-parallel problems such as:
- Dense matrix multiplication & deep neural network training.
- Fast Fourier Transforms (FFT) and signal processing.
- Molecular dynamics, climate modeling, and finite element simulations.

---

## 2. CPU vs GPU Hardware Architecture

CUDA uses a **Heterogeneous (Hybrid) Computing Model**:
- **Host**: The CPU and its system RAM. Responsible for control flow, I/O, and launching kernels.
- **Device**: The GPU and its on-board Video RAM (VRAM). Responsible for parallel compute.

```
┌──────────────────────┐                 ┌──────────────────────┐
│     HOST (CPU)       │   PCIe Bus      │     DEVICE (GPU)     │
│                      │ (Data Transfer) │                      │
│ [System RAM (DDR5)]  │ <=============> │ [High-Speed VRAM]    │
│                      │                 │                      │
│ Runs control program │ Launches Kernel │ Executes thousands of│
│ and coordinates data │ ──────────────> │ threads in parallel  │
└──────────────────────┘                 └──────────────────────┘
```

---

## 3. The CUDA Execution & Thread Hierarchy

### Grids, Blocks, Warps, and Threads

CUDA organizes parallel execution into a three-tiered hierarchy:

```
GRID (The entire kernel execution)
├── BLOCK (0, 0)                  BLOCK (1, 0)
│   ├── Warp 0 (Threads 0-31)     ├── Warp 0 (Threads 0-31)
│   ├── Warp 1 (Threads 32-63)    ├── Warp 1 (Threads 32-63)
│   └── ...                       └── ...
└── BLOCK (0, 1)                  BLOCK (1, 1)
```

1. **Thread**: The smallest unit of execution. Every thread executes the exact same kernel function on different data indices (**SIMT**: Single Instruction, Multiple Threads).
2. **Warp**: A hardware group of **32 consecutive threads** within a block that execute instructions simultaneously in lockstep.
3. **Thread Block**: A cooperative group of up to 1024 threads that run on the same Streaming Multiprocessor (SM) and can synchronize and share on-chip cache.
4. **Grid**: A collection of thread blocks launched across the entire GPU chip.

#### Calculating Global Thread Index
In 1D arrays:
$$\text{idx} = \text{blockIdx.x} \times \text{blockDim.x} + \text{threadIdx.x}$$

In 2D matrices (images, grids):
$$\text{col} = \text{blockIdx.x} \times \text{blockDim.x} + \text{threadIdx.x}$$
$$\text{row} = \text{blockIdx.y} \times \text{blockDim.y} + \text{threadIdx.y}$$
$$\text{global\_index} = \text{row} \times \text{width} + \text{col}$$

---

### Memory Hierarchy

| Memory Type | Location | Scope | Speed / Latency |
|---|---|---|---|
| **Registers** | On-chip | Single thread | Fastest (< 1 cycle) |
| **Shared Memory** | On-chip SRAM | Thread Block | Extremely fast (~1-2 cycles) |
| **Constant Memory** | On-chip cache | All threads (read-only) | Fast when cached |
| **Global Memory (VRAM)** | Off-chip GDDR/HBM | All threads & Host | Slower (200-400 cycles) |

---

## 4. PyCUDA Programming Model

**PyCUDA** brings Python's elegance and rapid prototyping to NVIDIA's CUDA C runtime.

### The 5-Step CUDA Lifecycle

```
[1. Host NumPy Arrays] ──> [2. Allocate GPU VRAM] ──> [3. memcpy_htod]
                                                            │
[5. memcpy_dtoh] <──────── [4. Launch CUDA Kernel] <────────┘
```

1. Create input data in CPU memory (typically a NumPy array).
2. Allocate device memory on the GPU using `cuda.mem_alloc(nbytes)`.
3. Copy data from Host to Device via `cuda.memcpy_htod(gpu_buf, host_buf)`.
4. Compile and launch the CUDA C kernel with defined `block` and `grid` dimensions.
5. Copy the result back from Device to Host via `cuda.memcpy_dtoh(host_buf, gpu_buf)`.

---

### Writing CUDA C Kernels with `SourceModule`

```python
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy as np

# Write CUDA C kernel directly in a Python string:
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

# Launch on GPU: 256 threads per block
vector_add(c_gpu, a_gpu, b_gpu, np.int32(1024),
           block=(256, 1, 1), grid=(4, 1))
```

---

### 🖥️ Demo Time

> **Now, let's see these theoretical topics in action.**
>
> - [`01_pycuda_kernel_and_memory.py`](./demo/01_pycuda_kernel_and_memory.py) —
>   1. `demo_cuda_kernel_and_memory()` — Vector addition with explicit GPU memory allocation & transfers
>   2. `demo_matrix_manipulation()` — 2D thread indexing for matrix operations

---

## 5. High-Level PyCUDA: GPUArray & ElementwiseKernel

Writing manual memory allocation and pointer math for simple array operations can be tedious. PyCUDA provides convenient high-level wrappers:

### NumPy on the GPU: `gpuarray.GPUArray`

`GPUArray` provides an array interface identical to NumPy, but stored entirely in GPU VRAM:

```python
import pycuda.gpuarray as gpuarray
import numpy as np

a_host = np.array([1, 2, 3, 4], dtype=np.float32)

# Copy to GPU in one step:
a_gpu = gpuarray.to_gpu(a_host)

# Arithmetic expressions execute directly as parallel GPU kernels!
b_gpu = 2.0 * a_gpu + 10.0

# Fetch result back to CPU:
b_host = b_gpu.get()
print(b_host)  # [12., 14., 16., 18.]
```

---

### Custom Fast Expressions: `ElementwiseKernel`

`ElementwiseKernel` compiles custom C expressions on-the-fly without requiring thread loop boilerplate:

```python
from pycuda.elementwise import ElementwiseKernel

# Linear combination: z = a * x + y
saxpy = ElementwiseKernel(
    "float a, float *x, float *y, float *z",
    "z[i] = a * x[i] + y[i]",
    "saxpy_kernel"
)

saxpy(2.5, x_gpu, y_gpu, z_gpu)
```

---

### GPU MapReduce with `ReductionKernel`

Calculates dot products, norms, sums, and min/max operations using tree reductions on the GPU:

```python
from pycuda.reduction import ReductionKernel

# Calculate vector dot-product: sum(x[i] * y[i])
dot_product = ReductionKernel(
    np.float32,
    neutral="0",
    reduce_expr="a + b",      # Reduction step
    map_expr="x[i] * y[i]",   # Map step
    arguments="float *x, float *y"
)

result = dot_product(x_gpu, y_gpu).get()
```

---

### 🖥️ Demo Time

> **Now, let's see these theoretical topics in action.**
>
> - [`02_pycuda_gpuarray_elementwise.py`](./demo/02_pycuda_gpuarray_elementwise.py) —
>   1. `demo_gpuarray_vector_ops()` — NumPy-style vector arithmetic running in parallel on GPU
>   2. `demo_elementwise_kernel()` — High-performance inline custom expressions
>   3. `demo_map_reduce_gpu()` — GPU-accelerated parallel tree reduction

---

## Session 1 Summary

| Abstraction Level | Tool | How it Works |
|---|---|---|
| **Low-Level CUDA C** | `SourceModule` | Direct C kernel code, explicit memory allocation (`mem_alloc`, `memcpy`) |
| **Mid-Level Expression** | `ElementwiseKernel` | Generates CUDA kernel from single-line C expression |
| **High-Level Array** | `gpuarray.GPUArray` | Object-oriented NumPy syntax executed directly on GPU |
| **MapReduce** | `ReductionKernel` | Parallel map followed by tree reduction |

---

> **Break time! Next up is Session 2: JIT Compilation with Numba & OpenCL with PyOpenCL → [README-session2.md](./README-session2.md)**
