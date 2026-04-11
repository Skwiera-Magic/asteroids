import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        if self.position.distance_to(other.position) <= (self.radius + other.radius):
            return True
        else:
            return False

    def wrap(self):
        buffer = self.radius
        if self.position.x > SCREEN_WIDTH + buffer:
            self.position.x = - buffer
        elif self.position.x < - buffer:
            self.position.x = SCREEN_WIDTH + buffer

        
        if self.position.y > SCREEN_HEIGHT + buffer:
            self.position.y = - buffer
        elif self.position.y < - buffer:
            self.position.y = SCREEN_HEIGHT + buffer