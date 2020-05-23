import pygame
import window
import helpers
import algorithms
 

pygame.init()


INFO = pygame.display.Info()

# Colours
BACKGROUND_COLOUR = (160,160,160, 255)
GRID_COLOUR = (0,0,0,255)
BORDER_COLOUR = GRID_COLOUR
CELL_COLOUR = (200,200,200, 255)
START_COLOUR = (0,0,255, 255)
FINAL_COLOUR = (255, 255, 255, 255)
CURRENT_COLOUR = (0,255,0,255)


def set_grid_size(size):
    dimensions = {
        "grid_size": size,
        "screenx": int((INFO.current_w*0.75)  - ((INFO.current_w*0.75) % size)),
        }
    dimensions["grid_pixels"] = int(dimensions["screenx"]/size)
    dimensions["screeny"] = int(dimensions["screenx"]*0.6) - (int(dimensions["screenx"]*0.6) % dimensions["grid_pixels"])
    dimensions["border_width"] = dimensions["grid_pixels"]*2
        
    helpers.update_dimensions(dimensions)
    algorithms.update_dimensions(dimensions)
    return dimensions

def main():
    # Declare variables to control algorithm choice 
    recursive = False
    ellers = False
    kruskals = False

    # Set events
    allowed = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]
    pygame.event.set_allowed(allowed)

    # Game loop
    while True:
        if not recursive and not ellers and not kruskals:

            # Launch window
            helpers.colour_set.refresh()
            popup = window.AlgoSelectWindow()

            # Check whether to exit program
            if popup.exit_status:
                return

            # Set dimensions of screen and grid
            size = popup.grid_var.get() * 10
            dimensions = set_grid_size(size)

            # Initialise screen
            pygame.display.set_caption('Maze Generation Visualiser')
            screen = pygame.display.set_mode((dimensions["screenx"], dimensions["screeny"]))
            background = pygame.Surface(screen.get_size())
            background.convert()
            
            # Blit everything to the screen
            screen.blit(background, (0, 0))
            pygame.display.flip()
            
            # Set speed
            speed = 221 - (popup.speed_var.get() * 20)
            helpers.set_wait_time(speed)
            
            # Set up selected algorithm
            algorithm = popup.choice
            if algorithm == window.algorithm_list[0]:
                recursive = True
                algorithms.set_recursive_bias(popup.recursive_bias_var.get())
                algorithms.setup_recursive(background)
                current_cell = None
                highlighted_cell = helpers.Cell(48,1)
            elif algorithm == window.algorithm_list[1]:
                ellers = True
                iterator = 1
                row = helpers.Row(iterator, None, background, first=True)
                algorithms.setup_ellers(background, row)
            elif algorithm == window.algorithm_list[2]:
                kruskals = True
                set_dictionary, grid_connections = algorithms.setup_kruskals(background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if recursive and not current_cell:
                mouse = pygame.mouse.get_pos()
                colour = background.get_at(mouse)
                if event.type == pygame.MOUSEBUTTONDOWN and colour != BORDER_COLOUR:
                    current_cell = highlighted_cell 

        if recursive:
            if not current_cell:
                if colour == BACKGROUND_COLOUR:
                    background.fill(BACKGROUND_COLOUR, rect=highlighted_cell)
                    x = int((mouse[0] - 1) / dimensions["grid_pixels"])
                    y = int((mouse[1] - 1) / dimensions["grid_pixels"])
                    highlighted_cell = helpers.Cell(x,y)
                    background.fill(START_COLOUR, rect=highlighted_cell)
                    fill_start = True
                    start_cell = highlighted_cell
            else:
                current_cell = algorithms.recursive_backtracker(current_cell, background)
                if fill_start == True:
                    background.fill(START_COLOUR, rect=start_cell)
                    fill_start = False
                if current_cell.coord == start_cell.coord:
                    recursive = False


                
        elif ellers:
            if iterator < ((dimensions["screeny"] / dimensions["grid_pixels"]) - 2):
                iterator += 1
                row = algorithms.ellers_algorithm(iterator, background, row)
            else:
                row.finish(background)
                ellers = False

        elif kruskals:
            if grid_connections:
                algorithms.kruskals_algorithm(background, grid_connections, set_dictionary)
            else:
                kruskals = False

            
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


