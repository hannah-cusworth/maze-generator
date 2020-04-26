import pygame.surfarray as surfarray
import numpy as np
import pygame
from pygame.locals import *
import window

pygame.init()

def main():
    pygame.init()
    # Initialise screen
    screen = pygame.display.set_mode((2500, 1500))
    pygame.display.set_caption('Visualiser')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 255, 0))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Launch window and define selected algorithm
    popup = window.AlgoSelectWindow()
    algorithm = popup.choice
    print(algorithm)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        pygame.display.update()

if __name__ == '__main__':main()
