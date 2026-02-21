import numpy as np
import matplotlib.pyplot as plt

from engine.core.body import BodySystem, Body
from engine.core.simulation import Simulation
from engine.forces.forces import MutualGravity
from engine.integrators.semi_implicit_euler import SemiImplicitEuler
from engine.analysis.energy import compute_energy_vert_grav, compute_energy_univ_grav

from visualization.animator import animate, energy_graph

earth = Body(6e24, [0.0, 0.0], [0.0, 0.0])
moon = Body(7.347673e22, [384000000.0, 0.0], [0.0, 1022.0])

system = BodySystem([earth, moon])

gravity = MutualGravity()
integrator = SemiImplicitEuler()

sim_dt = 2880

sim = Simulation(system, [gravity], integrator, dt=sim_dt)

trajectory = []
energy = []
t_arr = []
t = 0

animate(sim, body_system=system, dt=sim_dt, steps=2000)
energy_graph(compute_energy_univ_grav, body_system=system, dt=sim_dt, steps=2000)