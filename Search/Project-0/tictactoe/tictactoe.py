"""
Tic Tac Toe Player
"""

import math

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
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


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

    # Check rows for 3 in a row
    for row in board:
        if row == [X, X, X] or row == [O, O, O]:
            return True

    # Check columns for 3 in a column (now transposed to rows to facilitate checking)
    for row in [list(i) for i in zip(*board)]:
        if row == [X, X, X] or row == [O, O, O]:
            return True

    # Check diagonals for 3 in a diagonal
    diagonal = [board[0][0], board[1][1], board[2][2]]
    if diagonal == [X, X, X] or diagonal == [O, O, O]:
        return True

    diagonal = [board[0][2], board[1][1], board[2][0]]
    if diagonal == [X, X, X] or diagonal == [O, O, O]:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not terminal(board):
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
