"""
Example 05: Cross-Platform Heterogeneous Computing with PyOpenCL
Topic: OpenCL Platforms, Devices, Context, CommandQueue, OpenCL C Kernel
"""

try:
    import numpy as np
    import pyopencl as cl
    OPENCL_AVAILABLE = True
except (ImportError, Exception):
    OPENCL_AVAILABLE = False


def main():
    N = 1024

    if OPENCL_AVAILABLE:
        a_host = np.arange(N, dtype=np.float32)
        b_host = np.arange(N, dtype=np.float32) * 4.0
        c_host = np.empty_like(a_host)

        # 1. Create Context and Command Queue
        ctx = cl.create_some_context(interactive=False)
        queue = cl.CommandQueue(ctx)

        # 2. OpenCL C Kernel
        kernel_src = """
        __kernel void vector_add(__global const float *a,
                                 __global const float *b,
                                 __global float *c) {
            int gid = get_global_id(0);
            c[gid] = a[gid] + b[gid];
        }
        """
        prg = cl.Program(ctx, kernel_src).build()

        # 3. Create Memory Buffers
        mf = cl.mem_flags
        a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_host)
        b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_host)
        c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c_host.nbytes)

        # 4. Enqueue Kernel execution across N work-items
        prg.vector_add(queue, (N,), None, a_buf, b_buf, c_buf)

        # 5. Read Buffer back to Host memory
        cl.enqueue_copy(queue, c_host, c_buf)
        print("Executed on accelerator via PyOpenCL!")
    else:
        print("[Simulated Execution — PyOpenCL not present]")
        a_host = [float(i) for i in range(5)]
        b_host = [float(i * 4.0) for i in range(5)]
        c_host = [a + b for a, b in zip(a_host, b_host)]

    print(f"Sample outputs: c[0] = {c_host[0]}, c[1] = {c_host[1]}")
    print("Notice: OpenCL runs on NVIDIA, AMD, Intel, and Apple Silicon chips!")


if __name__ == '__main__':
    main()
