import pygame
import sys
from constants import *
from logger import log_state, log_event
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scores import load_high_scores, save_high_scores
from ui import draw_centered_text, display_high_scores, draw_menu, draw_input, draw_game_over
from setup import initialize_game

def main():
    screen, font, timer, updatable, drawable, asteroids, shots, high_scores = initialize_game()

    state = "MENU"
    dt = 0
    score = 0
    player_name = ""

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if state == "MENU":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    for sprite in updatable:
                        sprite.kill()
                    AsteroidField()
                    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    score = 0
                    state = "PLAYING"

            elif state == "INPUT_NAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        final_name = player_name if player_name.strip() else "Pilot"
                        high_scores.append({"name": final_name, "score": score})
                        high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:3]
                        save_high_scores(high_scores)
                        state = "GAME_OVER"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 10 and event.unicode.isprintable():
                            player_name += event.unicode

            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    for sprite in updatable:
                        sprite.kill()
                    AsteroidField()
                    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    score = 0
                    state = "PLAYING"

        screen.fill("black")

        if state == "MENU":
            draw_menu(screen, font, high_scores)

        elif state == "PLAYING":
            updatable.update(dt, score)

            for asteroid in asteroids:
                if asteroid.collides_with(my_player):
                    if state != "GAME_OVER" and state != "INPUT_NAME":
                        log_event("player_hit")
                        lowest_high_score = high_scores[-1]["score"]
                        if score > lowest_high_score:
                            state = "INPUT_NAME"
                            player_name = ""
                        else:
                            state = "GAME_OVER"
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

        elif state == "INPUT_NAME":
            draw_input(screen, font, player_name, score)

        elif state == "GAME_OVER":
            draw_game_over(screen, font, high_scores, score)

        pygame.display.flip()
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()