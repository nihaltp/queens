"""
    This script saves the board to the correct file.
    If it is not already in there it creates a new file for it.
    
    Made by: NIHAL T P
    GitHub: https://github.com/nihaltp
    LinkedIn: https://www.linkedin.com/in/nihal-tp
"""

import os

def save_board(board_size: int, board: list[list[int]]) -> None:
    """
    Save the board to the correct file, if it is not already in there it creates a new file for it.
    
    @param board_size: The size of the board to save.
    @param board     : The board to save.
    
    @return: None
    """
    
    # MARK: Step 1
    # Validate the list
    
    # make sure it contains board_size number of lists
    if len(board) != board_size:
        print(f"\033[91mError: Board size mismatch. Expected {board_size} lists, got {len(board)}.\033[0m")
        return
    
    # make sure each list contains board_size number of integers
    for row in board:
        if len(row) != board_size:
            print(f"\033[91mError: Each row must contain {board_size} integers.\033[0m")
            return
        
        # make sure each integer is between 1 and board_size
        for num in row:
            if num < 1 or num > board_size:
                print(f"\033[91mError: Each number must be an integer between 1 and {board_size}.\033[0m")
                return
    
    # Make sure it has all the numbers from 1 to board_size
    for i in range(1, board_size + 1):
        if i not in [num for row in board for num in row]:
            print(f"\033[91mError: Board must be complete.\033[0m")
            return
    
    # MARK: Step 2
    # Create/Open the file for the board size
    
    # Get the directory where *this file* is located
    base_dir = os.path.dirname(__file__)  # <- This will always point to where this file is located
    
    # Assuming the file is named "board_<size>.txt" and located in the same directory as this script
    filename = os.path.join(base_dir, f"board_{board_size}.txt")
    
    if os.path.exists(filename):
        with open(filename, "r") as f:
            # Read all non-empty lines
            boards = [line.strip() for line in f if line.strip()]
    
    else:
        print(f"\033[91mError: File \033[94m{filename}\033[91m not found.\n\033[92mCreating a new file named: {filename}.\033[0m")
        # Create a new file for the board size
        open(filename, "w").close()
        boards = []
    
    # MARK: Step 3
    # Convert the board to a string format
    board_str = str(board)
    
    # Make sure there is no board same as this one in the file loaded
    if board_str in boards:
        print("\033[92mBoard already saved.\033[0m")
        return
    
    # MARK: Step 4
    # Save the board to the file
    try:
        with open(filename, "a") as f:
            # in append mode write the list to the last empty line
            f.write(board_str + "\n")
            print(f"\033[92mBoard({board_size}) saved successfully to {filename}.\033[0m")
    except Exception as e:
        print(f"\033[91mError: {e}.\033[0m")

# Example usage
if __name__ == "__main__":
    board: list[list[int]] = [[6, 6, 6, 6, 6, 6, 6, 6],
                              [6, 6, 2, 2, 2, 2, 6, 6],
                              [6, 6, 2, 1, 1, 2, 6, 6],
                              [6, 5, 2, 2, 2, 2, 6, 6],
                              [5, 5, 7, 7, 7, 7, 6, 6],
                              [5, 3, 7, 4, 4, 4, 8, 6],
                              [5, 3, 7, 7, 7, 7, 8, 6],
                              [3, 3, 3, 3, 8, 8, 8, 8]
                              ]
    save_board(8, board)
