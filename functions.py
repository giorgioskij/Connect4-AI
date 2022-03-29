from types import FunctionType
from typing import Iterable
from player import Player
import random
from math import inf

def randomMove(board: Iterable, max_player_turn: bool = True, alpha: float = -inf, beta: float = inf, depth: int = 5, heuristic: FunctionType = None):
    moves = findAvailableMoves(board)
    col = random.choice(moves)
    return col, 0

def checkWinner(board) -> Player:
    '''
    Checks if the current board state has a winner
    Returns:
        Player.X/O  if a player has won
        Player.TIE  if the game is tied
        None        if the game is not over yet
    '''
    width = len(board[0])
    height = len(board)
    for s in 'XO':
        # Check horizontal locations
        for c in range(width-3):
            for r in range(height):
                if s in board[r][c] and s in board[r][c+1] and s in board[r][c+2] and s in board[r][c+3]:
                    return Player.X if s == 'X' else Player.O
        # Check vertical locations
        for c in range(width):
            for r in range(height-3):
                if s in board[r][c] and s in board[r+1][c] and s in board[r+2][c] and s in board[r+3][c]:
                    return Player.X if s == 'X' else Player.O
        # Check / diaganols
        for c in range(width-3):
            for r in range(height-3):
                if s in board[r][c] and s in board[r+1][c+1] and s in board[r+2][c+2] and s in board[r+3][c+3]:
                    return Player.X if s == 'X' else Player.O
        # Check \ diaganols
        for c in range(width-3):
            for r in range(3, height):
                if s in board[r][c] and s in board[r-1][c+1] and s in board[r-2][c+2] and s in board[r-3][c+3]:
                    return Player.X if s == 'X' else Player.O
    # check for at least one available spot
    for row in board:
        for cell in row:
            if not 'X' in cell and not 'O' in cell:
                return None
    return Player.TIE


def findAvailableMoves(board):
    '''
    Return a list with the indices of the colums where a piece can be still placed
    '''
    return [c for c in range(len(board[0])) if board[0][c].strip() == '']


def makeMove(board_original: Iterable, player: Player, col: int) -> list:
    '''
    Returns a copy of the board in which the move has been played
    '''
    # board = deepcopy(board_original)
    board = list(map(list, board_original)) # makes a copy of the board and converts it to a list in case it was a tuple
    height = len(board)
    width = len(board[0])
    # print('row: {}'.format(row))
    # print('col: {}'.format(col))
    # print('width: {}'.format(width))
    # if not ((row == -1 or 0 <= row < height) and 0 <= col <= width): return None        
    if not 0 <= col <= width: return None        
    # if row >= 0 and ('X' in board[row][col] or 'O' in board[row][col]): return None
    # if row == -1:
    for i in range(height - 1, -1, -1):
        if 'X' not in board[i][col] and 'O' not in board[i][col]:
            row = i
            break
    else:
        return None

    board[row][col] = '{}'.format('X' if player == Player.X else 'O')
    return board


def draw(board) -> None:
    '''
    Draws the given board to stdout
    '''
    width = len(board[0])
    height = len(board)
    row_count = 97
    col_count = 1
    print('  ', end='')
    for i in range(width):
        print('  {} '.format(col_count), end = '')
        col_count += 1
    print()
    for row in range(height):
        print('{} |'.format(chr(row_count)), end = ' ')
        row_count += 1
        for cell in range(width):
            print(board[row][cell], end = ' | ')
        print() 
    print()  