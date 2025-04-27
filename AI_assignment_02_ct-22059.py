import math
import time

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None
        self.move_history = []

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            self.move_history.append(square)

            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def undo_move(self, square):
        self.board[square] = ' '
        self.current_winner = None
        if self.move_history and square == self.move_history[-1]:
            self.move_history.pop()

    def check_winner(self, square, letter):
        row = square // 3
        col = square % 3

        # Check row
        if all(self.board[row*3 + i] == letter for i in range(3)):
            return True
        # Check column
        if all(self.board[col + i*3] == letter for i in range(3)):
            return True
        # Check diagonals
        if square % 2 == 0:
            if all(self.board[i] == letter for i in [0, 4, 8]):
                return True
            if all(self.board[i] == letter for i in [2, 4, 6]):
                return True
        return False

    def game_over(self):
        return self.current_winner is not None or not self.available_moves()

def minimax(game, depth, alpha=-math.inf, beta=math.inf, maximizing=True, use_pruning=True, nodes_evaluated=None):
    if nodes_evaluated is not None:
        nodes_evaluated[0] += 1

    if game.current_winner:
        return (10 - depth) if game.current_winner == 'X' else (-10 + depth)
    if not game.available_moves():
        return 0

    if maximizing:
        max_eval = -math.inf
        for move in game.available_moves():
            game.make_move(move, 'X')
            eval = minimax(game, depth + 1, alpha, beta, False, use_pruning, nodes_evaluated)
            game.undo_move(move)
            max_eval = max(max_eval, eval)
            if use_pruning:
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for move in game.available_moves():
            game.make_move(move, 'O')
            eval = minimax(game, depth + 1, alpha, beta, True, use_pruning, nodes_evaluated)
            game.undo_move(move)
            min_eval = min(min_eval, eval)
            if use_pruning:
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def get_ai_move(game, use_pruning=True):
    best_val = -math.inf
    best_move = None
    nodes_evaluated = [0]

    start_time = time.time()
    for move in game.available_moves():
        game.make_move(move, 'X')
        move_val = minimax(game, 0, use_pruning=use_pruning, nodes_evaluated=nodes_evaluated)
        game.undo_move(move)
        if move_val > best_val:
            best_val = move_val
            best_move = move
    duration = time.time() - start_time
    return best_move, nodes_evaluated[0], duration

# Setup functions for test cases
def mid_game_setup():
    game = TicTacToe()
    game.make_move(0, 'X')
    game.make_move(4, 'O')
    game.make_move(1, 'X')
    return game

def end_game_setup():
    game = TicTacToe()
    moves = [(0, 'X'), (1, 'O'), (3, 'X'), (4, 'O')]
    for pos, letter in moves:
        game.make_move(pos, letter)
    return game

def test_performance():
    test_cases = [
        ("Empty Board", TicTacToe()),
        ("Mid Game", mid_game_setup),
        ("End Game", end_game_setup)
    ]

    for name, setup in test_cases:
        game = setup() if callable(setup) else setup

        print(f"\n{name} Test Case:")

        # Standard Minimax
        _, nodes_std, time_std = get_ai_move(game, use_pruning=False)
        # Alpha-Beta Pruning
        _, nodes_ab, time_ab = get_ai_move(game, use_pruning=True)

        print(f"Standard Minimax: {time_std:.4f}s, {nodes_std} nodes evaluated")
        print(f"Alpha-Beta Pruning: {time_ab:.4f}s, {nodes_ab} nodes evaluated")
        
        improvement_time = (1 - time_ab / time_std) * 100 if time_std > 0 else 0
        improvement_nodes = (1 - nodes_ab / nodes_std) * 100 if nodes_std > 0 else 0
        print(f"Improvement: {improvement_time:.1f}% faster, {improvement_nodes:.1f}% fewer nodes")

def play_demo():
    game = TicTacToe()
    print("Welcome to Tic-Tac-Toe! You play 'O', AI plays 'X'.")
    print("Board positions are numbered 0 to 8 as follows:")
    print("0 | 1 | 2\n3 | 4 | 5\n6 | 7 | 8\n")

    while not game.game_over():
        game.print_board()
        if len(game.available_moves()) % 2 == 1:
            # Human turn
            try:
                move = int(input("Your move (0-8): "))
            except ValueError:
                print("Please enter a valid number 0-8.")
                continue
            if move not in game.available_moves():
                print("Invalid move! Try again.")
                continue
            game.make_move(move, 'O')
        else:
            # AI turn
            print("\nAI is thinking...")
            move, nodes, duration = get_ai_move(game, use_pruning=True)
            game.make_move(move, 'X')
            print(f"AI chose position {move} (evaluated {nodes} nodes in {duration:.4f} seconds)\n")

    game.print_board()
    if game.current_winner:
        if game.current_winner == 'O':
            print("Congratulations! You won!")
        else:
            print("AI wins! Better luck next time.")
    else:
        print("It's a tie!")

    print("Thanks for playing!")

if __name__ == "__main__":
    print("=== Performance Comparison ===")
    test_performance()
    print("\n=== Play Tic-Tac-Toe ===")
    play_demo()
