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
import signal

from boards.load_board import load_board
from boards.save_board import save_board

try:
    import pygame
except ImportError:
    print("\033[91mPygame is not installed. Please install it using \033[92m'pip install pygame'\033[0m")
    sys.exit(1)
except KeyboardInterrupt:
    print("Ctrl+C detected! Exiting...")
    sys.exit(1)

# MARK: solver
class solver:
    def __init__(self) -> None:
        # Bind the SIGINT (Ctrl+C) to the custom handler
        signal.signal(signal.SIGINT, self._handle_sigint)
        
        try:
            pygame.init() # Initialize Pygame
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            self._quit_game(1)
        
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
        
        self.buttons       : tuple[str, ...] = ("Simulation", "Manual")
        self.manual_buttons: tuple[str, ...] = ("Normal", "Colored")
        self.load_buttons  : tuple[str, ...] = ("New_Board", "Load_Board")
        self.positions     : tuple[tuple[int, int], ...] = ((25, 50), (50 + self.BUTTON_WIDTH, 50))
        
        self.delay: float = min(0.01, 0.3 * (0.5 ** self.board_size)) * 1000  # delay in milliseconds
        self.threats: bool = True  # show threats or not
        
        # Create the Pygame window for Getting Board Size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size//4))
        pygame.display.set_caption("N-Queens Solver Board Size")
        
        # Pygame font setup
        pygame.font.init()
        self.FONT = pygame.font.SysFont(None, 28)
        
        self.BOARD_SIZE_LIMIT: int = 12  # Maximum board size
        self.board_size = self.input_num("Size of the board (N x N): ", (self.SQUARE_WIDTH, self.SQUARE_WIDTH), self.BOARD_SIZE_LIMIT)
        
        self.GAME_MODE: str = self.get_mode(self.buttons, self.positions)
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
        
        self.screen.fill(self.BACKGROUND)  # draw the background
        self.game()
    
    # MARK: game
    def game(self) -> None:
        match self.GAME_MODE:
            case "Simulation":
                self.simulation()
            case "Normal":
                self.manual()
            case "Colored_New_Board":
                self.colored_game()
            case "Colored_Load_Board":
                self.colored_game(load = True)
    
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
        """Draw individual squares."""
        color: tuple = self.WHITE if ((row + column) % 2) == 0 else self.BLACK
        
        # Draw the square
        square_rect = pygame.Rect(
            self.BOARD_X + row * self.SQUARE_WIDTH,
            self.BOARD_Y + column * self.SQUARE_WIDTH,
            self.SQUARE_WIDTH, self.SQUARE_WIDTH
        )
        pygame.draw.rect(self.screen, color, square_rect)
        
        if board[row] == column:
            # Draw the queen
            self.screen.blit(self.queen_b if (row + column) % 2 == 0 else self.queen_w, square_rect.topleft)
        
        if show_threats and self.threats:
            self.is_under_threat(row, column, square_rect, board, error_full)
    
    # MARK: is_under_threat
    def is_under_threat(self, row: int, column: int, square_rect: pygame.Rect, board: list, error_full: bool = False) -> bool:
        """Check if the (row, column) is threatened by any existing queen."""
        i = row  # start from the current row
        
        if error_full:
            # Check the entire board
            i = self.board_size
        
        for r in range(i):
            col = board[r]
            if col == -1:
                continue
            if r == row and col == column:
                # Skip the current Queen
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
    def handle_events(self, events: list["pygame.event.Event"] | None = None) -> None:
        """Handle user input events."""
        if events is None:
            events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self._quit_game(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    self._quit_game(0)
                if (event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self._quit_game(0)
                elif event.key == pygame.K_UP:
                    self.delay *= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
                elif event.key == pygame.K_DOWN:
                    self.delay /= 2
                    print(f"\033[93mDelay: {self.delay}\033[0m")
                elif event.key == pygame.K_t:
                    self.threats = not self.threats
                    print(f"\033[93mShow threats: {self.threats}\033[0m")
                    if self.GAME_MODE == "Colored":
                        self.draw_color_board()
                    elif self.GAME_MODE == "Normal":
                        self.draw_board(self.board)
                    else:
                        self.draw_board(self.user_board)
                elif event.key == pygame.K_s:
                    self.take_screenshot()
                elif event.key == pygame.K_r:
                    # Change the colour board to something else
                    if hasattr(self, 'color_board') and self.color_board:
                        options: tuple[str, ...] = ("YES", "NO")
                        reload: str = self.get_mode(options, self.positions, "Do you want to reload the color board?")
                        self.screen.fill(self.BACKGROUND)  # clear the background
                        choise: bool = True if reload == "YES" else False
                        self.colored_game(color_board = choise, load = choise)
    
    # MARK: input_num
    def input_num(self, prompt: str, position: tuple, limit: int) -> int:
        input_active: bool = True
        input_text: list = []
        
        while input_active:
            events = pygame.event.get()
            self.handle_events(events)
            
            for event in events:
                if event.type != pygame.KEYDOWN:
                    continue
                if event.unicode == "\r" and input_text:
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
    def get_mode(self, buttons: tuple[str, ...], positions: tuple[tuple[int, int], ...], text: str | None = None) -> str:
        """Get the game mode"""
        self.screen.fill(self.BACKGROUND)
        
        if text != None:
            text_render = self.FONT.render(text, True, self.BLACK)
            text_rect = text_render.get_rect(topleft = (self.SQUARE_WIDTH / 2, self.SQUARE_WIDTH / 2))
            self.screen.blit(text_render, text_rect)
            pygame.display.flip()
        
        self.draw_buttons(buttons, positions)
        mode: str = ""
        
        while True:
            events = pygame.event.get()
            self.handle_events(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        if event.unicode <= str(len(buttons)):
                            mode = buttons[int(event.unicode) - 1]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mode = self.handle_buttons(buttons, positions)
                
                # return if it is not None
                if mode in ["", None]:
                    continue
                
                if mode == "Manual":
                    self.screen.fill(self.BACKGROUND)
                    self.draw_buttons(self.manual_buttons, positions)
                    return self.get_mode(self.manual_buttons, positions)
                
                if mode == "Colored":
                    self.screen.fill(self.BACKGROUND)
                    self.draw_buttons(self.load_buttons, positions)
                    load_mode: str = self.get_mode(self.load_buttons, positions)
                    return f"Colored_{load_mode}"
                
                return mode
    
    # MARK: draw_buttons
    def draw_buttons(self, buttons: tuple, positions: tuple[tuple[int, int]]) -> None:
        """Draw the buttons on the screen."""
        for i, button_name in enumerate(buttons):
            # Draw the buttons
            button_position: tuple = positions[i]
            button = pygame.Rect(button_position, (self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, button)
            
            text = self.FONT.render(button_name, True, self.BLACK)
            text_rect = text.get_rect(center=(button_position[0] + self.BUTTON_MARGIN_X, button_position[1] + self.BUTTON_MARGIN_Y))
            self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    # MARK: handle_buttons
    def handle_buttons(self, buttons: tuple[str, ...], positions: tuple[tuple[int, int]]) -> str:
        """Handle button clicks."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button_name, pos in zip(buttons, positions):
            if pos[0] <= mouse_x <= pos[0] + self.BUTTON_WIDTH and pos[1] <= mouse_y <= pos[1] + self.BUTTON_HEIGHT:
                return button_name
        return ""
    
    # MARK: manual
    def manual(self) -> None:
        self.user_board: list = [-1 for _ in range(self.board_size)]
        
        print("\033[96mClick on the board to place/remove queens. Press ENTER to solve.\033[0m")
        while True:
            self.draw_board(self.user_board, error_full=True)
            
            events = pygame.event.get()
            self.handle_events(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # if the user presses enter key
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
                    self.draw_text_at_location(f"Invalid Queen placement", self.SQUARE_WIDTH, self.SQUARE_WIDTH * 0.5)
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
    
    # MARK: colored_game
    def colored_game(self, color_board: bool = True, load: bool = False) -> None:
        """
        Colored Queens Solver (LinkedIn Queens Solver)
        """
        
        """
        Create a 2D list to represent the color board, if it has not been made already.
        The color board will be of size board_size x board_size.
        Each cell will be initialized to 0, indicating no color is assigned.
        The color board will be used to track the colors placed on the board.
        The colors will be represented by integers from self.colors dict.
        """
        if color_board:
            self.color_board: list[list[int]] = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        self.colors: dict = {
            1: (255, 0, 0),      # Red
            2: (0, 255, 0),      # Green
            3: (0, 0, 255),      # Blue
            4: (255, 255, 0),    # Yellow
            5: (255, 128, 0),    # Orange
            6: (255, 192, 203),  # Pink
            7: (0, 128, 128),    # Teal
            8: (128, 128, 128),  # Grey
        }
        
        """
        Create a 2D list to represent the board.
        Each cell will be initialized to 0, indicating no queen is placed.
        The board will be of size board_size x board_size.
        The board will be used to track the placement of queens and their colors.
        
        x will be used to track cells that are under threat.
        q will be used to track cells that are occupied by queens.
        0 will be used to track empty cells that are not under threat.
        """
        self.color_board_state: list[list[str]] = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        """
        Create a list to track the number of colors used.
        The list will be of size self.board_size.
        Each index will represent a color, and the value will represent the count of that color used.
        """
        self.color_board_count: list[int] = [0 for _ in range(self.board_size)]
        
        """
        Create a list to track the color of queens placed.
        The length of list will represent the number of queens placed.
        Each index will represent a queen, and the value will represent the color of that queen.
        """
        self.color_board_queens: list[int] = []
        
        """
        Create a list to track single color rows.
        """
        self.single_color_rows: list[int] = []
        
        """
        Create a list to track single color columns.
        """
        self.single_color_cols: list[int] = []
        
        # recalculate the screen size based on the new board_size
        self.screen_size = self.SQUARE_WIDTH * self.board_size + 2 * self.SQUARE_WIDTH
        # Create the Pygame window for Colored Queens Solver
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # to center the window
        self.screen = pygame.display.set_mode((self.screen_size + 2 * self.SQUARE_WIDTH, self.screen_size))
        pygame.display.set_caption(f"Colored {self.board_size} Queens Solver")
        self.screen.fill(self.BACKGROUND)  # draw the background
        
        self.color_selected: int = 0
        
        if color_board and load:
            self.color_board = load_board(self.board_size)
        
        self.update_color_board()
        self.solve_color_board()
    
    # MARK: update_color_board
    def update_color_board(self):
        self.draw_color_options()
        
        while True:
            self.draw_color_board()
            
            events = pygame.event.get()
            self.handle_events(events)
            
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # if the user presses enter key
                    if self.is_valid_color_board():
                        print("\033[92mStarting the colored queens solver...\033[0m")
                        return
                    print("\033[91mInvalid color setup. Make sure each color is used\033[0m")
                
                if event.type != pygame.MOUSEBUTTONDOWN:
                    continue
                
                self.handle_color_click()
    
    # MARK: draw_color_board
    def draw_color_board(self) -> None:
        """Draw the colored board."""
        for row in range(self.board_size):
            for column in range(self.board_size):
                color: tuple = self.colors[self.color_board[row][column]] if self.color_board[row][column] != 0 else self.WHITE
                self.draw_color_square(row, column, color)
                pygame.display.flip()
                pygame.time.delay(int(self.delay))  # Delay for visual effect
    
    # MARK: draw_color_square
    def draw_color_square(self, row: int, column: int, color: tuple = (0,0,0), mark: bool = True) -> None:
        # Draw the square
        square_rect = pygame.Rect(
            self.BOARD_X + row * self.SQUARE_WIDTH,
            self.BOARD_Y + column * self.SQUARE_WIDTH,
            self.SQUARE_WIDTH, self.SQUARE_WIDTH
        )
        pygame.draw.rect(self.screen, color, square_rect)
        
        if mark:
            self.mark_color_square(row, column, square_rect)
    
    # MARK: draw_color_options
    def draw_color_options(self) -> None:
        """Draw the colored board."""
        for row in range(self.board_size):
            # get color from the dict colors according to color
            color: tuple = self.colors[row + 1]
            self.draw_color_square(self.board_size + 1, row, color, False)
            pygame.display.flip()
    
    # MARK: mark_color_square
    def mark_color_square(self, row: int, column: int, square_rect: pygame.Rect) -> None:
        if self.color_board_state[row][column] == "q":
            # draw a queen
            self.screen.blit(self.queen_w, square_rect.topleft)
        
        if self.color_board_state[row][column] == "x" and self.threats:
            # draw an x mark
            thickness = 2
            
            one_third = self.SQUARE_WIDTH / 3
            top    = self.BOARD_X + ( row         * self.SQUARE_WIDTH) + one_third
            bottom = self.BOARD_X + ((row + 1)    * self.SQUARE_WIDTH) - one_third
            left   = self.BOARD_Y + ( column      * self.SQUARE_WIDTH) + one_third
            right  = self.BOARD_Y + ((column + 1) * self.SQUARE_WIDTH) - one_third
            
            # draw left to right line of x
            pygame.draw.line(self.screen, self.BLACK, (top, left), (bottom, right), thickness)
            # draw right to left line of x
            pygame.draw.line(self.screen, self.BLACK, (top, right), (bottom, left), thickness)
        
    # MARK: handle_color_click
    def handle_color_click(self) -> None:
        x, y = pygame.mouse.get_pos()
        col = (x - self.BOARD_X) // self.SQUARE_WIDTH
        row = (y - self.BOARD_Y) // self.SQUARE_WIDTH
        
        if (col == self.board_size + 1) and (0 <= row < self.board_size):
            if self.color_selected == row + 1:
                # remove selection if same color clicked twice
                self.color_selected = 0
                return
            
            self.color_selected = row + 1  # select color
            return
        
        if self.color_selected == 0:
            return
        
        if (0 <= row < self.board_size) and (0 <= col < self.board_size):
            if self.color_board[col][row] == self.color_selected:
                self.color_board[col][row] = 0  # remove color
                return
            
            # if the square is empty, add color
            self.color_board[col][row] = self.color_selected  # add color
            return
    
    # MARK: is_valid_color_board
    def is_valid_color_board(self) -> bool:
        """ Check if the current color placement is valid. """
        nums_needed = set(range(1, self.board_size + 1))
        all_nums = set(num for row in self.color_board for num in row)
        
        # if there is an empty square, return False
        if 0 in all_nums:
            return False
        
        # Checks if each color is used in atleast once.
        return nums_needed.issubset(all_nums)
    
    # MARK: solve_color_board
    def solve_color_board(self):
        """
        1. Reduce the window size
        2. Check if there is any color with only one cell
        3. Check if there is any color with only one cell remaining
        """
        
        # recalculate the screen size based on the new board_size
        self.screen_size = self.SQUARE_WIDTH * self.board_size + 2 * self.SQUARE_WIDTH
        # Create the Pygame window for Colored Queens Solver
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # to center the window
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption(f"Colored {self.board_size} Queens Solver")
        self.screen.fill(self.BACKGROUND)  # draw the background
        self.draw_color_board()
        
        self.count_numbers()
        self.assign_queens_to_unique_cells()
        
        while True:
            self.handle_events()
            self.mark_singleton_cells()
            self.check_single_color("row")
            self.check_single_color("column")
            self.validate_solution()
    
    # MARK: mark_singleton_cells
    def mark_singleton_cells(self) -> None:
        """ Check if there are any colors with only one cell remaining """
        checking: bool = True
        while checking:
            recheck : bool = False  # check if we need to check again
            
            # check for every color
            for i in range(self.board_size):
                # skip the colors with queens
                if i + 1 in self.color_board_queens:
                    continue
                
                # check how many cells does this colour have
                cells_available: int = 0
                first_xy: tuple = ()
                for x in range(self.board_size):
                    for y in range(self.board_size):
                        
                        # check if the color is threatened
                        if self.color_board[x][y] == i + 1 and self.color_board_state[x][y] != "x":
                            cells_available += 1
                            
                            # if it is the only available cell so far
                            if cells_available == 1:
                                first_xy = x,y
                
                # if this color has only one cell, mark it as queen
                if cells_available == 1:
                    recheck = True  # check the board once again
                    x, y = first_xy
                    self.mark_queen(x, y)
                    self.draw_color_board()
                    pygame.time.delay(int(self.delay))  # Delay for visual effect
                    break  # exit this for-loop and start over
            
            # if all checks are done, end the loop
            if not recheck:
                checking = False
    
    # MARK: check_single_color
    def check_single_color(self, axis: str) -> None:
        """ Check if there are any row/columns with only one color remaining """
        checking: bool = True
        while checking:
            recheck : bool = False
            
            for x in range(self.board_size):
                # skip row/column if it is already checked and marked
                if x in self.get_single_color(axis):
                    continue
                
                # skip row/col if it has a queen
                if x in self.color_board_queens:
                    self.add_single_color(axis, x)
                    continue
                
                # check how many colors does this row/col have
                colors_set: set = set()
                
                for y in range(self.board_size):
                    
                    # check if the cell has a queen or is threatened
                    if self.get_color_board_state(axis, x, y) in ["q", "x"]:
                        continue
                    
                    colors_set.add(self.get_color_board(axis, x, y))
                
                if len(colors_set) != 1:
                    # skip this row/column; more than one color found
                    continue
                
                color = list(colors_set)[0]
                
                # mark all instances of the color in other rows as "x"
                recheck = True
                self.add_single_color(axis, x)
                
                for i in range(self.board_size):
                    # skip the single color row/col
                    if i == x:
                        continue
                    
                    if i + 1 in self.color_board_queens:
                        continue
                    
                    for j in range(self.board_size):
                        if self.get_color_board(axis, i, j) == color and self.get_color_board_state(axis, i, j) not in ["q", "x"]:
                            self.mark_color_board_state(axis, i, j)
                            self.draw_custom_color_square(axis, i, j, color)
                            pygame.display.flip()
                            pygame.time.delay(int(self.delay))
            
            if not recheck:
                checking = False
    
    # MARK: get_single_color
    def get_single_color(self, axis: str) -> list:
        """
        Get the list of single color rows/columns.
        
        :param axis: "row" or "column"
        """
        return self.single_color_rows if axis == "row" else self.single_color_cols
    
    # MARK: add_single_color
    def add_single_color(self, axis: str, x: int) -> None:
        """
        Add the row/column to the list of single color rows/columns.
        
        :param axis: "row" or "column"
        :param x: row/column number
        """
        if axis == "row":
            self.single_color_rows.append(x)
        elif axis in ["col", "column"]:
            self.single_color_cols.append(x)
    
    # MARK: get_color_board_state
    def get_color_board_state(self, axis: str, x: int, y: int) -> str:
        """
        Get the color board state for a given row/column.
        
        :param axis: "row" or "column"
        :param x: row/column number
        :param y: row/column number
        """
        return self.color_board_state[x][y] if axis == "row" else self.color_board_state[y][x]
    
    # MARK: get_color_board
    def get_color_board(self, axis: str, x: int, y: int) -> int:
        """
        Get the color board for a given row/column.
        
        :param axis: "row" or "column"
        :param x: row/column number
        :param y: row/column number
        """
        return self.color_board[x][y] if axis == "row" else self.color_board[y][x]
    
    # MARK: mark_color_board_state
    def mark_color_board_state(self, axis: str, i: int, j: int) -> None:
        """
        Mark the color board state for a given row/column.
        
        :param axis: "row" or "column"
        :param i: row/column number
        :param j: row/column number
        """
        if axis == "row":
            self.color_board_state[i][j] = "x"
        elif axis in ["col", "column"]:
            self.color_board_state[j][i] = "x"
    
    # MARK: draw_custom_color_square
    def draw_custom_color_square(self, axis: str, i: int, j: int, color: int) -> None:
        """
        Draw a custom color square on the board.
        
        :param axis: "row" or "column"
        :param i: row/column number
        :param j: row/column number
        :param color: color number
        """
        if axis == "row":
            self.draw_color_square(i, j, self.colors[color], True)
        elif axis in ["col", "column"]:
            self.draw_color_square(j, i, self.colors[color], True)
    
    # MARK: assign_queens_to_unique_cells
    def assign_queens_to_unique_cells(self) -> None:
        """
        Assign queens to cells that have only one color.
        """
        for i in range(self.board_size):
            self.handle_events()
            c: int = self.color_board_count[i]
            if c == 1:
                self.place_queen_on_board(i)
    
    # MARK: place_queen_on_board
    def place_queen_on_board(self, i: int) -> None:
        """
        if there is a color with only one cell, make it a queen
        find its position in self.color_board and mark it as a queen
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.color_board[x][y] == i + 1:
                    self.mark_queen(x, y)
                    self.draw_color_board()
                    return
    
    # MARK: mark_queen
    def mark_queen(self, x: int, y: int):
        """
        Mark the row and coloum as occupied(x)
        Mark self.color_board_state[x][y] as queen(q)
        Mark the surroundings as occupied(x)
        """
        
        self.color_board_queens.append(self.color_board[x][y])
        
        self.color_board_state[x][y] = "q"
        
        for i in range(self.board_size):
            self.color_board_state[x][i] = "x" if self.color_board_state[x][i] != "q" else self.color_board_state[x][i]
            self.color_board_state[i][y] = "x" if self.color_board_state[i][y] != "q" else self.color_board_state[i][y]
        
        for i in [-1, +1]:
            for j in [-1, +1]:
                if 0 <= x + i < self.board_size and 0 <= y + j < self.board_size:
                    self.color_board_state[x + i][y + j] = "x"
    
    def count_numbers(self):
        for row in self.color_board:
            for num in row:
                self.color_board_count[num - 1] += 1
    
    # MARK: validate_solution
    def validate_solution(self) -> None:
        """ Check if the current queen placement is complete. """
        if len(self.color_board_queens) == self.board_size:
            self.answers.append(self.color_board_state)
            pygame.time.wait(3 * 1000)  # Pause to show the solution
            self._quit_game(0)
        
        else:
            # check if every square is filled, which means the board is incorrect
            for row in self.color_board_state:
                for cell in row:
                    if cell == "":
                        # if there is an empty square, it means space for a queen
                        return
            
            # if every square is filled, the board is incorrect
            pygame.time.wait(2 * 1000)  # Pause to show the state
            print("\033[91mBoard is incorrect.\033[0m")
            self.colored_game(False)
    
    # MARK: take_screenshot
    def take_screenshot(self, base: str = "screenshot", ext: str = ".png", folder: str = "screenshots") -> None:
        """
        Take a screenshot of the current Pygame window and save it to a file.
        
        :param base   : The base name for the screenshot file.
        :param ext    : Extention for the file
        :param folder : Folder the file saved into
        """
        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        max_index = 0
        for filename in os.listdir(folder):
            if filename.startswith(base) and filename.endswith(ext):
                try:
                    number_part = filename[len(base)+1 : -len(ext)]  # Extract the number between
                    index = int(number_part)
                    max_index = max(max_index, index)
                except ValueError:
                    continue  # Skip files that don't follow the pattern
        
        filename = os.path.join(folder, f"{base}_{max_index + 1}{ext}")
        pygame.image.save(self.screen, filename)
        print(f"\033[94mScreenshot saved as {filename}!\033[0m")
    
    # MARK: _handle_sigint
    def _handle_sigint(self, *args) -> None:
        print("\033[93mCtrl+C detected!\033[0m")
        self._quit_game(0)
    
    # MARK: _quit_game
    def _quit_game(self, error: int = 0) -> None:
        """Exit the Pygame window."""
        if hasattr(self, 'answers') and self.answers:
            print(f"\033[92mSolutions found \033[94m({len(self.answers)})\033[92m: \033[93m{self.answers}\033[0m")
        elif hasattr(self, 'answers'):
            print("\033[91mNo solutions were found.\033[0m")
        print("\033[93mExiting the game...\033[0m")
        pygame.quit()
        if hasattr(self, 'color_board') and self.color_board:
            save_board(self.board_size, self.color_board)
        sys.exit(error)


if __name__ == "__main__":
    game = solver()
