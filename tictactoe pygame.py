import pygame
import sys
from copy import deepcopy
import time
from mcts import *

MAX_ITER = 500
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
OFFSET = 600
LINE_COLOR = (0, 0, 0)
CHILD_SEPLINE_COLOR = (200, 200, 200)
BG_COLOR = (255, 255, 255)
PLAYER_HUMAN_COLOR = (255, 0, 0)
PLAYER_AI_COLOR = (0, 0, 255)
CHILD_PLAYER_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 100
SMALL_FONT_SIZE = 50
BUTTON_COLOR = (100, 100, 100)
BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 20
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class TicTacToe():
    def __init__(self, board=None):
        self.player_1 = 'HUMAN'
        self.player_2 = 'AI'
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
        screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        font = pygame.font.SysFont(None, FONT_SIZE)
        small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        button_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        clock = pygame.time.Clock()

        self.draw_board(screen, font)
        pygame.display.flip()
        clock.tick(30)

        mcts = MCTS()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > SCREEN_WIDTH:
                        continue
                    col = pos[0] // (SCREEN_WIDTH // 3)
                    row = pos[1] // (SCREEN_HEIGHT // 3)
                    move = row * 3 + col

                    if self.position[move] != self.empty_square:
                        continue

                    self = self.make_move(move)
                    
                    self.draw_board(screen, font)
                    pygame.display.flip()
                    clock.tick(30)

                    if self.is_win():
                        winning_combination = self.get_winning_combination()
                        self.draw_connecting_line(screen, winning_combination) 
                        time.sleep(4)                    
                        self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                        return
                    elif self.is_draw():
                        self.end_game_screen(screen, font, button_font, "Game is drawn!")
                        return
                    
                    best_move, children = mcts.search(self, MAX_ITER)
                    list_children =  list((children.values()))

                    pygame.display.flip()
                    clock.tick(30)

                    try:
                        self = best_move.board
                        self.draw_board(screen, font, list_children, small_font)
                        pygame.display.flip()
                        clock.tick(30)

                        if self.is_win():
                            winning_combination = self.get_winning_combination()
                            self.draw_connecting_line(screen, winning_combination) 
                            time.sleep(4)  
                            self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                            return
                        elif self.is_draw():
                            self.end_game_screen(screen, font, button_font, "Game is drawn!")
                            return
                    except:
                        pass

    def draw_board(self, screen, font, children=None, small_font=None):
        screen.fill(BG_COLOR)
        for i in range(1, 3):
            # main board
            pygame.draw.line(screen, LINE_COLOR, (0, i * SCREEN_HEIGHT // 3), (SCREEN_WIDTH, i * SCREEN_HEIGHT // 3), 3)
            pygame.draw.line(screen, LINE_COLOR, (i * SCREEN_WIDTH // 3, 0), (i * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 3)
            # side board
            pygame.draw.line(screen, CHILD_SEPLINE_COLOR, (SCREEN_WIDTH, i * SCREEN_HEIGHT // 3), (SCREEN_WIDTH + OFFSET, i * SCREEN_HEIGHT // 3), 3)
            pygame.draw.line(screen, CHILD_SEPLINE_COLOR, ((i * SCREEN_WIDTH // 3) + OFFSET, 0), ((i * SCREEN_WIDTH // 3) + OFFSET, SCREEN_HEIGHT), 3)

        pygame.draw.line(screen, LINE_COLOR, (3 * SCREEN_WIDTH // 3, 0), (3 * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 10)

        for pos, symbol in self.position.items():
            col = pos % 3
            row = pos // 3
            x = col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2
            y = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2

            x_child = col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2 + OFFSET
            y_child = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2

            if symbol == 'HUMAN':
                text = font.render('x', True, PLAYER_HUMAN_COLOR)
                text_child = font.render('x', True, CHILD_PLAYER_COLOR)
            elif symbol == 'AI':
                text = font.render('o', True, PLAYER_AI_COLOR)
                text_child = font.render('o', True, CHILD_PLAYER_COLOR)

            else:
                continue
            text_rect = text.get_rect(center=(x, y))
            text_child_rect = text_child.get_rect(center=(x_child, y_child))
            screen.blit(text, text_rect)
            screen.blit(text_child, text_child_rect)

        max_visits = 0
        max_score = 0
        if children is not None:
            for child in children:
                similarities = 0
                for child_pos, child_symbol in child.board.position.items():
                    for pos, symbol in self.position.items():
                        if child_pos == pos and child_symbol == symbol:
                            similarities += 1
                            if similarities == 9:
                                best_child = child
                                break
                        if child_pos == pos and child_symbol != symbol and symbol == '_':
                            #print(f'{child.board.position} visits: {child.visits} score: {child.score}')
                            print(child_pos, pos)
                            col = pos % 3
                            row = pos // 3
                            x = (col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2 + OFFSET)
                            y_1 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4
                            y_2 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4 * 2
                            y_3 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4 * 3
                            score = small_font.render(f'score: {child.score}', True, FONT_COLOR)
                            visits = small_font.render(f'visits: {child.visits}', True, FONT_COLOR)
                            uct = small_font.render(f'UCT: {child.uct:.2f}', True, FONT_COLOR)
                            score_rect = score.get_rect(center=(x, y_1))
                            visits_rect = visits.get_rect(center=(x, y_2))
                            uct_rect = uct.get_rect(center=(x, y_3))
                            screen.blit(score, score_rect)
                            screen.blit(visits, visits_rect)
                            screen.blit(uct, uct_rect)
                            break

            found = False
            for child in children:
                if child != best_child and not found:
                    found = True
                    for child_pos, child_symbol in child.board.position.items():
                        for best_child_pos, best_child_symbol in best_child.board.position.items():
                            if best_child_pos == child_pos and child_symbol != best_child_symbol and best_child_symbol == 'AI':
                                col = best_child_pos % 3
                                row = best_child_pos // 3
                                x = (col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2 + OFFSET)
                                y_1 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4
                                y_2 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4 * 2
                                y_3 = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 4 * 3
                                score = small_font.render(f'score: {best_child.score}', True, (255, 0, 0))
                                visits = small_font.render(f'visits: {best_child.visits}', True, (255, 0, 0))
                                uct = small_font.render(f'UCT: {best_child.uct:.2f}', True, (255, 0, 0))
                                score_rect = score.get_rect(center=(x, y_1))
                                visits_rect = visits.get_rect(center=(x, y_2))
                                uct_rect = uct.get_rect(center=(x, y_3))
                                screen.blit(score, score_rect)
                                screen.blit(visits, visits_rect)
                                screen.blit(uct, uct_rect)
                                break



    def end_game_screen(self, screen, font, button_font, message):
        screen.fill(BG_COLOR)
        text = font.render(message, True, FONT_COLOR)
        text_rect = text.get_rect(center=((SCREEN_WIDTH + OFFSET) // 2, SCREEN_HEIGHT // 2 - FONT_SIZE))
        screen.blit(text, text_rect)

        play_again_button_rect = pygame.Rect(((SCREEN_WIDTH + OFFSET) // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
        exit_button_rect = pygame.Rect(((SCREEN_WIDTH + OFFSET) // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + 10), (BUTTON_WIDTH, BUTTON_HEIGHT))

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
        for i in range(0, 9, 3):
            if self.position[i] == self.position[i+1] == self.position[i+2] == self.player_2:
                return [i, i+1, i+2]
        for i in range(3):
            if self.position[i] == self.position[i+3] == self.position[i+6] == self.player_2:
                return [i, i+3, i+6]
        if self.position[0] == self.position[4] == self.position[8] == self.player_2:
            return [0, 4, 8]
        if self.position[2] == self.position[4] == self.position[6] == self.player_2:
            return [2, 4, 6]
        return None
    
    def draw_connecting_line(self, screen, winning_combination):
        start = winning_combination[0]
        end = winning_combination[2]
        start_x = (start % 3) * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2
        start_y = (start // 3) * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2
        end_x = (end % 3) * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2
        end_y = (end // 3) * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2
        pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 5)
        pygame.display.flip()

if __name__ == '__main__':
    board = TicTacToe()
    board.game_loop()
