import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def draw_centered_text(screen, font, text, color, y_offset):
    surface = font.render(text, True, color)
    x = (SCREEN_WIDTH // 2) - (surface.get_width() // 2)
    y = (SCREEN_HEIGHT // 2) + y_offset
    screen.blit(surface, (x, y))

def display_high_scores(screen, font, high_scores):
    y_pos = 20
    high_score_label = font.render("HIGH SCORES:", True, "gold")
    screen.blit(high_score_label, (20, y_pos))

    for i, hs in enumerate(high_scores):
        y_pos += 40
        hs_surface = font.render(f"{i+1}. {hs['name']} - {hs['score']}", True, "white")
        screen.blit(hs_surface, (20, y_pos))

def draw_menu(screen, font, high_scores):    
    display_high_scores(screen, font, high_scores)
    draw_centered_text(screen, font, "ASTEROIDS", "white", -20)
    draw_centered_text(screen, font, "Press ENTER to Start", "gray", 20)
    controls = font.render("Controls:", True, (255, 255, 255))
    wsad = font.render("WSAD - Ship controls", True, (255, 255, 255))
    spacebar = font.render("Space - Shoot", True, (255, 255, 255))
    screen.blit(controls, (20, SCREEN_HEIGHT - 120))
    screen.blit(wsad, (20, SCREEN_HEIGHT - 80))
    screen.blit(spacebar, (20, SCREEN_HEIGHT - 40))

def draw_input(screen, font, player_name, score):
    screen.fill("black")
    draw_centered_text(screen, font, "NEW HIGH SCORE!", "gold", -60)
    draw_centered_text(screen, font, f"Score: {score}", "white", -20)
    draw_centered_text(screen, font, "Enter your name", "white", 20)
    draw_centered_text(screen, font, "Max 10 digits", "white", 60)
    cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else " "
    draw_centered_text(screen, font, player_name + "_", "cyan", 100)
    draw_centered_text(screen, font, "Press ENTER to confirm", "gray", 160)

def draw_game_over(screen, font, high_scores, score):
    display_high_scores(screen, font, high_scores)
    draw_centered_text(screen, font, "GAME OVER", "red", -20)
    draw_centered_text(screen, font, f"Final Score: {score}", "white", 20)
    draw_centered_text(screen, font, "Press R to Restart", "white", 60)