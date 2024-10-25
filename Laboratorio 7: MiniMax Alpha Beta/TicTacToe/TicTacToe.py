import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 400, 400
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
CELL_SIZE = WIDTH // 4

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 4x4")

# Utility Functions
def draw_board():
    """Draws the 4x4 board grid."""
    for x in range(0, WIDTH+1, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), 10)
    for y in range(0, HEIGHT+1, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y), 10)

def draw_symbols(board, cross, circle):
    """Draws X and O symbols on the board."""
    for row in range(4):
        for col in range(4):
            if board[row][col] == 'X':
                screen.blit(cross, (col * CELL_SIZE + 4, row * CELL_SIZE + 4))
            elif board[row][col] == 'O':
                screen.blit(circle, (col * CELL_SIZE + 4, row * CELL_SIZE + 4))

def get_cell_coords(pos):
    """Gets the coordinates of the clicked cell."""
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

def handle_mouse_events(pos, board, current_player):
    """Handles player click and updates the board."""
    row, col = get_cell_coords(pos)
    if board[row][col] == ' ':
        board[row][col] = current_player
        return True
    return False

def check_winner(board):
    """Checks if there's a winner."""
    for row in range(4):
        if board[row][0] == board[row][1] == board[row][2] == board[row][3] != ' ':
            return board[row][0]
    for col in range(4):
        if board[0][col] == board[1][col] == board[2][col] == board[3][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] != ' ':
        return board[0][0]
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] != ' ':
        return board[0][3]
    return 'Tie' if all(board[row][col] != ' ' for row in range(4) for col in range(4)) else None

def minimax(board, depth, is_maximizing, alpha, beta, max_depth=4):
    """Minimax algorithm with Alpha-Beta pruning and a maximum depth limit."""
    winner = check_winner(board)
    if winner == 'X':
        return -10 + depth  # Penalize deeper wins for the opponent
    elif winner == 'O':
        return 10 - depth  # Reward faster wins for the bot
    elif winner == 'Tie':
        return 0
    
    # Limitar la profundidad para mejorar rendimiento
    if depth >= max_depth:
        return 0  # Considera empate en profundidad máxima

    if is_maximizing:
        max_eval = -float('inf')
        for row in range(4):
            for col in range(4):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta, max_depth)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(4):
            for col in range(4):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta, max_depth)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def bot_turn(board):
    """Bot uses Minimax with Alpha-Beta pruning to decide its move."""
    best_score = -float('inf')
    best_move = None
    for row in range(4):
        for col in range(4):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False, -float('inf'), float('inf'), max_depth=4)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        board[row][col] = 'O'

def display_winner(winner):
    """Displays the winner on the screen."""
    font = pygame.font.Font(None, 74)
    wallpaper = pygame.image.load("Laboratorio 7: MiniMax Alpha Beta/TicTacToe/wallpaper.png").convert_alpha()

    # Calculate the area to display the winner
    area_height = HEIGHT // 3
    area_top = (HEIGHT - area_height) // 2
    area_rect = pygame.Rect(0, area_top, WIDTH, area_height)

    # Blit the wallpaper to the area
    wallpaper_cropped = wallpaper.subsurface(pygame.Rect(0, 0, WIDTH, area_height))
    screen.blit(wallpaper_cropped, (0, area_top))
    
    # Prepare the text
    if winner == 'O' or winner == 'X':
        text = f"{winner} wins!!!"
    else:
        text = "It's a tie!!!"

    text_surface = font.render(text, True, WHITE)
    shadow_surface = font.render(text, True, BLACK)
    
    # Calculate the position for the text
    text_rect = text_surface.get_rect(center=(WIDTH // 2, area_top + area_height // 2))
    shadow_rect = text_rect.copy()
    shadow_rect.move_ip(2, 2)  # Move the shadow slightly to the bottom-right
    
    # Blit the shadow text and then the main text
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)
    
    pygame.display.update()

# Game Modes
def pvp_mode(board, cross, circle):
    """Handles Player vs Player mode."""
    current_player = 'X'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if handle_mouse_events(pos, board, current_player):
                    current_player = 'O' if current_player == 'X' else 'X'
                    draw_board()
                    draw_symbols(board, cross, circle)
                    pygame.display.update()
                    winner = check_winner(board)
                    if winner:
                        return winner

def cpu_vs_player_mode(board, cross, circle):
    """Handles CPU vs Player mode."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if handle_mouse_events(pos, board, 'X'):
                    draw_board()
                    draw_symbols(board, cross, circle)
                    pygame.display.update()
                    if winner := check_winner(board):
                        return winner
                    pygame.time.wait(500)
                    bot_turn(board)
                    draw_board()
                    draw_symbols(board, cross, circle)
                    pygame.display.update()
                    if winner := check_winner(board):
                        return winner

def cpu_vs_cpu_mode(board, cross, circle):
    """Handles CPU vs CPU mode."""
    running = True
    current_player = 'X'
    
    while running:
        pygame.time.wait(500)  # Espera 500 ms entre movimientos
        if current_player == 'X':
            # Turno de 'X'
            best_score = float('inf')  # Minimizing for 'X'
            best_move = None
            for row in range(4):
                for col in range(4):
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        score = minimax(board, 0, True, -float('inf'), float('inf'), max_depth=4)
                        board[row][col] = ' '
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)
            if best_move:
                row, col = best_move
                board[row][col] = 'X'
        else:
            # Turno de 'O'
            best_score = -float('inf')  # Maximizing for 'O'
            best_move = None
            for row in range(4):
                for col in range(4):
                    if board[row][col] == ' ':
                        board[row][col] = 'O'
                        score = minimax(board, 0, False, -float('inf'), float('inf'), max_depth=4)
                        board[row][col] = ' '
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
            if best_move:
                row, col = best_move
                board[row][col] = 'O'

        draw_board()
        draw_symbols(board, cross, circle)
        pygame.display.update()

        if winner := check_winner(board):
            return winner
        
        # Cambia el jugador después de cada turno
        current_player = 'O' if current_player == 'X' else 'X'

# Main Game Function
def main_game(option):
    """Starts the selected game mode."""
    board = [[' ' for _ in range(4)] for _ in range(4)]
    cross = pygame.image.load("Laboratorio 7: MiniMax Alpha Beta/TicTacToe/Cross.png").convert_alpha()
    circle = pygame.image.load("Laboratorio 7: MiniMax Alpha Beta/TicTacToe/Circle.png").convert_alpha()
    screen.fill((50, 50, 50))
    draw_board()
    pygame.display.update()
    pygame.time.wait(500)
    if option == 1:
        return pvp_mode(board, cross, circle)
    elif option == 2:
        return cpu_vs_player_mode(board, cross, circle)
    elif option == 3:
        return cpu_vs_cpu_mode(board, cross, circle)

# Main Menu
def main_menu():
    """Displays the main menu and returns the selected option."""
    font = pygame.font.Font(None, 74)
    screen.fill(BLACK)
    wallpaper = pygame.image.load("Laboratorio 7: MiniMax Alpha Beta/TicTacToe/wallpaper.png").convert_alpha()
    screen.blit(wallpaper, [0, 0])
    
    options = ['PvP', 'CPU vs Player', 'CPU vs CPU']
    texts = [font.render(opt, True, WHITE) for opt in options]
    shadow_texts = [font.render(opt, True, BLACK) for opt in options]
    rects = [text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 100)) for i, text in enumerate(texts)]

    for i, text in enumerate(texts):
        shadow_rect = rects[i].copy()
        shadow_rect.move_ip(3, 3)  # Move the shadow slightly to the bottom-right
        screen.blit(shadow_texts[i], shadow_rect)  # Blit the shadow text
        screen.blit(text, rects[i])  # Blit the main text

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        return i + 1

# Main Loop
def main_loop():
    while True:
        option = main_menu()
        winner = main_game(option)
        display_winner(winner)
        print(f"Winner: {winner}")
        pygame.time.wait(2500)

if __name__ == "__main__":
    main_loop()
