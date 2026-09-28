"""
Demo 02: MPI Collective Communication Operations
================================================

Demonstrates collective operations across all processes in a communicator:
    - Broadcast (comm.bcast)  : One process sends the same data to ALL ranks
    - Scatter   (comm.scatter): Root splits an array into chunks for each rank
    - Gather    (comm.gather) : Root collects pieces from all ranks into one list
    - Reduction (comm.reduce) : Combines values from all ranks using an operation (SUM, MAX)
    - All-to-all(comm.alltoall): Every rank sends distinct data to every rank

How to run:
    mpirun -n 4 python3 02_mpi_collective.py
"""

import sys

try:
    from mpi4py import MPI
    MPI_AVAILABLE = True
except ImportError:
    MPI_AVAILABLE = False


def check_mpi():
    """Verify that mpi4py is installed and at least 2 processes are present."""
    if not MPI_AVAILABLE:
        print("=" * 60)
        print("mpi4py is NOT installed.")
        print("Please install open-mpi and mpi4py, then run:")
        print("    mpirun -n 4 python3 02_mpi_collective.py")
        print("=" * 60)
        return None, 0, 1

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print(f"Running with {size} process. Collective operations need >= 2 processes!")
            print("Please run using: mpirun -n 4 python3 02_mpi_collective.py")
        return comm, rank, size

    return comm, rank, size


# ===================================================================
# 1. Broadcast (One-to-All)
# ===================================================================

def demo_broadcast():
    """
    Root process (rank 0) broadcasts configuration parameters to all ranks.
    All ranks call bcast(..., root=0).
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    if rank == 0:
        config = {"model": "neural_net", "learning_rate": 0.01, "epochs": 100}
        print(f"[Rank {rank}] Broadcasting config to all {size} processes...")
    else:
        config = None

    # Broadcast happens here: root sends, all others receive
    config = comm.bcast(config, root=0)

    print(f"  [Rank {rank}] Received broadcasted config: {config}")


# ===================================================================
# 2. Scatter and Gather (Divide and Conquer)
# ===================================================================

def demo_scatter_gather():
    """
    Scatter: Root splits a list into chunks and gives one chunk to each rank.
    Gather : Each rank computes something on its chunk and root collects results.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    # Root prepares data: a list with length equal to number of ranks
    if rank == 0:
        data_chunks = [i * 10 for i in range(size)]
        print(f"[Rank {rank}] Scattering data {data_chunks} to all ranks...")
    else:
        data_chunks = None

    # Scatter one element to each rank
    local_data = comm.scatter(data_chunks, root=0)
    print(f"  [Rank {rank}] Received local piece: {local_data}")

    # Each rank performs local computation
    local_result = local_data ** 2
    print(f"  [Rank {rank}] Computed square: {local_result}")

    # Gather all results back to root
    gathered_results = comm.gather(local_result, root=0)

    if rank == 0:
        print(f"\n[Rank {rank}] Gathered all processed results: {gathered_results}")


# ===================================================================
# 3. Reduction Operation (comm.reduce & comm.allreduce)
# ===================================================================

def demo_reduction():
    """
    All ranks have a local value.
    Reduction aggregates values using an operation (e.g. SUM, MAX, MIN).
    - comm.reduce    : Only root gets the reduced result.
    - comm.allreduce : ALL ranks receive the reduced result.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    # Each rank contributes its rank number + 1
    local_val = rank + 1
    print(f"  [Rank {rank}] Local value = {local_val}")

    # Sum reduction to root (rank 0)
    total_sum = comm.reduce(local_val, op=MPI.SUM, root=0)

    # Max reduction to all ranks
    max_val = comm.allreduce(local_val, op=MPI.MAX)

    if rank == 0:
        print(f"\n[Rank {rank}] Total SUM across all ranks = {total_sum}")

    print(f"  [Rank {rank}] Global MAX value (via allreduce) = {max_val}")


# ===================================================================
# 4. All-to-All Exchange (comm.alltoall)
# ===================================================================

def demo_alltoall():
    """
    Each process sends unique, personalized data to every other process.
    Input: list of size elements (one for each rank).
    Output: list of size elements (one from each rank).
    Equivalent to a matrix transpose.
    """
    comm, rank, size = check_mpi()
    if not comm or size < 2:
        return

    # Each rank prepares a message for every process
    send_data = [f"R{rank}->R{i}" for i in range(size)]
    print(f"  [Rank {rank}] Sending: {send_data}")

    recv_data = comm.alltoall(send_data)
    print(f"  [Rank {rank}] Received: {recv_data}")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_broadcast()
    # demo_scatter_gather()
    # demo_reduction()
    # demo_alltoall()


if __name__ == "__main__":
    main()
