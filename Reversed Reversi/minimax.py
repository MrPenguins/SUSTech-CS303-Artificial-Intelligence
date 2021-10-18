import numpy as np
import random
import time
import math

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
infinity = math.inf
chess_piece_points = 30
search_layers = 2

# @formatter:off
point_weight = np.array([
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1],
    [1, 1,  1,  1,  1,  1, 1, 1]
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
        next_positions = self.possible_positions(chessboard, self.color)
        highest_value = -infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], self.color)
            value = self.min_value(next_chessboard, search_layers)
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

    # 在指定位置下棋并翻转棋子，返回新的chessboard
    def flip_chess_pieces(self, chessboard, x, y, self_color):
        # 因为这个chessboard是传引用的，所以要弄个新的
        new_chessboard = chessboard.copy()
        # 在指定位置下棋
        new_chessboard[x][y] = self_color
        # 检查所有方向，翻转棋子
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

    # 评估函数
    def evaluate(self, chessboard, self_color) -> int:
        count = 0
        points = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == -self_color:
                    count += 1
                    # points += point_weight[i][j]
        points += count * chess_piece_points
        return points

    def max_value(self, chessboard, depth):
        current_color = self.color
        if depth == 0:
            return self.evaluate(chessboard, current_color)
        next_positions = self.possible_positions(chessboard, current_color)
        if len(next_positions) == 0:
            return self.min_value(chessboard, depth - 1)
        value = -infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], current_color)
            value = max(value, self.min_value(next_chessboard, depth - 1))
        return value

    def min_value(self, chessboard, depth):
        current_color = self.opposite_color
        if depth == 0:
            return self.evaluate(chessboard, current_color)
        next_positions = self.possible_positions(chessboard, current_color)
        if len(next_positions) == 0:
            return self.max_value(chessboard, depth - 1)
        value = infinity
        for position in next_positions:
            next_chessboard = self.flip_chess_pieces(chessboard, position[0], position[1], current_color)
            value = min(value, self.max_value(next_chessboard, depth - 1))
        return value
