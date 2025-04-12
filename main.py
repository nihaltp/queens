
"""
    8 Queens solver
    
    Made by: NIHAL T P
    GitHub: https://github.com/nihaltp
    LinkedIn: https://www.linkedin.com/in/nihal-tp
"""
import os

# Hide the Pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
import random
from time import sleep

try:
    import pygame
except ImportError:
    print("\033[91mPygame is not installed. Please install it using \033[92m'pip install pygame'\033[0m")
    sys.exit(1)

# MARK: solver
class solver:
    def __init__(self) -> None:
        try:
            pygame.init() # Initialize Pygame
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            sys.exit(1)
        
        self.board_size : int = 8
        self.square_width : int = 50
        self.screen_size : int = self.square_width * self.board_size + 2 * self.square_width
        
        # Create an empty 8x8 matrix
        # when representing the queens the value is the column number
        # row is the index of the list
        self.board : list = [-1 for _ in range(self.board_size)]
        
        # Colors
        self.background : tuple = (135, 206, 250)
        self.yellow : tuple = (255, 255, 0)
        self.white : tuple = (255, 255, 255)
        self.black : tuple = (0, 0, 0)
        
        # Board positioning
        self.board_x : int = (self.screen_size - self.board_size * self.square_width) // 2
        self.board_y : int = (self.screen_size - self.board_size * self.square_width) // 2
        
        # Create the Pygame window
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption(f"{self.board_size} Queens Solver")
        
        # Pygame font setup
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 28)
        
        self.queen_image = pygame.image.load("pieces/queen.png").convert_alpha()
        self.queen_image = pygame.transform.scale(self.queen_image, (self.square_width, self.square_width))
        
        self.delay : int = 0.01
        
        self.screen.fill(self.background)  # draw the background
        self.game()
    
    # MARK: game
    def game(self) -> None:
        # Game loop
        self.queen_placement()
    
    # MARK: queen_placement
    def queen_placement(self, column: int = 0) -> None:
        print("\033[92mStarting the game...\033[0m")
        for col in range(self.board_size):
            if col < column:
                continue
            if self.board[col] == -1:
                self.board[col] = 0  # Start from the first row
            self.draw_board()
            self.handle_events()
            
            # Check if the queen placement is valid
            while not self.is_valid_placement():
                self.board[col] += 1  # Move to the next row
                print(f"Incrementing row \033[93m{col}\033[0m to \033[94m{self.board[col]}\033[0m")
                
                if self.board[col] >= self.board_size:
                    # Backtrack to the previous column
                    print(f"\033[91mBacktracking by resetting \033[93m{col}\033[91m and incrementing \033[93m{col - 1}\033[0m")
                    self.board[col] = -1  # Reset the current column
                    self.board[col - 1] += 1  # On the previous row, Move to the next column
                    self.queen_placement(col - 1)  # Recursive call to the previous column
                    return
                
                self.draw_board()
                self.handle_events()
            
            print(f"\033[92m{self.board}\033[0m")
    
    # MARK: is_valid_placement
    def is_valid_placement(self) -> bool:
        """Check if the current queen placement is valid.
        
        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        
        for i in range(self.board_size):
            # Check if the queen is placed
            if self.board[i] == -1:
                print(f"\033[91mQueen not placed in \033[93mrow: \033[94m{i}\033[0m")
                return True
            
            if self.board[i] >= self.board_size:
                print(f"\033[91mQueen out of bounds in \033[93mrow: \033[94m{i}\033[0m")
                return False
            
            # Check if the queen is in the same row
            for j in range(self.board_size):
                if i == j:
                    continue # Skip the same row
                if self.board[j] == -1:
                    break
                if self.board[i] == self.board[j]:
                    print(f"\033[91mQueens in same \033[93mcolumn: \033[94m{i} and {j}\033[0m")
                    return False
                
                # Check if the queens are in the same diagonal
                if abs(self.board[i] - self.board[j]) == abs(i - j):
                    print(f"\033[91mQueens in same \033[95mdiagonal: \033[94m{i} and {j}\033[0m")
                    return False
        
        return True
    
    # MARK: draw_board
    def draw_board(self) -> None:
        """Draw the sensor values on the screen."""
        # Draw each square based on sensor value
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_square(row, column, True if self.board[row] == column else False)
                pygame.display.flip()
                sleep(self.delay)  # Delay for visual effect
    
    # MARK: draw_square
    def draw_square(self, row: int, column: int, queen: bool) -> None:
        """Draw individual sensor squares."""
        color = self.white if ((row + column) % 2) == 0 else self.black
        
        # Draw the square
        square_rect = pygame.Rect(
            self.board_x + row * self.square_width, 
            self.board_y + column * self.square_width, 
            self.square_width, 
            self.square_width
        )
        pygame.draw.rect(self.screen, color, square_rect)
        
        if queen:
            # Draw the queen
            self.screen.blit(self.queen_image, square_rect.topleft)
    
    # MARK: handle_events
    def handle_events(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                elif event.key == pygame.K_q:
                    self.quit_game()
                elif event.key == pygame.K_UP:
                    self.delay *= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
                elif event.key == pygame.K_DOWN:
                    self.delay /= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
    
    # MARK: quit_game
    def quit_game(self) -> None:
        """Exit the Pygame window."""
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = solver()
