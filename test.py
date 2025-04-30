from vpython import * 
from vpython import plane_tilt, p
import numpy as np
import random
import time

# ... [assume previous solar system code is already running up to "while True"]

# === STARSHIP SIMULATION START === #
planets = []
for name, col, orbit_radius, size, speed in bodies:
    # [planet creation]
    planets.append(p)

# Use Earth and Mars references from existing planet list
earth = planets[2]  # assuming Earth is 3rd in list
mars = planets[3]   # Mars



# Create launch ship
starship = cone(pos=earth.pos + vector(0, 0.5, 0),
                axis=vector(0, 1, 0),
                radius=0.1,
                color=color.red,
                make_trail=True,
                retain=100)

# Refueling ships (just visuals, will orbit Earth)
refuelers = []

def launch_to_orbit(ship, center, altitude=1.5, speed=0.2, tilt_angle=plane_tilt):
    """Simulates circular orbit by updating position in a thread."""
    angle = 0
    while angle < 2*np.pi:
        rate(60)
        angle += speed * 0.02
        x = altitude * np.cos(angle)
        z = altitude * np.sin(angle)
        orbit_pos = vector(x, 0, z).rotate(angle=tilt_angle, axis=vector(1, 0, 0)) + center
        ship.pos = orbit_pos
    return ship

# === Stage 1: Starship Launches to Earth Orbit ===
launch_to_orbit(starship, earth.pos)

# === Stage 2: Refuelers Launch and Cluster Around Starship ===
for i in range(4):  # 4 refuelers
    ref = cone(pos=earth.pos + vector(0, 0.5, 0),
               axis=vector(0, 1, 0),
               radius=0.07,
               color=color.green,
               make_trail=True,
               retain=50)
    refuelers.append(ref)
    launch_to_orbit(ref, earth.pos, altitude=1.6 + 0.1 * i)
    # Drift toward starship to cluster
    for _ in range(30):
        rate(30)
        ref.pos += (starship.pos - ref.pos) * 0.05

# === Refueling Pause ===
for _ in range(50):
    rate(30)

# === Stage 3: Starship Burns Toward Mars ===
def transfer_to_mars(ship, start, end, frames=300):
    """Simulates an elliptical transfer arc from Earth to Mars."""
    for i in range(frames):
        rate(60)
        t = i / frames
        theta = np.pi * t  # half ellipse
        x = (1 - np.cos(theta)) * 0.5
        y = np.sin(theta)
        arc_pos = vector(x * (end.x - start.x),
                         y * 6,  # height of arc
                         x * (end.z - start.z))
        ship.pos = start + arc_pos

transfer_to_mars(starship, earth.pos, mars.pos)

# Fade out refuelers
for ref in refuelers:
    ref.visible = False
    ref.clear_trail()

# Optional: leave Starship orbiting Mars
for _ in range(200):
    rate(60)
    angle = _ * 0.02
    r = 0.8
    offset = vector(r * np.cos(angle), 0.2, r * np.sin(angle))
    starship.pos = mars.pos + offset

