from copy import deepcopy
from mcts import *

MAX_ITER = 1000

class TicTacToe():
    def __init__(self, board=None):
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '_'
        self.position = {}
        self.init_board()
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for pos in range(9):
            self.position[pos] = self.empty_square
    
    def make_move(self, pos):
        board = TicTacToe(self)
        board.position[pos] = self.player_1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        return board

    def is_draw(self):
        for pos in self.position:
            if self.position[pos] == self.empty_square:
                return False
        return True
    
    def is_win(self):
        # Check horizontal
        for i in range(0, 9, 3):
            if self.position[i] == self.position[i+1] == self.position[i+2] == self.player_2:
                return True
        # Check vertical
        for i in range(3):
            if self.position[i] == self.position[i+3] == self.position[i+6] == self.player_2:
                return True
        # Check diagonal
        if self.position[0] == self.position[4] == self.position[8] == self.player_2:
            return True
        if self.position[2] == self.position[4] == self.position[6] == self.player_2:
            return True
        return False
    
    def legal_moves(self):
        actions = []
        for pos in self.position:
            if self.position[pos] == self.empty_square:
                actions.append(self.make_move(pos))
        return actions

    def game_loop(self):
        print('  Type "exit" to quit the game')
        print('  Move format 0 to 8')
        print(self)

        mcts = MCTS()
        while True:
            user_input = input('> ')
            if user_input == 'exit': break
            if user_input == '': continue
            
            try:
                pos = int(user_input)

                if self.position[pos] != self.empty_square:
                    print(' Illegal move!')
                    continue

                self = self.make_move(pos)
                print(self)

                best_move = mcts.search(self, MAX_ITER)
                try:
                    self = best_move.board
                except:
                    pass
                print(self)

                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
            
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format 0 to 8')

    def __str__(self):
        board_string = ''
        for pos in range(9):
            board_string += ' %s' % self.position[pos]
            if pos in [2, 5, 8]:
                board_string += '\n'
        
        if self.player_1 == 'x':
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
        
        elif self.player_1 == 'o':
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
        return board_string

if __name__ == '__main__':
    board = TicTacToe()
    board.game_loop()
        
        
        
    
    
    
    
    
    
    
    
