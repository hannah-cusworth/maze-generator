import pygame
import window
import helpers
import algorithms
 

pygame.init()

# Dimensions
info = pygame.display.Info()
grid = 50
screenx = int((info.current_w*0.75)  - ((info.current_w*0.75) % grid))
grid_size = int(screenx/grid)
screeny = int(screenx*0.6) - (int(screenx*0.6) % grid_size)
border_width = grid_size*2 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (160,160,160, 255)
grid_colour = (0,0,0,255)
border_colour = grid_colour
cell_colour = (200,200,200, 255)
start_colour = (0,0,255, 255)
final_colour = (255, 255, 255, 255)
current_colour = (0,255,0,255)


# Algorithms
recursive = False
ellers = False
kruskals = False
 
def main():
    # Declare global variables to control algorithm choice and speed
    global recursive
    global ellers
    global kruskals

    # Initialise screen
    pygame.display.set_caption('Visualiser')
    screen = pygame.display.set_mode((screenx, screeny))
    background = pygame.Surface(screen.get_size())
    background.convert()

    # Set events
    allowed = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]
    pygame.event.set_allowed(allowed)
 
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Game loop
    while True:
        if not recursive and not ellers and not kruskals:
            # Launch window
            helpers.colour_set.refresh()
            popup = window.AlgoSelectWindow()
            # Set speed
            speed = 221 - (popup.speed_var.get() * 20)
            helpers.set_wait_time(speed)
            # Get selected algorithm
            algorithm = popup.choice
            if algorithm == window.algorithm_list[0]:
                recursive = True
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
                if event.type == pygame.MOUSEBUTTONDOWN and colour != border_colour:
                    current_cell = highlighted_cell 

        if recursive:
            if not current_cell:
                if colour == background_colour:
                    background.fill(background_colour, rect=highlighted_cell)
                    x = int((mouse[0] - 1) / grid_size)
                    y = int((mouse[1] - 1) / grid_size)
                    highlighted_cell = helpers.Cell(x,y)
                    background.fill(start_colour, rect=highlighted_cell)
                    fill_start = True
                    start_cell = highlighted_cell
            else:
                current_cell = algorithms.recursive_backtracker(current_cell, background)
                if fill_start == True:
                    background.fill(start_colour, rect=start_cell)
                    fill_start = False
                if current_cell.coord == start_cell.coord:
                    recursive = False


                
        elif ellers:
            if iterator < ((screeny/grid_size) - 2):
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


