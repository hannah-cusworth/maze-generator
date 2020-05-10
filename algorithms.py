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
     
    # Define directions: [(dx,dy), traversed border coord 1, traversed border coord 2]
    top = current.rect.top
    bottom = current.rect.bottom
    left = current.rect.left
    right = current.rect. right

    directions = [
                [(0, -main.grid_size), (left, top - 1), (right - 1, top - 1)], # N
                [(0, main.grid_size), (left, bottom), (right - 1, bottom)], # S
                [(main.grid_size, 0), (right, top), (right, bottom - 1)], # E
                [(-main.grid_size, 0), (left - 1, top), (left - 1, bottom - 1)], # W
            ]           
    random.shuffle(directions)   # Shuffle order

    # Iterate over randomly ordered directions, checking whether moving into cell already visited
    for move in directions:
        test = current.rect.move(move[0])
        colour = background.get_at((test.left, test.top))   # Check unvisted based on colour

        # If in this direction unvisited, move current there, fill cell and erase border
        if colour == main.background_colour:
            background.fill(main.cell_colour, rect=current.rect)
            current.rect.move_ip(move[0])
            background.fill(main.current_colour, rect=current.rect)
            pygame.draw.line(background, main.cell_colour, move[1], move[2])  # Erase traversed border
            
            helpers.wait()
            return

    # If there are no available cells, retrace path and fill new colour.
    # This is the equivalent of recursive calls returning
    for move in directions:
        test = current.rect.move(move[0])
        colour = background.get_at(move[1])
        if colour == main.cell_colour:
            background.fill(main.final_colour, rect=current.rect)
            current.rect.move_ip(move[0])
            background.fill(main.current_colour, rect=current.rect)
            pygame.draw.line(background, main.final_colour, move[1], move[2])
            helpers.wait()
            return

def setup_ellers(background, row):
    background.fill(main.grid)  
    helpers.draw_border(background)
    row.set_random_same(background)
    row.merge_cells(background, row.merged)
    row.draw(background) 
    helpers.wait()

def ellers_algorithm(iterator, background, row):
    if iterator < (main.screeny/50):
                print("ffffffffffffffffff")
                print(helpers.colour_set.length())
                print(iterator)
                print("ffffffffffffffff")
                row.draw(background)
                prev = row              
                row = helpers.Row(iterator, prev, background)
                row.draw(background)
                helpers.wait()
                
                row.set_random_same(background)
                row.draw(background)
         
                row.merge_cells(background, row.merged)
                prev.merge_cells(background, row.merged)
                row.draw(background)
                prev.draw(background)
                helpers.wait()

                #prev.finish(background)
                helpers.wait()

    else:
        row.finish(background)
    return row