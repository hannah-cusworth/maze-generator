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
            random.seed()
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
        #self.start = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.coord = (x,y)
        self.rect = pygame.Rect((main.grid_size * x) + 1, (main.grid_size * y) + 1, main.grid_size-1, main.grid_size-1)
        self.colour = None
        self.index = x

    def get_grid(self, edge): # -> pygame.Rect
        surf = pygame.Surface((main.screenx, main.screeny))
        edges = {
            "top": ((self.rect.left, self.rect.top - 1), (self.rect.right - 1, self.rect.top - 1)),
            "bottom": ((self.rect.left, self.rect.bottom), (self.rect.right - 1, self.rect.bottom)),
            "right": ((self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom - 1)),
            "left": ((self.rect.left - 1, self.rect.top), (self.rect.left - 1, self.rect.bottom - 1))
        }
        x, y = edges[edge]
        return pygame.draw.line(surf, main.cell_colour, x, y)

    def draw_grid(self, edge, colour, background) -> None:
        grid = self.get_grid(edge)
        background.fill(colour,rect=grid)

    def get_colour_adjacent(self, coords, background): # coords: (dx,dy)
        test = Cell((self.coord[0] + coords[0]), (self.coord[1] + coords[1]))
        return background.get_at((test.rect.center))

    def get_grid_colour(self, edge, background):
        grid = self.get_grid(edge)
        return background.get_at((grid.center))


class Line():
    def __init__(self, line, colour):
        self.rect = line
        self.colour = colour
  
colour_set = ColourSet()

class Row():
    def __init__(self, iterator, prev, background):
        border = Cell(0,iterator)
        border.colour = main.border_colour

        self.y = (main.grid_size * iterator) + 1 
        self.border = border
        self.cells = [self.border]
        self.lines = []
        self.merged = {}
        

        for i in range(1, main.grid-1):
            new = Cell(i, iterator)

            # Initiate first row by assigning colours from queue
            if iterator == 1:
                new.colour = colour_set.dequeue()

            # For other rows, decide whether to create vertical connection 
            # or leave cell blank by examining adjecent cells
            else: 
                triple = self.get_triple(i, prev)
                prev_colour = triple[1]
                
                # If another vertical connect definitely exists for this set, choice can be random
                if triple[2] == prev_colour or triple[0] == prev_colour:
                    probability = [0, 0, 1, 1]
                    random.seed()
                    choice = random.choice(probability)
                    if choice:
                        new.colour = main.background_colour
                    else:
                        new.colour = prev_colour

                # Else create vertical connection
                else:
                    new.colour = prev_colour

                # If vertical connection, remove grid border
                if new.colour == prev_colour:
                    grid = new.get_grid("top")
                    self.lines.append(Line(grid, new.colour))              
            
            self.cells.append(new)
  
        self.cells.append(self.border)
          
    def test_colour_adjacent(self, cell, dx) -> bool:
        adjacent_colour = self.cells[cell.index+dx].colour
        return adjacent_colour == cell.colour

    def get_colour_adjacent(self, cell, dx):
        return self.cells[cell.index + dx].colour
    
    def get_triple(self, i, prev):
        return [self.cells[i-1].colour , prev.cells[i].colour, prev.cells[i+1].colour]

    def random_merge(self, background):
        ''' Iterate over row randomly merging adjacent sets'''
        changed = {}
        
        for cell in self.cells[2:49]:
            adjacent_colour = self.get_colour_adjacent(cell, -1)
            if adjacent_colour == main.background_colour or cell.colour == main.background_colour:
                continue
            if cell.colour in changed.keys():
                cell.colour = changed[cell.colour]
            elif random.randint(0,1) and not self.test_colour_adjacent(cell, -1):
                changed[cell.colour] = adjacent_colour
                colour_set.enqueue(cell.colour)
                cell.colour = adjacent_colour
                border = cell.get_grid("left")
                self.lines.append(Line(border, cell.colour))
        

    def fill_empty(self, background):
        ''' Assign blank cells there own new set '''
        for cell in self.cells:
            adjacent_colour = self.get_colour_adjacent(cell, 1)
            if cell.colour == main.background_colour:
                if random.randint(0,1) or adjacent_colour == main.border_colour:
                    cell.colour = colour_set.dequeue()
                else:
                    cell.colour = adjacent_colour
                    grid = cell.get_grid("right")
                    self.lines.append(Line(grid, cell.colour))

    def draw(self, background):
        for cell in self.cells:
            background.fill(cell.colour, rect=cell.rect)
        for line in self.lines:
            background.fill(line.colour, rect=line)
            
    def clear(self, background):
        for cell in self.cells:
            if cell.colour != main.border_colour:
                background.fill(main.final_colour, rect=cell.rect)
        for line in self.lines:
            background.fill(main.final_colour, rect=line.rect)

    def finish(self, background):
        final_set = self.cells[1].colour
        for cell in self.cells:
            if cell.colour != final_set:
                grid = cell.get_grid("right")
                self.lines.append(Line(grid, cell.colour))
        self.clear(background)