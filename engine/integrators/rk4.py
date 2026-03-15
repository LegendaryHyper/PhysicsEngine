class RungeKutta4:
    def step(self, body_system, dt, compute_forces):
        
        bodies = body_system.bodies
        n = len(bodies)
        
        pos0 = [b.position.copy() for b in bodies]
        vel0 = [b.velocity.copy() for b in bodies]
        
        compute_forces()

        k1_v = [b.force / b.mass for b in bodies]
        k1_x = [b.velocity.copy() for b in bodies]
        
        for i, b in enumerate(bodies):
            b.position = pos0[i] + 0.5*dt*k1_x[i]
            b.velocity = vel0[i] + 0.5*dt*k1_v[i]
        
        compute_forces()

        k2_v = [b.force / b.mass for b in bodies]
        k2_x = [b.velocity.copy() for b in bodies]
        
        for i, b in enumerate(bodies):
            b.position = pos0[i] + 0.5*dt*k2_x[i]
            b.velocity = vel0[i] + 0.5*dt*k2_v[i]
        
        compute_forces()

        k3_v = [b.force / b.mass for b in bodies]
        k3_x = [b.velocity.copy() for b in bodies]
        
        for i, b in enumerate(bodies):
            b.position = pos0[i] + dt*k3_x[i]
            b.velocity = vel0[i] + dt*k3_v[i]
        
        compute_forces()
        
        k4_v = [b.force / b.mass for b in bodies]
        k4_x = [b.velocity.copy() for b in bodies]
        
        for i, b in enumerate(bodies):
            b.position = pos0[i] + dt/6 * (k1_x[i] + 2 * k2_x[i] + 2 * k3_x[i] + k4_x[i])
            b.velocity = vel0[i] + dt/6 * (k1_v[i] + 2 * k2_v[i] + 2 * k3_v[i] + k4_v[i])