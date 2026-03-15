class Leapfrog: 
    def step(self, body_system, dt, compute_forces):
        compute_forces()
        
        for body in body_system.bodies:
            accel = body.force / body.mass
            body.velocity += 0.5 * accel * dt
        
        for body in body_system.bodies:
            body.position += body.velocity * dt
        
        compute_forces()
        
        for body in body_system.bodies:
            accel = body.force / body.mass
            body.velocity += 0.5 * accel * dt