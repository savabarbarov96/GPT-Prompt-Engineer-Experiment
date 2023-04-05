import pygame
import sys
import math
import random
import cv2
import numpy as np
import os

# Determine the current directory
if getattr(sys, 'frozen', False):
    CURRENT_DIR = os.path.dirname(sys.executable)
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_WIDTH = 15
LINE_COLOR = BLACK
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
TEXT_SIZE = 60
TEXT_SHADOW_OFFSET = 2
TEXT_ANIMATION_SPEED = 0.1
SHADOW_OFFSET = 5
SHADOW_COLOR = (100, 100, 100)
VIBRATION_OFFSET = 5
BLUR_AMOUNT = 0.5
BLUR_ITERATIONS = 20

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(WHITE)

# Use default pygame font
font = pygame.font.Font(None, TEXT_SIZE)

# Image paths
O_IMAGES_PATH = os.path.join(CURRENT_DIR, "Assets", "O")
X_IMAGES_PATH = os.path.join(CURRENT_DIR, "Assets", "X")

# Load O and X images
O_IMAGES = [pygame.image.load(os.path.join(O_IMAGES_PATH, f'O{i}.png')) for i in range(1, 10)]
X_IMAGES = [pygame.image.load(os.path.join(X_IMAGES_PATH, f'X{i}.png')) for i in range(1, 10)]

# Initialize the board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Convert mouse position to row and column
def get_row_col_from_mouse(pos):
    return pos[1] // 200, pos[0] // 200

# Draw the grid lines on the screen
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

# Draw O and X figures on the board
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

# Draw O at specified row and column
def draw_o(row, col):
    o_image = O_IMAGES[0]
    o_rect = o_image.get_rect()
    o_rect.center = (int(col * 200 + 100), int(row * 200 + 100))
    screen.blit(o_image, o_rect)

# Draw X at the specified row and column
# Draw X at the specified row and column
def draw_x(row, col):
    x_image = X_IMAGES[0]
    x_rect = x_image.get_rect()
    x_rect.center = (int(col * 200 + 100), int(row * 200 + 100))
    screen.blit(x_image, x_rect)

# Mark the square on the board with the player's symbol
def mark_square(row, col, player):
    board[row][col] = player

# Check if the square at the specified row and column is empty
def check_square(row, col):
    return board[row][col] is None

# Check if the board is full and the game is a draw
def check_draw():
    for row in board:
        for col in row:
            if col is None:
                return False
    return True

# Check if the specified player has won the game
def check_winner(player):
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

# Display the current player's turn
def display_turn(player):
    if not game_over:
        turn_text = f"Player {player} turn!"
        text_surface, text_rect, text_surface_shadow, text_rect_shadow = create_text_surface_with_shadow(turn_text, font, RED)
        screen.blit(text_surface_shadow, text_rect_shadow)
        screen.blit(text_surface, text_rect)

# Animate the text
def animate_text(text, progress, color):
    x = SCREEN_WIDTH // 2
    y = TEXT_SIZE // 2
    scale = 1 + math.sin(math.pi * progress) * TEXT_ANIMATION_SPEED
    draw_text(text, x, y, color, scale)

# Draw the text with shadow
def draw_text(text, x, y, color, scale=1.0):
    text_surface = font.render(text, True, color)
    text_surface_shadow = font.render(text, True, BLACK)
    rect = text_surface.get_rect()
    rect_shadow = text_surface_shadow.get_rect()
    rect.center = (x, y)
    rect_shadow.center = (x + TEXT_SHADOW_OFFSET * scale, y + TEXT_SHADOW_OFFSET * scale)
    screen.blit(text_surface_shadow, rect_shadow)
    screen.blit(text_surface, rect)

# Draw lines and set initial game state
draw_lines()
player = 'X'
game_over = False
winner_text = None
text_progress = 0

# Create a text surface with shadow
def create_text_surface_with_shadow(text, font, color):
    text_surface = font.render(text, True, color)
    text_surface_shadow = font.render(text, True, SHADOW_COLOR)
    text_rect = text_surface.get_rect()
    text_rect_shadow = text_surface_shadow.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, TEXT_SIZE // 2)
    text_rect_shadow.center = (SCREEN_WIDTH // 2 + SHADOW_OFFSET, TEXT_SIZE // 2 + SHADOW_OFFSET)
    return text_surface, text_rect, text_surface_shadow, text_rect_shadow
# Check if the "Play Again" button is clicked
def check_play_again_button_click(button_rect, mouse_pos):
    return button_rect.collidepoint(mouse_pos)
def apply_blur(surface, amount, iterations):
    if surface.get_width() == 0 or surface.get_height() == 0:
        return None
    
    np_surface = pygame.surfarray.array3d(surface)
    np_surface = cv2.cvtColor(np_surface, cv2.COLOR_RGB2BGR)
    for _ in range(iterations):
        np_surface = cv2.GaussianBlur(np_surface, (0, 0), amount)
    np_surface = cv2.cvtColor(np_surface, cv2.COLOR_BGR2RGB)
    blurred_surface = pygame.surfarray.make_surface(np_surface)
    return blurred_surface

# Draw a glassy button
def draw_glassy_button(text, x, y, width, height, font, color, alpha=128):
    button = pygame.Surface((width, height), pygame.SRCALPHA)
    button.fill((255, 255, 255, alpha))
    pygame.draw.rect(button, color, (0, 0, width, height), 2)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    button.blit(text_surface, text_rect)

    button_rect = button.get_rect(topleft=(x, y))
    return button, button_rect

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row, clicked_col = get_row_col_from_mouse(event.pos)
            if check_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()

                if check_winner(player):
                    game_over = True
                    winner_text = f"Player {player} wins!"
                elif check_draw():
                    game_over = True
                    winner_text = "It's a draw!"
                else:
                    player = 'O' if player == 'X' else 'X'

        if game_over:
            screen_copy = screen.copy()
            blurred_screen = apply_blur(screen_copy, BLUR_AMOUNT, BLUR_ITERATIONS)
            screen.blit(blurred_screen, (0, 0))

            if text_progress < 1:
                text_progress += 0.01
            else:
                text_progress = 1

            animate_text(winner_text, text_progress, RED)
            play_again_button, play_again_button_rect = draw_glassy_button("Play Again", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50, font, RED)
            play_again_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 * text_progress)
            play_again_button = pygame.transform.scale(play_again_button, (int(150 * text_progress), int(50 * text_progress)))
            screen.blit(play_again_button, play_again_button_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                if check_play_again_button_click(play_again_button_rect, (mouseX, mouseY)):
                    # Reset the game state
                    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                    player = 'X'
                    game_over = False
                    winner_text = ""
                    text_progress = 0
                    screen.fill(WHITE)  # clear the screen
                    draw_lines()  # redraw the grid lines
                    draw_figures()  # redraw the board figures


    display_turn(player)
    pygame.display.update()