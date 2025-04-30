from vpython import *
import numpy as np
import random

scene.title = "Moving Solar System with Stars and Reference Grid"
scene.width = 1200
scene.height = 800
scene.background = color.black
scene.range = 25
scene.forward = vector(0, -0.3, -1)

# Sun
sun = sphere(pos=vector(0,0,0), radius=1.2, color=color.orange, emissive=True)
local_light(pos=sun.pos, color=color.white)

# Planet data (name, color, orbit_radius, size, speed)
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

# Tilt and motion
plane_tilt = radians(15)  # orbital plane tilt
system_velocity = vector(0, 0, -0.01)  # drift through space

# Create planets
planets = []
for name, col, orbit_radius, size, speed in bodies:
    pos = vector(orbit_radius, 0, 0).rotate(angle=plane_tilt, axis=vector(1,0,0))
    p = sphere(pos=pos,
               radius=size,
               color=col,
               make_trail=True,
               trail_type="curve",
               retain=200)
    p.orbit_radius = orbit_radius
    p.angle = random.uniform(0, 2*np.pi)
    p.speed = speed / orbit_radius
    planets.append(p)

# Background stars
num_stars = 300
for _ in range(num_stars):
    x = random.uniform(-150, 150)
    y = random.uniform(-100, 100)
    z = random.uniform(-150, 150)
    star = sphere(pos=vector(x,y,z), radius=0.1, color=color.white, emissive=True, opacity=random.uniform(0.2, 1))

# Animate
while True:
    rate(60)
    
    # Move Sun
    sun.pos += system_velocity

    for p in planets:
        p.angle += p.speed * 0.01
        x = p.orbit_radius * np.cos(p.angle)
        z = p.orbit_radius * np.sin(p.angle)
        new_pos = vector(x, 0, z).rotate(angle=plane_tilt, axis=vector(1,0,0))
        p.pos = new_pos + sun.pos  # orbit relative to moving sun

    # Move planets' trails
    for obj in planets + [sun]:
        obj.clear_trail()

