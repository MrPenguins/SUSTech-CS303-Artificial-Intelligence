import numpy as np
import random
import time
import math
import numba as nb

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
infinity = math.inf
chess_piece_points = -10
search_layers = 3
last_places = 10
mobility = 10
stability = 20

# @formatter:off
point_weight = np.array([
    # [500, -25, 10, 5, 5, 10, -25, 500],
    # [-25, -45, 1, 1, 1, 1, -45, -25],
    # [10, 1, 3, 2, 2, 3, 1, 10],
    # [5, 1, 2, 1, 1, 2, 1, 5],
    # [5, 1, 2, 1, 1, 2, 1, 5],
    # [10, 1, 3, 2, 2, 3, 1, 10],
    # [-25, -45, 1, 1, 1, 1, -45, -25],
    # [500, -25, 10, 5, 5, 10, -25, 500]
    [600, -50, 20, 10, 10, 20, -50, 600],
    [-50, -90,  3, -5, -5,  3, -90, -50],
    [ 20,   3,  5,  2,  2,  5,   3,  20],
    [ 10,  -5,  2,  1,  1,  2,  -5,  10],
    [ 10,  -5,  2,  1,  1,  2,  -5,  10],
    [ 20,   3,  5,  2,  2,  5,   3,  20],
    [-50, -90,  3, -5, -5,  3, -90, -50],
    [600, -50, 20, 10, 10, 20, -50, 600]
    # [-150, 20, -8, -6, -6, -8, 20, -150],
    # [20, 50, 4, 4, 4, 4, 50, 20],
    # [-8, 4, -6, -4, -4, -6, -4, -8],
    # [-6, 4, -4, 0, 0, 4, -4, -6],
    # [-6, 4, -4, 0, 0, 4, -4, -6],
    # [-8, 4, -6, -4, -4, -6, -4, -8],
    # [20, 50, 4, 4, 4, 4, 50, 20],
    # [-150, 20, -8, -6, -6, -8, 20, -150]
])
# @formatter:on


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.opposite_color = -color
        self.time_out = time_out
        self.candidate_list = []
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def go(self, chessboard):
        self.candidate_list.clear()
        chessboard = np.array(chessboard)
        next_positions = self.possible_positions(chessboard, self.color)
        highest_value = -infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], self.color)
            if len(np.where(chessboard == 0)[0]) <= last_places:
                value = self.min_value(next_chessboard, last_places, -infinity, infinity, True)
            else:
                value = self.min_value(next_chessboard, search_layers, -infinity, infinity, False)
            if value > highest_value:
                highest_value = value
                self.candidate_list.append(position)
            else:
                self.candidate_list.insert(0, position)
        return self.candidate_list

    # Decide the possible positions for placing a chess piece
    def possible_positions(self, chessboard, self_color) -> list:
        positions = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == COLOR_NONE and self.check_legal(chessboard, i, j, self_color):
                    positions.append((i, j))
        return positions

    # Decide whether the current position is legal to place a chess piece
    def check_legal(self, chessboard, x, y, self_color) -> bool:
        for direction in self.directions:
            possible_x = x + direction[0]
            possible_y = y + direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] != -self_color:
                continue
            while 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] == -self_color:
                possible_x += direction[0]
                possible_y += direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] == self_color:
                return True
        return False

    # ???????????????????????????????????????????????????chessboard
    def flip_chess_pieces(self, chessboard, x, y, self_color):
        # ????????????chessboard???????????????????????????????????????
        new_chessboard = chessboard.copy()
        # ?????????????????????
        new_chessboard[x][y] = self_color
        # ?????????????????????????????????
        for direction in self.directions:
            possible_x = x + direction[0]
            possible_y = y + direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] != -self_color:
                continue
            while 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] == -self_color:
                possible_x += direction[0]
                possible_y += direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] == self_color:
                while possible_x != x:
                    possible_x -= direction[0]
                    possible_y -= direction[1]
                    new_chessboard[possible_x][possible_y] = self_color
        return new_chessboard

    # ????????????
    def evaluate(self, chessboard) -> int:
        left_moves = len(np.where(chessboard == 0)[0])
        points = 0
        points += np.sum(chessboard * point_weight)
        points *= self.opposite_color
        # ?????????????????????????????????????????????????????????
        if left_moves > 10:
            points += len(np.where(chessboard == self.color)[0]) * chess_piece_points
        mobility_score = len(self.possible_positions(chessboard, self.opposite_color))
        points -= mobility_score
        # ?????????????????????????????????????????????
        if left_moves < 34:
            points += self.calculate_stability(chessboard)
        return points

    # ???????????????????????????
    def evaluate_greedy(self, chessboard) -> int:
        count = len(np.where(chessboard == self.color)[0])
        return count * chess_piece_points

    def max_value(self, chessboard, depth, alpha, beta, enable_greedy):
        current_color = self.color
        if depth == 0:
            if enable_greedy:
                return self.evaluate_greedy(chessboard)
            else:
                return self.evaluate(chessboard)
        next_positions = self.possible_positions(chessboard, current_color)
        if len(next_positions) == 0:
            return self.min_value(chessboard, depth - 1, alpha, beta, enable_greedy)
        value = -infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], current_color)
            value = max(value, self.min_value(next_chessboard, depth - 1, alpha, beta, enable_greedy))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, chessboard, depth, alpha, beta, enable_greedy):
        current_color = self.opposite_color
        if depth == 0:
            if enable_greedy:
                return self.evaluate_greedy(chessboard)
            else:
                return self.evaluate(chessboard)
        next_positions = self.possible_positions(chessboard, current_color)
        if len(next_positions) == 0:
            return self.max_value(chessboard, depth - 1, alpha, beta, enable_greedy)
        value = infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], current_color)
            value = min(value, self.max_value(next_chessboard, depth - 1, alpha, beta, enable_greedy))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    # ????????????????????????
    def calculate_stability(self, chessboard) -> int:
        count_self = 0
        count_opposite = 0
        if len(np.where(chessboard[0] == 0)[0]) == 0:
            count_self += len(np.where(chessboard[0] == self.color)[0])
            count_opposite += len(np.where(chessboard[0] == self.opposite_color)[0])
        if len(np.where(chessboard[7] == 0)[0]) == 0:
            count_self += len(np.where(chessboard[7] == self.color)[0])
            count_opposite += len(np.where(chessboard[7] == self.opposite_color)[0])
        if len(np.where(chessboard[:, 0] == 0)[0]) == 0:
            count_self += len(np.where(chessboard[:, 0] == self.color)[0])
            count_opposite += len(np.where(chessboard[:, 0] == self.opposite_color)[0])
        if len(np.where(chessboard[:, 7] == 0)[0]) == 0:
            count_self += len(np.where(chessboard[:, 7] == self.color)[0])
            count_opposite += len(np.where(chessboard[:, 7] == self.opposite_color)[0])

        return count_self * stability * (-1) + count_opposite * stability
