import helpers
import pygame
import main
import random

recursive_bias = None
dimensions = {"grid_size":0, "screenx":0, "grid_pixels":0, "screeny":0, "border_width":0}


def update_dimensions(new_dimensions):
    global dimensions
    dimensions = new_dimensions

def set_recursive_bias(bias):
    global recursive_bias
    recursive_bias = str(bias)

 
def setup_recursive(background):
    background.fill(main.BACKGROUND_COLOUR)
    helpers.draw_grid(background)
    helpers.draw_border(background)
    #background.fill(start_colour, rect=highlighted_cell)

def recursive_backtracker(current, background):
    # Define directions: [(dx,dy), traversed border]
    directions = helpers.DirectionSet(recursive_bias)
    directions.shuffle()
    
    # Iterate over randomly ordered directions, checking whether moving into cell already visited
    for direction in directions.list:
        colour = current.get_colour_adjacent(direction[0], background)
         # If in this direction unvisited, move current there, fill cell and erase border
        if colour == main.BACKGROUND_COLOUR:
            background.fill(main.CELL_COLOUR, rect=current.rect)
            current.draw_grid(direction[1], main.CELL_COLOUR, background)
            current = helpers.Cell((current.coord[0] + direction[0][0]), (current.coord[1] + direction[0][1]))
            background.fill(main.CURRENT_COLOUR, rect=current.rect)
            

            helpers.wait()
            return current

    # If there are no available cells, retrace path and fill new colour.
    # This is the equivalent of recursive calls returning
    for direction in directions.list:
        colour = current.get_grid_colour(direction[1], background)

        if colour == main.CELL_COLOUR:
            background.fill(main.FINAL_COLOUR, rect=current.rect)
            current.draw_grid(direction[1], main.FINAL_COLOUR, background)
            current = helpers.Cell((current.coord[0] + direction[0][0]), (current.coord[1] + direction[0][1]))
            background.fill(main.CURRENT_COLOUR, rect=current.rect)
            

            helpers.wait()
            return current

def setup_ellers(background, row):
    background.fill(dimensions["grid_size"])  
    helpers.draw_border(background)
    row.draw(background)
    helpers.wait()

   
    row.random_merge(background)
    row.draw(background) 
    helpers.wait()

def ellers_algorithm(iterator, background, row):
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
    return row

def setup_kruskals(background):
    helpers.draw_grid(background)
    set_dictionary = {}
    grid_connections = []
    grid_y = (dimensions["screeny"]/dimensions["grid_pixels"]) - 1
    
    # Create rows with random colour_sets
    for y in range(1, int(grid_y)):
        helpers.colour_set.refresh()
        row = helpers.Row(y, None, background, first=True)
        # Iterate over row, adding each colour_set to dictionary
        for cell in row.cells:
            if cell.colour != main.BORDER_COLOUR:
                set_dictionary[tuple(cell.colour)] = helpers.BinaryTree(cell.rect)
                # And add grid connections to list
                if 0 < cell.index < (dimensions["grid_size"] - 2):
                    grid_connections.append(helpers.Line(cell.get_grid("right"), main.GRID_COLOUR))
                if y > 1 and cell.index >= 1:
                    grid_connections.append(helpers.Line(cell.get_grid("top"), main.GRID_COLOUR))
        row.draw(background)
    
    return set_dictionary, grid_connections
    

def kruskals_algorithm(background, grid_connections, set_dictionary):
    random.shuffle(grid_connections)
    grid_connection = grid_connections[0]
    cell = grid_connection.get_cell()
    
    # Work out whether the grid connection is horizontal or vertical and get the correct cell
    if grid_connection.rect.width > 1:
        coords = (0,1)
    else:
        coords = (1,0)
    adj = cell.get_adjacent(coords, background)
    
    # Get the colours of the cells divided by the given grid connection
    colour_one = tuple(cell.get_colour_adjacent(coords, background))
    colour_two = tuple(background.get_at((cell.rect.center)))
    keys = set_dictionary.keys()

    # If the colours are different, merge one set with the other 
    if colour_one == colour_two:
        pass
    elif colour_one in keys and colour_two in keys:
        expanded_set = set_dictionary[colour_one]
        merged_set = set_dictionary[colour_two]

        merged_set.add_node(grid_connection.rect)
        del set_dictionary[colour_two]

        merged_set.fill_tree(background, colour_one)
        expanded_set.add_node(merged_set.head)      

    grid_connections.remove(grid_connection)
    helpers.wait()




