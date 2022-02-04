import simulator
import parseXML


# Time variable
t = 0

# Scene object initialization
scene = parseXML.get_data('./tests/test-vortex.xml')

# Create window and draw initial frame
sim = simulator.Frame()
sim.new_frame(scene, 0)

# Run the simulation
while t <= scene.t_exit:
    # Update positions and velocities of all particles
    scene.step()

    # Draw the next frame
    sim.new_frame(scene, t)

    # Increment t
    t += scene.dt

    # Pause the frame
    sim.wait(scene.dt)
