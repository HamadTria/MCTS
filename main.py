from gridworld import GridWorld
from graph_visualisation import GraphVisualisation
from qtable import QTable
from single_agent_mcts import SingleAgentMCTS
from upper_confidence_bounds import UpperConfidenceBounds

for i in range(20):
    gridworld = GridWorld()
    qfunction = QTable()
    root_node = SingleAgentMCTS(gridworld, qfunction, UpperConfidenceBounds()).mcts(timeout=0.001 + i * 0.001)
    gv = GraphVisualisation(max_level=6)
    graph = gv.single_agent_mcts_to_graph(root_node, filename=f"mcts{i}")
    graph.render(directory='images', view=False)