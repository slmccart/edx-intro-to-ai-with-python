"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    num_X = 0
    num_O = 0

    for row in board:
        for column in row:
            if column == X:
                num_X += 1
            elif column == O:
                num_O += 1

    if num_O < num_X:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if not 0 <= i <= 2 or not 0 <= j <= 2:
        raise IndexError(f"Invalid index provided: {action}")

    if not board[i][j] == EMPTY:
        raise IndexError(f"The board space provided is already filled: {action}")
    new_board = copy.deepcopy(board)

    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for 3 in a row
    for row in board:
        if row == [X, X, X]:
            return X
        elif row == [O, O, O]:
            return O

    # Check columns for 3 in a column (now transposed to rows to facilitate checking)
    for row in [list(i) for i in zip(*board)]:
        if row == [X, X, X]:
            return X
        elif row == [O, O, O]:
            return O

    # Check diagonals for 3 in a diagonal
    diagonal = [board[0][0], board[1][1], board[2][2]]
    if diagonal == [X, X, X]:
        return X
    elif diagonal == [O, O, O]:
        return O

    diagonal = [board[0][2], board[1][1], board[2][0]]
    if diagonal == [X, X, X]:
        return X
    elif diagonal == [O, O, O]:
        return O

    # No winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if board is completely full
    found_empty_space = False
    for row in board:
        for column in row:
            if column == EMPTY:
                found_empty_space = True

    if not found_empty_space:
        return True

    return bool(winner(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who = winner(board)
    if who == X:
        return 1
    elif who == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    p = player(board)
    a = actions(board)
    optimal_action = None

    if p == X:
        optimal_val = -math.inf
        for action in a:
            val = min_value(result(board, action))
            if val > optimal_val:
                optimal_val = val
                optimal_action = action
    else:
        optimal_val = math.inf
        for action in a:
            val = max_value(result(board, action))
            if val < optimal_val:
                optimal_val = val
                optimal_action = action

    return optimal_action


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
