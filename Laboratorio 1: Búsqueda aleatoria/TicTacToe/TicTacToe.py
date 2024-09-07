import pygame
import random

# Initialize Pygame
pygame.init()

# Window dimensions
width = 400
height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Cell size
cell_size = width // 4

# Create the window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe 4x4")

# Function to draw the board
def draw_board():
    for x in range(0, width+1, cell_size):
        pygame.draw.line(screen, black, (x, 0), (x, height), 10)
    for y in range(0, height+1, cell_size):
        pygame.draw.line(screen, black, (0, y), (width, y), 10)

# Function to draw the symbols (X or O)
def draw_symbols(board, cross, circle):
    for row in range(4):
        for col in range(4):
            if board[row][col] == 'X':
                screen.blit(cross, (col * cell_size + 4, row * cell_size + 4))
            elif board[row][col] == 'O':
                screen.blit(circle, (col * cell_size + 4, row * cell_size + 4))
    return 0

# Function to get the selected cell coordinates
def get_cell_coords(pos):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return row, col

# Function to handle mouse events
def handle_mouse_events(pos, board):
    row, col = get_cell_coords(pos)
    if board[row][col] == ' ':
        board[row][col] = 'X'
        return 1
    else:
        return 0

# Function for the bot's turn
def botPlayTurn(board):
    available_positions = [(row, col) for row in range(4) for col in range(4) if board[row][col] == ' ']

    if available_positions:
        x, y = random.choice(available_positions)
        board[x][y] = 'O'
    
    return 0

# Function to display the winner message
def draw_winner(winner, screen):
    floating_window = pygame.Surface((400, 100))
    floating_window.fill((255, 255, 255))

    font = pygame.font.Font(None, 36)
    if winner == 'X':
        text = font.render("You win!!!", True, (0, 0, 0))
    elif winner == 'O':
        text = font.render("You lose!!!", True, (0, 0, 0))
    elif winner == 'Tie':
        text = font.render("It's a tie!!!", True, (0, 0, 0))
    else:
        return 0

    floating_window.blit(text, (20, 40))
    screen.blit(floating_window, (0, 150))

# Function to check for a winner
def check_winner(board):
    # Check rows
    for row in range(4):
        if board[row][0] == board[row][1] == board[row][2] == board[row][3] != ' ':
            return board[row][0]
    
    # Check columns
    for col in range(4):
        if board[0][col] == board[1][col] == board[2][col] == board[3][col] != ' ':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] != ' ':
        return board[0][0]
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] != ' ':
        return board[0][3]
    
    # Check for a tie
    for row in range(4):
        for col in range(4):
            if board[row][col] == ' ':
                return 0  # Game is still ongoing
    
    return 'Tie'  # No empty spaces and no winner

# Function to restart the game
def restart(board, screen):
    for row in range(4):
        for col in range(4):
            board[row][col] = ' '  # Reset each cell of the board
    screen.fill((50, 50, 50))
    draw_board()
    pygame.display.update()

# Main game loop function
def main_loop():
    running = True
    board = [[' ' for _ in range(4)] for _ in range(4)]  # Initialize the board

    # Load symbol textures
    image_cross = pygame.image.load("TicTacToe/Cross.png").convert_alpha()
    cross = pygame.Surface(image_cross.get_size(), pygame.SRCALPHA)
    cross.blit(image_cross, (0, 0))

    image_circle = pygame.image.load("TicTacToe/Circle.png").convert_alpha()
    circle = pygame.Surface(image_circle.get_size(), pygame.SRCALPHA)
    circle.blit(image_circle, (0, 0))

    screen.fill((50, 50, 50))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if handle_mouse_events(pos, board):
                    draw_symbols(board, cross, circle)
                    winner = check_winner(board)
                    draw_winner(winner, screen)
                    pygame.display.update()

                    if winner == 0:
                        pygame.time.wait(500)
                        botPlayTurn(board)
                        draw_symbols(board, cross, circle)

        screen.fill((50, 50, 50))
        draw_board()
        draw_symbols(board, cross, circle)
        winner = check_winner(board)
        draw_winner(winner, screen)
        pygame.display.update()

        if winner != 0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    restart(board, screen)
                    break

if __name__ == "__main__":
    main_loop()
