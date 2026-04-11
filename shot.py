import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt, *args):
        self.position += self.velocity * dt
        if (self.position.x > SCREEN_WIDTH or self.position.x < 0 or 
            self.position.y > SCREEN_HEIGHT or self.position.y < 0):
            self.kill()