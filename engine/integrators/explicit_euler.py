class ExplicitEuler:
    def step(self, system, dt):
        for body in system.bodies:
            body.position += body.velocity * dt
            accel = body.force / body.mass
            body.velocity += accel * dt