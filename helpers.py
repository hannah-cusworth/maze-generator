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

class ColourSet():
    def __init__(self):
        self.all = []
        for i in range(main.grid - 2):
            # keep between 1 and 255 to exclude border/grid/background
            self.all.append((random.randint(1,255), random.randint(1,255), random.randint(1,255), 255))
        self.queue = self.all

    def enqueue(self, colour):
        if colour not in self.queue:
            self.queue.append(colour)

    def dequeue(self):
        return self.queue.pop(0)

    def length(self):
        return len(self.queue)


class Cell():
    def __init__(self, x, y):
        self.start = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.coord = (x,y)
        self.rect = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.colour = None
        self.new = None
        self.index = x

class Line():
    def __init__(self, line, colour):
        self.rect = line
        self.colour = colour
  
colour_set = ColourSet()

class Row():
    def __init__(self, iterator, prev, background):
        self.y = (main.grid_size * iterator) + 1 
        border = Cell(0,iterator)
        border.colour = main.border_colour
        self.border = border
        self.cells = [border]
        self.lines = []
        self.merged = {}
        

        for i in range(1, main.grid-1):
            new = Cell(i, iterator)
            if iterator == 1:
                new.colour = colour_set.dequeue()
            else: 
                triple = self.get_triple(i, prev)
                prev_colour = triple[1]
                
                if triple[2] == prev_colour or triple[0] == prev_colour:
                    probability = [0, 1, 1, 1]
                    choice = random.choice(probability)
                    if choice:
                        new.colour = colour_set.dequeue()
                        print(new.colour)
                    else:
                        new.colour = prev_colour

                else:
                    new.colour = prev_colour
                if new.colour == prev_colour:
                    rect = pygame.draw.line(background, new.colour, (new.rect.left, new.rect.top - 1), (new.rect.right - 1, new.rect.top - 1))
                    line = Line(rect, new.colour)
                    self.lines.append(line)              
            self.cells.append(new)    
        self.cells.append(border)
          
    def test_colour_adjacent(self, cell, dx):
        adjacent_colour = self.cells[cell.index+dx].colour
        return adjacent_colour == cell.colour

    def get_colour_adjacent(self, cell, dx):
        return self.cells[cell.index + dx].colour
    
    def get_triple(self, i, prev):
        return [self.cells[i-1].colour , prev.cells[i].colour, prev.cells[i+1].colour]
    
    def merge_cells(self, background, merged):
        for cell in self.cells:
            if cell.colour in merged.keys():
                cell.colour = merged.get(cell.colour)
            
        for line in self.lines:
            if line.colour in merged.keys():
                line.colour = merged.get(line.colour)    
    
    def set_random_same(self, background):
        #set_count = grid - len(colour_set)
        #merge_count = int(set_count * 0.5)
        #for i in range(merge_count):
        for i in range(30):
            curr = random.choice(self.cells)   # select random cell from row
            
            new_colour = curr.colour
            replace_colour = self.get_colour_adjacent(curr, 1)
            if replace_colour == main.border_colour or curr.colour == main.border_colour:
                return
            rect = pygame.draw.line(background, curr.colour, (curr.rect.right, curr.rect.top), (curr.rect.right, curr.rect.bottom - 1))
            line = Line(rect, new_colour)
            self.lines.append(line)
            colour_set.enqueue(replace_colour)
            self.merged[replace_colour] = new_colour
    
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