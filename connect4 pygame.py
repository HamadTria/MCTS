import pygame
import sys
from copy import deepcopy
import time
from mcts import *

MAX_ITER = 500
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
PLAYER_HUMAN_COLOR = (255, 0, 0)
PLAYER_AI_COLOR = (0, 0, 255)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 50
BUTTON_COLOR = (100, 100, 100)
BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 20
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class ConnectFour():
    def __init__(self, board=None):
        self.player_1 = 'HUMAN'
        self.player_2 = 'AI'
        self.empty_square = '_'
        self.position = [['_' for _ in range(7)] for _ in range(6)]
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def make_move(self, col):
        board = ConnectFour(self)
        for row in range(5, -1, -1):
            if board.position[row][col] == '_':
                board.position[row][col] = self.player_1
                (board.player_1, board.player_2) = (board.player_2, board.player_1)
                break
        return board

    def is_draw(self):
        for row in self.position:
            if '_' in row:
                return False
        return True

    def is_win(self):
        # horizontal
        for row in self.position:
            for col in range(4):
                if row[col] == row[col+1] == row[col+2] == row[col+3] == self.player_2:
                    return True

        # vertical
        for col in range(7):
            for row in range(3):
                if self.position[row][col] == self.position[row+1][col] == self.position[row+2][col] == self.position[row+3][col] == self.player_2:
                    return True

        # diagonal (top-left to bottom-right)
        for col in range(4):
            for row in range(3):
                if self.position[row][col] == self.position[row+1][col+1] == self.position[row+2][col+2] == self.position[row+3][col+3] == self.player_2:
                    return True

        # diagonal (top-right to bottom-left)
        for col in range(4, 7):
            for row in range(3, -1, -1):
                if self.position[row][col] == self.position[row-1][col-1] == self.position[row-2][col-2] == self.position[row-3][col-3] == self.player_2:
                    return True
        return False

    def legal_moves(self):
        actions = []
        for col in range(7):
            if self.position[0][col] == '_':
                actions.append(self.make_move(col))        
        
        # random.shuffle(actions)
        return actions

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Connect Four")
        font = pygame.font.SysFont(None, FONT_SIZE)
        button_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        clock = pygame.time.Clock()

        mcts = MCTS()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (SCREEN_WIDTH // 7)

                    if self.position[0][col] != '_':
                        continue

                    self = self.make_move(col)

                    screen.fill(BG_COLOR)
                    self.draw_board(screen, font)
                    pygame.display.flip()
                    clock.tick(30)

                    if self.is_win():
                        winning_combination = self.get_winning_combination()
                        screen.fill(BG_COLOR)
                        self.draw_board(screen, font)
                        pygame.display.flip()
                        clock.tick(30)
                        self.draw_connecting_line(screen, winning_combination) 
                        time.sleep(1)                    
                        self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                        return
                    elif self.is_draw():
                        self.end_game_screen(screen, font, button_font, "Game is drawn!")
                        return

                    best_move = mcts.search(self, MAX_ITER)
                    try:
                        self = best_move.board
                        if self.is_win():
                            winning_combination = self.get_winning_combination()
                            screen.fill(BG_COLOR)
                            self.draw_board(screen, font)
                            pygame.display.flip()
                            clock.tick(30)
                            self.draw_connecting_line(screen, winning_combination) 
                            time.sleep(1)  
                            self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                            return
                        elif self.is_draw():
                            self.end_game_screen(screen, font, button_font, "Game is drawn!")
                            return
                    except:
                        pass

            screen.fill(BG_COLOR)
            self.draw_board(screen, font)
            pygame.display.flip()
            clock.tick(30)

    def draw_board(self, screen, font):
        for i in range(1, 7):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SCREEN_HEIGHT // 6), (SCREEN_WIDTH, i * SCREEN_HEIGHT // 6), 3)
            pygame.draw.line(screen, LINE_COLOR, (i * SCREEN_WIDTH // 7, 0), (i * SCREEN_WIDTH // 7, SCREEN_HEIGHT), 3)

        for row in range(6):
            for col in range(7):
                x = col * (SCREEN_WIDTH // 7) + (SCREEN_WIDTH // 7) // 2
                y = row * (SCREEN_HEIGHT // 6) + (SCREEN_HEIGHT // 6) // 2

                if self.position[row][col] == 'HUMAN':
                    text = font.render('o', True, PLAYER_HUMAN_COLOR)
                elif self.position[row][col] == 'AI':
                    text = font.render('o', True, PLAYER_AI_COLOR)
                else:
                    continue

                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

    def end_game_screen(self, screen, font, button_font, message):
        screen.fill(BG_COLOR)
        text = font.render(message, True, FONT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - FONT_SIZE))
        screen.blit(text, text_rect)

        play_again_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
        exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + 10), (BUTTON_WIDTH, BUTTON_HEIGHT))

        pygame.draw.rect(screen, BUTTON_COLOR, play_again_button_rect)
        pygame.draw.rect(screen, BUTTON_COLOR, exit_button_rect)

        play_again_text = button_font.render("Play Again", True, BUTTON_FONT_COLOR)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
        screen.blit(play_again_text, play_again_text_rect)

        exit_text = button_font.render("Exit", True, BUTTON_FONT_COLOR)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button_rect.collidepoint(event.pos):
                        self.__init__()
                        self.game_loop()
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
    
    def get_winning_combination(self):
        # horizontal
        for row in range(6):
            for col in range(4):
                if self.position[row][col] == self.position[row][col+1] == self.position[row][col+2] == self.position[row][col+3] == self.player_2:
                    return [(row, col), (row, col+1), (row, col+2), (row, col+3)]

        # vertical
        for col in range(7):
            for row in range(3):
                if self.position[row][col] == self.position[row+1][col] == self.position[row+2][col] == self.position[row+3][col] == self.player_2:
                    return [(row, col), (row+1, col), (row+2, col), (row+3, col)]

        # diagonal (top-left to bottom-right)
        for col in range(4):
            for row in range(3):
                if self.position[row][col] == self.position[row+1][col+1] == self.position[row+2][col+2] == self.position[row+3][col+3] == self.player_2:
                    return [(row, col), (row+1, col+1), (row+2, col+2), (row+3, col+3)]

        # diagonal (top-right to bottom-left)
        for col in range(4, 7):
            for row in range(3, -1, -1):
                if self.position[row][col] == self.position[row-1][col-1] == self.position[row-2][col-2] == self.position[row-3][col-3] == self.player_2:
                    return [(row, col), (row-1, col-1), (row-2, col-2), (row-3, col-3)]

    def draw_connecting_line(self, screen, winning_combination):
        start_row, start_col = winning_combination[0]
        end_row, end_col = winning_combination[-1]
        start_x = start_col * (SCREEN_WIDTH // 7) + (SCREEN_WIDTH // 7) // 2
        start_y = start_row * (SCREEN_HEIGHT // 6) + (SCREEN_HEIGHT // 6) // 2
        end_x = end_col * (SCREEN_WIDTH // 7) + (SCREEN_WIDTH // 7) // 2
        end_y = end_row * (SCREEN_HEIGHT // 6) + (SCREEN_HEIGHT // 6) // 2
        pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 5)
        pygame.display.flip()

if __name__ == '__main__':
    board = ConnectFour()
    board.game_loop()
