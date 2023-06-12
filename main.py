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

class Piece:
    def __init__(self, typenum):
        self.idnum = typenum
        stats = id2stats[typenum]
        self.move, self.atk, self.hp = stats
        self.current_movepoints = self.move
    
    def harm(self, dmg):
        self.hp -= dmg

    def is_dead(self):
        return self.hp <= 0

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
piece2id = {"Inf-red": -1, "Cav-red": -2, "Empty": 0, "Inf-blue": 1, "Cav-blue": 2}
id2piece = {-1: "Inf-red", -2: "Cav-red", 0: "Empty", 1: "Inf-blue", 2: "Cav-blue"}
id2img = {
    1: pygame.image.load("./Inf-blue.png").convert(),
    2: pygame.image.load("./Cav-blue.png").convert(),
    -1: pygame.image.load("./Inf-red.png").convert(),
    -2: pygame.image.load("./Cav-red.png").convert()
    }
# (movement, attack, hp)
id2stats = {
    -1: (1, 1, 2),
    -2: (2, 1, 2),
    1: (1, 1, 2),
    2: (2, 1, 2)
}

game_board_rows = gridheight // squaresize
game_board_cols = gridwidth // squaresize

game_board = []
for i in range(game_board_rows):
    game_board.append([0]*game_board_cols)

def draw_grid(square_size):
    for x in range(0, gridwidth+square_size, square_size):
        pygame.draw.line(screen, GRID_GREEN, (x, 0), (x, gridheight), 1)
        for y in range(0, gridheight+square_size, square_size):
           pygame.draw.line(screen, GRID_GREEN, (0, y), (gridwidth, y))

def get_grid_pos(mousex, mousey):
    x = mousex // squaresize
    y = mousey // squaresize
    if x >= game_board_cols or y >= game_board_rows:
        return (-1, -1)
    return (x, y)

def coords_to_pos(x, y):
    return (x*squaresize, y*squaresize)

def hurt(board, x, y, dmg):
    if board[y][x] != 0:
        board[y][x].harm(dmg)
    return board

def check_for_dead(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != 0:
                if board[y][x].is_dead():
                    board[y][x] = 0
    return board

def move_piece(board, x, y, movx, movy):
    # moves the piece on board[y][x] movx steps to the right and movy steps up
    # then returns the board afterwards
    # movx and movy are both either 1 or 0 or -1
    piece = board[y][x]
    if movx == 1 and x+1 < game_board_cols:
        target = board[y][x+1]
        if target == 0:
            board[y][x+1] = board[y][x]
            board[y][x] = 0
            x, y = x+1, y
    elif movx == -1 and x-1 >= 0:
        target = board[y][x-1]
        if target == 0:
            board[y][x-1] = board[y][x]
            board[y][x] = 0
            x, y = x-1, y
    if movy == 1 and y-1 >= 0:
        target = board[y-1][x]
        if target == 0:
            board[y-1][x] = board[y][x]
            board[y][x] = 0
            x, y = x, y-1
    elif movy == -1 and y+1 < game_board_rows:
        target = board[y+1][x]
        if target == 0:
            board[y+1][x] = board[y][x]
            board[y][x] = 0
            x, y = x, y+1
    
    return board

def tick(board):
    return board

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
    if x != -1 and y != -1:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if keys[pygame.K_0]:
                game_board[y][x] = 0
            if keys[pygame.K_1]:
                game_board[y][x] = Piece(-1)
            if keys[pygame.K_2]:
                game_board[y][x] = Piece(-2)
        else:
            if keys[pygame.K_0]:
                game_board[y][x] = 0
            if keys[pygame.K_1]:
                game_board[y][x] = Piece(1)
            if keys[pygame.K_2]:
                game_board[y][x] = Piece(2)
        
        if keys[pygame.K_UP]:
            game_board = move_piece(game_board, x, y, 0, 1)
        if keys[pygame.K_DOWN]:
            game_board = move_piece(game_board, x, y, 0, -1)
        if keys[pygame.K_LEFT]:
            game_board = move_piece(game_board, x, y, -1, 0)
        if keys[pygame.K_RIGHT]:
            game_board = move_piece(game_board, x, y, 1, 0)
    if keys[pygame.K_h]:
        game_board = hurt(game_board, x, y, 1)
    if keys[pygame.K_BACKSPACE]:
        game_board = []
        for i in range(game_board_rows):
            game_board.append([0]*game_board_cols)
    if keys[pygame.K_SPACE]:
        game_board = tick(game_board)
  
    # Update
    game_board = check_for_dead(game_board)
  
    # Draw
    for y in range(0, game_board_rows):
        for x in range(0, game_board_cols):
            xcoord, ycoord = x*squaresize, y*squaresize
            piece = game_board[y][x]
            if piece != 0:
                img = id2img[piece.idnum]
                screen.blit(img, (xcoord, ycoord))

    draw_grid(squaresize)
  
    pygame.display.flip()
    fpsClock.tick(fps)