import math
import random

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
            if str(state.position) not in node.children:
                new_node = Node(state, node)
                node.children[str(state.position)] = new_node

                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                return new_node
    
    def rollout(self, board):
        while not board.is_win():
            try:
                board = random.choice(board.legal_moves())
            except:
                return 0
        if board.player_2 == 'x': 
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
            if child_node.board.player_2 == 'x': current_player = 1
            elif child_node.board.player_2 == 'o': current_player = -1

            exploration = exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))   
            exploitation = current_player * child_node.score / child_node.visits                                  
            move_score = exploitation + exploration
            
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
            elif move_score == best_score:
                best_moves.append(child_node)
        return random.choice(best_moves)




























