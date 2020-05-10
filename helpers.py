import pygame
import random
import main

def draw_grid(background):

    for x in range(0, main.screenx, main.grid_size):
        pygame.draw.line(background, main.grid_colour, (x, 0), (x, main.screeny), 1)
        
    for y in range(0, main.screeny, main.grid_size):
        pygame.draw.line(background, main.grid_colour, (0, y), (main.screenx, y), 1)
   
def draw_border(background):
    border = pygame.Rect(0, 0, main.screenx - 1, main.screeny)
    pygame.draw.rect(background, main.border_colour, border, main.border_width)

def wait():
    time = pygame.time.get_ticks()                      
    while pygame.time.get_ticks() < time + main.wait_time: 
        pass

class Cell():
    def __init__(self, x, y):
        self.start = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.coord = (x,y)
        self.rect = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.colour = None
        self.index = x

class Line():
    def __init__(self, line, colour):
        self.rect = line
        self.colour = colour
  
class Row():
    def __init__(self, y, prev, background):
        self.y = (main.grid_size * y) + 1 
        border = Cell(0,y)
        border.colour = main.border_colour
        self.border = border
        self.cells = [border]
        self.lines = []
        self.merged = {}
        

        for i in range(1, main.grid-1):
            new = Cell(i, y)
            if y == 1:
                new.colour = main.set_colours[0]
            else: 
                triple = self.get_triple(i, prev)
                adj_colour = triple[1]
                
                if triple[2] == adj_colour or triple[0] == adj_colour:
                    new.colour = random.choice([adj_colour, random.choice(main.set_colours)])   
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
            index = random.randint(1,main.grid-2)
            curr = self.cells[index]   # select random cell from row
            
            
            new_colour = curr.colour
            adj_colour = self.get_colour_adjacent(curr, 1)
            if adj_colour == main.border_colour:
                break
            rect = pygame.draw.line(background, curr.colour, (curr.rect.right, curr.rect.top), (curr.rect.right, curr.rect.bottom - 1))
            line = Line(rect, new_colour)
            self.lines.append(line)
            main.set_colours.append(adj_colour)
            self.merged[adj_colour] = new_colour
    
    def draw(self, background):
        for cell in self.cells:
            background.fill(cell.colour, rect=cell.rect)
        for line in self.lines:
            background.fill(line.colour, rect=line)

            
    def finish(self, background):
        for cell in self.cells:
            if cell.colour != main.border_colour:
                background.fill(main.final_colour, rect=cell.rect)
        for line in self.lines:
            background.fill(main.final_colour, rect=line.rect)