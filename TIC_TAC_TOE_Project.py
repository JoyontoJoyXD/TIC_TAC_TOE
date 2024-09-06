#  Tic Tac Toe AI Challenge

# Constants for player symbols
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

# Define the Tic Tac Toe board size
BOARD_SIZE = 3

# Function to print the game board with row and column headings
def print_board(board):
    print("    0   1   2  ")     #prints column no above the board
    for i in range(BOARD_SIZE):
        print(f"{i}   {' | '.join(board[i])}")       #for each row---prints row no., followed by contents of each cell, separated by v.l.
        if i < BOARD_SIZE - 1:
            print("   -----------")                  #prints horizontal lines between rows to visually separate them, except for the last row.

        

# Function to check if the game is over
def is_game_over(board):
    # Check rows
    for row in board:
        if all([spot == PLAYER_X for spot in row]) or all([spot == PLAYER_O for spot in row]):
            return True

    # Check columns
    for col in range(BOARD_SIZE):
        if all([board[row][col] == PLAYER_X for row in range(BOARD_SIZE)]) or all([board[row][col] == PLAYER_O for row in range(BOARD_SIZE)]):
            return True

    # Check diagonals
    if all([board[i][i] == PLAYER_X for i in range(BOARD_SIZE)]) or all([board[i][i] == PLAYER_O for i in range(BOARD_SIZE)]):
        return True
    if all([board[i][BOARD_SIZE-i-1] == PLAYER_X for i in range(BOARD_SIZE)]) or all([board[i][BOARD_SIZE-i-1] == PLAYER_O for i in range(BOARD_SIZE)]):
        return True

    # Check for tie
    if all([spot != EMPTY for row in board for spot in row]):
        return True

    return False


# Function to evaluate the board for the AI player  "10, -10"
def evaluate_board(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    # Check rows/ columns/  diagonals for winning positions
    for row in board:
        if all([spot == player for spot in row]):
            return 10
        if all([spot == opponent for spot in row]):
            return -10
    for col in range(BOARD_SIZE):
        if all([board[row][col] == player for row in range(BOARD_SIZE)]):
            return 10
        if all([board[row][col] == opponent for row in range(BOARD_SIZE)]):
            return -10
    if all([board[i][i] == player for i in range(BOARD_SIZE)]) or all([board[i][i] == opponent for i in range(BOARD_SIZE)]):
        return 10
    if all([board[i][BOARD_SIZE-i-1] == player for i in range(BOARD_SIZE)]) or all([board[i][BOARD_SIZE-i-1] == opponent for i in range(BOARD_SIZE)]):
        return 10
    return 0   # neutral or Draw



# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player, player):
    
    if is_game_over(board) or depth == 0:
        return evaluate_board(board, PLAYER_X), None

    if maximizing_player:
        max_eval = -float('inf')  
        best_move = None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):  # This nested loop iterates over each position of board
                if board[i][j] == EMPTY:   #if the current position is empty
                    board[i][j] = player
                    eval, _ = minimax(board, depth-1, alpha, beta, False, get_opponent(player))    #minimax function recursive call, tuple-unpacking
                    board[i][j] = EMPTY    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:             #alpha beta logical relation for pruning
                        break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = player
                    eval, _ = minimax(board, depth-1, alpha, beta, True, get_opponent(player))   #discarding the best move using underscore
                    board[i][j] = EMPTY
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move

# Function to get the opponent's symbol
def get_opponent(player):
    return PLAYER_X if player == PLAYER_O else PLAYER_O

# Function to make the AI's move
def make_ai_move(board, player):
    depth = BOARD_SIZE * BOARD_SIZE
    _, move = minimax(board, depth, -float('inf'), float('inf'), True, player)
    if move:
        board[move[0]][move[1]] = player


# Main game loop for Human vs AI
def play_human_vs_ai():
    while True:
        # Initialize the game board
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        current_player = PLAYER_X

        while not is_game_over(board):
            # Print current board state
            print_board(board)
            print(f"It's {current_player}'s turn.")

            # Human player's turn
            if current_player == PLAYER_X:
                while True:
                    try:
                        row, col = map(int, input("Enter row and column (0-2): ").split())
                        if board[row][col] == EMPTY:
                            board[row][col] = PLAYER_X
                            break
                        else:
                            print("That spot is already taken!")
                    except ValueError:
                        print("Invalid input! Please enter two integers separated by space.")
                    except IndexError:
                        print("Invalid row or column! Please enter values between 0 and 2.")

            # AI player's turn
            else:
                print("Computer's turn:")
                make_ai_move(board, PLAYER_O)

            # Switch player
            current_player = get_opponent(current_player)

        # Print final board state
        print_board(board)

        # Check game result
        print("\n")
        print("*" * 38)
        if evaluate_board(board, PLAYER_X) == 10:
            print("🎉 Congratulations! You win! 🏆")
        elif evaluate_board(board, PLAYER_O) == -10:
            print("😔 Sorry, you lose! 😢")
        else:
            print("🎮 It's a draw! Let's have a rematch! 🤝")
        print("*" * 38)
        print("\n")


        # Ask for restart or exit
        choice = input("Do you want to play again? (yes/no): ")
        if choice.lower() != 'yes':
            break


# Main game loop for AI vs AI
def play_ai_vs_ai():
    while True:
        # Initialize the game board
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        current_player = PLAYER_X

        while not is_game_over(board):
            # Print current board state
            print_board(board)
            print(f"It's {current_player}'s turn.")

            # AI player's turn
            print("Computer's turn:")
            make_ai_move(board, current_player)

            # Switch player
            current_player = get_opponent(current_player)

        # Print final board state
        print_board(board)
        print("\n")
        print("*" * 38)
        if evaluate_board(board, PLAYER_X) == 10:
             print("🎉 Congratulations! Player X wins! 🏆")
        elif evaluate_board(board, PLAYER_O) == -10:
             print("🎉 Congratulations! Player O wins! 🏆")
        else:
             print("🎮 It's a draw! Let's have a rematch! 🤝")
        print("*" * 38)
        print("\n")
        

        # Ask for restart or exit
        choice = input("Do you want to play again? (yes/no): ")
        if choice.lower() != 'yes':
            break

# Run Human vs AI game
def main_human_vs_ai():
    print("Human vs AI Tic Tac Toe\n")
    play_human_vs_ai()

# Run AI vs AI game
def main_ai_vs_ai():
    print("AI vs AI Tic Tac Toe\n")
    play_ai_vs_ai()

#  Run the selected game mode 

# 🌟🎮✨ Welcome to the Ultimate Tic Tac Toe Showdown! ✨🎮🌟

if __name__ == "__main__":       #executing the python script directly
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║      🚀 Let's Play Tic Tac Toe! 🎲      ")
        print("╚══════════════════════════════════════╝")
        
        choice = input("\n🎮 Select your game mode:\n\n"
                       
                       "1. Human vs AI\n"
                       "2. AI vs AI\n"
                       "3. Exit\n\n"
                       
                       "Enter your choice (1, 2, or 3): ")
        if choice == '1':
            main_human_vs_ai()
        elif choice == '2':
            main_ai_vs_ai()
        elif choice == '3':
            print("\n👋 Thank you for playing! Have a blast and see you next time!\n")
            break
        else:
            print("\n❌ Oops! That's an invalid choice. Please enter 1, 2, or 3.")


