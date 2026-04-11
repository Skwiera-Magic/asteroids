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
        hs_surface = font.render(f"{i+1}. {hs}", True, "white")
        screen.blit(hs_surface, (20, y_pos))