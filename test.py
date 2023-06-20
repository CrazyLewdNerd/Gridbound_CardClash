import pygame

# Game class
class TicTacToeGame:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.cell_size = self.width // self.grid_size
        self.board = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.current_player = 'X'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                x, y = pygame.mouse.get_pos()
                row = y // self.cell_size
                col = x // self.cell_size
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.current_player
                    if self.current_player == 'X':
                        self.current_player = 'O'
                    else:
                        self.current_player = 'X'

    def draw(self, screen, active):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        screen.fill(WHITE)

        for i in range(1, self.grid_size):
            pygame.draw.line(screen, BLACK, (i * self.cell_size, 0), (i * self.cell_size, self.height))
            pygame.draw.line(screen, BLACK, (0, i * self.cell_size), (self.width, i * self.cell_size))

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                symbol = self.board[row][col]
                if symbol == 'X':
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    pygame.draw.line(screen, BLACK, (x - 40, y - 40), (x + 40, y + 40), 4)
                    pygame.draw.line(screen, BLACK, (x - 40, y + 40), (x + 40, y - 40), 4)
                elif symbol == 'O':
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    pygame.draw.circle(screen, BLACK, (x, y), 40, 4)

        if active:
            pygame.draw.rect(screen, RED, (self.width - 50, self.height - 50, 40, 40))

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 300, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")

# Create game instances
game1 = TicTacToeGame(width, height, 3)
game2 = TicTacToeGame(width, height, 3)

# Define game states
games = [game1, game2]
current_game = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:  # Right mouse button
                x, y = pygame.mouse.get_pos()
                if width - 50 <= x <= width - 10 and height - 50 <= y <= height - 10:
                    current_game = (current_game+1)%len(games)

                    # Draw the games
                for i, game in enumerate(games):
                    active = i==current_game
                    game.draw(screen, active)

                # Update the screen
                pygame.display.flip()

                # Quit the game
                pygame.quit()
