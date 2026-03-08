from engine.core.body import Body, BodySystem
from engine.core.simulation import Simulation
from engine.forces.forces import MutualGravity
from engine.integrators.semi_implicit_euler import SemiImplicitEuler

class OrbitalScenario:
    def create_simulation(self):
        earth = Body("Earth", 6e24, [0.0, 0.0], [0.0, 29780.0])
        moon = Body("Moon", 7.347673e22, [384000000.0, 0.0], [0.0, 30802.0])
        sun = Body("Sun", 1.9891e30, [-150000000000.0, 0.0], [0.0, 0.0])
        
        system = BodySystem([earth, moon, sun])
        gravity = MutualGravity()
        integrator = SemiImplicitEuler()

        sim_dt = 14400

        sim = Simulation(system, [gravity], integrator, dt=sim_dt)
        
        return sim