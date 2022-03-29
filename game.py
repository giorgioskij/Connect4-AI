from enum import Enum, auto
from montecarlo import MonteCarloTree
from minimax import minimax, minimax_ab, minimax_ab_heur
from player import Player
from functions import checkWinner, draw, makeMove, randomMove
from heuristics import heuristic_one, heuristic_one_bis, heuristic_two
from datetime import datetime
from math import inf

class State(Enum):
    PLAYING = auto()
    OVER = auto()

class Algorithm(Enum):
    '''
    Available algorithms to implement the ai
    '''
    RANDOM = randomMove
    MINIMAX = minimax
    MINIMAX_AB = minimax_ab
    MINIMAX_HEUR = minimax_ab_heur
    MONTECARLO = 'monteCarlo'

class Connect4:
    '''
    This class implements the game engine to play Connect4 against the ai
    '''

    def __init__(self, algorithm: Algorithm = Algorithm.RANDOM, width: int = 7, height: int = 6, depth: int = 5):
        self.algorithm = algorithm
        self.width = width
        self.height = height if height > -1 else width
        self.depth = depth
        self.players = [Player.X, Player.O]
        self.last_move = None
        if width > 25 or height > 25: raise Exception('size too big')

        # self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.state = State.OVER


    def askMove(self):
        '''
        Asks the player to input his move on stdin 
        '''
        first_time = True
        accepted = False

        while not accepted:
            if first_time:
                print('input your move as the number of your chosen column: ', end = '')
                first_time = False
            else:
                print('string not accepted. Insert another one: ', end = '')
            print()

            s = str(input()).strip()
            if not(1 <= len(s) <= 2) or not s[0].isdigit() or not s[-1].isdigit(): continue
            col = int(s) - 1
            if col < 0 or col >= self.width: continue
            row = -1
            # check that the column is not full
            for i in range(self.height - 1, -1, -1):
                if 'X' not in self.board[i][col] and 'O' not in self.board[i][col]:
                    row = i
                    break
            if row == -1: 
                print('the selected column is full')
                continue
            if 0 <= col < self.width and 0 <= row < self.height:
                accepted = True
        return col


    def newGame(self, starting_player: Player, num_iterations: int = 1000, num_rollout: int = 100, verbose: bool = False):
        '''
        Starts a new game
        '''
        self.state = State.PLAYING
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.verbose = verbose
        if self.algorithm == Algorithm.MONTECARLO:
            self.montecarlo = MonteCarloTree(board=self.board, num_iterations=num_iterations, num_rollout=num_rollout, starting_player=starting_player, verbose=verbose)

        print('Starting a new game!')
        draw(self.board)
        print()
        self.turn(starting_player)

        return

        


    def turn(self, player: Player):
        '''
        Plays a turn in the game, either asking the player for his move
        or calling the ai to find the best move
        '''
        print('Player {} turn:'.format('X' if player == Player.X else 'O'))
        if player == Player.X:
            move = self.findBestMove()
        else:
            move = self.askMove()
        self.board = makeMove(self.board, player, move)
        self.last_move = move
        draw(self.board)
        winner = checkWinner(self.board)
        if winner is not None:
            self.state = State.OVER

        if self.state == State.PLAYING:
            self.turn(Player.X if player == Player.O else Player.O)
        return 


    def findBestMove(self) -> int:
        '''
        Uses the ai algorithm to find and return the best move.
        '''

        tic = datetime.now()
        
        if self.algorithm == Algorithm.MONTECARLO:
            
            self.montecarlo.updateOpponentMove(self.last_move)
            self.montecarlo.train()
            move = self.montecarlo.findBestMove()
        
        else:
            move, value = self.algorithm(board=self.board, depth = self.depth, heuristic = heuristic_one_bis)

        
        # mc = MonteCarloTree(self.board)
        # mc.train()
        # move = mc.findBestMove()
        

        toc = datetime.now()

        print('\nfound best move in : {}'.format(toc - tic))
        # print('value: {}'.format(value))


        return move



game = Connect4(algorithm=Algorithm.MONTECARLO, width=7, height=6)
game.newGame(starting_player=Player.X, num_iterations=5000)


# statistical model checking
