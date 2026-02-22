import numpy as np

def compute_energy_vert_grav(body, g=9.81):
    kinetic = 0.5 * body.mass * (body.velocity ** 2)
    kinetic = kinetic.sum(axis=1)
    
    potential = body.mass * g * body.position
    
    return kinetic + potential

def compute_energy_univ_grav(body_system, G=6.67e-11):

    bodies = body_system.bodies

    kinetic = 0.0
    for body in bodies:
        v2 = np.dot(body.velocity, body.velocity)
        kinetic += 0.5 * body.mass * v2

    potential = 0.0
    n = len(bodies)

    for i in range(n):
        for j in range(i+1, n):
            r_vec = bodies[j].position - bodies[i].position
            r = np.linalg.norm(r_vec)
            if r == 0:
                continue
            potential -= G * bodies[i].mass * bodies[j].mass / r

    return kinetic + potential