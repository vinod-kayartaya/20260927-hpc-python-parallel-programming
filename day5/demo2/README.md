# Day 5 Demo 2: Simple & Compact GPU Programming Examples

> **Location:** `day5/demo2/`  
> **Topic:** Clean, focused, minimal GPU coding examples for PyCUDA, Numba CUDA, and PyOpenCL.

---

## Files in this Directory

| File | Topic | Key Concepts | Lines |
|---|---|---|:---:|
| [`01_device_query.py`](./01_device_query.py) | GPU Device Query | `cuda.Device`, VRAM memory, Compute capability, Multiprocessors | ~25 |
| [`02_pycuda_vector_add.py`](./02_pycuda_vector_add.py) | PyCUDA Vector Addition | `SourceModule`, `cuda.mem_alloc`, `memcpy_htod`, `memcpy_dtoh` | ~40 |
| [`03_pycuda_gpuarray.py`](./03_pycuda_gpuarray.py) | PyCUDA GPUArray | `gpuarray.to_gpu()`, `c_gpu = 2.0 * a_gpu + b_gpu`, `.get()` | ~30 |
| [`04_numba_cuda_vector_add.py`](./04_numba_cuda_vector_add.py) | Numba CUDA JIT | Pure Python `@cuda.jit`, `cuda.grid(1)`, `[blocks, threads]` | ~35 |
| [`05_pyopencl_vector_add.py`](./05_pyopencl_vector_add.py) | PyOpenCL (Cross-Platform) | `cl.Program.build()`, Context, CommandQueue, OpenCL C kernel | ~40 |
| [`run_gpu.sh`](./run_gpu.sh) | Supercomputer Batch Script | SLURM job script for PARAM Rudra cluster (`#SBATCH --partition=gpu`) | ~30 |

---

## How to Run

### 1. Locally on your Laptop (Simulated / CPU mode)
Run any script directly using Python:
```bash
python3 01_device_query.py
python3 02_pycuda_vector_add.py
python3 03_pycuda_gpuarray.py
python3 04_numba_cuda_vector_add.py
python3 05_pyopencl_vector_add.py
```
*(Each script includes automatic fallback to ensure it runs cleanly on any laptop without crashing).*

---

### 2. On the Supercomputer (PARAM Rudra GPU Nodes)
1. **Submit the batch job:**
   ```bash
   sbatch run_gpu.sh
   ```
2. **Monitor job queue:**
   ```bash
   squeue -u $USER
   ```
3. **View output and diagnostic logs:**
   ```bash
   cat day5_gpu_*.out
   cat day5_gpu_*.err
   ```
