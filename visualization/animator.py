import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(simulation, body_system, dt, steps):
    
    fig, ax = plt.subplots()
    ax.set_xlim(-1000000000, 1000000000)
    ax.set_ylim(-1000000000, 1000000000)
    bodies = body_system.bodies
    
    points = []
    trails = []
    histories = []
    
    for body in bodies:
        p, = ax.plot([], [], 'ro')
        t, = ax.plot([], [], 'b-')
        points.append(p)
        trails.append(t)
        histories.append([[], []])
    
    def update(frame):
        simulation.step()
        artists = []
        
        for i, body in enumerate(bodies):
            x, y = body.position
            hx, hy = histories[i]
            
            hx.append(x)
            hy.append(y)
            
            points[i].set_data(x, y)
            trails[i].set_data(hx, hy)
            artists.append(points[i])
            artists.append(trails[i])
        return artists
    ani = FuncAnimation(fig, update, frames=steps, interval = 20, blit=True)
    plt.show()

def energy_graph(energy_method, body_system, dt, steps):
    fig, ax = plt.subplots()
    ax.set_xlim(-1000000000, 1000000000)
    ax.set_ylim(-1000000000, 1000000000)
    
    points = []
    trails = []
    histories = []
    bodies = body_system.bodies
    t = 0
    
    for body in bodies:
        p, = ax.plot([], [], 'ro')
        t, = ax.plot([], [], 'b-')
        points.append(p)
        trails.append(t)
        histories.append([[], []])
    
    
    
    def update(frame):
        artists = []
        
        for i, body in enumerate(bodies):
            energy = energy_method(body_system, body, G=6.67e-11)
            hx, hy = histories[i]
            t += dt
            
            hx.append(energy)
            hy.append(t)
            
            points[i].set_data(energy, t)
            trails[i].set_data(hx, hy)
            artists.append(points[i])
            artists.append(trails[i])
        return artists
        
    ani = FuncAnimation(fig, update, frames=steps, interval = 20, blit=True)