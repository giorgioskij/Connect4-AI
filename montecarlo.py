from math import sqrt, log, inf
from typing import Iterable
from functions import checkWinner, findAvailableMoves, makeMove
from player import Player
import random
import numpy as np


C = 1.5


class Node:

    def __init__(self, board: tuple, has_next_move: Player, last_move: int):
        self.board = board
        self.last_move = last_move
        self.has_next_move = has_next_move

        self.visits: int = 0
        self.total_value: int = 0

        self.is_terminal: bool = checkWinner(self.board) is not None


    def computeUcb(self, parent_visits):

        if not self.visits:
            return inf

        ucb = (self.total_value/self.visits) + C * sqrt(log(parent_visits) / self.visits)
        
        return ucb

    def __repr__(self):
        return f'Node:\n  visits:{self.visits}\n  total_value:{self.total_value}\n  has_next_move:{self.has_next_move}\n  is_terminal:{self.is_terminal}\n  last_move:{self.last_move}\n  board:\n{np.array(self.board)}\n'


class MonteCarloTree:

    def __init__(self, board: Iterable, num_iterations: int = 1000, num_rollout: int = 100, starting_player = Player.X, verbose = False):
        self.starting_player = starting_player
        self.tree = dict()
        self.children = {}
        self.v = verbose
        self.num_iterations = num_iterations
        self.num_rollout = num_rollout

        frozen_board = tuple(map(tuple, board))
        self.root = Node(board = frozen_board, has_next_move=starting_player, last_move=None)
        self.current_node = self.root
        self.children[self.root] = []

    def findBestMove(self, node: Node = None):
        '''
        Finds the best move from the current node, comparing the children based on average value.
        '''
        if node is None:
            node = self.current_node

        best_child = None
        best_value = -inf
        for child in self.children[node]:
            value = child.total_value / child.visits
            if value > best_value:
                best_value = value
                best_child = child

        self.current_node = best_child
        return best_child.last_move

    def updateOpponentMove(self, move: int):

        # print('move: {}'.format(move))

        if move is None: return

        if self.current_node in self.children and self.children[self.current_node]:
            for child in self.children[self.current_node]:
                if child.last_move == move:
                    new_node = child
                    # self.current_node = child
        else:
            new_board = makeMove(self.current_node.board, Player.O, move)
            new_frozen_board = tuple(map(tuple, new_board))
            new_node = Node(new_frozen_board, has_next_move=Player.X, last_move=move)
            # self.current_node = new_node

        if self.current_node in self.children:
            self.children[self.current_node].append(new_node)
        else:
            self.children[self.current_node] = [new_node]
        
        self.current_node = new_node

        return 


    def train(self):
        '''
        Trains itself executing self.num_iterations iterations
        '''
        # print('starting to train from node: {}'.format(self.current_node))
        for _ in range(self.num_iterations):
            self.iteration(node = self.current_node)


    def iteration(self, node: Node = None):
        '''
        Performs one full iteration of the MCTS algorithm
        '''

        if node is None:
            node = self.current_node

        if self.v: 
            print('Starting iteration from node: {}\n'.format(node))

        # select a path to a leaf based on some policy
        path: list = self.choosePath(node)

        # the leaf is the last non explored node
        leaf: Node = path[-1]

        if self.v: 
            print('the leaf is: {}\n'.format(leaf))

        # pick a child of the last unexplored node
        if leaf.is_terminal:
            new_node = leaf
        else:
            new_node = self.expand(leaf)
            path.append(new_node)
        # new_node = self.expand(leaf) if not leaf.is_terminal else leaf
        # path.append(new_node)

        if self.v: 
            print('the new node is: {}\n'.format(new_node))

        # simulation
        reward = 0
        if new_node.is_terminal:
            winner = checkWinner(new_node.board)
            if winner is Player.X:
                reward = 100
            elif winner is Player.O:
                reward = 0
            else: 
                reward = 50

        wins = 0
        for _ in range(self.num_rollout):
            winner = self.simulateGameFromNode(new_node)
            if winner == Player.X:
                wins += 1
        reward = int(round((wins/self.num_rollout) * 100 ))

        if self.v: 
            print('the reward of this node is: {}\n'.format(reward))

    
        # backpropagation
        for n in path[::-1]:
            n.visits += 1
            n.total_value += reward

        
        if self.v: 
            print('tree at the end of the iteration: {}\n\n'.format(self.children))


    # choose a random unexplored move from node and add a corresponding new node to the tree
    def expand(self, node: Node):
        '''
        Expands the tree choosing a child of the current leaf node
        '''

        # if self.v: 
        #     print('expanding node: {}\n'.format(node))

        # find already explored moves
        explored_moves = {child.last_move for child in self.children[node]} if node in self.children else set()

        new_moves = set(findAvailableMoves(node.board)) - explored_moves
        move = random.choice(list(new_moves))

        if self.v: 
            print('available moves: {}'.format(new_moves))

        new_board = makeMove(node.board, node.has_next_move, move)
        new_frozen_board = tuple(map(tuple, new_board))
        next_player = Player.X if node.has_next_move == Player.O else Player.O
        new_node = Node(board=new_frozen_board,has_next_move=next_player, last_move=move)

        if node in self.children:
            self.children[node].append(new_node)
        else:
            self.children[node] = [new_node]

        return new_node
            



    # choose a path starting from node and ending on a leaf (node with no children)
    def choosePath(self, node) -> list:
        '''
        Navigates the tree choosing the path to the best leaf
        '''
        path = [node]
        last = node
        while True:
            # last is a leaf if it has at least one child that hasn't been explored yet
            if last not in self.children or len(self.children[last]) < len(findAvailableMoves(last.board)):
                break
            chosen_child = self.chooseBestChild(last)
            last = chosen_child
            path.append(last)
        return path
        

    def simulateGameFromNode(self, node: Node) -> Player:
        '''
        Runs a single simulation of a game starting from the state of the given node
        played by random players.
        '''
        board = node.board
        player = node.has_next_move
        winner = checkWinner(board)
        while winner is None:
            moves = findAvailableMoves(board)
            move = random.choice(moves)
            board = makeMove(board, player, move)
            player = Player.X if player == Player.O else Player.O

            winner = checkWinner(board)

        return winner

    # choose the child with highest ucb
    def chooseBestChild(self, node):
        '''
        Computes UCB to find the best child of the current node
        '''
        best_ucb = -inf
        best_child = None

        for child in self.children[node]:
            ucb = child.computeUcb(node.visits)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child
    
        return best_child
        


