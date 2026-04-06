import pygame
from constants import *
from logger import log_state
from circleshape import *
from player import Player

def main():
    pygame.init()
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    my_player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    timer = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        my_player.draw(screen)
        pygame.display.flip()
        timer.tick(60)
        dt = timer.tick(60) / 1000

if __name__ == "__main__":
    main()
