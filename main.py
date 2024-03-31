from tictactoe import TicTacToe
from mcts import MCTS

# Example of using MCTS to play Tic-Tac-Toe
player = input("Do you want to play first? (y/n): ") == "y"
game = TicTacToe()
mcts = MCTS(iterations=1000)
while not game.is_terminal():
    if game.player_turn() == player:
        move = int(input("Your move: "))
    else:
        move = mcts.search(game)
        print("AI chooses move:", move)
    game.apply_move(move)
    game.print_board()
print("Winner is player", game.current_winner)