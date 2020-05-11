import pygame
import window
import helpers
import algorithms


pygame.init()

# Dimensions
info = pygame.display.Info()
grid = 50
screenx = int((info.current_w * 0.75)  - ((info.current_w*0.75) % grid))
grid_size = int(screenx/grid)
screeny = int(screenx * 0.6) - (int(screenx * 0.6) % grid_size)
border_width = grid_size*2 # note that because the border grows either side of line, only half of this is visible

# Colours
background_colour = (160,160,160, 255)
grid_colour = (0,0,0,255)
border_colour = grid_colour
cell_colour = (200,200,200, 255)
start_colour = (0,0,255, 255)
final_colour = (255, 255, 255, 255)
current_colour = (0,255,0,255)

# Timings
wait_time = 200

# Algorithms
recursive = False
ellers = False
 
def main():
    # Initialise screen
    pygame.display.set_caption('Visualiser')
    screen = pygame.display.set_mode((screenx, screeny))
    background = pygame.Surface(screen.get_size())
    background.convert()

    # Set events
    allowed = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]
    pygame.event.set_allowed(allowed)

    # Launch window and define selected algorithm
    popup = window.AlgoSelectWindow()
    algorithm = popup.choice
    if algorithm == window.algorithm_list[0]:
        global recursive
        recursive = True
    elif algorithm == window.algorithm_list[1]:
        global ellers
        ellers = True

    # Create background and draw grid
    if recursive:
        algorithms.setup_recursive(background)
        current_cell = None
        highlighted_cell = helpers.Cell(48,1)
        
    elif ellers:
        iterator = 1
        row = helpers.Row(iterator, None, background)
        algorithms.setup_ellers(background, row)
 
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if recursive:
                mouse = pygame.mouse.get_pos()
                colour = background.get_at(mouse)
                if event.type == pygame.MOUSEBUTTONDOWN and colour != border_colour:
                    current_cell = highlighted_cell
        if recursive:
            if not current_cell:
                if colour == background_colour:
                    background.fill(background_colour, rect=highlighted_cell)
                    x = int((mouse[0] - 1) / grid_size)
                    y = int((mouse[1] - 1)/ grid_size)
                    highlighted_cell = helpers.Cell(x,y)
                    background.fill(start_colour, rect=highlighted_cell)    
            else:
                background.fill(start_colour, current_cell.start)
                algorithms.recursive_backtracker(current_cell, background)
        
        if ellers:

            iterator += 1
            row = algorithms.ellers_algorithm(iterator, background, row)

            
        screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':main()


