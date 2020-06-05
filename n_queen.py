import numpy as np
import pygame
import sys
import math

# global variables
ROW_COUNT = 8
COL_COUNT = 8
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 8)
WHITE, BLACK, RED, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
IMAGE = pygame.image.load(r'images.jpg')
IMAGE_SMALL = pygame.transform.scale(IMAGE, (100, 100))


# ----------------------------Game functions-------------------------------------
def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


# def print_board(board):
#     print(board)


def is_valid_position(board, row, col):
    return board[row][col] == 0


def put_queen(board, row, col):
    board[row][col] = 1


def change_board(board, row, col):
    # changing rows and columns
    for k in range(0, ROW_COUNT):
        if board[row][k] != 1:
            board[row][k] = 3
        if board[k][col] != 1:
            board[k][col] = 3
    # changing diagonals
    for k in range(0, ROW_COUNT):
        for l in range(0, ROW_COUNT):
            if (k + l == row + col) or (k - l == row - col):
                if board[k][l] != 1:
                    board[k][l] = 3


def is_winner():
    queen_count = 0
    for r in board:
        if 1 in r:
            queen_count += 1
    if queen_count == ROW_COUNT:
        return True


def is_attack(i, j):
    # checking rows and columns
    for k in range(0, ROW_COUNT):
        if board[i][k] == 1 or board[k][j] == 1:
            return True
    # checking diagonals
    for k in range(0, ROW_COUNT):
        for l in range(0, ROW_COUNT):
            if (k + l == i + j) or (k - l == i - j):
                if board[k][l] == 1:
                    return True
    return False


def generate_result(n):
    if n == 0:
        return True
    for i in range(0, ROW_COUNT):
        for j in range(0, ROW_COUNT):
            if (not (is_attack(i, j))) and (board[i][j] != 1):
                board[i][j] = 1
                if generate_result(n - 1):
                    return True
                board[i][j] = 0
    return False


def check_game(board):
    if 0 in board:
        return False
    return True

# -----------------------------------------------------------------------------


# ---------------------------GUI functions-------------------------------------
def button_text():
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('SOLVE', True, WHITE)
    screen.blit(text, (15, ROW_COUNT*SQUARESIZE+45))
    text = font.render('CLEAR', True, WHITE)
    screen.blit(text, ((COL_COUNT-1)*SQUARESIZE+15, ROW_COUNT*SQUARESIZE+45))


def text_winner():
    font = pygame.font.Font('freesansbold.ttf', ROW_COUNT*4)
    text = font.render('Congrats, You solved it!', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (COL_COUNT/2*SQUARESIZE, (ROW_COUNT)*(SQUARESIZE+10))
    screen.blit(text, textRect)
    pygame.display.update()


def text_loser():
    font = pygame.font.Font('freesansbold.ttf', ROW_COUNT*4)
    text = font.render('Uh oh! Try Again', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (COL_COUNT/2*SQUARESIZE, (ROW_COUNT)*(SQUARESIZE+10))
    screen.blit(text, textRect)
    pygame.display.update()


def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if r % 2 == 0:
                if c % 2 == 0:
                    pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            else:
                if c % 2 == 0:
                    pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))

    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == 1:
                screen.blit(IMAGE_SMALL, (c * SQUARESIZE, r * SQUARESIZE))
            elif board[r][c] == 3:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.draw.rect(screen, BLUE, (0 * SQUARESIZE, ROW_COUNT * SQUARESIZE, SQUARESIZE, SQUARESIZE))  # solve button
    pygame.draw.rect(screen, BLUE, ((COL_COUNT - 1) * SQUARESIZE, ROW_COUNT * SQUARESIZE, SQUARESIZE, SQUARESIZE))  # clear button
    button_text()
    pygame.display.update()


# -------------------------------------------------------------------------------

board = create_board()
game_over = False

# pygame initialisations
pygame.init()
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("n-Queens Puzzle")
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos[0], event.pos[1]
            row, col = int(math.floor(posy / SQUARESIZE)), int(math.floor(posx / SQUARESIZE))

            # to solve the puzzle
            if row == ROW_COUNT and col == 0:
                board = create_board()
                generate_result(ROW_COUNT)
                draw_board(board)

            # to clear the board
            elif row == ROW_COUNT and col == COL_COUNT - 1:
                board = create_board()
                draw_board(board)

            # to play the game
            else:
                if is_valid_position(board, row, col):
                    put_queen(board, row, col)
                    change_board(board, row, col)
                    draw_board(board)

                game_over = check_game(board)

if is_winner():
    text_winner()
else:
    text_loser()

pygame.time.wait(3000)

# ---------------------------------------------------------------------------------


# -------------------------------Command line game-----------------------------------
# while not game_over:
#     row, col = map(int, input("Enter the position : ").split())
#     if is_valid_position(board, row, col):
#         put_queen(board, row, col)
#         change_board(board, row, col)
#         print_board(board)
#     else:
#         print("INVALID POSITION!!")
#     game_over = check_game(board)
#
# if is_winner():
#     print("You solved it. Congratulations!!!")
# else:
#     choice = input("Want to reveal the answer ? (y/n) : ")
#     if choice == 'y' or choice == 'Y':
#         generate_result(ROW_COUNT)
#         print_board(board_new)
#     else:
#         print("Thank-you for playing :)")
#         exit()
