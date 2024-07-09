import numpy as np
import random as rd
import time

# Constants
ROWS = 6
COLUMNS = 7
IN_A_ROW = 4
TIME_LIMIT = 3
DEPTH_LIMIT = 5

# Transposition table to store heuristic scores
transposition_table = {}

def grid_to_bitboard(grid):
    """Convert the grid to a bitboard representation."""
    bitboard = np.array([0, 0], dtype=np.int64)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] != 0:
                bitboard[grid[row][col] - 1] ^= (1 << ((ROWS - 1) - row + col * COLUMNS))
    return bitboard

def bitboard_to_grid(bitboard):
    """Convert the bitboard to grid representation."""
    grid = np.zeros((ROWS, COLUMNS), dtype=np.int64)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if bitboard[0] & (1 << ((ROWS - 1) - row + col * COLUMNS)):
                grid[row][col] = 1
            elif bitboard[1] & (1 << ((ROWS - 1) - row + col * COLUMNS)):
                grid[row][col] = 2
    return grid

def get_height(grid):
    """Calculate the height of pieces in each column."""
    height = np.array([col * COLUMNS for col in range(COLUMNS)], dtype=np.int64)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if grid[row][col] != 0:
                height[col] += 1
    return height

def drop_piece(bitboard, height, col, piece):
    """Drop a piece into the bitboard."""
    bitboard[piece - 1] ^= (1 << height[col])
    height[col] += 1
    return bitboard, height

def remove_piece(bitboard, height, col, piece):
    """Remove a piece from the bitboard."""
    height[col] -= 1
    bitboard[piece - 1] ^= (1 << height[col])
    return bitboard, height

def check_window(window, discs, piece):
    """Check if a window meets the criteria."""
    return np.count_nonzero(window == piece) == discs and np.count_nonzero(window == 0) == IN_A_ROW - discs

def count_windows(grid, discs, piece):
    """Count the number of valid windows in the grid."""
    n_windows = 0
    for row in range(ROWS):
        for col in range(COLUMNS - IN_A_ROW + 1):
            window = grid[row, col:col + IN_A_ROW]
            if check_window(window, discs, piece):
                n_windows += 1
    for row in range(ROWS - IN_A_ROW + 1):
        for col in range(COLUMNS):
            window = grid[row:row + IN_A_ROW, col]
            if check_window(window, discs, piece):
                n_windows += 1
    for row in range(ROWS - IN_A_ROW + 1):
        for col in range(COLUMNS - IN_A_ROW + 1):
            window = grid[range(row, row + IN_A_ROW), range(col, col + IN_A_ROW)]
            if check_window(window, discs, piece):
                n_windows += 1
    for row in range(IN_A_ROW - 1, ROWS):
        for col in range(COLUMNS - IN_A_ROW + 1):
            window = grid[range(row, row - IN_A_ROW, -1), range(col, col + IN_A_ROW)]
            if check_window(window, discs, piece):
                n_windows += 1
    return n_windows

def get_heuristic(bitboard, piece):
    """Calculate the heuristic score of the bitboard."""
    grid = bitboard_to_grid(bitboard)
    score = 0
    score += 1e9 * count_windows(grid, IN_A_ROW - 0, piece)
    score -= 1e6 * count_windows(grid, IN_A_ROW - 0, (piece % 2) + 1)
    score += 1e3 * count_windows(grid, IN_A_ROW - 1, piece)
    score -= 1e0 * count_windows(grid, IN_A_ROW - 1, (piece % 2) + 1)
    return score

def is_draw(height):
    """Check if the state is a draw."""
    return all(height[col] == (ROWS + col * COLUMNS) for col in range(COLUMNS))

def is_terminal_bitboard(bitboard, piece):
    """Check if the state is terminal (win)."""
    board = bitboard[piece - 1]
    if (board & (board >> 1) & (board >> 2) & (board >> 3)) != 0:  # vertical
        return True
    if (board & (board >> 7) & (board >> 14) & (board >> 21)) != 0:  # horizontal
        return True
    if (board & (board >> 6) & (board >> 12) & (board >> 18)) != 0:  # diagonal \
        return True
    if (board & (board >> 8) & (board >> 16) & (board >> 24)) != 0:  # diagonal /
        return True
    return False

def is_terminal(bitboard):
    """Check if the state is terminal (win or loss)."""
    return is_terminal_bitboard(bitboard, 1) or is_terminal_bitboard(bitboard, 2)

def minimax(bitboard, height, depth, maximizing_player, piece, alpha, beta):
    """Minimax algorithm with alpha-beta pruning."""
    bitboard_tuple = tuple(bitboard)
    if bitboard_tuple in transposition_table:
        return transposition_table[bitboard_tuple]

    if depth == 0 or is_terminal(bitboard) or is_draw(height):
        score = get_heuristic(bitboard, piece)
        transposition_table[bitboard_tuple] = score
        return score

    valid_moves = [col for col in range(COLUMNS) if height[col] != (ROWS + col * COLUMNS)]
    rd.shuffle(valid_moves)

    if maximizing_player:
        max_eval = -np.inf
        for col in valid_moves:
            bitboard, height = drop_piece(bitboard, height, col, piece)
            eval = minimax(bitboard, height, depth - 1, False, piece, alpha, beta)
            bitboard, height = remove_piece(bitboard, height, col, piece)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        transposition_table[bitboard_tuple] = max_eval
        return max_eval
    else:
        min_eval = np.inf
        for col in valid_moves:
            bitboard, height = drop_piece(bitboard, height, col, (piece % 2) + 1)
            eval = minimax(bitboard, height, depth - 1, True, piece, alpha, beta)
            bitboard, height = remove_piece(bitboard, height, col, (piece % 2) + 1)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        transposition_table[bitboard_tuple] = min_eval
        return min_eval

def score_move(bitboard, height, depth, piece, col):
    """Score a potential move using minimax."""
    bitboard, height = drop_piece(bitboard, height, col, piece)
    score = minimax(bitboard, height, depth - 1, False, piece, -np.inf, np.inf)
    bitboard, height = remove_piece(bitboard, height, col, piece)
    return score

def play(bitboard, height, piece, valid_moves):
    """Play a move using iterative deepening."""
    start_time = time.time()
    max_depth, max_time = 1, 0
    while max_depth <= DEPTH_LIMIT and max_time <= TIME_LIMIT:
        transposition_table.clear()
        valid_moves = sorted(valid_moves, key=lambda col: score_move(bitboard, height, max_depth, piece, col), reverse=True)
        max_depth, max_time = max_depth + 1, time.time() - start_time
    return valid_moves[0]

def agent(observation, configuration):
    """Agent to play the game."""
    grid = np.asarray(observation['board'], dtype=np.int64).reshape(ROWS, COLUMNS)
    piece = observation['mark']
    bitboard = grid_to_bitboard(grid)
    height = get_height(grid)
    valid_moves = [col for col in range(COLUMNS) if height[col] != (ROWS + col * COLUMNS)]
    rd.shuffle(valid_moves)
    return play(bitboard, height, piece, valid_moves)