from vpython import color, sphere, vector, scene, rate, local_light
import numpy as np

scene.title = "Solar System Simulation"
scene.width = 1200
scene.height = 800
scene.background = color.black
scene.range = 20
scene.forward = vector(0, -0.3, -1)

# Celestial bodies (name, color, orbit_radius, size, speed_multiplier)
bodies = [
    ("Mercury", color.gray(0.6), 4, 0.2, 4.7),
    ("Venus", color.orange, 6, 0.4, 3.5),
    ("Earth", color.blue, 8, 0.4, 3.0),
    ("Mars", color.red, 10, 0.3, 2.4),
    ("Jupiter", color.orange, 13, 0.8, 1.3),
    ("Saturn", color.yellow, 16, 0.7, 1.0),
    ("Uranus", color.cyan, 18.5, 0.5, 0.7),
    ("Neptune", color.blue, 21, 0.5, 0.5)
]

# Create the Sun
sun = sphere(pos=vector(0,0,0), radius=1.2, color=color.orange, emissive=True)

# Add light to the scene
local_light(pos=sun.pos, color=color.white)

# Create planets
planets = []
for name, col, orbit_radius, size, speed in bodies:
    p = sphere(pos=vector(orbit_radius,0,0),
               radius=size,
               color=col,
               make_trail=True,
               trail_type="curve",
               retain=200)
    p.orbit_radius = orbit_radius
    p.angle = np.random.rand() * 2 * np.pi  # random start angle
    p.speed = speed / orbit_radius
    planets.append(p)

# Animation loop
while True:
    rate(60)
    for p in planets:
        p.angle += p.speed * 0.01
        x = p.orbit_radius * np.cos(p.angle)
        z = p.orbit_radius * np.sin(p.angle)
        p.pos = vector(x, 0, z)

