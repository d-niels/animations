import xml.etree.ElementTree as ET
import forces
import scene as sc


# Extract the arguments from the xml dictionary
def get_args(d):
    args = ''
    for key in d.keys():
        args += key
        args += '='
        args += d[key]
        args += ', '

    return args[:len(args)-2]


# Construct initial scene using data from an XML file and return the scene
def get_data(path_to_xml):
    tree = ET.parse(path_to_xml)
    root = tree.getroot()
    particles = []
    planes = []
    t_exit = float(root.attrib['t'])
    dt = float(root.attrib['dt'])
    for child in root:
        if child.tag == 'particle':
            particles.append(child.attrib)
        if child.tag == 'plane':
            planes.append(child.attrib)
        if child.tag == 'simplegravity':
            eval(f'forces.SimpleGravity({get_args(child.attrib)})')
        if child.tag == 'centripetalforce':
            eval(f'forces.CentripetalForce({get_args(child.attrib)})')

    # Create the scene object
    scene = sc.Scene(len(particles), t_exit, dt)

    # Add particles to the scene
    scene.add_particles(particles)

    # Add planes to the scene
    scene.add_planes(planes)

    return scene
