from main import *
global background

def setup_recursive(background):
    background.fill(background_colour)
    draw_grid(background)
    draw_border(background)
    #background.fill(start_colour, rect=highlighted_cell)

def recursive_backtracker(current, background):
     
    # Define directions: [(dx,dy), traversed border coord 1, traversed border coord 2]
    top = current.rect.top
    bottom = current.rect.bottom
    left = current.rect.left
    right = current.rect. right

    directions = [
                [(0, -grid_size), (left, top - 1), (right - 1, top - 1)], # N
                [(0, grid_size), (left, bottom), (right - 1, bottom)], # S
                [(grid_size, 0), (right, top), (right, bottom - 1)], # E
                [(-grid_size, 0), (left - 1, top), (left - 1, bottom - 1)], # W
            ]           
    rand = random.shuffle(directions)   # Shuffle order

    # Iterate over randomly ordered directions, checking whether moving into cell already visited
    for move in directions:
        test = current.rect.move(move[0])
        colour = background.get_at((test.left, test.top))   # Check unvisted based on colour

        # If in this direction unvisited, move current there, fill cell and erase border
        if colour == background_colour:
            background.fill(cell_colour, rect=current.rect)
            current.rect.move_ip(move[0])
            background.fill(current_colour, rect=current.rect)
            pygame.draw.line(background, cell_colour, move[1], move[2])  # Erase traversed border
            
            wait()
            return

    # If there are no available cells, retrace path and fill new colour.
    # This is the equivalent of recursive calls returning
    for move in directions:
        test = current.rect.move(move[0])
        colour = background.get_at(move[1])
        if colour == cell_colour:
            background.fill(final_colour, rect=current.rect)
            current.rect.move_ip(move[0])
            background.fill(current_colour, rect=current.rect)
            pygame.draw.line(background, final_colour, move[1], move[2])
            wait()
            return

def setup_ellers(background, row):
    background.fill(grid_colour)  
    draw_border(background)
    row.set_random_same(background)
    row.merge_cells(background, row.merged)
    row.draw(background)
    wait()

def ellers_algorithm(background, row):
    global iterator
    if iterator < (screeny/50):
                row.draw(background)
                prev = row              
                row = Row(iterator, prev, background)
                row.draw(background)
                wait()
                
                row.set_random_same(background)
                row.draw(background)
         
                row.merge_cells(background, row.merged)
                prev.merge_cells(background, row.merged)
                row.draw(background)
                prev.draw(background)
                wait()

                prev.finish(background)
                iterator += 1
                wait()

    else:
        row.finish(background)
    return row