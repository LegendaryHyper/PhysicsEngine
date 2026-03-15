from engine.core.body import Body, BodySystem
from engine.core.simulation import Simulation
from engine.forces.forces import DownwardsGravity
from engine.integrators.semi_implicit_euler import SemiImplicitEuler

class EarthSurfaceScenario:
    def create_simulation(self):
        ball = Body("Ball", mass=1.0, position=[0.0, 100.0], velocity=[10.0, 0.0], radius=1.0)
        system = BodySystem([ball])

        gravity = DownwardsGravity(g=9.81) 
        integrator = SemiImplicitEuler()
        
        return Simulation(system, [gravity], integrator, dt=0.01)