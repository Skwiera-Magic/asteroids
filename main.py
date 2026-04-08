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
    state = "MENU"
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
    game_over = False
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField()
    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    font = pygame.font.Font(None, 36)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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
            title_text = font.render("ASTEROIDS", True, (255, 255, 255))
            start_text = font.render("Press ENTER to Start", True, (200, 200, 200))
            controls = font.render("Controls:", True, (255, 255, 255))
            wsad = font.render("WSAD - Ship controls", True, (255, 255, 255))
            spacebar = font.render("Space - Shoot", True, (255, 255, 255))
            screen.blit(title_text, ((SCREEN_WIDTH / 2) - (title_text.get_width() / 2), SCREEN_HEIGHT / 2 - 20))
            screen.blit(start_text, ((SCREEN_WIDTH / 2) - (start_text.get_width() / 2), SCREEN_HEIGHT / 2 + 20))
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
            if game_over:
                state = "GAME_OVER"
            score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surface, (10, 10))
        elif state == "GAME_OVER":
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            final_score_text = font.render(f"Final score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to start again", True, (255, 255, 255))
            screen.blit(game_over_text, ((SCREEN_WIDTH / 2) - (game_over_text.get_width() / 2), SCREEN_HEIGHT / 2 - 20))
            screen.blit(final_score_text, ((SCREEN_WIDTH / 2) - (final_score_text.get_width() / 2), SCREEN_HEIGHT / 2 + 20))
            screen.blit(restart_text, ((SCREEN_WIDTH / 2) - (restart_text.get_width() / 2), SCREEN_HEIGHT / 2 + 60))
        pygame.display.flip()
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()
