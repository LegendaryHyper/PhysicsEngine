class VelocityVerlet: 
    def step(self, body_system, dt, compute_forces):
        compute_forces()
        
        accels = []
        
        for body in body_system.bodies:
            accel = body.force / body.mass
            accels.append(accel)
            body.position += body.velocity * dt + 0.5*accel*dt*dt
        
        compute_forces()
        
        for body, accel_old in zip(body_system.bodies, accels):
            accel_new = body.force / body.mass
            body.velocity += 0.5 * (accel_old + accel_new) * dt
            