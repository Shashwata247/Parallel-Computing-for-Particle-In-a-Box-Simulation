# Particle-in-a-Box Simulation

A high-performance, parallelized particle-in-a-box simulation written in Python, intended for educational and demonstration purposes. The simulation uses a 4th-order Runge–Kutta integrator to evolve particle trajectories, enforces reflective boundary conditions, and outputs step-by-step states to a file. Real-time progress tracking and timing are included to monitor performance.

## Features

* **Parallel Processing**: Utilizes Python's `multiprocessing.Pool` to distribute per-particle computations across all CPU cores (ideal for Apple Silicon or multicore systems).
* **Runge–Kutta Integration**: 4th-order RK step implemented in `rk4.py` for accurate time evolution.
* **Reflective Boundaries**: Particles reflect elastically off the walls of the box (`box.py`).
* **Real-Time Tracking**: Prints per-step completion status, elapsed time, and estimated time remaining (ETA).
* **Timing**: Measures total execution time for benchmarking.
* **Reliable Output**: Writes simulation states to a timestamped text file with immediate flushing to disk.

## Repository Structure

```plain
├── sim.py            # Main simulation script with parallelization & tracking
├── eqnmotion.py      # Defines the equations of motion (forces/interactions)
├── box.py            # Box geometry, boundary checks, and reflection logic
├── rk4.py            # 4th-order Runge–Kutta integration step
├── output.py         # Handles writing particle states to the output file
├── const.py          # Simulation parameters (N, box_size, dt, t_max, v_max)
├── energy.py         # (Optional) Computes energy diagnostics
├── README.md         # Project overview and instructions
└── sim_001.txt       # Example output file (generated after running)
```

## Requirements

* Python 3.8 or higher
* NumPy

Install dependencies with:

```bash
pip install numpy
```

## Installation & Setup

### Cloning or Initializing the Repository

If you've already created a repository on GitHub and it’s currently empty, add this project to it by running:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/particle-box-sim.git
git push -u origin main
```

Otherwise, to clone an existing repository:

```bash
git clone https://github.com/yourusername/particle-box-sim.git
cd particle-box-sim
```

4. Ensure your Python interpreter is set to a version ≥ 3.8.
5. (Optional) Create and activate a virtual environment:

   ```bash
   ```

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows

````
6. Install required packages:
   ```bash
pip install numpy
````

## Usage

Run the simulation with:

```bash
python sim.py
```

* Output will be written to `sim_001.txt` in the working directory.
* Console logs will display:

  * Working directory and output path
  * Total steps to simulate
  * Per-step completion, elapsed time, and ETA
  * Total execution time upon completion

To limit CPU usage, edit the pool size in `sim.py`:

```python
# Use only 4 worker processes:
pool = mp.Pool(processes=4)
```

## Customization

* **Simulation Parameters**: Modify `const.py` to change number of particles `N`, box size, timestep `dt`, total time `t_max`, and maximum initial velocity `v_max`.
* **Physics**: Extend or modify `eqnmotion.py` to include different force laws or interactions.
* **Diagnostics**: Use `energy.py` to compute and log energy conservation or add new metrics.

## Contributing

Contributions are welcome! Feel free to:

* Open issues for bugs or features
* Submit pull requests with improvements or new modules

Please follow standard GitHub workflows and add tests/documentation for any new code.

## License

This project is provided under the MIT License. See `LICENSE` for details.
