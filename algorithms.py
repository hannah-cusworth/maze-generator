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
    helpers.fill_grid(background)