import pygame.surfarray as surfarray
import numpy as np
import pygame
from pygame.locals import *
import window
import algorithms
import random

pygame.init()
# Dimensions
screenx = 2500
screeny = 1500

grid_size = 50
border_width = grid_size*2 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (255,255,255)
grid_colour = (0,0,0)
border_colour = (255, 0, 0)
cell_colour = (160,160,160)
    
def draw_grid(background):

    for x in range(0, screenx, grid_size + 1):
        pygame.draw.line(background, grid_colour, (x, 0), (x, screeny), 1)
        
    for y in range(0, screeny, grid_size + 1):
        pygame.draw.line(background, grid_colour, (0, y), (screenx, y), 1)
    
    # Draw border
    border = pygame.Rect(0, 0, screenx, screeny)
    pygame.draw.rect(background, border_colour, border, border_width)

class Cell():
    def __init__(self, x, y):
        self.start = (x,y)
        self.coord = [x,y]
        self.rect = Rect(self.coord[0], self.coord[1], grid_size, grid_size)
        self.colour = cell_colour
    def move(self):
        directions = {
            "North": (0, grid_size + 1),
            "South": (0, -grid_size - 1), 
            "East": (grid_size + 1, 0), 
            "West": (-grid_size - 1, 0)
            }
        move = random.choice(list(directions.items()))
        print(move[1])
        self.rect.move_ip(move[1])
        
        
    
        



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
    current = Cell(511,1021)
    background.fill(current.colour, rect=current.rect)
    for i in range(50):
        current.move()
        background.fill(current.colour, rect=current.rect)
        print(current.rect)

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


