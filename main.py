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
        self.SQUARE_WIDTH : int = 50
        self.screen_size  : int = self.SQUARE_WIDTH * self.board_size + 2 * self.SQUARE_WIDTH
        
        # Colors
        self.BACKGROUND   : tuple = (135, 206, 250)
        self.WHITE        : tuple = (255, 255, 255)
        self.BLACK        : tuple = (0, 0, 0)
        self.SEMI_RED     : tuple = (255, 0, 0, 150)  # RGBA
        self.BUTTON_COLOR : tuple = (70, 130, 180)
        self.TEXT_COLOR   : tuple = self.BLACK
        
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
        
        self.BOARD_SIZE_LIMIT: int = 12  # Maximum board size
        self.board_size = self.input_num("Size of the board (N x N): ", (self.SQUARE_WIDTH, self.SQUARE_WIDTH), self.BOARD_SIZE_LIMIT)
        
        self.GAME_MODE: str = self.get_mode()
        print(f"\033[92mGame mode selected: {self.GAME_MODE}\033[0m")
        
        self.screen_size = self.SQUARE_WIDTH * self.board_size + 2 * self.SQUARE_WIDTH  # recalculate the screen size based on the new board_size
        
        # Create an empty list
        # when representing the queens:
            # row is the index of the list
            # and the value is the column number
        self.board   : list = [-1 for _ in range(self.board_size)]
        self.answers : list = []
        
        # Board positioning
        self.BOARD_X : int = (self.screen_size - self.board_size * self.SQUARE_WIDTH) // 2  # starting x position of the chess board
        self.BOARD_Y : int = (self.screen_size - self.board_size * self.SQUARE_WIDTH) // 2  # starting y position of the chess board
        
        # Create the Pygame window for Queens Solver
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # to center the window
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption(f"{self.board_size} Queens Solver")
        
        # Load the queen images
        self.queen_b = pygame.image.load("pieces/queen_b.png").convert_alpha()
        self.queen_w = pygame.image.load("pieces/queen_w.png").convert_alpha()
        self.queen_b = pygame.transform.scale(self.queen_b, (self.SQUARE_WIDTH, self.SQUARE_WIDTH))
        self.queen_w = pygame.transform.scale(self.queen_w, (self.SQUARE_WIDTH, self.SQUARE_WIDTH))
        
        self.delay: float = min(0.01, 0.3 * (0.5 ** self.board_size)) * 1000  # delay in milliseconds
        
        self.screen.fill(self.BACKGROUND)  # draw the background
        self.game()
    
    # MARK: game
    def game(self) -> None:
        match self.GAME_MODE:
            case "Simulation":
                self.simulation()
            case "Manual":
                self.manual()
    
    # MARK: simulation
    def simulation(self) -> None:
        print(f"\033[92mStarting the {self.board_size}-Queens solver...\033[0m")
        col: int = 0
        self.draw_board(self.board)
        
        while col >= 0:
            self.board[col] += 1
            
            while self.board[col] < self.board_size and not self.is_valid_placement(col):
                # if the placement is not valid, move the queen to the next column
                self.board[col] += 1
                self.draw_board(self.board)
                self.handle_events()
            
            if self.board[col] < self.board_size:
                # if the queen is within bounds
                if col == self.board_size - 1:
                    self.answers.append(self.board.copy())
                    print(f"\033[92mSolution found \033[94m({len(self.answers)})\033[92m: \033[93m{self.board}\033[0m")
                    self.draw_board(self.board, show_threats=False)
                    pygame.time.wait(3 * 1000)  # Pause to show the solution
                    self.handle_events()
                else:
                    col += 1              # Move to the next column
                    self.board[col] = -1  # Reset the next column
            else:
                self.board[col] = -1  # Reset the current column
                col -= 1              # Backtrack to the previous column
            
            self.draw_board(self.board)
        
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
    def draw_board(self, board: list, error_full: bool = False, show_threats: bool = True) -> None:
        """Draw the sensor values on the screen."""
        # Draw each square based on sensor value
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_square(row, column, board, error_full, show_threats)
                pygame.display.flip()
                pygame.time.delay(int(self.delay))  # Delay for visual effect
    
    # MARK: draw_square
    def draw_square(self, row: int, column: int, board: list, error_full: bool = False, show_threats: bool = True) -> None:
        """Draw individual sensor squares."""
        color: tuple = self.WHITE if ((row + column) % 2) == 0 else self.BLACK
        
        # Draw the square
        square_rect = pygame.Rect(
            self.BOARD_X + row * self.SQUARE_WIDTH, 
            self.BOARD_Y + column * self.SQUARE_WIDTH, 
            self.SQUARE_WIDTH, 
            self.SQUARE_WIDTH
        )
        pygame.draw.rect(self.screen, color, square_rect)
        
        if board[row] == column:
            # Draw the queen
            self.screen.blit(self.queen_b if (row + column) % 2 == 0 else self.queen_w, square_rect.topleft)
        
        if show_threats:
            self.is_under_threat(row, column, square_rect, board, error_full)
    
    # MARK: is_under_threat
    def is_under_threat(self, row: int, column: int, square_rect: pygame.Rect, board: list, error_full: bool = False) -> bool:
        """Check if the (row, column) is threatened by any existing queen."""
        if error_full:
            row = self.board_size
        
        for r in range(row):
            col = board[r]
            if col == -1:
                continue
            if col == column or abs(col - column) == abs(r - row):
                self.draw_threat(square_rect)
                return True
        return False
    
    # MARK: draw_threat
    def draw_threat(self, square_rect: pygame.Rect) -> None:
        # Draw the threat indicator
        s = pygame.Surface((self.SQUARE_WIDTH, self.SQUARE_WIDTH), pygame.SRCALPHA)
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
                        # if the user presses enter key and there is text
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        # if the user presses backspace, remove the last character
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
    
    # MARK: manual
    def manual(self) -> None:
        self.user_board: list = [-1 for _ in range(self.board_size)]
        
        print("\033[96mClick on the board to place/remove queens. Press ENTER to solve.\033[0m")
        while True:
            self.draw_board(self.user_board, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        self.quit_game(0)
                    elif event.key == pygame.K_RETURN:  # if the user presses enter key
                        if self.is_valid_manual_board():
                            self.solve_from_partial()
                            return
                        else:
                            print("\033[91mInvalid setup. No two queens should threaten each other.\033[0m")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                    self.clear_text_at_location(self.SQUARE_WIDTH, self.SQUARE_WIDTH * 0.5)
    
    # MARK: is_valid_manual_board
    def is_valid_manual_board(self) -> bool:
        for i in range(self.board_size):
            if self.user_board[i] == -1:
                continue
            for j in range(i):
                if self.user_board[j] == -1:
                    continue
                if self.user_board[i] == self.user_board[j] or abs(self.user_board[i] - self.user_board[j]) == abs(i - j):
                    self.draw_text_at_location(f"Invalid Queen placement at ({i}, {self.user_board[i]})", self.SQUARE_WIDTH, self.SQUARE_WIDTH * 0.5)
                    return False
        return True
    
    # MARK: draw_text_at_location
    def draw_text_at_location(self, text: str, x: float, y: float) -> None:
        rendered_text = self.FONT.render(str(text), True, self.TEXT_COLOR)
        self.screen.blit(rendered_text, (x, y))
    
    # MARK: clear_text_at_location
    def clear_text_at_location(self, x: float, y: float) -> None:
        self.screen.fill(self.BACKGROUND, (x, y, self.screen_size, self.screen_size))
    
    # MARK: handle_click
    def handle_click(self, pos: tuple):
        x, y = pos
        col = (x - self.BOARD_X) // self.SQUARE_WIDTH
        row = (y - self.BOARD_Y) // self.SQUARE_WIDTH
        
        if (0 <= row < self.board_size) and (0 <= col < self.board_size):
            if self.user_board[col] == row:
                self.user_board[col] = -1  # remove queen
                return
            
            # if the square is empty, place a queen
            self.user_board[col] = row
    
    # MARK: solve_from_partial
    def solve_from_partial(self) -> None:
        print("\033[96mSolving from your custom board...\033[0m")
        col = 0
        
        # go through each coloumn and look for a queen
        while col < self.board_size and self.user_board[col] != -1:
            col += 1  # queen is found
        
        # if the number of queens found is equal to the board size, add it to the answers and find the next, you dont have to verify this because it is already veryfied in manual using is_valid_manual_board
        if col == self.board_size:
            print("\033[93mBoard already has a complete solution!\033[0m")
            self.answers.append(self.user_board.copy())
            self.draw_board(self.user_board, show_threats=False)
            pygame.time.wait(1000)  # Pause to show the solution
        
        self.manual_game()
        print(f"\033[92mAll solutions found \033[94m({len(self.answers)})\033[92m: \033[93m{self.answers}\033[0m")
    
    # MARK: manual_game
    def manual_game(self) -> None:
        print(f"\033[92mStarting the manual {self.board_size}-Queens solver...\033[0m")
        col: int = 0
        self.draw_board(self.board)
        
        while col >= 0:
            if self.user_board[col] == -1:
                # if the user has not placed a queen, place a queen
                self.board[col] += 1
            elif self.user_board[col] == self.board[col]:
                col -= 1  # Backtrack to the previous column
                continue
            else:
                # if the user has placed a queen, set the board to the user board
                self.board[col] = self.user_board[col]
                print(f"\033[93mUser placed a queen at ({col}, {self.board[col]})\033[0m")
            
            while self.board[col] < self.board_size and not self.is_valid_placement(col):
                # if the placement is not valid, move the queen to the next column
                self.board[col] += 1
                self.draw_board(self.board)
                self.handle_events()
            
            if self.board[col] < self.board_size:
                # if the queen is within bounds
                if col == self.board_size - 1:
                    self.answers.append(self.board.copy())
                    print(f"\033[92mSolution found \033[94m({len(self.answers)})\033[92m: \033[93m{self.board}\033[0m")
                    self.draw_board(self.board, show_threats=False)
                    pygame.time.wait(3 * 1000)  # Pause to show the solution
                    self.handle_events()
                else:
                    col += 1              # Move to the next column
                    self.board[col] = -1  # Reset the next column
            else:
                self.board[col] = -1  # Reset the current column
                col -= 1              # Backtrack to the previous column
            
            self.draw_board(self.board)
    
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
