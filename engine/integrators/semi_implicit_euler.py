class SemiImplicitEuler:
    def step(self, system, dt, compute_forces):
        compute_forces()
        for body in system.bodies:
            accel = body.force / body.mass
            body.velocity += accel * dt
            body.position += body.velocity * dt