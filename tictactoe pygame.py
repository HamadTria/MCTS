import pygame
import sys
from copy import deepcopy
from mcts import *

MAX_ITER = 1000
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 50

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
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        font = pygame.font.SysFont(None, FONT_SIZE)
        clock = pygame.time.Clock()

        mcts = MCTS()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (SCREEN_WIDTH // 3)
                    row = pos[1] // (SCREEN_HEIGHT // 3)
                    move = row * 3 + col

                    if self.position[move] != self.empty_square:
                        continue

                    self = self.make_move(move)
                    if self.is_win():
                        print('Player "%s" has won the game!\n' % self.player_2)
                        pygame.quit()
                        sys.exit()
                    elif self.is_draw():
                        print('Game is drawn!\n')
                        pygame.quit()
                        sys.exit()

                    best_move = mcts.search(self, MAX_ITER)
                    try:
                        self = best_move.board
                    except:
                        pass

            screen.fill(BG_COLOR)
            self.draw_board(screen, font)
            pygame.display.flip()
            clock.tick(30)

    def draw_board(self, screen, font):
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SCREEN_HEIGHT // 3), (SCREEN_WIDTH, i * SCREEN_HEIGHT // 3), 3)
            pygame.draw.line(screen, LINE_COLOR, (i * SCREEN_WIDTH // 3, 0), (i * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 3)

        for pos, symbol in self.position.items():
            col = pos % 3
            row = pos // 3
            x = col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2
            y = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2

            if symbol == 'x':
                text = font.render(symbol, True, PLAYER_X_COLOR)
            elif symbol == 'o':
                text = font.render(symbol, True, PLAYER_O_COLOR)
            else:
                continue

            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

if __name__ == '__main__':
    board = TicTacToe()
    board.game_loop()
