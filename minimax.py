import random
from types import FunctionType
from typing import Iterable 
from functions import checkWinner, draw,findAvailableMoves, makeMove
from heuristics import heuristic_one, monteCarlo
from player import Player
from math import inf
import time


'''
A collection of algorithms to find the best move in a given board.
They all have the same parameters for ease of switching from one to the other
'''


# minimax with no optimizations. takes too long even for a 4 by 4 game.
def minimax(board: Iterable, max_player_turn: bool = True, alpha: float = -inf, beta: float = inf, depth: int = 5, heuristic: FunctionType = heuristic_one):

    '''
    Algoritmo Minimax senza alcuna ottimizzazione.
    Effettua una ricerca completa, quindi impiega troppo anche per una partita con dimensione 4x4.
    '''
    moves = findAvailableMoves(board)
    winner = checkWinner(board)
    # draw(board)
    # time.sleep(0.01)

    minimax.counter += 1
    print('\r{}'.format(minimax.counter), end = '')

    if winner is not None:
        if winner == Player.X:
            return (None, inf)
        elif winner == Player.O:
            return (None, -inf)
        elif winner == Player.TIE:
            return (None, 0)
    
    if max_player_turn:
        value = -inf
        best_column = random.choice(moves)
        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.X, col)
            new_score = minimax(board=new_board, max_player_turn=False)[1]

            if new_score > value:
                value = new_score
                best_column = col

        return (best_column, value)
    
    else:
        value = inf
        best_column = random.choice(moves)

        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.O, col)
            new_score = minimax(board=new_board, max_player_turn=True)[1]
            if new_score < value:
                value = new_score
                best_column = col

        return (best_column, value)


minimax.counter = 0

 
def minimax_ab(board: Iterable, max_player_turn: bool = True, alpha: float = -inf, beta: float = inf, depth: int = 5, heuristic: FunctionType = heuristic_one):

    moves = findAvailableMoves(board)
    winner = checkWinner(board)
    minimax_ab.counter += 1
    print('\r{}'.format(minimax_ab.counter), end = '')

    if winner is not None:
        if winner == Player.X:
            return (None, inf)
        elif winner == Player.O:
            return (None, -inf)
        elif winner == Player.TIE:
            return (None, 0)
    
    if max_player_turn:
        value = -inf
        best_column = random.choice(moves)
        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.X, col)
            new_score = minimax_ab(board=new_board, alpha=alpha, beta=beta, max_player_turn=False)[1]
            if new_score > value:
                value = new_score
                best_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            # if max(alpha, value) >= inf:
            #     break
        return (best_column, value)
    
    else:
        value = inf
        best_column = random.choice(moves)
        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.O, col)
            new_score = minimax_ab(board=new_board, alpha=alpha, beta=beta, max_player_turn=True)[1]
            if new_score < value:
                value = new_score
                best_column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
            # if min(beta, value) <= -inf:
            #     break
        return (best_column, value)
minimax_ab.counter = 0




def minimax_ab_heur(board: Iterable, max_player_turn: bool = True, alpha: float = -inf, beta: float = inf, depth: int = 5, heuristic: FunctionType = heuristic_one):

    '''
    Minimax algorithm with alpha beta pruning and a heuristic 
    '''

    moves = findAvailableMoves(board)
    winner = checkWinner(board)
    minimax_ab_heur.counter += 1
    print('\r{}'.format(minimax_ab_heur.counter), end = '')


    if winner is not None:
        if winner is not None:
            if winner == Player.X:
                return (None, inf)
            elif winner == Player.O:
                return (None, -inf)
            elif winner == Player.TIE:
                return (None, 0)
    
    if not depth:
        if heuristic == monteCarlo:
            value = heuristic(board, Player.X if max_player_turn else Player.O, 10)
        else:
            value = heuristic(board, Player.X)
        # draw(board)
        # print('value: {}'.format(value))
        return (None, value)

    if max_player_turn:
        value = -inf
        best_column = random.choice(moves)
        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.X, col)
            new_score = minimax_ab_heur(board=new_board, depth=depth -1, alpha=alpha, beta=beta, max_player_turn=False, heuristic=heuristic)[1]
            if new_score > value:
                value = new_score
                best_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (best_column, value)
    
    else:
        value = inf
        best_column = random.choice(moves)
        for col in moves:
            # new_board = deepcopy(board)
            new_board = makeMove(board, Player.O, col)
            new_score = minimax_ab_heur(board=new_board, depth=depth -1, alpha=alpha, beta=beta, max_player_turn=True, heuristic=heuristic)[1]
            if new_score < value:
                value = new_score
                best_column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (best_column, value)

minimax_ab_heur.counter = 0


