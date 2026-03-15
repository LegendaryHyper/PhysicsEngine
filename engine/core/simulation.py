from engine.forces.forces import apply_force
from engine.forces.collisions import resolve_collisions
import time

class Simulation:
    def __init__(self, body_system, forces, integrator, dt):
        self.body_system = body_system
        self.forces = forces
        self.integrator = integrator
        self.dt = dt
        self.time = 0
        self.start_real_time = time.perf_counter()
        self.real_time = 0
        self.force_events = []
    
    def step(self):
        self.integrator.step(self.body_system, self.dt, self.compute_forces)
        self.time += self.dt
        self.real_time = time.perf_counter() - self.start_real_time
    def compute_forces(self):
        for body in self.body_system.bodies:
            body.force[:] = 0
        for force in self.forces:
            force.apply(self.body_system)
        alive_events = []
        for event in self.force_events:
            event.body.force += event.force
            event.remaining_time -= self.dt
            
            if event.remaining_time > 0:
                alive_events.append(event)
        self.force_events = alive_events
        for force_event in self.force_events:
            apply_force(force_event=force_event)
        for _ in range (3):
            resolve_collisions(body_system=self.body_system, e=0.1)