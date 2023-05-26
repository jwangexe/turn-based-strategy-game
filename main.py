import sys
import pygame
from pygame.locals import *

# initialize color tuples
BLACK = (0,0,0)
BLACK_ALT = (0, 0, 1)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRID_GREEN = (0, 153, 51)

# init pygame
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
gridwidth, gridheight = 640, 360
squaresize = 40
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turn-based Strategy Game")

# define piece data
piece2id = {"Empty": 0, "Inf": 1, "Cav": 2}
id2piece = {0: "Empty", 1: "Inf", 2: "Cav"}
id2img = {1: pygame.image.load("./Inf.png").convert(), 2: pygame.image.load("./Cav.png").convert()}

game_board_rows = gridheight // squaresize
game_board_cols = gridwidth // squaresize

game_board = []
for i in range(game_board_rows):
    game_board.append([0]*game_board_cols)
#game_board = [[0]*game_board_cols]*game_board_rows

game_board[0][1] = 1
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

def coords_to_pos(x, y):
    return (x*squaresize, y*squaresize)

# Game loop

while True:
    screen.fill(BLACK)
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
    # Check keypresses
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x, y = get_grid_pos(mouse_x, mouse_y)
    if keys[pygame.K_p]:
        print(x, y)
    if -1 not in (x, y):
        if keys[pygame.K_0]:
            game_board[y][x] = 0
        if keys[pygame.K_1]:
            game_board[y][x] = 1
        if keys[pygame.K_2]:
            game_board[y][x] = 2
    if keys[pygame.K_BACKSPACE]:
        game_board = [[0]*game_board_cols]*game_board_rows
  
    # Update
    
  
    # Draw
    for y in range(0, game_board_rows):
        for x in range(0, game_board_cols):
            xcoord, ycoord = x*squaresize, y*squaresize
            pieceid = game_board[y][x]
            if pieceid != 0:
                #print("blitted piece to", x, y)
                img = id2img[pieceid]
                screen.blit(img, (xcoord, ycoord))

    draw_grid(squaresize)
  
    pygame.display.flip()
    fpsClock.tick(fps)