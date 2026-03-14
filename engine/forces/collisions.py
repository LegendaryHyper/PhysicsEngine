import numpy as np

def resolve_collisions(body_system, e):
    for i, body1 in enumerate(body_system.bodies):
        for j in range(i+1, len(body_system.bodies)):
            body2 = body_system.bodies[j]
            r = body2.position - body1.position
            dist = np.linalg.norm(r)
            if dist < body1.radius + body2.radius and dist != 0:
                n = r/dist
                slop = 1e-3
                overlap = body1.radius + body2.radius - dist
                
                if overlap > slop:
                    correction = n * overlap
                    body1.position -= correction * (body2.mass / (body1.mass + body2.mass))
                    body2.position += correction * (body1.mass / (body1.mass + body2.mass))
                
                v_rel = body2.velocity - body1.velocity
                vel_normal = np.dot(v_rel, n)
                if vel_normal > 0:
                    continue
                j = -(1 + e) * vel_normal
                j /= (1/body1.mass + 1/body2.mass)
                
                impulse = j * n
                
                body1.velocity -= impulse/body1.mass
                body2.velocity += impulse/body2.mass
                print("Colliding!")