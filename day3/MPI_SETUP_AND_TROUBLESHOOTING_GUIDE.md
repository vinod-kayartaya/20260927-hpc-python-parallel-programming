# MPI Installation, Setup & Troubleshooting Guide (macOS & Linux)

> **Location:** `day3/MPI_SETUP_AND_TROUBLESHOOTING_GUIDE.md`  
> **Topic:** Setting up OpenMPI, `mpirun`, and `mpi4py` on Development Machines (Bypassing Homebrew Compilation Issues)

---

## Table of Contents

1. [Introduction & The Problem](#1-introduction--the-problem)
   - [Why Homebrew Fails on Intel macOS](#why-homebrew-fails-on-intel-macos)
   - [The `stage1-bubble` GCC Build Error Explained](#the-stage1-bubble-gcc-build-error-explained)
2. [The Robust Solution: Miniforge & Conda-Forge](#2-the-robust-solution-miniforge--conda-forge)
   - [Why Conda-Forge Succeeded Where Homebrew Failed](#why-conda-forge-succeeded-where-homebrew-failed)
3. [Step-by-Step Installation Walkthrough](#3-step-by-step-installation-walkthrough)
   - [Step 1: Download Miniforge](#step-1-download-miniforge)
   - [Step 2: Run the Silent Installation](#step-2-run-the-silent-installation)
   - [Step 3: Activate the Environment](#step-3-activate-the-environment)
   - [Step 4: Install OpenMPI and `mpi4py`](#step-4-install-openmpi-and-mpi4py)
   - [Step 5: Verify the Installation](#step-5-verify-the-installation)
4. [Running Day 3 MPI Demos with `mpirun`](#4-running-day-3-mpi-demos-with-mpirun)
   - [Understanding `mpirun -n <N>`](#understanding-mpirun--n-n)
   - [Running Point-to-Point Communication](#running-point-to-point-communication)
   - [Running Collective Communication](#running-collective-communication)
   - [The `--oversubscribe` Flag](#the---oversubscribe-flag)
5. [Cross-Platform Setup Matrix](#5-cross-platform-setup-matrix)
6. [Common Troubleshooting & FAQs](#6-common-troubleshooting--faqs)

---

## 1. Introduction & The Problem

To develop and test distributed memory Python programs locally, developers need two components:
1. **The underlying C/C++ MPI Implementation:** Provides the `mpirun` CLI and low-level communication libraries (usually **OpenMPI** or **MPICH**).
2. **The Python Wrapper (`mpi4py`):** Provides the Python bindings to call MPI functions from Python.

When developers attempt to install OpenMPI on macOS via Homebrew (`brew install open-mpi`), they frequently encounter build failures.

---

### Why Homebrew Fails on Intel macOS

As seen in typical Homebrew logs:

```text
Warning: You are using macOS on Intel x86_64.
We do not provide support for this platform (announced August 2025).
Homebrew no longer builds bottles for this configuration.
Existing bottles may still work, but updated formulae may build from source.
```

1. **No Precompiled Binaries (Bottles):** Homebrew stopped building pre-compiled `.tar.gz` binary bottles for Intel Macs.
2. **Building from Source:** Homebrew fell back to compiling OpenMPI and its entire dependency tree directly on your machine.
3. **The GCC Requirement:** The OpenMPI formula includes Fortran bindings (`mpifort`). To compile Fortran, Homebrew required **GCC 16.2.0**.

---

### The `stage1-bubble` GCC Build Error Explained

Compiling the entire GCC compiler toolchain from scratch on modern macOS is notoriously brittle:

```text
gmake[2]: Leaving directory '/private/tmp/.../gcc-16.2.0/build'
gmake[1]: *** [Makefile:25080: stage1-bubble] Error 2
gmake: *** [Makefile:1138: all] Error 2
```

- GCC uses a 3-stage bootstrap build process (`stage1`, `stage2`, `stage3`).
- macOS SDK headers (Xcode Clang) frequently conflict with GCC's internal C++ standard library during bootstrap.
- The build aborted, Homebrew rolled back, and **`mpirun` remained uninstalled**.

---

## 2. The Robust Solution: Miniforge & Conda-Forge

### Why Conda-Forge Succeeded Where Homebrew Failed

```
                      PACKAGE RESOLUTION COMPARISON
                      
[Homebrew on Intel Mac]                 [Conda-Forge]
         │                                    │
         ▼                                    ▼
No precompiled bottle               Pre-built binaries maintained
         │                          for ALL architectures:
         ▼                          (Intel macOS, Apple Silicon, Linux)
Attempts to compile GCC 16.2                  │
from C++ source code                          ▼
         │                          Downloads ready-to-run binaries
         ▼                          (mpirun, libmpi.dylib, mpi4py)
gmake Error -> ABORT!                         │
                                              ▼
                                    INSTALLED IN 15 SECONDS!
```

**Conda-Forge** is an open-source, community-led software distribution. Unlike Homebrew:
- It maintains dedicated, automated build farms producing **pre-compiled binary packages for macOS Intel (`osx-64`)**.
- It bundles binaries with their required dynamic libraries isolated into user space.
- **Zero source compilation required:** It unpacks pre-tested binaries directly to disk without needing `sudo` or Xcode compiler modifications.

---

## 3. Step-by-Step Installation Walkthrough

Follow these 5 steps to set up `mpirun` and `mpi4py` cleanly on any development machine.

---

### Step 1: Download Miniforge

Open your terminal and download the official Miniforge installer for macOS Intel (`x86_64`):

```bash
curl -fsSL -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh"
```

*(Note for Apple Silicon M1/M2/M3/M4 users: replace `x86_64` with `arm64`).*

---

### Step 2: Run the Silent Installation

Install Miniforge into your user directory (no `sudo` required):

```bash
bash Miniforge3-MacOSX-x86_64.sh -b -p $HOME/miniforge3
```

- `-b`: Batch mode (accepts license agreement automatically).
- `-p $HOME/miniforge3`: Installs everything into a clean, self-contained directory in your home folder.

---

### Step 3: Activate the Environment

Add Miniforge to your active shell session:

```bash
source $HOME/miniforge3/bin/activate
```

*(To make this permanent, run `conda init zsh` or `conda init bash`).*

---

### Step 4: Install OpenMPI and `mpi4py`

Install precompiled OpenMPI and Python bindings directly from the `conda-forge` channel:

```bash
conda install -y openmpi mpi4py numpy
```

Conda downloads and links:
- `openmpi` (provides `mpirun`, `mpicc`, `mpicxx`, `ompi_info`)
- `mpi4py` (provides the Python `MPI` module)
- `numpy` (enables high-speed zero-copy buffer transfers with `comm.Send`/`comm.Recv`)

---

### Step 5: Verify the Installation

Confirm that both the CLI binary and the Python library are operational:

```bash
# 1. Check mpirun binary
which mpirun
# Output: /Users/<username>/miniforge3/bin/mpirun

# 2. Check mpirun version
mpirun --version
# Output: mpirun (Open MPI) 5.0.x

# 3. Test mpi4py import
python3 -c "from mpi4py import MPI; print('MPI Version:', MPI.Get_version())"
# Output: MPI Version: (3, 1)
```

---

## 4. Running Day 3 MPI Demos with `mpirun`

Now that `mpirun` is active, you can launch multi-process MPI applications.

---

### Understanding `mpirun -n <N>`

When you run:
```bash
mpirun -n 4 python3 my_script.py
```
1. `mpirun` launches **4 independent operating system processes** in parallel.
2. Each process executes `my_script.py` from the first line.
3. Behind the scenes, OpenMPI establishes inter-process loopback TCP sockets or shared-memory channels between all 4 processes.
4. Each process receives a unique rank ID (`comm.Get_rank()` returns `0`, `1`, `2`, or `3`).

---

### Running Point-to-Point Communication

Test two processes swapping messages:

```bash
cd day3/demo
mpirun -n 2 python3 01_mpi_point_to_point.py
```

**Expected Output:**
```text
[Rank 0] Sending data to Rank 1: {'message': 'Hello from Rank 0', 'data': [1, 2, 3, 4], 'status': 'OK'}
[Rank 1] Received data from Rank 0: {'message': 'Hello from Rank 0', 'data': [1, 2, 3, 4], 'status': 'OK'}
```

---

### Running Collective Communication

Test broadcast, scatter, gather, and reduction across 4 ranks:

```bash
mpirun -n 4 python3 02_mpi_collective.py
```

**Expected Output:**
```text
[Rank 0] Broadcasting config to all 4 processes...
  [Rank 0] Received broadcasted config: {'model': 'neural_net', 'learning_rate': 0.01, 'epochs': 100}
  [Rank 1] Received broadcasted config: {'model': 'neural_net', 'learning_rate': 0.01, 'epochs': 100}
  [Rank 2] Received broadcasted config: {'model': 'neural_net', 'learning_rate': 0.01, 'epochs': 100}
  [Rank 3] Received broadcasted config: {'model': 'neural_net', 'learning_rate': 0.01, 'epochs': 100}
```

---

### The `--oversubscribe` Flag

By default, OpenMPI prevents you from requesting more processes (`-n`) than physical CPU cores on your laptop.

If your machine has 4 physical cores and you want to simulate an 8-rank cluster:
```bash
# May fail with: "There are not enough slots available in the system"
mpirun -n 8 python3 02_mpi_collective.py

# Solution: Add --oversubscribe
mpirun --oversubscribe -n 8 python3 02_mpi_collective.py
```
This forces OpenMPI to multiplex multiple ranks onto the same CPU cores for testing purposes.

---

## 5. Cross-Platform Setup Matrix

| Operating System | Recommended Installation Method | Command |
|---|---|---|
| **macOS (Intel x86_64)** | **Miniforge / Conda-Forge** | `conda install -y openmpi mpi4py numpy` |
| **macOS (Apple Silicon M1-M4)** | Homebrew OR Miniforge | `brew install open-mpi && pip3 install mpi4py` |
| **Ubuntu / Debian** | APT Package Manager | `sudo apt update && sudo apt install -y libopenmpi-dev openmpi-bin && pip3 install mpi4py` |
| **RHEL / Rocky / AlmaLinux** | DNF / YUM | `sudo dnf install -y openmpi openmpi-devel && pip3 install mpi4py` |
| **Supercomputer / HPC Cluster** | Environment Modules | `module load openmpi && python3 ...` (or via SLURM) |

---

## 6. Common Troubleshooting & FAQs

### Q1: `zsh: command not found: mpirun`
**Cause:** The terminal session has not activated the Miniforge environment.  
**Fix:** Run:
```bash
source $HOME/miniforge3/bin/activate
```

---

### Q2: macOS Firewall Popup Alert
**Symptom:** macOS shows a dialog: *"Do you want the application 'python' to accept incoming network connections?"*  
**Cause:** OpenMPI uses local TCP loopback sockets (`127.0.0.1`) to communicate between local processes. macOS treats this as local network listening.  
**Fix:** Click **Allow**. It only communicates locally on your machine.

---

### Q3: How do I switch back to my standard virtualenv (`.venv`)?
If you have a dedicated virtual environment, you can deactivate Conda at any time:
```bash
conda deactivate
source /path/to/my_venv/bin/activate
```
To use MPI within that venv, make sure `/Users/<username>/miniforge3/bin` is in your `$PATH`, or install `mpi4py` inside that venv pointing to the conda-installed MPI library.

---

### Summary Checklist
- [x] Downloaded Miniforge installer script.
- [x] Installed to `$HOME/miniforge3` without `sudo`.
- [x] Installed `openmpi`, `mpi4py`, and `numpy` via `conda install`.
- [x] Verified `which mpirun` returns the active binary path.
- [x] Executed Day 3 demos with `mpirun -n 2` and `mpirun -n 4`.
