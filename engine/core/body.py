import numpy as np

class Body:
    def __init__(self, mass, position, velocity):
        
        """
        Masses: NumPy array of (m)
        Pos: " " " ([rX, rY])
        Velocities: " " " ([vX, vY])
        """
        
        self.mass = np.array(mass, dtype=float)
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.force = np.zeros_like(position, dtype=float)
    def clear_forces(self):
        self.force.fill(0.0)

class BodySystem:
    def __init__(self, bodies):
        self.bodies = bodies