# This file is part of the particle-in-a-box simulation written
# by Lex Wennmacher for educational purpose only. Do not re-distribute.

# sim.py: Main program for the simulation (parallelized) with timing, real-time tracking, and reliable output flushing

import numpy as np
import eqnmotion
import box
from const import N, box_size, dt, t_max, v_max
import random
from rk4 import rk4_step
from output import output
import multiprocessing as mp
import time
import os

outfile = "sim_001.txt"
simbox = box.box(0.0, box_size, 0.0, box_size)

# Print working directory and output path for debugging
print(f"Working directory: {os.getcwd()}")
print(f"Simulation output will be written to: {os.path.abspath(outfile)}")

# Initialize particle states: [x, y, vx, vy]
particles_s_old = np.zeros((N, 4))
for i in range(N):
    x = random.uniform(0.0, box_size)
    y = random.uniform(0.0, box_size)
    vx = random.uniform(-v_max, v_max)
    vy = random.uniform(-v_max, v_max)
    particles_s_old[i, :] = [x, y, vx, vy]

# Buffer for updated states
t_particles_new = np.zeros_like(particles_s_old)
particles_s_new = t_particles_new

def compute_particle(idx, particles):
    """Worker function to compute one RK4 step (with box boundary) for particle idx."""
    s_old = particles[idx, :]
    # First RK4 step on dt
    s_new = s_old + rk4_step(eqnmotion.eqnmotion, s_old,
                              particles, idx, dt)
    # Check for leaving box and handle reflection
    where, lambda_inters = simbox.left_box(s_old, s_new)
    if where is not None:
        # Partial step to intersection
        s_inters = s_old + rk4_step(eqnmotion.eqnmotion,
                                     s_old, particles,
                                     idx, lambda_inters * dt)
        # Reflect at wall
        s_inters = box.box.reflect(s_inters, where)
        # Remaining step after reflection
        s_new = s_inters + rk4_step(eqnmotion.eqnmotion,
                                     s_inters, particles,
                                     idx, (1.0 - lambda_inters) * dt)
    return idx, s_new

if __name__ == '__main__':
    # Record start time
    start_time = time.time()
    total_steps = int(np.ceil(t_max / dt))
    print(f"Simulation started: {total_steps} total steps")

    # Open output file and write initial state in line-buffered mode
    with open(outfile, 'w', buffering=1) as f:
        t = 0.0
        current_step = 0
        output(f, t, particles_s_old)
        f.flush()
        os.fsync(f.fileno())

        # Create a pool of worker processes
        pool = mp.Pool()

        # Time-stepping loop
        while current_step < total_steps:
            # Prepare arguments and execute in parallel
            args = [(i, particles_s_old) for i in range(N)]
            results = pool.starmap(compute_particle, args)

            # Unpack results into the new state buffer
            for idx, s_new in results:
                particles_s_new[idx, :] = s_new

            # Swap buffers for next iteration
            particles_s_old, particles_s_new = particles_s_new, particles_s_old

            # Advance time and step count
            current_step += 1
            t = current_step * dt

            # Write output and flush immediately
            output(f, t, particles_s_old)
            f.flush()
            os.fsync(f.fileno())

            # Real-time tracking: elapsed & ETA
            elapsed = time.time() - start_time
            avg_per_step = elapsed / current_step
            remaining_steps = total_steps - current_step
            eta = avg_per_step * remaining_steps
            print(f"Step {current_step}/{total_steps} completed at t={t:.3f}s | "
                  f"Elapsed: {elapsed:.2f}s | ETA: {eta:.2f}s")

        # Clean up the process pool
        pool.close()
        pool.join()

    # Compute and print total execution time
    end_time = time.time()
    total_elapsed = end_time - start_time
    print(f"Simulation completed in {total_elapsed:.2f} seconds")