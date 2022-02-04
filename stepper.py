# Updates the positions and velocities of particles using the explicit euler method
def explicit_euler(q, q_dot, grad_E, m, dt):
    for i in range(len(q)):
        q[i] = q[i] + dt * q_dot[i]
        q_dot[i] = q_dot[i] - dt * grad_E[i] / m[i // 2]
    return q, q_dot
