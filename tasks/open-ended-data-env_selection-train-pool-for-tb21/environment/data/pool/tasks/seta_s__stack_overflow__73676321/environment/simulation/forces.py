import numpy as np


def compute_gravity(particle, g=9.81):
    """Apply gravitational force. Positive y is downward."""
    return 0.0, particle.mass * g


def compute_buoyancy(particle, fluid_density, fluid_top, fluid_bottom, g=9.81):
    """Compute buoyancy force based on submerged area in a 2D fluid region.

    Buoyancy is proportional to the displaced fluid area (2D cross-section)
    times the fluid density times gravity, acting upward.
    """
    obj_top = particle.top
    obj_bottom = particle.bottom

    overlap_top = max(obj_top, fluid_top)
    overlap_bottom = min(obj_bottom, fluid_bottom)

    if overlap_bottom <= overlap_top:
        return 0.0, 0.0

    submerged_height = overlap_bottom - overlap_top
    submerged_area = submerged_height * particle.width

    buoyancy_force = -fluid_density * submerged_area * g
    return 0.0, buoyancy_force


def compute_drag(particle, fluid_density, fluid_top, fluid_bottom, drag_coeff=0.47):
    """Compute drag force opposing motion, proportional to submerged area.

    Drag = -0.5 * Cd * rho * A * |v| * v  (opposing velocity direction)
    """
    obj_top = particle.top
    obj_bottom = particle.bottom

    overlap_top = max(obj_top, fluid_top)
    overlap_bottom = min(obj_bottom, fluid_bottom)

    if overlap_bottom <= overlap_top:
        return 0.0, 0.0

    submerged_height = overlap_bottom - overlap_top
    submerged_area = submerged_height * particle.width

    speed = particle.speed
    if speed < 1e-10:
        return 0.0, 0.0

    drag_magnitude = 0.5 * drag_coeff * fluid_density * submerged_area * speed

    if particle.vx > 0:
        drag_fx = drag_magnitude * (particle.vx / speed)
    else:
        drag_fx = drag_magnitude * (particle.vx / speed)

    if particle.vy > 0:
        drag_fy = drag_magnitude * (particle.vy / speed)
    else:
        drag_fy = drag_magnitude * (particle.vy / speed)

    return drag_fx, drag_fy
