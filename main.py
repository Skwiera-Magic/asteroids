import pygame
import sys
from constants import *
from logger import log_state, log_event
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    timer = pygame.time.Clock()
    dt = 0
    score = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField()
    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    while True:
        log_state()
        font = pygame.font.Font(None, 36)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(my_player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collides_with(asteroid):
                    log_event("asteroid_shot")
                    if asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 1
                    elif asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += 3
                    else:
                        score += 2
                    bullet.kill()
                    asteroid.split()
        for draw in drawable:
            draw.draw(screen)
            score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()
