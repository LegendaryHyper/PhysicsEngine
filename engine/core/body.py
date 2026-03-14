import numpy as np

class Body:
    def __init__(self, name, mass, position, velocity, radius):
        
        """
        Masses: NumPy array of (m)
        Pos: " " " ([rX, rY])
        Velocities: " " " ([vX, vY])
        """
        self.name = name
        self.mass = np.array(mass, dtype=float)
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.force = np.zeros_like(position, dtype=float)
        self.radius = radius
    def clear_forces(self):
        self.force.fill(0.0)

class BodySystem:
    def __init__(self, bodies):
        self.bodies = bodies