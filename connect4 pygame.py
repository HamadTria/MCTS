import math
import random
import pygame
import sys
from copy import deepcopy

class Node():
    def __init__(self, board, parent):
        self.board = board
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}

class MCTS():
    def search(self, initial_state, max_iterations=1000):
        self.root = Node(initial_state, None)

        for _ in range(max_iterations):
            node = self.select(self.root)
            score = self.rollout(node.board)
            self.backpropagate(node, score)
        for child in self.root.children:
            print(child.score, child.visits)
        return self.get_best_move(self.root, 0)

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        states = node.board.legal_moves()
        for state in states:
            if str(state) not in node.children:
                new_node = Node(state, node)
                node.children[str(state)] = new_node

                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

    def rollout(self, board):
        while not board.is_win():
            try:
                board = random.choice(board.legal_moves())
            except:
                return 0
        if board.player_2 == 'HUMAN': 
            return 1
        return -1

    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            if child_node.board.player_2 == 'HUMAN': current_player = 1
            elif child_node.board.player_2 == 'AI': current_player = -1

            exploration = exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
            exploitation = current_player * child_node.score / child_node.visits
            move_score = exploitation + exploration

            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
            elif move_score == best_score:
                best_moves.append(child_node)
        return random.choice(best_moves)

MAX_ITER = 1000
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
        self.board = [['_' for _ in range(7)] for _ in range(6)]
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def make_move(self, col):
        board = ConnectFour(self)
        for row in range(5, -1, -1):
            if board.board[row][col] == '_':
                board.board[row][col] = self.player_1
                (board.player_1, board.player_2) = (board.player_2, board.player_1)
                break
        return board

    def is_draw(self):
        for row in self.board:
            if '_' in row:
                return False
        return True

    def is_win(self):
        # horizontal
        for row in self.board:
            for col in range(4):
                if row[col] == row[col+1] == row[col+2] == row[col+3] == self.player_2:
                    return True

        # vertical
        for col in range(7):
            for row in range(3):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] == self.player_2:
                    return True

        # diagonal (top-left to bottom-right)
        for col in range(4):
            for row in range(3):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] == self.player_2:
                    return True

        # diagonal (top-right to bottom-left)
        for col in range(4, 7):
            for row in range(3, -1, -1):
                if self.board[row][col] == self.board[row-1][col-1] == self.board[row-2][col-2] == self.board[row-3][col-3] == self.player_2:
                    return True

        return False

    def legal_moves(self):
        actions = []
        for col in range(7):
            if self.board[0][col] == '_':
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

                    if self.board[0][col] != '_':
                        continue

                    self = self.make_move(col)

                    screen.fill(BG_COLOR)
                    self.draw_board(screen, font)
                    pygame.display.flip()
                    clock.tick(30)

                    if self.is_win():
                        self.end_game_screen(screen, font, button_font, "'%s' has won!" % self.player_2)
                        return
                    elif self.is_draw():
                        self.end_game_screen(screen, font, button_font, "Game is drawn!")
                        return

                    best_move = mcts.search(self, MAX_ITER)
                    try:
                        self = best_move.board
                        if self.is_win():
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

                if self.board[row][col] == 'HUMAN':
                    text = font.render('o', True, PLAYER_HUMAN_COLOR)
                elif self.board[row][col] == 'AI':
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

if __name__ == '__main__':
    board = ConnectFour()
    board.game_loop()
