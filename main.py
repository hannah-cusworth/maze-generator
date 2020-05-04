import pygame.surfarray as surfarray
import numpy as np
import pygame
from pygame.locals import *
import window
import algorithms
import random


pygame.init()

# Dimensions
info = pygame.display.Info()
grid = 50
screenx = int((info.current_w * 0.75)  - ((info.current_w*0.75) % grid))
grid_size = int(screenx/grid)
screeny = int(screenx * 0.6) - (int(screenx * 0.6) % grid_size)
border_width = grid_size*2 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (160,160,160, 255)
grid_colour = (0,0,0,255)
border_colour = (255, 0, 0, 255)
cell_colour = (200,200,200, 255)
start_colour = (0,0,255, 255)
final_colour = (255, 255, 255, 255)
current_colour = (0,255,0,255)
set_colours = [(random.randint(1,255), random.randint(1,255), random.randint(1,255), 255) for i in range(grid-2)] # keep between 1 and 255 to exclude border/grid/background

# Timings
wait_time = 10

# Control set up 
recursive = False
    
def draw_grid(background):

    for x in range(0, screenx, grid_size):
        pygame.draw.line(background, grid_colour, (x, 0), (x, screeny), 1)
        
    for y in range(0, screeny, grid_size):
        pygame.draw.line(background, grid_colour, (0, y), (screenx, y), 1)
   
def draw_border(background):
    border = pygame.Rect(0, 0, screenx - 1, screeny)
    pygame.draw.rect(background, border_colour, border, border_width)


class Cell():
    def __init__(self, x, y):
        self.start = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.coord = (x,y)
        self.rect = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.colour = None
    
    def test_colour_adjacent(self, dx, dy, background):
        test = Cell(self.coord[0] + dx, self.coord[1] + dy)
        adjacent_colour = background.get_at((test.rect.left, test.rect.top))
        return adjacent_colour == self.colour

    def get_colour_adjacent(self, dx, dy, background):
        test = Cell(self.coord[0] + dx, self.coord[1] + dy)
        adjacent_colour = background.get_at((test.rect.left, test.rect.top))
        return adjacent_colour 

    
class Row():
    def __init__(self, y):
        self.y = (grid_size * y) + 1 
        border = Cell(0,y)
        border.colour = border_colour
        self.border = border
        self.cells = [border]
    
        for i in range(1, grid-1):
            new = Cell(i, y)
            if y == 1:
                new.colour = set_colours[0]
            else: 
                new.colour = random.choice([random.choice(set_colours), new.get_colour_adjacent(0,1,background)])
            index = set_colours.index(new.colour)
            set_colours.pop(index)
            self.cells.append(new)
        self.cells.append(border)
        
    
    def merge_same_horizontal(self, background):
        for cell in self.cells:
            if cell.test_colour_adjacent(1,0,background):
                pygame.draw.line(background, cell.colour, (cell.rect.right, cell.rect.top), (cell.rect.right, cell.rect.bottom -1))
    
    def set_random_same(self, background):
        set_count = grid - len(set_colours)
        merge_count = int(set_count * 0.2)
        for i in range(merge_count):
            index = random.randint(1,grid_size-2)
            curr = self.cells[index]   # select random cell from row
            print("hannah")
            print(curr.colour)
            direction = random.choice([1,-1])
            print(curr.test_colour_adjacent(direction,0,background))
            while curr.test_colour_adjacent(direction,0,background):
                index += direction
                curr = self.cells[index]
            adj_colour = curr.get_colour_adjacent(direction,0,background)
            new_colour = curr.colour
            print(adj_colour)
            if adj_colour == self.border.colour:
                return
            set_colours.append(adj_colour)
            while curr.get_colour_adjacent(direction,0,background) == adj_colour:
                index += direction
                curr = self.cells[index]
                curr.colour = new_colour
        
    
    def draw(self, background):
        for cell in self.cells:
            background.fill(cell.colour, rect=cell.rect)
            print(cell.colour)
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbooooooooooooobbbbb")

        

    def merge_vertical(self, background, row):
        pass

    
            

            
        

    
    

        
        
            



def main():
    pygame.init()
    # Initialise screen
    screen = pygame.display.set_mode((screenx, screeny))
    pygame.display.set_caption('Visualiser')

    # Set events
    allowed = [MOUSEBUTTONUP, MOUSEBUTTONDOWN]
    pygame.event.set_allowed(allowed)

    # Create background and draw grid
    background = pygame.Surface(screen.get_size())
    background.convert()
    
    if recursive:
        background.fill(background_colour)
        draw_grid(background)
    if not recursive:
        background.fill(grid_colour)
        row = Row(1)
        row.draw(background)
        row.set_random_same(background)
        row.merge_same_horizontal(background)
        row.draw(background)
    draw_border(background)
    

    # Set up start
    highlighted_cell = Cell(48,1)
    background.fill(start_colour, rect=highlighted_cell)
    current_cell = None
   
    
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
            if recursive:
                if event.type == MOUSEBUTTONDOWN and colour != border_colour:
                    current_cell = highlighted_cell
        if recursive:
            if not current_cell:
                mouse = pygame.mouse.get_pos()
                colour = background.get_at(mouse)
                if colour == background_colour:
                    background.fill(background_colour, rect=highlighted_cell)
                    x = int((mouse[0] - 1) / grid_size)
                    y = int((mouse[1] - 1)/ grid_size)
                    highlighted_cell = Cell(x,y)
                    background.fill(start_colour, rect=highlighted_cell)
                    screen.blit(background, (0,0))
            
            else:
                background.fill(start_colour, current_cell.start)
                algorithms.recursive_backtracker(current_cell, background)
        
        if not recursive:
            pass
            

            
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


