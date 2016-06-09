import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from min_max_class import MinMax

class Histogram:
    """ plot histogram on given x-y data """

    def __init__(self, y):
        self.y = y
        self.s = pd.Series(y, index=['x', 'o', 'draw'])
        self.my_colors = 'rgb'

    def histogram(self, title):
        fig = plt.figure(1, figsize=(14, 14))
        ax = fig.add_subplot(111)
        ax.set_xlabel(title)
        ax.set_ylabel('Win Frequency')
        ax.set_ylim([0, 1000])
        self.s.plot(kind='bar', color=self.my_colors)
        fig.savefig("../results/task1.2/" + title)
        plt.close()


class TicTacToe:
    """ tic tac toe implementation """

    def __init__(self):
        # relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
        self.symbols = {1: 'x', -1: 'o', 0: ' '}
        self.result = []
        # x_board and o_board hold the win information after 1000 runs
        self.x_board, self.o_board = np.zeros((3, 3), dtype=float), np.zeros((3, 3), dtype=float)
        # hold all the three in a line information
        self.Three_in_a_Row = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8],
                                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                                        [0, 4, 8], [2, 4, 6]])
        # heuristic array
        self.Heuristic_Array = [[0, -10, -100, -1000],
                                [10, 0, 0, 0],
                                [100, 0, 0, 0],
                                [1000, 0, 0, 0]]
        self.nodeDict, self.succDict = {}, {}
        self.strategy = ''

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

    # get the indices of max value in board, which is not occupied in S
    def indices_of_max_value(self, S, board):
        xs, ys = np.where(S == 0)
        max_v, max_p = -1, -1
        for index, item in enumerate(xs):
            if board[item][ys[index]] > max_v:
                max_v = board[item][ys[index]]
                max_p = index
        return xs[max_p], ys[max_p]

    # move to the position based on values the x_board
    def move_at_probability_x_board(self, S, p):
        px, py = self.indices_of_max_value(S, self.x_board)
        S[px, py] = p
        return S, px, py

    # move to the position based on values on the board = x_board + o_board
    def move_at_probability_whole_board(self, S, p):
        px, py = self.indices_of_max_value(S, np.add(self.x_board, self.o_board))
        S[px, py] = p
        return S, px, py

    # evaluation function
    def evaluation(self, S, p):
        opponent = p * -1
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

    def move_at_heuristic(self, S, p):
        xs, ys = np.where(S == 0)
        ts = []
        for index, item in enumerate(xs):
            s_copy = S.copy()
            s_copy[xs[index], ys[index]] = p
            ts.append(self.evaluation(s_copy, p))
        # get the index of max t value
        index = np.argmax(np.array(ts))
        S[xs[index], ys[index]] = p
        return S, xs[index], ys[index]

    def move_at_heuristic_forward(self, S, p):
        opponent = p * -1
        xs, ys = np.where(S == 0)
        ts, heuristic, best, tmp = [], float("-INF"), 0, 0
        for index, item in enumerate(xs):
            s_copy = S.copy()
            s_copy[xs[index], ys[index]] = p
            utility = self.evaluation(s_copy, p)

            # find the worst your opponent could do
            worst = float("-INF")
            xs_, ys_ = np.where(s_copy == 0)
            for index_, item_ in enumerate(xs_):
                s_copy_ = s_copy
                s_copy_[xs_[index_], ys_[index_]] = opponent
                tmp = self.evaluation(s_copy_, opponent)
                if tmp > worst :
                    worst = tmp

            if worst == float("-INF"):
                worst = 0

            utility -= worst
            if utility > heuristic: # heuristic keep the largest utility value
                heuristic = utility
                best = index

        S[xs[best], ys[best]] = p
        return S, xs[best], ys[best]

    def move_min_max(self, state, player, level):
        minmax = MinMax(TicTacToe(), 'ttt', player * -1, level, state)
        new_state, score = minmax.run_min_max()
        xs, ys = np.nonzero(np.subtract(state, new_state))  # get new added position
        return new_state, xs[0], ys[0]

    def execute(self, strategy_x):
        tmp = []
        moves_in_each_game_x = []
        moves_in_each_game_o = []

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
            if name == 'x' and strategy_x == 'move at probability x_board':
                game_state, x, y = self.move_at_probability_x_board(game_state, player)
            elif name == 'x' and strategy_x == 'move at probability x_o_board':
                game_state, x, y = self.move_at_probability_whole_board(game_state, player)
            elif name == 'x' and strategy_x == 'move at heuristic':
                game_state, x, y = self.move_at_heuristic(game_state, player)
            elif name == 'x' and strategy_x == 'move at heuristic forward':
                game_state, x, y = self.move_at_heuristic(game_state, player)
            else:
                game_state, x, y = self.move_min_max(game_state, player, 3)

            moves = [x, y]
            if( name == 'x'):
                moves_in_each_game_x.append(moves)
            else:
                moves_in_each_game_o.append(moves)

            # evaluate game state
            if self.move_was_winning_move(game_state, player):
                if( name == 'x'):
                    tmp.extend([name, moves_in_each_game_x])
                else:
                    tmp.extend([name, moves_in_each_game_o])
                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            tmp.append('draw')
        return tmp

    def run(self, times, strategy):
        del self.result[:]  # every time before another run, clean previous results
        self.strategy = strategy
        for i in range(times):
            self.result.append(self.execute(strategy))

    def draw(self, is_board_positions_save):
        fx, fo, fd = 0, 0, 0
        for index, item in enumerate(self.result):
            if 'x' in item:
                fx += 1
                if( is_board_positions_save ):
                    for taken_position in item[1]:
                        self.x_board[taken_position[0]][taken_position[1]] += 1
            elif 'o' in item:
                fo += 1
                if( is_board_positions_save ):
                    for taken_position in item[1]:
                        self.o_board[taken_position[0]][taken_position[1]] += 1
            else:
                fd += 1
        print fx, fo, fd

        # Normalize arrays
        
        x_board_sum = np.sum(self.x_board)
        self.x_board = self.x_board / float(x_board_sum)
        
        np.savetxt('x_board.txt', self.x_board )

        o_board_sum = np.sum(self.o_board)
        self.o_board = self.o_board / float(o_board_sum)        
        np.savetxt('o_board.txt', self.o_board )

        Histogram([fx, fo, fd]).histogram(self.strategy)

