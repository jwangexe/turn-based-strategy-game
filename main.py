import sys
 
import pygame
from pygame.locals import *

BLACK = (0,0,0)
BLACK_ALT = (0, 0, 1)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRID_GREEN = (0, 153, 51)

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
gridwidth, gridheight = 640, 360
squaresize = 40
screen = pygame.display.set_mode((width, height))

game_board_rows = gridheight // squaresize
game_board_cols = gridwidth // squaresize
game_board = [[0]*game_board_cols]*game_board_rows

print(game_board)

def draw_grid(square_size):
    for x in range(0, gridwidth+square_size, square_size):
        pygame.draw.line(screen, GRID_GREEN, (x, 0), (x, gridheight), 1)
        for y in range(0, gridheight+square_size, square_size):
           pygame.draw.line(screen, GRID_GREEN, (0, y), (gridwidth, y))

def get_grid_pos(mousex, mousey):
    x = mousex // squaresize
    y = mousey // squaresize
    if x > game_board_cols or y > game_board_rows:
        return (-1, -1)
    return (x, y)


# Game loop

while True:
    screen.fill(BLACK)
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
    # Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(get_grid_pos(mouse_x, mouse_y))
  
    # Update
  
  
    # Draw
    draw_grid(squaresize)
  
    pygame.display.flip()
    fpsClock.tick(fps)