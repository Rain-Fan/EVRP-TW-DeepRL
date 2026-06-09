# Environment Record - EVRP-TW Research

## Operating System
- **OS**: macOS 15.6 (Sequoia)
- **Build**: 24G84
- **Architecture**: arm64 (Apple Silicon)

## Python Version
- **Base environment** (`/opt/anaconda3`): Python 3.13.9
- **evrp environment** (`miniconda3/envs/evrp`): Python 3.10.20
- **vrp101 environment** (`miniconda3/envs/vrp101`): Python 3.10.x

## Package Manager
- **Primary**: pip 24.3.1
- **Environment Manager**: conda (Anaconda3)

## Solver / Codebase Version

### OR-Tools based Solvers
- **OR-Tools**: 9.15.6755 (installed in both `evrp` and `vrp101` conda environments)
- **PyVRP**: 0.11.3 (installed in `evrp` environment)
- **vrplib**: 1.5.1 (installed in `evrp` environment)

### Deep RL Frameworks (base environment)
- **PyTorch**: 2.10.0
- **torchvision**: 0.25.0
- **torchaudio**: 2.10.0
- **TensorFlow**: 2.21.0

### Key Scientific Packages (base environment)
- **NumPy**: 2.4.4
- **SciPy**: 1.15.3

### Other Utilities (evrp/vrp101 environments)
- **matplotlib**: 3.10.9
- **pandas**: 2.3.3
- **networkx**: 3.4.2 (evrp)
- **tqdm**: 4.68.1 (evrp)

## Exact Install Commands

### Create and setup conda environments
```bash
# Create evrp environment (Python 3.10, OR-Tools + PyVRP)
conda create -n evrp python=3.10
conda activate evrp
pip install ortools==9.15.6755
pip install pyvrp==0.11.3
pip install vrplib
pip install matplotlib pandas networkx tqdm

# Create vrp101 environment (Python 3.10, OR-Tools only)
conda create -n vrp101 python=3.10
conda activate vrp101
pip install ortools==9.15.6755
pip install matplotlib pandas
```

### Base environment (PyTorch / TensorFlow for Deep RL)
```bash
pip install torch torchvision torchaudio
pip install tensorflow
pip install numpy scipy matplotlib pandas
```

## Hardware Used for Runtime
- **CPU**: Apple M4
- **RAM**: 16 GB (17,179,869,184 bytes)
- **Architecture**: ARM64 (Apple Silicon)
- **Machine Type**: Mac (Laptop / Desktop)
