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

def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
            scores = []
            for line in lines:
                scores.append(int(line.strip()))
            return sorted(scores + [0, 0, 0], reverse = True)[:3]
    except (FileNotFoundError, ValueError):
        return [0, 0, 0]

def save_high_scores(scores):
    with open("high_scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")

def display_high_scores(screen, font, high_scores):
    y_pos = 20
    high_score_label = font.render("HIGH SCORES:", True, "gold")
    screen.blit(high_score_label, (20, y_pos))

    for i, hs in enumerate(high_scores):
        y_pos += 40
        hs_surface = font.render(f"{i+1}. {hs}", True, "white")
        screen.blit(hs_surface, (20, y_pos))

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
    high_scores = load_high_scores()

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
            display_high_scores(screen, font, high_scores)
            draw_centered_text(screen, font, "ASTEROIDS", "white", -20)
            draw_centered_text(screen, font, "Press ENTER to Start", "gray", 20)
            controls = font.render("Controls:", True, (255, 255, 255))
            wsad = font.render("WSAD - Ship controls", True, (255, 255, 255))
            spacebar = font.render("Space - Shoot", True, (255, 255, 255))
            screen.blit(controls, (20, SCREEN_HEIGHT - 120))
            screen.blit(wsad, (20, SCREEN_HEIGHT - 80))
            screen.blit(spacebar, (20, SCREEN_HEIGHT - 40))

        elif state == "PLAYING":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(my_player):
                    if state != "GAME_OVER":
                        log_event("player_hit")
                        state = "GAME_OVER"
                        high_scores.append(score)
                        high_scores = sorted(high_scores, reverse=True)[:3]
                        save_high_scores(high_scores)
                        break

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
            display_high_scores(screen, font, high_scores)
            draw_centered_text(screen, font, "GAME OVER", "red", -20)
            draw_centered_text(screen, font, f"Final Score: {score}", "white", 20)
            draw_centered_text(screen, font, "Press R to Restart", "white", 60)

        pygame.display.flip()
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()