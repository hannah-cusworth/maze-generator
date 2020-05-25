import pygame
import random
import main

wait_time = 1
dimensions = {"grid_size":0, "screenx":0, "grid_pixels":0, "screeny":0, "border_width":0}

def update_dimensions(new_dimensions):
    global dimensions
    dimensions = new_dimensions

def draw_grid(background):
    for x in range(0, dimensions["screenx"], dimensions["grid_pixels"]):
        pygame.draw.line(background, main.GRID_COLOUR, (x, 0), (x, dimensions["screeny"]), 1)
        
    for y in range(0, dimensions["screeny"], dimensions["grid_pixels"]):
        pygame.draw.line(background, main.GRID_COLOUR, (0, y), (dimensions["screenx"], y), 1)
   
def draw_border(background):
    border = pygame.Rect(0, 0, dimensions["screenx"] - 1, dimensions["screeny"])
    pygame.draw.rect(background, main.BORDER_COLOUR, border, dimensions["border_width"])

def set_wait_time(speed):
    global wait_time
    wait_time = speed

def wait():
    time = pygame.time.get_ticks()                     
    while pygame.time.get_ticks() < time + wait_time: 
        pass

class BinaryTree():
    def __init__(self, data):
        self.head = BinaryTreeNode(data)

    def add_node(self, node):
        curr = self.head
        if not isinstance(node, BinaryTreeNode):
            node = BinaryTreeNode(node)
        while True:
            if curr.data.top > node.data.top:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = node
                    
                    
                    return
            else:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = node
                    return

    
    
    def fill_tree(self, background, colour):
        def fill_subtree(tree, background, colour):
            background.fill(colour, rect=tree.data)
            if not tree.right and not tree.left:
                return
            if tree.left:
                fill_subtree(tree.left, background, colour)
            if tree.right:
                fill_subtree(tree.right, background, colour)

        fill_subtree(self.head, background, colour)
        

class BinaryTreeNode():
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

class DirectionSet():
    def __init__(self, bias):
        self.dict = {
                "S": [(0,1), "bottom"], 
                "N": [(0,-1), "top"], 
                "E": [(1,0), "right"], 
                "W": [(-1,0), "left"]   
            }
        self.list = list(self.dict.values())
        for x in range(2):
            if bias == "X":
                self.list.append(self.dict["W"])
                self.list.append(self.dict["E"])
            elif bias == "Y":
                self.list.append(self.dict["N"])
                self.list.append(self.dict["S"])
            elif bias:
                self.list.append(self.dict[bias])
        

    def shuffle(self):
        random.shuffle(self.list)


class ColourSet():
    def __init__(self):
        self.all = []
        for i in range(dimensions["grid_size"] - 2):
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

    def refresh(self):
        self.__init__()


class Cell():
    def __init__(self, x, y):
        #self.start = pygame.Rect((main.grid_pixels * x) + 1, (main.grid_pixels * y) + 1, main.grid_pixels-1, main.grid_pixels-1)
        self.coord = (x,y)
        self.rect = pygame.Rect((dimensions["grid_pixels"] * x) + 1, (dimensions["grid_pixels"] * y) + 1, dimensions["grid_pixels"]-1, dimensions["grid_pixels"]-1)
        self.colour = None
        self.index = x

    def get_grid(self, edge): # -> pygame.Rect
        surf = pygame.Surface((dimensions["screenx"], dimensions["screeny"]))
        edges = {
            "top": ((self.rect.left, self.rect.top - 1), (self.rect.right - 1, self.rect.top - 1)),
            "bottom": ((self.rect.left, self.rect.bottom), (self.rect.right - 1, self.rect.bottom)),
            "right": ((self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom - 1)),
            "left": ((self.rect.left - 1, self.rect.top), (self.rect.left - 1, self.rect.bottom - 1))
        }
        x, y = edges[edge]
        return pygame.draw.line(surf, main.CELL_COLOUR, x, y)

    def draw_grid(self, edge, colour, background) -> None:
        grid = self.get_grid(edge)
        background.fill(colour,rect=grid)

    def get_colour_adjacent(self, coords, background): # coords: (dx,dy)
        test = Cell((self.coord[0] + coords[0]), (self.coord[1] + coords[1]))
        return background.get_at((test.rect.center))

    def get_adjacent(self, coords, background):
        return Cell((self.coord[0] + coords[0]), (self.coord[1] + coords[1]))

    def get_grid_colour(self, edge, background):
        grid = self.get_grid(edge)
        return background.get_at((grid.center))


class Line():
    def __init__(self, line, colour):
        self.rect = line
        self.colour = colour

    def get_cell(self):
        coords = self.rect.center
        if self.rect.width > 1:
            x = (coords[0] - 1) / dimensions["grid_pixels"]
            y = (coords[1] - 5) / dimensions["grid_pixels"]
        else:
            x = (coords[0] - 5) / dimensions["grid_pixels"]
            y = (coords[1] - 1) / dimensions["grid_pixels"]
        return Cell(int(x), int(y))



colour_set = ColourSet()

class Row():
    def __init__(self, iterator, prev, background, first=False):
        border = Cell(0,iterator)
        border.colour = main.BORDER_COLOUR

        self.y = (dimensions["grid_pixels"] * iterator) + 1 
        self.border = border
        self.cells = [self.border]
        self.lines = []
        self.merged = {}
        

        for i in range(1, dimensions["grid_size"] - 1):
            new = Cell(i, iterator)

            # Initiate first row by assigning colours from queue
            if first:
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
                        new.colour = main.BACKGROUND_COLOUR
                    else:
                        new.colour = prev_colour
                        
                # Else create vertical connection
                else:
                    new.colour = prev_colour

                # If vertical connection, remove grid border
                if new.colour == prev_colour:
                    grid = new.get_grid("top")
                    line = Line(grid, new.colour)
                    self.lines.append(line)       
            
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
        
        for cell in self.cells:
            ignore = [main.BACKGROUND_COLOUR, main.BORDER_COLOUR]
            adjacent_colour = self.get_colour_adjacent(cell, -1)
            if adjacent_colour in ignore or cell.colour in ignore:
                continue
            if cell.colour in changed.keys():
                cell.colour = changed[cell.colour]
            elif random.randint(0,1) and not self.test_colour_adjacent(cell, -1):
                changed[cell.colour] = adjacent_colour
                border = cell.get_grid("left")
                self.lines.append(Line(border, adjacent_colour))
                
                colour_set.enqueue(cell.colour)
                cell.colour = adjacent_colour
                    


            

    def fill_empty(self, background):
        ''' Assign blank cells their own new set '''
        for cell in self.cells:
            adjacent_colour = self.get_colour_adjacent(cell, 1)
            if cell.colour == main.BACKGROUND_COLOUR:
                if random.randint(0,1) or adjacent_colour == main.BORDER_COLOUR:
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
            if cell.colour != main.BORDER_COLOUR:
                background.fill(main.FINAL_COLOUR, rect=cell.rect)
        for line in self.lines:
            background.fill(main.FINAL_COLOUR, rect=line.rect)

    def finish(self, background):
        final_set = self.cells[1].colour
        for cell in self.cells:
            if cell.colour != final_set:
                grid = cell.get_grid("right")
                self.lines.append(Line(grid, cell.colour))
        self.clear(background)