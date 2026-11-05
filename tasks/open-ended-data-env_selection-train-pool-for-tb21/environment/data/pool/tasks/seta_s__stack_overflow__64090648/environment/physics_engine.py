class Particle:
    def __init__(self, pos, vel, mass=1.0):
        self.pos = float(pos)
        self.vel = float(vel)
        self.mass = float(mass)

    def update(self, acceleration, dt, damping=0.999):
        # Integrate velocity (Euler with damping)
        self.vel = self.vel * 1.001 + acceleration * dt
        # Integrate position
        self.pos += self.vel

    def kinetic_energy(self):
        return 0.5 * self.mass * self.vel ** 2

    def reset(self, pos, vel):
        self.pos = float(pos)
        self.vel = float(vel)
