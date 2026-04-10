import pygame
import sys
from constants import *
from logger import log_state, log_event
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def draw_centered_text(screen, font, text, color, y_offset):
    surface = font.render(text, True, color)
    x = (SCREEN_WIDTH // 2) - (surface.get_width() // 2)
    y = (SCREEN_HEIGHT // 2) + y_offset
    screen.blit(surface, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    timer = pygame.time.Clock()

    state = "MENU"
    dt = 0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    AsteroidField()
                    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    state = "PLAYING"

            if state == "GAME_OVER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for sprite in updatable:
                        sprite.kill()
                    AsteroidField()
                    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    score = 0
                    state = "PLAYING"

        screen.fill("black")

        if state == "MENU":
            draw_centered_text(screen, font, "ASTEROIDS", "white", -20)
            draw_centered_text(screen, font, "Press ENTER to Start", "gray", 20)
            controls = font.render("Controls:", True, (255, 255, 255))
            wsad = font.render("WSAD - Ship controls", True, (255, 255, 255))
            spacebar = font.render("Space - Shoot", True, (255, 255, 255))
            screen.blit(controls, (20, 20))
            screen.blit(wsad, (20, 60))
            screen.blit(spacebar, (20, 100))

        elif state == "PLAYING":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(my_player):
                    log_event("player_hit")
                    state = "GAME_OVER"
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

        elif state == "GAME_OVER":
            draw_centered_text(screen, font, "GAME OVER", "red", -20)
            draw_centered_text(screen, font, f"Final Score: {score}", "white", 20)
            draw_centered_text(screen, font, "Press R to Restart", "white", 60)

        pygame.display.flip()
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()