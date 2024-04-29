import math
import copy

X = "X"
O = "O"
EMPTY = None


# Returns starting state of the board.
def initial_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


# Returns player who has the next turn on a board.
def player(board):
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1

    if board == initial_state():
        return X
    if count % 2 == 1:
        return O
    else:
        return X


# Returns set of all possible actions (i, j) available on the board.
def actions(board):
    posActions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                posActions.add((i, j))
    return posActions


# Returns the board that results from making move (i, j) on the board.
def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid Action!")

    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


# Returns the winner of the game, if there is one.
def winner(board):
    # Rows
    for row in board:
        if all(tile == X for tile in row):
            return X
        elif all(tile == O for tile in row):
            return O

    # Columns
    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        elif all(board[row][col] == O for row in range(3)):
            return O

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # If no winner, return None
    return None


# Returns True if game is over, False otherwise.
def terminal(board):
    if winner(board) is not None:
        return True
    else:
        for row in board:
            if EMPTY in row:
                return False
        return True


# Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
def utility(board):
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


# Returns the optimal action for the current player on the board.
def minimax(board):
    if terminal(board):
        return None
    Max = -math.inf
    Min = math.inf

    if player(board) == X:
        return Max_Value(board, Max, Min)[1]
    else:
        return Min_Value(board, Max, Min)[1]


def Max_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None]

    v = -math.inf
    for action in actions(board):
        test = Min_Value(result(board, action), Max, Min)[0]
        Max = max(Max, test)
        if test > v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]


def Min_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None]

    v = math.inf
    for action in actions(board):
        test = Max_Value(result(board, action), Max, Min)[0]
        Min = min(Min, test)
        if test < v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]
