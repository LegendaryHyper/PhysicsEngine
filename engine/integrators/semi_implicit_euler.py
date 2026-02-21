class SemiImplicitEuler:
    def step(self, system, dt):
        for body in system.bodies:
            accel = body.force / body.mass
            body.velocity += accel * dt
            body.position += body.velocity * dt