import numpy as np
import stepper
import forces


# Object to hold data for each frame
class Scene(object):
    def __init__(self, num_particles, t_exit, dt, dimensions=2):
        # Particles
        self.q = [0 for i in range(num_particles * dimensions)]
        self.q_dot = [0 for i in range(num_particles * dimensions)]
        self.r = [0 for i in range(num_particles)]
        self.m = [1 for i in range(num_particles)]
        self.fixed = [0 for i in range(num_particles)]
        self.color = [(0, 0, 0) for i in range(num_particles)]

        # Planes
        self.plane_q = []
        self.plane_n = []
        self.plane_color = []

        # Time
        self.t = 0
        self.t_exit = t_exit
        self.dt = dt

    def step(self):
        self.q, self.q_dot = stepper.explicit_euler(
            self.q, self.q_dot, forces.total_grad_E(self), self.m, self.dt)

    # Add a particle to the scene
    def add_particle(self, p):
        id = int(p['id'])
        if 'x' in p.keys():
            self.q[id * 2] = float(p['x'])
        else:
            self.q[id * 2] = 0
        if 'y' in p.keys():
            self.q[id * 2 + 1] = float(p['y'])
        else:
            self.q[id * 2 + 1] = 0
        if 'vx' in p.keys():
            self.q_dot[id * 2] = float(p['vx'])
        else:
            self.q_dot[id * 2] = 0
        if 'vy' in p.keys():
            self.q_dot[id * 2 + 1] = float(p['vy'])
        else:
            self.q_dot[id * 2 + 1] = 0
        if 'radius' in p.keys():
            self.r[id] = int(p['radius'])
        else:
            self.r[id] = 20
        if 'm' in p.keys():
            self.m[id] = float(p['m'])
        else:
            self.m[id] = 1
        if 'r' in p.keys():
            self.color[id] = (int(p['r']), int(p['g']), int(p['b']))
        else:
            self.color[id] = (0, 0, 0)
        if 'fixed' in p.keys():
            self.fixed = 0

    # Add a list of particles to the scene
    def add_particles(self, ps):
        for p in ps:
            self.add_particle(p)

    # Add a plane to the scene
    def add_plane(self, p):
        self.plane_q.append(np.array([0, 0]))
        self.plane_n.append(np.array([0, 1]))
        self.plane_color.append((0, 0, 0))
        if 'x' in p.keys():
            self.plane_q[-1][0] = int(p['x'])
        if 'y' in p.keys():
            self.plane_q[-1][1] = int(p['y'])
        if 'nx' in p.keys():
            self.plane_n[-1][0] = int(p['nx'])
        if 'ny' in p.keys():
            self.plane_n[-1][1] = int(p['ny'])
        if 'r' in p.keys():
            self.plane_color[-1] = (int(p['r']), int(p['g']), int(p['b']))

    # Add a list of planes to the scene
    def add_planes(self, ps):
        for p in ps:
            self.add_plane(p)
