class Node {
    constructor(board, parent) {
        this.board = board;
        if (this.board.isWin() || this.board.isDraw()) {
            this.isTerminal = true;
        } else {
            this.isTerminal = false;
        }
        this.isFullyExpanded = this.isTerminal;
        this.parent = parent;
        this.visits = 0;
        this.score = 0;
        this.children = {};
    }
}

class MCTS {
    search(initialState, maxIterations = 1000) {
        this.root = new Node(initialState, null);

        for (let i = 0; i < maxIterations; i++) {
            let node = this.select(this.root);
            let score = this.rollout(node.board);
            this.backpropagate(node, score);
        }

        return this.getBestMove(this.root, 0);
    }

    select(node) {
        while (!node.isTerminal) {
            if (node.isFullyExpanded) {
                node = this.getBestMove(node, 2);
            } else {
                return this.expand(node);
            }
        }
        return node;
    }

    expand(node) {
        let states = node.board.legalMoves();
        for (let state of states) {
            if (!node.children[state.position.toString()]) {
                let newNode = new Node(state, node);
                node.children[state.position.toString()] = newNode;

                if (states.length === Object.keys(node.children).length) {
                    node.isFullyExpanded = true;
                }
                return newNode;
            }
        }
    }

    rollout(board) {
        while (!board.isWin()) {
            try {
                board = board.legalMoves()[Math.floor(Math.random() * board.legalMoves().length)];
            } catch {
                return 0;
            }
        }
        if (board.player2 === 'x') return 1;
        else if (board.player2 === 'o') return -1;
    }

    backpropagate(node, score) {
        while (node !== null) {
            node.visits += 1;
            node.score += score;
            node = node.parent;
        }
    }

    getBestMove(node, explorationConstant) {
        let bestScore = -Infinity;
        let bestMoves = [];

        for (let childNode of Object.values(node.children)) {
            let currentPlayer = childNode.board.player2 === 'x' ? 1 : -1;

            let exploration = explorationConstant * Math.sqrt(Math.log(node.visits / childNode.visits));
            let exploitation = currentPlayer * childNode.score / childNode.visits;
            let moveScore = exploitation + exploration;

            if (moveScore > bestScore) {
                bestScore = moveScore;
                bestMoves = [childNode];
            } else if (moveScore === bestScore) {
                bestMoves.push(childNode);
            }
        }
        return bestMoves[Math.floor(Math.random() * bestMoves.length)];
    }
}

