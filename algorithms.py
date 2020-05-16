import helpers
import pygame
import main
import random
 
def setup_recursive(background):
    background.fill(main.background_colour)
    helpers.draw_grid(background)
    helpers.draw_border(background)
    #background.fill(start_colour, rect=highlighted_cell)

def recursive_backtracker(current, background):
    # Define directions: [(dx,dy), traversed border]
    directions = [
        [(0,1), "bottom"], 
        [(0,-1), "top"], 
        [(1,0), "right"], 
        [(-1,0), "left"]
    ]            
    random.shuffle(directions)

    # Iterate over randomly ordered directions, checking whether moving into cell already visited
    for direction in directions:
        colour = current.get_colour_adjacent(direction[0], background)
         # If in this direction unvisited, move current there, fill cell and erase border
        if colour == main.background_colour:
            background.fill(main.cell_colour, rect=current.rect)
            current.draw_grid(direction[1], main.cell_colour, background)
            current = helpers.Cell((current.coord[0] + direction[0][0]), (current.coord[1] + direction[0][1]))
            background.fill(main.current_colour, rect=current.rect)
            

            helpers.wait()
            return current

    # If there are no available cells, retrace path and fill new colour.
    # This is the equivalent of recursive calls returning
    for direction in directions:
        colour = current.get_grid_colour(direction[1], background)

        if colour == main.cell_colour:
            background.fill(main.final_colour, rect=current.rect)
            current.draw_grid(direction[1], main.final_colour, background)
            current = helpers.Cell((current.coord[0] + direction[0][0]), (current.coord[1] + direction[0][1]))
            background.fill(main.current_colour, rect=current.rect)
            

            helpers.wait()
            return current

def setup_ellers(background, row):
    background.fill(main.grid)  
    helpers.draw_border(background)
    row.draw(background)
    helpers.wait()

    row.random_merge(background)
    row.draw(background) 
    helpers.wait()

def ellers_algorithm(iterator, background, row):
    if iterator < (main.screeny/main.grid):

                row.draw(background)
                prev = row              
                row = helpers.Row(iterator, prev, background)
                row.draw(background)
                helpers.wait()
                
                row.random_merge(background)
                row.draw(background)
                helpers.wait()

                row.fill_empty(background)
                row.draw(background)
                helpers.wait()

                prev.clear(background)
                helpers.wait()
    else:
        row.finish(background)
    return row

def setup_kruskals(background):
    helpers.draw_grid(background)
    set_dictionary = {}
    grid_connections = []
    grid_y = (main.screeny/main.grid) + 1
    
    for y in range(1, int(grid_y)):
        helpers.colour_set.refresh()
        row = helpers.Row(y, None, background, first=True)
        for cell in row.cells:
            if cell.colour != main.border_colour:
                set_dictionary[tuple(cell.colour)] = helpers.BinaryTree((cell.rect))
                if 0 < cell.index < (main.grid - 2):
                    grid_connections.append(helpers.Line(cell.get_grid("right"),main.grid_colour))
                if y > 1 and cell.index >= 1:
                    grid_connections.append(helpers.Line(cell.get_grid("top"), main.grid_colour))
        row.draw(background)
    
    return set_dictionary, grid_connections
    

def kruskals_algorithm(background, grid_connections, set_dictionary):
    if grid_connections:
        #print(len(grid_connections))
        random.shuffle(grid_connections)
        grid_connection = grid_connections[0]
        cell = grid_connection.get_cell()

        if grid_connection.rect.width > 1:
            coords = (0,1)
        else:
            coords = (1,0)    

        colour_one = tuple(background.get_at((cell.rect.center)))
        colour_two = tuple(cell.get_colour_adjacent(coords, background))
        keys = set_dictionary.keys()
        #print(len(keys))
        

        if colour_one in keys and colour_two in keys:
            print("yes")
            merged_set = set__dictionary[colour_two]
            merged_set.add_node(grid_connection)
            del set_dictionary[colour_two]
            merged_set.fill_tree(background, colour_one)
            set_dictionary[colour_one].add_node(merged_set.data)
        grid_connections.remove(grid_connection)
        helpers.wait()

