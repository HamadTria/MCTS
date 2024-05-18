import pygame
import sys
from copy import deepcopy
import time
from mcts import *

MAX_ITER = 500
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
OFFSET = 400
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
PLAYER_HUMAN_COLOR = (255, 0, 0)
PLAYER_AI_COLOR = (0, 0, 255)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 100
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
                    col = pos[0] // (SCREEN_WIDTH // 3)
                    row = pos[1] // (SCREEN_HEIGHT // 3)
                    move = row * 3 + col

                    if self.position[move] != self.empty_square:
                        continue

                    self = self.make_move(move)
                    
                    screen.fill(BG_COLOR)
                    self.draw_board(screen, font)
                    pygame.display.flip()
                    clock.tick(30)

                    if self.is_win():
                        winning_combination = self.get_winning_combination()
                        self.draw_connecting_line(screen, winning_combination) 
                        time.sleep(1)                    
                        self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                        return
                    elif self.is_draw():
                        self.end_game_screen(screen, font, button_font, "Game is drawn!")
                        return

                    try:
                        best_move, children = mcts.search(self, MAX_ITER)
                        list_children =  list((children.values()))

                        best_move_score = best_move.score
                        first_child_score = list_children[0].score
                        best_move_visits = best_move.visits
                        first_child_visits = list_children[0].visits

                        self.draw_small_board(screen, SCREEN_WIDTH + 10, 10, font)
                        self.draw_scores(screen, SCREEN_WIDTH + 10, SCREEN_HEIGHT // 3 + 10, font, best_move_score, first_child_score, best_move_visits, first_child_visits)

                        pygame.display.flip()
                        
                        self = best_move.board

                        screen.fill(BG_COLOR)
                        self.draw_board(screen, font)
                        self.draw_child_nodes(screen, font, children, OFFSET, 0, 0.5)
                        pygame.display.flip()
                        clock.tick(30)

                        if self.is_win():
                            winning_combination = self.get_winning_combination()
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

    def draw_child_nodes(self, screen, font, children, offset_x, offset_y, scale_factor):
        board_width = SCREEN_WIDTH // 3 * 3
        board_height = SCREEN_HEIGHT // 3 * 3

        for i, (_, child_node) in enumerate(children.items()):
            child_offset_x = offset_x + (i % 3) * (board_width // 3) * scale_factor
            child_offset_y = offset_y + (i // 3) * (board_height // 3) * scale_factor

            self.draw_board(screen, font, child_node, child_offset_x, child_offset_y, scale_factor)

            score_text = font.render(str(child_node.score), True, FONT_COLOR)
            visits_text = font.render(str(child_node.visits), True, FONT_COLOR)

            score_rect = score_text.get_rect(center=(child_offset_x + (board_width // 3) * scale_factor, child_offset_y - board_height // 10 * scale_factor))
            visits_rect = visits_text.get_rect(center=(child_offset_x + (board_width // 3) * scale_factor, child_offset_y + board_height // 8 * scale_factor))

            screen.blit(score_text, score_rect)
            screen.blit(visits_text, visits_rect)


    def draw_board(self, screen, font):
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SCREEN_HEIGHT // 3), (SCREEN_WIDTH, i * SCREEN_HEIGHT // 3), 3)
            pygame.draw.line(screen, LINE_COLOR, (i * SCREEN_WIDTH // 3, 0), (i * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 3)
        pygame.draw.line(screen, LINE_COLOR, (3 * SCREEN_WIDTH // 3, 0), (3 * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 3)

        for pos, symbol in self.position.items():
            col = pos % 3
            row = pos // 3
            x = col * (SCREEN_WIDTH // 3) + (SCREEN_WIDTH // 3) // 2
            y = row * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 3) // 2

            if symbol == 'HUMAN':
                text = font.render('x', True, PLAYER_HUMAN_COLOR)
            elif symbol == 'AI':
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

    def draw_small_board(self, screen, x, y, font):
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (x, y + i * SCREEN_HEIGHT // 9), (x + SCREEN_WIDTH // 3, y + i * SCREEN_HEIGHT // 9), 1)
            pygame.draw.line(screen, LINE_COLOR, (x + i * SCREEN_WIDTH // 9, y), (x + i * SCREEN_WIDTH // 9, y + SCREEN_HEIGHT // 3), 1)

        for pos, symbol in self.position.items():
            col = pos % 3
            row = pos // 3
            x_small = x + col * (SCREEN_WIDTH // 9) + (SCREEN_WIDTH // 18)
            y_small = y + row * (SCREEN_HEIGHT // 9) + (SCREEN_HEIGHT // 18)

            if symbol == 'HUMAN':
                text = font.render('x', True, PLAYER_HUMAN_COLOR)
            elif symbol == 'AI':
                text = font.render('o', True, PLAYER_AI_COLOR)
            else:
                continue

            screen.blit(text, (x_small, y_small))

    def draw_scores(self, screen, x, y, font, best_move_score, first_child_score, best_move_visits, first_child_visits):
        score_text = font.render("Score: " + str(best_move_score), True, FONT_COLOR)
        screen.blit(score_text, (x, y))

        first_child_score_text = font.render("First Child Score: " + str(first_child_score), True, FONT_COLOR)
        screen.blit(first_child_score_text, (x, y + 20))

        visits_text = font.render("Visits: " + str(best_move_visits), True, FONT_COLOR)
        screen.blit(visits_text, (x, y + 40))

        first_child_visits_text = font.render("First Child Visits: " + str(first_child_visits), True, FONT_COLOR)
        screen.blit(first_child_visits_text, (x, y + 60))



if __name__ == '__main__':
    board = TicTacToe()
    board.game_loop()
