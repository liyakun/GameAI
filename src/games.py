import numpy as np
import matplotlib.pyplot as plt


class Histogram:
    """ plot histogram on given x-y data """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def histogram(self):
        plt.bar(self.x, self.y, align='center')
        plt.xlabel('Results')
        plt.ylabel('Frequency')
        for i in range(len(self.y)):
            plt.hlines(self.y[i], 0, self.x[i])
        plt.show()

class TicTacToe:
    """ tic tac toe implementation"""

    def __init__(self):
        # relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
        self.symbols = {1: 'x', -1: 'o', 0: ' '}
        self.result = []
        self.x_board, self.o_board = np.zeros((3, 3), dtype=int), np.zeros((3, 3), dtype=int)
        self.Three_in_a_Row = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8],
                                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                                        [0, 4, 8], [2, 4, 6]])
        self.Heuristic_Array = [[0, -10, -100, -1000],
                                [10, 0, 0, 0],
                                [100, 0, 0, 0],
                                [1000, 0, 0, 0]]

    def evaluation(self, S, p):
        opponent = ' '
        if p is 'x':
            opponent = 'o'
        else:
            opponent = 'x'

        t = 0
        for i, items in enumerate(self.Three_in_a_Row):
            players, others = 0, 0
            for j, item in enumerate(items):
                piece = S[self.Three_in_a_Row[i][j] / 3][self.Three_in_a_Row[i][j] % 3]
                if piece == p:
                    players += 1
                elif piece == opponent:
                    others += 1
            t += self.Heuristic_Array[players][others]
        return t

    def move_still_possible(self, S):
        return not (S[S == 0].size == 0)

    def move_at_random(self, S, p):
        xs, ys = np.where(S == 0)
        i = np.random.permutation(np.arange(xs.size))[0]
        S[xs[i], ys[i]] = p
        return S, xs[i], ys[i]

    def move_was_winning_move(self, S, p):
        if np.max((np.sum(S, axis=0)) * p) == 3:
            return True

        if np.max((np.sum(S, axis=1)) * p) == 3:
            return True

        if (np.sum(np.diag(S)) * p) == 3:
            return True

        if (np.sum(np.diag(np.rot90(S))) * p) == 3:
            return True

        return False

    # print game state matrix using symbols
    def print_game_state(self, S):
        B = np.copy(S).astype(object)
        for n in [-1, 0, 1]:
            B[B == n] = self.symbols[n]
        print B

    # get the indices of max value in self.x_board, which is not occupied in S
    def indices_of_max_value(self, S):
        xs, ys = np.where(S == 0)
        max_v, max_p = -1, -1
        for index, item in enumerate(xs):
            if self.x_board[item][ys[index]] > max_v:
                max_v = self.x_board[item][ys[index]]
                max_p = index
        return xs[max_p], ys[max_p]

    # move to the position on the board
    def move_at_probability(self, S, p):
        px, py = self.indices_of_max_value(S)
        S[px, py] = p
        return S, px, py

    def move_at_heuristic(self, S, p):
        xs, ys = np.where(S == 0)
        ts = []
        for index, item in enumerate(xs):
            s_copy = S.copy()
            s_copy[xs[index], ys[index]] = p
            ts.append(self.evaluation(s_copy, p))
        index = np.argmax(np.array(ts))
        S[xs[index], ys[index]] = p
        return S, xs[index], ys[index]

    def execute(self, strategy_x):
        tmp = []
        # initialize 3x3 tic tac toe board
        game_state = np.zeros((3, 3), dtype=int)

        # initialize player number, move counter
        player = 1
        mvcntr = 1

        # initialize flag that indicates win
        noWinnerYet = True

        # game running
        while self.move_still_possible(game_state) and noWinnerYet:
            # get player symbol
            name = self.symbols[player]

            x, y = '', ''
            if name == 'x' and strategy_x == 'map':
                game_state, x, y = self.move_at_probability(game_state, player)
            elif name == 'x' and strategy_x == 'mah':
                game_state, x, y = self.move_at_heuristic(game_state, player)
            else:
                game_state, x, y = self.move_at_random(game_state, player)

            # evaluate game state
            if self.move_was_winning_move(game_state, player):
                tmp.extend([name, x, y])
                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            tmp.append('draw')
        return tmp

    def run(self, times, strategy):
        del self.result[:]
        for i in range(times):
            self.result.append(self.execute(strategy))

    def draw(self):
        fx, fo, fd = 0, 0, 0
        position_x, position_o = [], []
        for index, item in enumerate(self.result):
            if 'x' in item:
                fx += 1
                self.x_board[item[1]][item[2]] += 1
                position_x.append(item[-2:])
            elif 'o' in item:
                fo += 1
                self.o_board[item[1]][item[2]] += 1
                position_o.append(item[-2:])
            else:
                fd += 1
        print fx, fo, fd
        Histogram([1, 2, 3], [fx, fo, fd]).histogram()


