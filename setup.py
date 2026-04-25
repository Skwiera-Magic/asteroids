import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scores import load_high_scores

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    timer = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    high_scores = load_high_scores()

    explosion_sound = None
    hit_sound = None
    shot_sound = None

    try:
        pygame.mixer.init()
        explosion_sound = pygame.mixer.Sound("sound1.wav")
        explosion_sound.set_volume(0.3)
        hit_sound = pygame.mixer.Sound("sound2.wav")
        hit_sound.set_volume(0.3)
        shot_sound = pygame.mixer.Sound("sound3.wav")
        shot_sound.set_volume(0.3)
    except pygame.error:
        print("Warning: Audio device not found, playing without sound.")


    return (
        screen, font, timer, updatable, drawable, asteroids, shots, high_scores,
        explosion_sound, hit_sound, shot_sound
        )