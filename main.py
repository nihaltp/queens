"""
    N Queens solver
    
    Made by: NIHAL T P
    GitHub: https://github.com/nihaltp
    LinkedIn: https://www.linkedin.com/in/nihal-tp
"""

import os

# Hide the Pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
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
            self.quit_game(1)
        
        self.board_size   : int = 8  # for making the inital window
        self.square_width : int = 50
        self.screen_size  : int = self.square_width * self.board_size + 2 * self.square_width
        
        # Colors
        self.BACKGROUND   : tuple = (135, 206, 250)
        self.WHITE        : tuple = (255, 255, 255)
        self.BLACK        : tuple = (0, 0, 0)
        self.SEMI_RED     : tuple = (255, 0, 0, 150)  # RGBA
        self.BUTTON_COLOR : tuple = (70, 130, 180)
        
        # Button properties
        self.BUTTON_WIDTH: int = 200
        self.BUTTON_HEIGHT: int = self.BUTTON_WIDTH // 4
        self.BUTTON_MARGIN_X: int = self.BUTTON_WIDTH // 4
        self.BUTTON_MARGIN_Y: int = self.BUTTON_HEIGHT // 2
        
        self.BUTTON_POSITIONS = {
            "Simulation": (25, 50),
            "Manual": (25 + self.BUTTON_WIDTH + 25, 50),
        }
        
        # Create the Pygame window for Getting Board Size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size//4))
        pygame.display.set_caption("N-Queens Solver Board Size")
        
        # Pygame font setup
        pygame.font.init()
        self.FONT = pygame.font.SysFont(None, 28)
        
        self.board_size_limit: int = 12  # Maximum board size
        self.board_size = self.input_num("Size of the board (N x N): ", (self.square_width, self.square_width), self.board_size_limit)
        
        self.game_mode: str = self.get_mode()
        print(f"\033[92mGame mode selected: {self.game_mode}\033[0m")
        
        self.screen_size = self.square_width * self.board_size + 2 * self.square_width  # recalculate the screen size based on the new board_size
        
        # Create an empty 8x8 matrix
        # when representing the queens:
            # row is the index of the list
            # and the value is the column number
        self.board   : list = [-1 for _ in range(self.board_size)]
        self.answers : list = []
        
        # Board positioning
        self.board_x : int = (self.screen_size - self.board_size * self.square_width) // 2
        self.board_y : int = (self.screen_size - self.board_size * self.square_width) // 2
        
        # Create the Pygame window for Queens Solver
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # to center the window
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption(f"{self.board_size} Queens Solver")
        
        self.queen_b = pygame.image.load("pieces/queen_b.png").convert_alpha()
        self.queen_w = pygame.image.load("pieces/queen_w.png").convert_alpha()
        self.queen_b = pygame.transform.scale(self.queen_b, (self.square_width, self.square_width))
        self.queen_w = pygame.transform.scale(self.queen_w, (self.square_width, self.square_width))
        
        self.delay = min(0.01, 0.3 * (0.5 ** self.board_size))
        
        self.screen.fill(self.BACKGROUND)  # draw the background
        self.game()
    
    # MARK: game
    def game(self) -> None:
        match self.game_mode:
            case "Simulation":
                self.simulation()
            case "Manual":
                pass
    
    # MARK: simulation
    def simulation(self) -> None:
        print(f"\033[92mStarting the {self.board_size}-Queens solver...\033[0m")
        col: int = 0
        self.draw_board()
        
        while col >= 0:
            self.board[col] += 1
            
            while self.board[col] < self.board_size and not self.is_valid_placement(col):
                # if the placement is not valid, move the queen to the next column
                self.board[col] += 1
                self.draw_board()
                self.handle_events()
            
            if self.board[col] < self.board_size:
                # if the queen is within bounds
                if col == self.board_size - 1:
                    self.answers.append(self.board.copy())
                    print(f"\033[92mSolution found \033[94m({len(self.answers)})\033[92m: \033[93m{self.board}\033[0m")
                    self.draw_board()
                    sleep(3) # Pause to show the solution
                    self.handle_events()
                else:
                    col += 1              # Move to the next column
                    self.board[col] = -1  # Reset the next column
            else:
                self.board[col] = -1  # Reset the current column
                col -= 1              # Backtrack to the previous column
            
            self.draw_board()
        
        print(f"\033[92mAll solutions found \033[94m({len(self.answers)})\033[92m: \033[93m{self.answers}\033[0m")
    
    # MARK: is_valid_placement
    def is_valid_placement(self, current_col: int) -> bool:
        """Check if the current queen placement is valid.
        
        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        
        for i in range(current_col):
            if (self.board[i] == self.board[current_col] or  # Check for column
                abs(self.board[i] - self.board[current_col]) == abs(i - current_col)):  # Check for diagonal
                return False
        return True
    
    # MARK: draw_board
    def draw_board(self) -> None:
        """Draw the sensor values on the screen."""
        # Draw each square based on sensor value
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_square(row, column)
                pygame.display.flip()
                sleep(self.delay)  # Delay for visual effect
    
    # MARK: draw_square
    def draw_square(self, row: int, column: int) -> None:
        """Draw individual sensor squares."""
        color: tuple = self.WHITE if ((row + column) % 2) == 0 else self.BLACK
        
        # Draw the square
        square_rect = pygame.Rect(
            self.board_x + row * self.square_width, 
            self.board_y + column * self.square_width, 
            self.square_width, 
            self.square_width
        )
        pygame.draw.rect(self.screen, color, square_rect)
        
        if self.board[row] == column:
            # Draw the queen
            self.screen.blit(self.queen_b if (row + column) % 2 == 0 else self.queen_w, square_rect.topleft)
        
        self.is_under_threat(row, column, square_rect)
    
    # MARK: is_under_threat
    def is_under_threat(self, row: int, column: int, square_rect: pygame.Rect) -> bool:
        """Check if the (row, column) is threatened by any existing queen."""
        for r in range(row):
            col = self.board[r]
            if col == -1:
                continue
            if col == column or abs(col - column) == abs(r - row):
                self.draw_threat(square_rect)
                return True
        return False
    
    # MARK: draw_threat
    def draw_threat(self, square_rect: pygame.Rect) -> None:
        # Draw the threat indicator
        s = pygame.Surface((self.square_width, self.square_width), pygame.SRCALPHA)
        s.fill(self.SEMI_RED)
        self.screen.blit(s, square_rect.topleft)
    
    # MARK: handle_events
    def handle_events(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    self.quit_game(0)
                elif event.key == pygame.K_UP:
                    self.delay *= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
                elif event.key == pygame.K_DOWN:
                    self.delay /= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
    
    # MARK: input_num
    def input_num(self, prompt: str, position: tuple, limit: int) -> int:
        input_active: bool = True
        input_text: list = []
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        self.quit_game(0)
                    elif event.unicode == "\r" and input_text:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < len(str(limit)) and event.unicode.isdigit():
                        # Limit the length of the text
                        # and check if the input is a digit
                        input_text.append(event.unicode)
            
            self.screen.fill(self.BACKGROUND)
            
            # Display the input text
            current_text: str = ''.join(input_text)
            value: str = f"{prompt} {current_text}"
            text = self.FONT.render(value, True, self.BLACK)
            text_rect = text.get_rect(topleft = position)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
        
        current_num: int = int(current_text)
        while current_num > limit:
            current_num = self.input_num(prompt + f" limit is {limit}", position, limit)
        return current_num
    
    # MARK: get_mode
    def get_mode(self) -> str:
        """Get the game mode"""
        self.screen.fill(self.BACKGROUND)
        self.draw_buttons()
        
        while True:
            self.handle_events()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # return if it is not None
                    mode = self.handle_buttons()
                    if mode is not None:
                        return mode
    
    # MARK: draw_buttons
    def draw_buttons(self) -> None:
        """Draw the buttons on the screen."""
        for button_name in self.BUTTON_POSITIONS.keys():
            # Draw the buttons
            button_position = self.BUTTON_POSITIONS[button_name]
            button = pygame.Rect(button_position, (self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, button)
            
            text = self.FONT.render(button_name, True, self.BLACK)
            text_rect = text.get_rect(center=(button_position[0] + self.BUTTON_MARGIN_X, button_position[1] + self.BUTTON_MARGIN_Y))
            self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    # MARK: handle_buttons
    def handle_buttons(self) -> str:
        """Handle button clicks."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button_name, pos in self.BUTTON_POSITIONS.items():
            if pos[0] <= mouse_x <= pos[0] + self.BUTTON_WIDTH and pos[1] <= mouse_y <= pos[1] + self.BUTTON_HEIGHT:
                return button_name
        return ""
    
    # MARK: quit_game
    def quit_game(self, error: int = 0) -> None:
        """Exit the Pygame window."""
        if hasattr(self, 'answers') and self.answers:
            print(f"\033[92mSolutions found \033[94m({len(self.answers)})\033[92m: \033[93m{self.answers}\033[0m")
        elif hasattr(self, 'answers'):
            print("\033[91mNo solutions were found.\033[0m")
        print("\033[93mExiting the game...\033[0m")
        pygame.quit()
        sys.exit(error)


if __name__ == "__main__":
    game = solver()
