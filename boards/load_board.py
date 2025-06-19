"""
    This module provides a function to load a random board of a specified size from the corresponding file.
    
    Made by: NIHAL T P
    GitHub: https://github.com/nihaltp
    LinkedIn: https://www.linkedin.com/in/nihal-tp
"""

import os
import ast
import random

def load_board(board_size: int) -> list[list[int]]:
    """
    Load a random board of the specified board_size from the corresponding file.
    
    @param board_size: The size of the board to load.
    @return: A list representing the board.
    """
    
    # MARK: Step 1
    # Get the directory where *this file* is located
    base_dir = os.path.dirname(__file__)  # <- This will always point to where this file is located
    
    # Assuming the file is named "board_<size>.txt"
    # and located in the same directory as this script
    filename = os.path.join(base_dir, f"board_{board_size}.txt")
    
    # Load all the boards from a file
    try:
        with open(filename, "r") as f:
            # Read all non-empty lines
            boards = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\033[91mError: File \033[94m{filename}\033[91m not found.\033[0m")
        return [[0 for _ in range(board_size)] for _ in range(board_size)]
    
    # MARK: Step 2
    # Pick a random board and return a parsed version of it
    if not boards:
        print(f"\033[91mError: No boards found in \033[94m{filename}\033[91m.\033[0m")
        return [[0 for _ in range(board_size)] for _ in range(board_size)]
    
    # Choose a random board from the list
    board = random.choice(boards)
    
    # Parse the board string into a list
    try:
        parsed_list = ast.literal_eval(board)
    except (ValueError, SyntaxError):
        print("\033[91mError: Line is not a valid list.\033[0m")
        parsed_list = load_board(board_size)  # Retry loading a board
    except Exception as e:
        print(f"\033[91mUnexpected error: {e}.\033[0m")
        parsed_list = load_board(board_size)  # Retry loading a board
    
    return parsed_list


# Example usage
if __name__ == "__main__":
    board: list[list[int]] = []
    board_size: int = 0
    
    while board == []:
        # Choose a random board size from 1 to 12
        board_size = random.randint(1, 12)
        board = load_board(board_size)
    
    print(f"\033[94mLoaded board of size {board_size}: {board}\033[0m")
