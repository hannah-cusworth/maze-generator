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
set_colours = [(random.randint(1,255), random.randint(1,255), random.randint(1,255), 255) for bob in range(grid-1)] # keep between 1 and 255 to exclude border/grid/background

# Timings
wait_time = 800


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

def wait():
    time = pygame.time.get_ticks()                      # Wait
    while pygame.time.get_ticks() < time + wait_time: 
        pass


class Cell():
    def __init__(self, x, y):
        self.start = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.coord = (x,y)
        self.rect = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.colour = None
        self.index = x
        self.merge = False
        

    
class Row():
    def __init__(self, y, prev):
        self.y = (grid_size * y) + 1 
        border = Cell(0,y)
        border.colour = border_colour
        self.border = border
        self.cells = [border]
        self.lines = []

        for i in range(1, grid-1):
            new = Cell(i, y)
            if y == 1:
                new.colour = set_colours[0]
                
            else: 
                triple = self.get_triple(i, prev)
                adj_colour = triple[1]
                if triple[2] == adj_colour or (triple[0] == adj_colour and self.cells[i-1].colour == adj_colour):
                    new.colour = random.choice([adj_colour, random.choice(set_colours)])
                    
                else: 
                    new.colour = adj_colour 
            try:      
                index = set_colours.index(new.colour)
                set_colours.pop(index)
            except:
                pass
            self.cells.append(new)    
        self.cells.append(border)
          
    def test_colour_adjacent(self, cell, dx):
        adjacent_colour = self.cells[cell.index +dx].colour
        return adjacent_colour == cell.colour

    def get_colour_adjacent(self, cell, dx):
        return self.cells[cell.index + dx].colour
    
    def get_triple(self, i, prev):
        return [prev.cells[i -1].colour, prev.cells[i].colour, prev.cells[i+1].colour]
    
    def merge_same_horizontal(self, background):
        for cell in self.cells:
            if self.test_colour_adjacent(cell, 1) and cell.merge:
                pygame.draw.line(background, cell.colour, (cell.rect.right, cell.rect.top), (cell.rect.right, cell.rect.bottom -1))
                self.lines.append(((cell.rect.right, cell.rect.top), (cell.rect.right, cell.rect.bottom -1)))
    
    def set_random_same(self, background):
        set_count = grid - len(set_colours)
        merge_count = int(set_count * 0.2)
        for i in range(merge_count):
            index = random.randint(1,grid-2)
            curr = self.cells[index]   # select random cell from row
            direction = random.choice([1,-1])
            while self.test_colour_adjacent(curr, direction):
                index += direction
                curr = self.cells[index]
            new_colour = curr.colour
            adj_colour = self.get_colour_adjacent(curr, direction)

            if adj_colour == border_colour:
                return
            curr.merge=True
            set_colours.append(adj_colour)
            while self.get_colour_adjacent(curr,direction) == adj_colour:
                index += direction
                curr = self.cells[index]
                curr.colour = new_colour
        
    
    def draw(self, background):
        for cell in self.cells:
            background.fill(cell.colour, rect=cell.rect)
            

        

    def merge_vertical(self, prev, background):
        for x, cell in enumerate(self.cells):
            if cell.colour == prev.cells[x].colour:
                pygame.draw.line(background, cell.colour, (cell.rect.left, cell.rect.top - 1), (cell.rect.right - 1, cell.rect.top - 1))


    
            

            
        

    
    

        
        
            



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
        
       
    draw_border(background)
    

    # Set up start
    if recursive:
        highlighted_cell = Cell(48,1)
        background.fill(start_colour, rect=highlighted_cell)
        current_cell = None
   
    else:
        i = 1
        row = Row(i, None)
        
        

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
            if i < (30):
                row.draw(background)
                wait()
                row.set_random_same(background)
                row.draw(background)
                wait()
                row.merge_same_horizontal(background)
                row.draw(background)
                prev = row
                wait()
                i += 1
                row = Row(i,prev)
                row.draw(background)
                wait()
                row.merge_vertical(prev, background)
                row.draw(background)
                
            
           
            

            
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


        #print("me: {}\nnext: {}\nsame? {}".format(cell.colour, row.get_colour_adjacent(cell,1), row.test_colour_adjacent(cell,1)))
