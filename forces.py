import numpy as np


fs = []


# Class for forces
class Force(object):
    def __init__(self, force):
        fs.append(force)

    def calculate_grad_E(self):
        raise NotImplementedError


# Constant gravity force
class SimpleGravity(Force):
    def __init__(self, gx=0, gy=-9.8):
        super().__init__(self)
        self.const = [gx, gy]

    def calculate_grad_E(self, scene):
        grad_E = np.array([0 for i in range(len(scene.q))])
        i = 0
        while i < len(scene.q):
            grad_E[i] = scene.m[i // 2] * self.const[0]
            grad_E[i + 1] = scene.m[i // 2] * self.const[1]
            i += 2
        return -grad_E


class CentripetalForce(Force):
    def __init__(self):
        super().__init__(self)

    def calculate_grad_E(self, scene):
        grad_E = np.array([0 for i in range(len(scene.q))])
        i = 0
        while i < len(scene.q):
            x = scene.q[i]
            y = scene.q[i + 1]
            r = np.sqrt(x**2 + y**2)
            theta = np.pi / 2
            if x != 0:
                theta = np.arctan2(y, x)
            v2 = scene.q_dot[i]**2 + scene.q_dot[i + 1]**2
            if x == 0 and y == 0:
                grad_E[i] = 0
                grad_E[i + 1] = 0
            else:
                grad_E[i] = -scene.m[i // 2] * v2 / r * np.cos(theta)
                grad_E[i + 1] = -scene.m[i // 2] * v2 / r * np.sin(theta)
            i += 2
        return -grad_E


# Calculate energy gradient created by ALL forces
def total_grad_E(scene):
    total_grad_E = 0
    for f in fs:
        total_grad_E += f.calculate_grad_E(scene)
    return total_grad_E
