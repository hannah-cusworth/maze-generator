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
wait_time = 100
global iterator 
iterator = 1

# Algorithms
recursive = False
ellers = False
    
def draw_grid(background):

    for x in range(0, screenx, grid_size):
        pygame.draw.line(background, grid_colour, (x, 0), (x, screeny), 1)
        
    for y in range(0, screeny, grid_size):
        pygame.draw.line(background, grid_colour, (0, y), (screenx, y), 1)
   
def draw_border(background):
    border = pygame.Rect(0, 0, screenx - 1, screeny)
    pygame.draw.rect(background, border_colour, border, border_width)

def wait():
    time = pygame.time.get_ticks()                      
    while pygame.time.get_ticks() < time + wait_time: # Wait
        pass


class Cell():
    def __init__(self, x, y):
        self.start = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.coord = (x,y)
        self.rect = Rect((grid_size * x) + 1, (grid_size * y) + 1, grid_size-1, grid_size-1)
        self.colour = None
        self.index = x

class Line():
    def __init__(self, line, colour):
        self.rect = line
        self.colour = colour
  
class Row():
    def __init__(self, y, prev, background):
        self.y = (grid_size * y) + 1 
        border = Cell(0,y)
        border.colour = border_colour
        self.border = border
        self.cells = [border]
        self.lines = []
        self.merged = {}
        

        for i in range(1, grid-1):
            new = Cell(i, y)
            if y == 1:
                new.colour = set_colours[0]
            else: 
                triple = self.get_triple(i, prev)
                adj_colour = triple[1]
                
                if triple[2] == adj_colour or triple[0] == adj_colour:
                    new.colour = random.choice([adj_colour, random.choice(set_colours)])   
                else:
                    new.colour = adj_colour
                if new.colour == adj_colour:
                    rect = pygame.draw.line(background, new.colour, (new.rect.left, new.rect.top - 1), (new.rect.right - 1, new.rect.top - 1))
                    line = Line(rect, new.colour)
                    self.lines.append(line)
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
        return [self.cells[i-1].colour , prev.cells[i].colour, prev.cells[i+1].colour]
    
    def merge_cells(self, background, merged):
        for cell in self.cells:
            if cell.colour in merged.keys():
                cell.colour=merged.get(cell.colour)
            
        for line in self.lines:
            if line.colour in merged.keys():
                line.colour=merged.get(line.colour)    
    
    def set_random_same(self, background):
        #set_count = grid - len(set_colours)
        #merge_count = int(set_count * 0.5)
        #for i in range(merge_count):
        for i in range(30):
            index = random.randint(1,grid-2)
            curr = self.cells[index]   # select random cell from row
            
            
            new_colour = curr.colour
            adj_colour = self.get_colour_adjacent(curr, 1)
            if adj_colour == border_colour:
                break
            rect = pygame.draw.line(background, curr.colour, (curr.rect.right, curr.rect.top), (curr.rect.right, curr.rect.bottom - 1))
            line = Line(rect, new_colour)
            self.lines.append(line)
            set_colours.append(adj_colour)
            self.merged[adj_colour] = new_colour
    
    def draw(self, background):
        for cell in self.cells:
            background.fill(cell.colour, rect=cell.rect)
        for line in self.lines:
            background.fill(line.colour, rect=line)

            
    def finish(self, background):
        for cell in self.cells:
            if cell.colour != border_colour:
                background.fill(final_colour, rect=cell.rect)
        for line in self.lines:
            background.fill(final_colour, rect=line.rect)


    

    
            

            
        
   
    

        
        
            



def main():
    global iterator
    global background
   
    # Initialise screen
    pygame.display.set_caption('Visualiser')
    screen = pygame.display.set_mode((screenx, screeny))
    background = pygame.Surface(screen.get_size())
    background.convert()
    


    # Set events
    allowed = [MOUSEBUTTONUP, MOUSEBUTTONDOWN]
    pygame.event.set_allowed(allowed)

    # Launch window and define selected algorithm
    popup = window.AlgoSelectWindow()
    algorithm = popup.choice
    if algorithm == window.algorithm_list[0]:
        global recursive
        recursive = True
    elif algorithm == window.algorithm_list[1]:
        global ellers
        ellers = True

    # Create background and draw grid

    
    if recursive:
        algorithms.setup_recursive()
        current_cell = None
        highlighted_cell = Cell(48,1)
        
    elif ellers:
        row = Row(iterator, None, background)
        algorithms.setup_ellers(background, row)
        iterator += 1
 
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if recursive:
                mouse = pygame.mouse.get_pos()
                colour = background.get_at(mouse)
                if event.type == MOUSEBUTTONDOWN and colour != border_colour:
                    current_cell = highlighted_cell
        if recursive:
            if not current_cell:
                if colour == background_colour:
                    background.fill(background_colour, rect=highlighted_cell)
                    x = int((mouse[0] - 1) / grid_size)
                    y = int((mouse[1] - 1)/ grid_size)
                    highlighted_cell = Cell(x,y)
                    background.fill(start_colour, rect=highlighted_cell)    
            else:
                background.fill(start_colour, current_cell.start)
                algorithms.recursive_backtracker(current_cell, background)
        
        if ellers:
            row = algorithms.ellers_algorithm(background, row)
            
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


