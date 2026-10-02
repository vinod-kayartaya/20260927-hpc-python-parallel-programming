"""
Example 01: Querying GPU Device Properties
Topic: PyCUDA Initialization and Hardware Query
"""

try:
    import pycuda.driver as cuda
    cuda.init()

    num_devices = cuda.Device.count()
    print(f"Total CUDA GPUs detected: {num_devices}\n")

    for i in range(num_devices):
        dev = cuda.Device(i)
        print(f"--- GPU Device {i}: {dev.name()} ---")
        print(f"  Compute Capability : {dev.compute_capability()}")
        print(f"  Total Memory       : {dev.total_memory() / (1024**3):.2f} GB")
        print(f"  Multiprocessors    : {dev.get_attribute(cuda.device_attribute.MULTIPROCESSOR_COUNT)}")
        print(f"  Max Threads/Block  : {dev.get_attribute(cuda.device_attribute.MAX_THREADS_PER_BLOCK)}")

except (ImportError, Exception) as e:
    print(f"[Note] PyCUDA or NVIDIA GPU not found: {e}")
    print("\nOn a cluster GPU node (e.g. PARAM Rudra), this script prints:")
    print("  --- GPU Device 0: NVIDIA A100-PCIE-40GB ---")
    print("    Compute Capability : (8, 0)")
    print("    Total Memory       : 40.00 GB")
    print("    Multiprocessors    : 108")
    print("    Max Threads/Block  : 1024")
