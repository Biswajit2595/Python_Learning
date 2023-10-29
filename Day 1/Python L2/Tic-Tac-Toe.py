import numpy as np

class TicTacToe:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = np.full((board_size, board_size), ' ')
        self.current_player = 'X'
        self.scores = {'X': 0, 'O': 0}
        self.moves_history = []
        self.undo_history = []

    def print_board(self):
        print("  " + " ".join([chr(i) for i in range(65, 65 + self.board_size)]))
        for i in range(self.board_size):
            print(str(i + 1) + " " + " ".join(self.board[i]))

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.moves_history.append((row, col, self.current_player))
            self.undo_history = []  # Clear the undo history
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            print("Cell already taken. Try again.")

    def undo_move(self):
        if self.moves_history:
            row, col, player = self.moves_history.pop()
            self.board[row][col] = ' '
            self.current_player = player
            self.undo_history.append((row, col, player))

    def redo_move(self):
        if self.undo_history:
            row, col, player = self.undo_history.pop()
            self.make_move(row, col)

    def check_winner(self):
        rows = self.board
        cols = np.transpose(self.board)
        diags = [np.diag(self.board), np.diag(np.fliplr(self.board))]
        lines = np.concatenate((rows, cols, diags))
        for line in lines:
            if all(x == 'X' for x in line):
                return 'X'
            elif all(x == 'O' for x in line):
                return 'O'
        if ' ' not in self.board:
            return 'Tie'
        return None

    def play(self):
        while True:
            self.print_board()
            print(f"Player {self.current_player}'s turn.")
            move = input("Enter your move (e.g., A1 for top-left): ")
            if move.lower() == 'undo':
                self.undo_move()
                continue
            elif move.lower() == 'redo':
                self.redo_move()
                continue
            if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
                print("Invalid input. Try again.")
                continue
            row = int(move[1]) - 1
            col = ord(move[0].upper()) - 65
            if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
                print("Invalid input. Try again.")
                continue
            self.make_move(row, col)
            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == 'Tie':
                    print("It's a tie!")
                else:
                    print(f"Player {winner} wins!")
                    self.scores[winner] += 1
                print(f"Scores: X-{self.scores['X']} O-{self.scores['O']}")
                play_again = input("Do you want to play again? (yes/no): ")
                if play_again.lower() == 'no':
                    break
                else:
                    self.reset_game()

    def reset_game(self):
        self.board = np.full((self.board_size, self.board_size), ' ')
        self.current_player = 'X'
        self.moves_history = []
        self.undo_history = []


if __name__ == '__main__':
    print("Welcome to Tic-Tac-Toe!")
    while True:
        board_size = int(input("Enter the board size (3, 4, 5, etc.): "))
        if board_size < 3:
            print("Board size must be at least 3.")
        else:
            game = TicTacToe(board_size)
            game.play()
            play_again = input("Do you want to play another game? (yes/no): ")
            if play_again.lower() == 'no':
                break
