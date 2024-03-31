import math
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state      # TicTacToe instance
        self.parent = parent    # Node instance
        self.children = []      # List of Node instances
        self.value = 0          # Value of the node : sum of wins - sum of losses
        self.visits = 0         # Number of visits

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def select_child(self, exploration_constant):
        """Select a child node according to the UCB1 formula."""
        best_child = None
        best_score = float('-inf')
        for child in self.children:
            exploit = child.value / child.visits if child.visits != 0 else 0
            explore = math.sqrt(math.log(self.visits) / child.visits) if child.visits != 0 else float('inf')
            score = exploit + exploration_constant * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
        return child

class MCTS:
    def __init__(self, exploration_constant=1.4, iterations=1000):
        self.exploration_constant = exploration_constant
        self.iterations = iterations

    def search(self, initial_state):
        root = Node(initial_state)
        player = 'X' if initial_state.player_turn() else 'O'

        for _ in range(self.iterations):
            node = root
            state = initial_state.copy()

            # Select
            while node.is_fully_expanded() and not node.state.is_terminal():
                node = node.select_child(self.exploration_constant)
                state.apply_move(node.state.last_move)

            # Expand
            if not node.is_fully_expanded() and not state.is_terminal():
                unvisited = [move for move in state.get_legal_moves() if move not in [child.state.last_move for child in node.children]]
                move = random.choice(unvisited)
                state.apply_move(move)
                node = node.add_child(state)

            # Rollout
            while not state.is_terminal():
                move = random.choice(state.get_legal_moves())
                state.apply_move(move)

            # Backpropagate
            while node is not None:
                node.visits += 1
                if state.is_winner(player):
                    node.value += 1
                elif state.is_draw():
                    pass
                else:
                    node.value -= 1
                node = node.parent

        return max(root.children, key=lambda node: node.visits).state.last_move



            

            

            

