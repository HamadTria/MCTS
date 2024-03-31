class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.last_move = None

    def copy(self):
        new_board = TicTacToe()
        new_board.board = self.board.copy()
        new_board.current_winner = self.current_winner
        new_board.last_move = self.last_move
        return new_board
    
    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    def is_winner(self, player):
        # Check horizontal
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                return True
            
        # Check vertical
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                return True
            
        # Check diagonal
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        
        return False
    
    def is_draw(self):
        return ' ' not in self.board
    
    def is_terminal(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()
    
    def player_turn(self):
        return self.board.count('X') == self.board.count('O')
    
    def get_legal_moves(self):
        return [i for i, x in enumerate(self.board) if x == ' ']  # Return empty cells
    
    def apply_move(self, move):
        if self.board[move] != ' ':
            raise Exception('Invalid move')
        player = 'X' if self.player_turn() else 'O'
        self.board[move] = player
        self.last_move = move
        if self.is_winner(player):
            self.current_winner = player
        elif self.is_draw():
            self.current_winner = 'DRAW'

if __name__ == "__main__":
    game = TicTacToe()
    game.print_board()
    while not game.is_terminal():
        move = int(input('Enter your move: '))
        game.apply_move(move)
        game.print_board()
        if game.is_terminal():
            if game.current_winner == 'DRAW':
                print('It is a draw!')
