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
grid_size = 50
screeny = 1500
border_width = grid_size*2 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (255,255,255, 255)
grid_colour = (0,0,0,255)
border_colour = (255, 0, 0, 255)
cell_colour = (160,160,160, 255)


# Timings
wait_time = 500
    
def draw_grid(background):

    for x in range(0, screenx, grid_size):
        pygame.draw.line(background, grid_colour, (x, 0), (x, screeny), 1)
        
    for y in range(0, screeny, grid_size):
        pygame.draw.line(background, grid_colour, (0, y), (screenx, y), 1)
    
    # Draw border
    border = pygame.Rect(0, 0, screenx - 1, screeny)
    pygame.draw.rect(background, border_colour, border, border_width)

class Cell():
    def __init__(self, x, y):
        self.start = (x,y)
        self.coord = [x,y]
        self.rect = Rect(self.coord[0], self.coord[1], grid_size-1, grid_size-1)
        self.colour = cell_colour
    
    def move(self, move):
        self.rect.move_ip(move[1])
        
        
def algorithm(current, background):

    # Define directions: [(coord translation), traversed border coord 1, traversed border coord 2]
    top = current.rect.top
    bottom = current.rect.bottom
    left = current.rect.left
    right = current.rect. right

    directions = [
                [(0, -grid_size), (left, top - 1), (right - 1, top - 1)], # N
                [(0, grid_size), (left, bottom), (right - 1, bottom)], # S
                [(grid_size, 0), (right, top), (right, bottom - 1)], # E
                [(-grid_size, 0), (left - 1, top), (left - 1, bottom - 1)], # W
            ]           
    rand = random.shuffle(directions)   # Shuffle order

    # Iterate over randomly ordered directions, checking whether moving into cell already visited
    for move in directions:
        test = current.rect.move(move[0])
        colour = background.get_at((test.left, test.top))   # Check unvisted based on colour

        # If in this direction unvisited, move current there, fill cell and erase border
        if colour != cell_colour and colour != border_colour:
            current.rect.move_ip(move[0])
            background.fill(current.colour, rect=current.rect)
            pygame.draw.line(background, current.colour, move[1], move[2])  # Erase traversed border
            
            time = pygame.time.get_ticks()                      # Wait
            while pygame.time.get_ticks() < time + wait_time: 
                pass
            break
        
        
            



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
    current = Cell(501, 1001)
    background.fill(current.colour, rect=current.rect)
    
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Launch window and define selected algorithm
    '''popup = window.AlgoSelectWindow()
    algorithm = popup.choice
    print(algorithm)'''

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        mouse = pygame.mouse.get_pos()
        
        algorithm(current,background)
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


