from copy import deepcopy
from mcts import *

class TicTacToe():
    def __init__(self, board=None):
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        self.position = {}
        self.init_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for i in range(9):
            self.position[i] = self.empty_square
    
    def make_move(self, pos):
        board = TicTacToe(self)
        board.position[pos] = self.player_1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        return board
    
    def is_draw(self):
        return all([self.position[i] != self.empty_square for i in range(9)])
    
    def is_win(self):
        

            