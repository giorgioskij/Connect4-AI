from typing import Iterable
from player import Player
from functions import checkWinner, findAvailableMoves, makeMove
import random

def heuristic_one_bis(board: Iterable, player: Player):
    '''
    This is a slightly improved version of heuristic one
    Currently it values every streak of 3 with starting or trailing whitespace as 500 points, streaks of 3 as 100 points, and every streak of 2 as 1 point.
    It also tries to prevent the opponent to win, valuing the opponent's streaks with negative points.
    '''

    def checkForStreaks(board: Iterable, symbol: str, streak: int, whitespace: bool = False):
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == symbol or (whitespace and board[i][i].strip() == ''):
                    count += verticalStreak(i, j, board, streak, symbol, whitespace)
                    count += horizontalStreak(i, j, board, streak, symbol, whitespace)
                    count += diagonalCheck(i, j, board, streak, symbol, whitespace)
        return count

    def verticalStreak(row, col, board, streak, symbol, whitespace = False):
        consecutive_count = 0
        for i in range(row+1, len(board)):
            if board[i][col] == symbol:
                consecutive_count += 1
            elif whitespace and board[i][col].strip() == '' and board[row][col].strip() != '':
                consecutive_count += 1
            else: break
        return int( ((consecutive_count -1) if whitespace else consecutive_count) >= streak)

    def horizontalStreak(row, col, board, streak, symbol, whitespace = False):
        consecutive_count = 0
        for j in range(col+1, len(board[0])):
            if board[row][j] == symbol:
                consecutive_count += 1
            elif whitespace and board[row][j].strip() == '' and board[row][col].strip() != '':
                consecutive_count += 1
            else: break
        return int(((consecutive_count -1) if whitespace else consecutive_count) >= streak)

    def diagonalCheck(row, col, board, streak, symbol, whitespace = False):
        height, width = len(board), len(board[0])
        total = 0
        consecutive_count = 0
        j = col
        for i in range(row+1, height):
            if j >= width: break
            elif board[i][j] == symbol: consecutive_count += 1
            elif whitespace and board[i][j].strip() == '' and board[row][col].strip() != '': consecutive_count += 1
            else: break
            j += 1 
        if ((consecutive_count -1) if whitespace else consecutive_count) >= streak: total += 1
        consecutive_count = 0
        j = col
        for i in range(row-1, -1, -1):
            if j >= width: break
            elif board[i][j] == symbol: consecutive_count += 1
            elif whitespace and board[i][j].strip() == '' and board[row][col].strip() != '': consecutive_count += 1
            else: break
            j += 1 
        if ((consecutive_count -1) if whitespace else consecutive_count) >= streak: total += 1
        return total



    symbol = 'X' if player == Player.X else 'O'
    opp_symbol = 'X' if symbol == 'O' else 'O'

    my_threes = checkForStreaks(board, symbol, 3)
    my_threes_whitespace = checkForStreaks(board, symbol, 3, whitespace=True)
    my_twos = checkForStreaks(board, symbol, 2)
    opp_threes = checkForStreaks(board, opp_symbol, 3)
    opp_threes_whitespace = checkForStreaks(board, opp_symbol, 3, whitespace=True)

    return my_threes_whitespace*500 - opp_threes_whitespace*500 + my_threes*100 - opp_threes*100 + my_twos


def heuristic_one(board: Iterable, player: Player):
    '''
    This is a basic heuristic that evaluates the status of the board, giving it a score.
    Currently it values every streak of 3 as 100 points, and every streak of 2 as 1 point.
    '''

    def checkForStreaks(board: Iterable, symbol: str, streak: int):
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == symbol:
                    count += verticalStreak(i, j, board, streak)
                    count += horizontalStreak(i, j, board, streak)
                    count += diagonalCheck(i, j, board, streak)
        return count

    def verticalStreak(row, col, board, streak):
        consecutive_count = 0
        for i in range(row, len(board)):
            if board[i][col] == board[row][col]:
                consecutive_count += 1
            else: break
        return int(consecutive_count >= streak)

    def horizontalStreak(row, col, board, streak):
        consecutive_count = 0
        for j in range(col, len(board[0])):
            if board[row][j] == board[row][col]:
                consecutive_count += 1
            else: break
        return int(consecutive_count >= streak)

    def diagonalCheck(row, col, board, streak):
        height, width = len(board), len(board[0])
        total = 0
        consecutive_count = 0
        j = col
        for i in range(row, height):
            if j >= width: break
            elif board[i][j] == board[row][col]: consecutive_count += 1
            else: break
            j += 1 
        if consecutive_count >= streak: total += 1
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j >= width: break
            elif board[i][j] == board[row][col]: consecutive_count += 1
            else: break
            j += 1 
        if consecutive_count >= streak: total += 1
        return total

    symbol = 'X' if player == Player.X else 'O'
    opp_symbol = 'X' if symbol == 'O' else 'O'

    my_fours = checkForStreaks(board, symbol, 4)
    my_threes = checkForStreaks(board, symbol, 3)
    my_twos = checkForStreaks(board, symbol, 2)
    opp_fours = checkForStreaks(board, opp_symbol, 4)
    opp_threes = checkForStreaks(board, opp_symbol, 3)

    if opp_fours > 0:
        return -100000
    else:
        return my_fours*100000 + my_threes*100 - opp_threes*100 + my_twos



def heuristic_two(board: Iterable, player: Player):
    '''
    A better heuristic that uses a new pattern matching algorithm to support more complex rules
    EDIT: too slow, practically useless
    '''

    def countPatterns(board: Iterable, pattern: str):
        '''
        Counts and returns the number of times the given pattern appears on the board.
        The diagonals and rows are only read right to left, and the verticals top to bottom
        '''
        match_list = list(pattern)
        # match_list = [c if c != ' ' else '' for c in match_list]
        match_len = len(match_list)
        height, width = len(board), len(board[0])
        patterns = [0, 0, 0, 0]
        # match with rows
        for row in board:
            patterns[0] += len([i for i in range(width - match_len + 1) if row[i : i + match_len] == match_list])
        # match with columns
        for col_index in range(len(board[0])):
            col = [board[row][col_index] for row in range(height)]
            patterns[1] += len([i for i in range(height - match_len + 1) if col[i : i + match_len] == match_list])
        # match with / diagonals
        for row in range(match_len -1, height):
            for col in range(width - match_len + 1):
                diagonal = [board[row-i][col+i]for i in range(len(match_list))]
                patterns[2] += len([i for i in range(len(diagonal) - match_len + 1) if diagonal[i : i + match_len] == match_list])
        # match with \ diagonals
        for row in range(height - match_len + 1):
            for col in range(width - match_len + 1):
                diagonal = [board[row+i][col+i]for i in range(len(match_list))]
                patterns[3] += len([i for i in range(len(diagonal) - match_len + 1) if diagonal[i : i + match_len] == match_list])
        return sum(patterns)
    
    width = len(board[0])
    symbol = 'X' if player == Player.X else 'O'
    opp_symbol = 'X' if symbol == 'O' else 'O'

    # p1 = countPatterns(board, ' ' + symbol*3 + ' ')             # ' --- '    
    p2 = countPatterns(board, symbol*3 + ' ')                   # '--- '
    p3 = countPatterns(board, ' ' + symbol*3)                   # ' ---'
    p4 = countPatterns(board, symbol*2 + ' ' + symbol)          # '-- -'
    p5 = countPatterns(board, symbol + ' ' + symbol*2)          # '- --'
    # p6 = countPatterns(board, ' ' + symbol*2 + ' ')             # ' -- '
    # p7 = countPatterns(board, symbol*2 + '  ')                  # '--  '
    # p8 = countPatterns(board, '  ' + symbol*2)                  # '  --'
    # p9 = countPatterns(board, symbol + '  ' + symbol)           # '-  -
    p10 = countPatterns(board, symbol*2)                        # '--' 
    p11 = countPatterns(board, symbol*3)
    # o1 = countPatterns(board, ' ' + opp_symbol*3 + ' ')         # ' --- '
    o2 = countPatterns(board, opp_symbol*3 + ' ')               # '--- '
    o3 = countPatterns(board, ' ' + opp_symbol*3)               # ' ---'
    o4 = countPatterns(board, opp_symbol*2 + ' ' + opp_symbol)  # '-- -'
    o5 = countPatterns(board, opp_symbol + ' ' + opp_symbol*2)  # '- --'
    # o6 = countPatterns(board, ' ' + opp_symbol*2 + ' ')         # ' -- '
    # o7 = countPatterns(board, opp_symbol*2 + '  ')              # '--  '
    # o8 = countPatterns(board, '  ' + opp_symbol*2)              # '  --'
    # o9 = countPatterns(board, opp_symbol + '  ' + opp_symbol)   # '-  -'
    o10 = countPatterns(board, opp_symbol*2)                    # '--' 
    o11 = countPatterns(board, opp_symbol*3)

    # pieces in the central column(s)
    center = width // 2 
    center_col = [board[i][center] for i in range(len(board))]
    pieces_center = center_col.count(symbol)
    opp_pieces_center = center_col.count(opp_symbol)
    
    # if width is even consider the two central columns
    if not width % 2:
        center2 = width // 2 - 1
        center_col2 = [board[i][center2] for i in range(len(board))]
        pieces_center += center_col2.count(symbol)
        opp_pieces_center += center_col2.count(opp_symbol)

    factor1     = 1000
    factor23    = 100
    factor45    = 100
    factor6     = 50
    factor789   = 20
    factor10    = 1
    factor11 = 50

    pattern_value = (
        # (p1-o1) * factor1 + 
        (p2+p3-o2-o3) * factor23 + 
        (p4+p5-o4-o5) * factor45 + 
        (p11 - o11) * factor11 +
        # (p6 - o6) * factor6
        # (p7+p8+p9-o7-o8-o9) * factor789 + 
        (p10-o10) * factor10
    )
    center_value = (pieces_center - opp_pieces_center) * 10
    return pattern_value + center_value


def monteCarlo(board: Iterable, has_next_move: Player, num_rollout: int):
    '''
    A heuristic that uses the Monte Carlo method to evalueate a board state.
    It is too slow for use in a Minimax algorithm though.
    '''

    def simulate(board, has_next_move: Player):
        player = has_next_move
        winner = checkWinner(board)
        while winner is None:
            moves = findAvailableMoves(board)
            move = random.choice(moves)
            board = makeMove(board, player, move)
            player = Player.X if player == Player.O else Player.O
            winner = checkWinner(board)
        return winner

    wins = 0
    for _ in range(num_rollout):
        winner = simulate(board, has_next_move)
        if winner == Player.X:
            wins += 1
    reward = int(round((wins/num_rollout) * 100 ))

    return reward