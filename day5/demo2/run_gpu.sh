#!/bin/bash
#SBATCH --job-name=day5_gpu_demo
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:05:00
#SBATCH --output=day5_gpu_%j.out
#SBATCH --error=day5_gpu_%j.err

echo "=================================================="
echo "PARAM RUDRA - GPU DEMO EXECUTION"
echo "=================================================="

echo "Node Hostname:"
hostname

echo
echo "Allocated CUDA Device(s):"
echo "CUDA_VISIBLE_DEVICES = $CUDA_VISIBLE_DEVICES"

echo
echo "NVIDIA System Management Interface (nvidia-smi):"
nvidia-smi

echo
echo "=================================================="
echo "1. Running PyCUDA Device Query"
echo "=================================================="
python3 01_device_query.py

echo
echo "=================================================="
echo "2. Running PyCUDA Vector Add (Explicit Memory)"
echo "=================================================="
python3 02_pycuda_vector_add.py

echo
echo "=================================================="
echo "3. Running PyCUDA GPUArray"
echo "=================================================="
python3 03_pycuda_gpuarray.py

echo
echo "=================================================="
echo "4. Running Numba CUDA Vector Add"
echo "=================================================="
python3 04_numba_cuda_vector_add.py

echo
echo "All Day 5 GPU demos completed successfully!"
