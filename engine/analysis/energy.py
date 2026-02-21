import numpy as np

def compute_energy_vert_grav(body, g=9.81):
    kinetic = 0.5 * body.mass * (body.velocity ** 2)
    kinetic = kinetic.sum(axis=1)
    
    potential = body.mass * g * body.position
    
    return kinetic + potential

def compute_energy_univ_grav(body_system, body, G=6.67e-11):
    kinetic = 0.5 * body.mass * (body.velocity ** 2)
    kinetic = kinetic.sum(axis=1)
    
    bodies = body_system.bodies
    
    pot_w_vec = [0.0, 0.0] # Potential energy with vectors (even though energy is scalar, we must use vectors for the sake of calculation.)
    
    for i, body2 in enumerate(bodies):
        if body2 == body:
            continue
        r = body2.position - body.position
        dist = np.linalg.norm(r)
        if dist == 0:
            continue
        pot_w_vec_mag = G * body.mass * body2.mass / dist**2
        pot_w_vec += pot_w_vec_mag * r
    
    potential = np.linalg.norm(pot_w_vec)
    return kinetic + potential