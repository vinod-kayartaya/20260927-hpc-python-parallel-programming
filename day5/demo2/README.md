# Day 5 Demo 2: Simple & Compact GPU Programming Examples

> **Location:** `day5/demo2/`  
> **Target Environment:** GPU Compute Nodes (e.g. PARAM Rudra cluster GPU nodes with NVIDIA GPUs)  
> **Description:** Minimal, focused GPU programs with zero boilerplate and pure native GPU execution (no CPU simulations).

---

## Files in this Directory

| File | Topic | Key Primitives / Concepts | Lines |
|---|---|---|:---:|
| [`01_device_query.py`](./01_device_query.py) | GPU Device Query | `cuda.init()`, `cuda.Device`, VRAM memory, Compute capability, SMs | ~18 |
| [`02_pycuda_vector_add.py`](./02_pycuda_vector_add.py) | PyCUDA Vector Addition | `SourceModule`, `cuda.mem_alloc`, `memcpy_htod`, `memcpy_dtoh`, `[block, grid]` | ~45 |
| [`03_pycuda_gpuarray.py`](./03_pycuda_gpuarray.py) | PyCUDA GPUArray | `gpuarray.to_gpu()`, `c_gpu = 2.0 * a_gpu + b_gpu`, `.get()` | ~28 |
| [`04_numba_cuda_vector_add.py`](./04_numba_cuda_vector_add.py) | Numba CUDA JIT | Pure Python `@cuda.jit`, `cuda.grid(1)`, `[blocks, threads]` | ~35 |
| [`05_pyopencl_vector_add.py`](./05_pyopencl_vector_add.py) | PyOpenCL (Cross-Platform) | OpenCL Context, CommandQueue, `cl.Program.build()`, buffers | ~38 |
| [`run_gpu.sh`](./run_gpu.sh) | Supercomputer Batch Script | SLURM batch job script configured for PARAM Rudra (`#SBATCH --partition=gpu`) | ~35 |

---

## How to Run on GPU Nodes

### Option 1: Via SLURM Batch Submission (Recommended on Cluster)
Submit the bundled job script:
```bash
sbatch run_gpu.sh
```
Check status and view outputs:
```bash
squeue -u $USER
cat day5_gpu_*.out
```

---

### Option 2: Running Individually (Interactive GPU Node Session)
If inside an interactive allocation (`srun --partition=gpu --gres=gpu:1 --pty bash`) or on a workstation with an NVIDIA GPU:
```bash
python3 01_device_query.py
python3 02_pycuda_vector_add.py
python3 03_pycuda_gpuarray.py
python3 04_numba_cuda_vector_add.py
python3 05_pyopencl_vector_add.py
```
