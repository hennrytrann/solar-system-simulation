from vpython import *
import numpy as np
import random

scene.title = "Moving Solar System + Starship Refueling Mission"
scene.width = 1200
scene.height = 800
scene.background = color.black
scene.range = 25
scene.forward = vector(0, -0.3, -1)

# === Solar System Setup ===

# Sun
sun = sphere(pos=vector(0,0,0), radius=1.2, color=color.orange, emissive=True)
local_light(pos=sun.pos, color=color.white)

# Planet data
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

plane_tilt = radians(15)
system_velocity = vector(0, 0, -0.01)

planets = []
for name, col, orbit_radius, size, speed in bodies:
    pos = vector(orbit_radius, 0, 0).rotate(angle=plane_tilt, axis=vector(1,0,0))
    p = sphere(pos=pos, radius=size, color=col, make_trail=True, trail_type="curve", retain=200)
    p.orbit_radius = orbit_radius
    p.angle = random.uniform(0, 2*np.pi)
    p.speed = speed / orbit_radius
    planets.append(p)

# Stars
for _ in range(300):
    x, y, z = [random.uniform(-150, 150) for _ in range(3)]
    sphere(pos=vector(x,y,z), radius=0.1, color=color.white, emissive=True, opacity=random.uniform(0.3, 1))

# Grid
for i in range(-40, 41, 2):
    curve(pos=[vector(i,0,-40), vector(i,0,40)], color=color.gray(0.2))
    curve(pos=[vector(-40,0,i), vector(40,0,i)], color=color.gray(0.2))

# === Animate Planets ===

def update_planets():
    sun.pos += system_velocity
    for p in planets:
        p.angle += p.speed * 0.01
        x = p.orbit_radius * np.cos(p.angle)
        z = p.orbit_radius * np.sin(p.angle)
        pos = vector(x, 0, z).rotate(angle=plane_tilt, axis=vector(1,0,0))
        p.pos = pos + sun.pos

# === Starship Mission ===

earth = planets[2]
mars = planets[3]

# Launch ship
starship = cone(pos=earth.pos + vector(0, 0.5, 0),
                axis=vector(0, 1, 0),
                radius=0.1,
                color=color.red,
                make_trail=True,
                retain=100)

refuelers = []

def launch_to_orbit(ship, center, altitude=1.5, speed=0.2):
    angle = 0
    while angle < 2*np.pi:
        rate(60)
        update_planets()
        angle += speed * 0.02
        x = altitude * np.cos(angle)
        z = altitude * np.sin(angle)
        orbit_pos = vector(x, 0, z).rotate(angle=plane_tilt, axis=vector(1, 0, 0)) + center
        ship.pos = orbit_pos

# Starship launches
launch_to_orbit(starship, earth.pos)

# Refueling ships
for i in range(4):
    ref = cone(pos=earth.pos + vector(0, 0.5, 0),
               axis=vector(0, 1, 0),
               radius=0.07,
               color=color.green,
               make_trail=True,
               retain=50)
    refuelers.append(ref)
    launch_to_orbit(ref, earth.pos, altitude=1.6 + 0.1 * i)
    for _ in range(30):
        rate(30)
        update_planets()
        ref.pos += (starship.pos - ref.pos) * 0.05

# Pause for refueling
for _ in range(50):
    rate(30)
    update_planets()

# Transfer arc to Mars
def transfer_to_mars(ship, start, end, frames=300):
    for i in range(frames):
        rate(60)
        update_planets()
        t = i / frames
        theta = np.pi * t
        x = (1 - np.cos(theta)) * 0.5
        y = np.sin(theta)
        arc_pos = vector(x * (end.x - start.x),
                         y * 6,
                         x * (end.z - start.z))
        ship.pos = start + arc_pos

transfer_to_mars(starship, earth.pos, mars.pos)

# Clean up refuelers
for ref in refuelers:
    ref.visible = False
    ref.clear_trail()

# Mars orbit loop
for _ in range(200):
    rate(60)
    update_planets()
    angle = _ * 0.02
    r = 0.8
    offset = vector(r * np.cos(angle), 0.2, r * np.sin(angle))
    starship.pos = mars.pos + offset

