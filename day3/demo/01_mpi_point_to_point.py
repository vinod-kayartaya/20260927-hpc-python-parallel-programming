"""
Demo 01: MPI Point-to-Point Communication & Deadlock Avoidance
==============================================================

Demonstrates point-to-point message passing using `mpi4py`:
    - Basic blocking send and recv (comm.send, comm.recv)
    - Non-blocking communication (comm.isend, comm.irecv)
    - Deadlock scenario and avoidance using comm.sendrecv

How to run:
    mpirun -n 2 python3 01_mpi_point_to_point.py

Note: If mpi4py is not installed, running this directly with `python3`
      will display installation instructions.
"""

import sys

# ---------------------------------------------------------------------------
# MPI Import with graceful fallback
# ---------------------------------------------------------------------------
try:
    from mpi4py import MPI
    MPI_AVAILABLE = True
except ImportError:
    MPI_AVAILABLE = False


def check_mpi():
    """Verify that mpi4py is installed and multiple processes are running."""
    if not MPI_AVAILABLE:
        print("=" * 60)
        print("mpi4py is NOT installed.")
        print("To install:")
        print("  macOS (Homebrew) : brew install open-mpi && pip3 install mpi4py")
        print("  Ubuntu/Debian    : sudo apt install libopenmpi-dev && pip3 install mpi4py")
        print("  Conda            : conda install -c conda-forge mpi4py")
        print("=" * 60)
        return None, 0, 1

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("=" * 60)
            print(f"Running with only {size} process.")
            print("MPI point-to-point requires at least 2 processes!")
            print("Please run using:")
            print("    mpirun -n 2 python3 01_mpi_point_to_point.py")
            print("=" * 60)
        return comm, rank, size

    return comm, rank, size


# ===================================================================
# 1. Blocking Point-to-Point Communication (send / recv)
# ===================================================================

def demo_basic_send_recv():
    """
    Rank 0 sends a Python dictionary to Rank 1.
    Rank 1 receives it and prints the contents.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    if rank == 0:
        data = {"message": "Hello from Rank 0", "data": [1, 2, 3, 4], "status": "OK"}
        print(f"[Rank {rank}] Sending data to Rank 1: {data}")
        comm.send(data, dest=1, tag=11)
    elif rank == 1:
        data = comm.recv(source=0, tag=11)
        print(f"[Rank {rank}] Received data from Rank 0: {data}")


# ===================================================================
# 2. Non-blocking Communication (isend / irecv)
# ===================================================================

def demo_nonblocking_isend():
    """
    Non-blocking isend() and irecv() return Request handles.
    Processes can do other useful work while the communication transfers in background.
    req.wait() waits for completion.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    if rank == 0:
        msg = "Large payload from Rank 0"
        print(f"[Rank {rank}] Initiating non-blocking isend...")
        req = comm.isend(msg, dest=1, tag=22)
        # Process can do other calculations here
        print(f"[Rank {rank}] Doing computation while message is in transit...")
        req.wait()
        print(f"[Rank {rank}] isend completed successfully.")
    elif rank == 1:
        print(f"[Rank {rank}] Initiating non-blocking irecv...")
        req = comm.irecv(source=0, tag=22)
        print(f"[Rank {rank}] Doing computation while waiting for message...")
        data = req.wait()
        print(f"[Rank {rank}] Received payload: '{data}'")


# ===================================================================
# 3. Deadlock Avoidance (sendrecv)
# ===================================================================

def demo_deadlock_avoidance():
    """
    Two ranks want to swap data with each other.
    If both call blocking comm.send() first, both may wait for a receiver -> DEADLOCK!
    Solution:
      - Rank 0 sends then receives; Rank 1 receives then sends, OR
      - Use comm.sendrecv() which handles the atomic send-and-receive safely.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    my_data = f"Secret from Rank {rank}"
    peer = 1 if rank == 0 else 0

    print(f"[Rank {rank}] Swapping data with Rank {peer} using sendrecv()...")
    received = comm.sendrecv(sendobj=my_data, dest=peer, sendtag=33,
                             source=peer, recvtag=33)

    print(f"[Rank {rank}] Successfully received from Rank {peer}: '{received}'")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_basic_send_recv()
    # demo_nonblocking_isend()
    # demo_deadlock_avoidance()


if __name__ == "__main__":
    main()
