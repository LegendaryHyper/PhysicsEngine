class ExplicitEuler:
    def step(self, system, dt, compute_forces):
        compute_forces()
        
        for body in system.bodies:
            body.position += body.velocity * dt
            accel = body.force / body.mass
            body.velocity += accel * dt