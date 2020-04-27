import pygame.surfarray as surfarray
import numpy as np
import pygame
from pygame.locals import *
import window
import algorithms

pygame.init()
# Dimensions
screenx = 2500
screeny = 1500

grid_size = 20
border_width = 40 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (255,255,255)
grid_colour = (0,0,0)
border_colour = (255, 0, 0)
cell_colour = (0,0,255)
    
def draw_grid(background):

    for x in range(0, screenx, grid_size):
        pygame.draw.line(background, grid_colour, (x, 0), (x, screeny), 1)
        
    for y in range(0, screeny, grid_size):
        pygame.draw.line(background, grid_colour, (0, y), (screenx, y), 1)
    
    # Draw border
    border = pygame.Rect(0, 0, screenx, screeny)
    pygame.draw.rect(background, border_colour, border, border_width)

class Cell():
    def __init__(self, start):
        self.start = start
        self.dirnx = 0
        self.dirny = 0
        self.colour = cell_colour

    def draw(self, background):
        pygame.draw.rect(background, self.colour, self.start)

def main():
    pygame.init()
    # Initialise screen
    screen = pygame.display.set_mode((screenx, screeny))
    pygame.display.set_caption('Visualiser')

    # Create background and draw grid
    background = pygame.Surface(screen.get_size())
    background.convert()
    background.fill(background_colour)
    draw_grid(background)

    # Create cell
    start = Rect(300,300,20,20)
    current = Cell(start)
    current.draw(background)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    '''# Launch window and define selected algorithm
    popup = window.AlgoSelectWindow()
    algorithm = popup.choice
    print(algorithm)'''

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        pygame.display.update()

if __name__ == '__main__':main()


