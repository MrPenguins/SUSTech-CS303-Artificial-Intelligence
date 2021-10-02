import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


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
        self.candidate_list = self.possible_positions(chessboard)
        return self.candidate_list

    # Decide the possible positions for placing a chess
    def possible_positions(self, chessboard):
        positions = []
        for i in range(0, self.chessboard_size):
            for j in range(0, self.chessboard_size):
                if chessboard[i][j] == COLOR_NONE and self.check_legal(chessboard, i, j):
                    positions.append((i, j))
        return positions

    # Decide whether the current position is legal to place a chess piece
    def check_legal(self, chessboard, x, y):
        flag = False
        for direction in self.directions:
            possible_x = x + direction[0]
            possible_y = y + direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] == self.opposite_color:
                possible_x += direction[0]
                possible_y += direction[1]
                while 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size:
                    if chessboard[possible_x][possible_y] == self.opposite_color:
                        possible_x += direction[0]
                        possible_y += direction[1]
                    elif chessboard[possible_x][possible_y] == self.color:
                        flag = True
                        break
                    else:
                        break
                if flag:
                    break
        return flag
