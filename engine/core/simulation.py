class Simulation:
    def __init__(self, body_system, forces, integrator, dt):
        self.body_system = body_system
        self.forces = forces
        self.integrator = integrator
        self.dt = dt
        self.time = 0
    
    def step(self):
        for body in self.body_system.bodies:
            body.force[:] = 0
        for force in self.forces:
            force.apply(self.body_system)
        self.integrator.step(self.body_system, self.dt)
        self.time += self.dt
        print(f"Days: {self.time/86400}")