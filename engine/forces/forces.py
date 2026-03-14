import numpy as np

def apply_force(force_event):
        force_event.body.force += force_event.force

class Force:
    pass

class MutualGravity(Force):
    def __init__(self, G=6.67e-11):
        self.G = G
    
    def apply(self, body_system):
        bodies = body_system.bodies
        if len(bodies) > 1:
            for i, body1 in enumerate(bodies):
                for j in range(i + 1, len(bodies)):
                    body2 = bodies[j]
                    r = body2.position - body1.position
                    dist = np.linalg.norm(r)
                    if dist == 0:
                        continue
                    force_mag = self.G * body1.mass * body2.mass / dist**3
                    force = force_mag * r
                    body1.force += force
                    body2.force -= force

class DownwardsGravity(Force):
    def __init__(self, g=9.81):
        self.g = g
    
    def apply(self, body_system):
        bodies = body_system.bodies
        for i, body in enumerate(bodies):
            body.force[1] -= self.g * body.mass