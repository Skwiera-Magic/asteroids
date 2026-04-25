import pygame
import random
from circleshape import *
from constants import *
from logger import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = []
        num_vertices = 8
        for i in range(num_vertices):
            angle = i * (360 / num_vertices)
            p = pygame.Vector2(0, self.radius * random.uniform(0.7, 1.2))
            p = p.rotate(angle)
            self.points.append(p)

    def draw(self, screen):
        actual_points = [self.position + p for p in self.points]
        pygame.draw.polygon(screen, "white", actual_points, LINE_WIDTH)

    def update(self, dt, *args):
        self.position += self.velocity * dt
        self.wrap()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        velo1 = self.velocity.rotate(angle)
        velo2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = velo1 * 1.2
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2.velocity = velo2 * 1.2
