import numpy as np


class TicTacToe:
    """ tic tac toe implementation"""

    def __init__(self):
        # relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
        self.symbols = {1: 'x', -1: 'o', 0: ' '}

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

    def execute(self):
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
            # print '%s moves' % name

            # let player move at random
            game_state, x, y = self.move_at_random(game_state, player)

            # print current game state
            # self.print_game_state(game_state)

            # evaluate game state
            if self.move_was_winning_move(game_state, player):
                # print 'player %s wins after %d moves' % (name, mvcntr)
                print '%s, %s, %s' % (name, x, y)
                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            print 'draw'

    def run(self, times):
        for i in range(times):
            self.execute()