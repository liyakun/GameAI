import time
import numpy as np
from min_max_class import MinMax


evaluationTable = [[3, 4, 5, 7, 5, 4, 3], 
                                          [4, 6, 8, 10, 8, 6, 4],
                                          [5, 8, 11, 13, 11, 8, 5], 
                                          [5, 8, 11, 13, 11, 8, 5],
                                          [4, 6, 8, 10, 8, 6, 4],
                                          [3, 4, 5, 7, 5, 4, 3]]

class ConnectFour:

    def __init__(self, columns=7, rows=6):
        self.size = {'c': columns, 'r': rows}  # 7 columns x 6 rows
        self.gameState = np.zeros((6, 7), dtype=int)
        self.player = 1
        self.mvcntr = 1
        self.noWinnerYet = True
        self.symbols = {1: 'x', -1: 'o', 0: ' '}
        self.boardwidth = columns

    def is_valid_move(self, S, column):
        if column < 0 or column >= self.boardwidth or S[0][column] != 0:
            return False
        return True

    def make_move(self, S, player, column):
        row = np.argmax(np.where(S[:, column] == 0))
        S[row][column] = player

    def move_still_possible(self, S):
        return 0 in S[0]

    def move_at_random(self, S, p):
        y = np.random.choice(np.where(S[0] == 0)[0])
        x = np.argmax(np.where(S[:,y] == 0))
        S[x,y] = p
        return S

    def move_desired(self, S, p, column):
        y = column
        x = np.argmax(np.where(S[:, y] == 0))
        S[x, y] = p
        return S

    def move_was_winning_move(self, S, p):
        # we do not need to check the sign of the largest stroke because we do
        # the check after our own move and only we can win here

        for r in S:
            tmp = [len(a) for a in np.split(r, np.where(np.diff(r) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) >= 4:
                return True

        for c in S.T:
            tmp = [len(a) for a in np.split(c, np.where(np.diff(c) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) >= 4:
                return True

        for k in range(-3,4):
            d = np.diag(S, k)
            tmp = [len(a) for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) >= 4:
                return True

        return False

    def check_for_streak(self, S, p, size):
        ctr = 0
        for r in S:
            ctr += sum([1 for a in np.split(r, np.where(np.diff(r) != 0)[0] + 1) if a[0] != 0 and len(a) == size])

        for c in S.T:
            ctr +=sum([1 for a in np.split(c, np.where(np.diff(c) != 0)[0] + 1) if a[0] == p and len(a) == size])

        for k in range(-3, 4):
            d = np.diag(S, k)
            ctr += sum([1 for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0 and len(a) == size])
        return ctr

    def move_min_max(self, S, p, depth):
        minmax = MinMax(ConnectFour(), 'connect_four', p * -1, depth, S)
        new_state, score = minmax.run_min_max()
        return new_state

    def evaluation(self, state, player):
        utility = 138
        sum = 0
        for i in range(6):
           for j in range(7):
               if (state[i][j] == 1):
                   sum += evaluationTable[i][j]
               elif (state[i][j] == -1):
                   sum -= evaluationTable[i][j]
        return utility + sum;

    # print game state matrix using symbols
    def print_game_state(self, S):
        B = np.copy(S).astype(object)
        for n in [-1, 0, 1]:
            B[B == n] = self.symbols[n]

    def execute(self):
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        # initialize flag that indicates win
        noWinnerYet = True
        game_state = self.gameState
        result = 0
        # game running
        while self.move_still_possible(game_state) and noWinnerYet:
            # get player symbol
            name = self.symbols[player]
            if player == 1:
                game_state = self.move_min_max(game_state, player, 3)
            else:
                game_state = self.move_at_random(game_state, player)

            # evaluate game state
            if self.move_was_winning_move(game_state, player):
                result = player
                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            print 'draw'

        return result

    def run(self, times):
        result = []
        for i in range(times):
            print '%i running' % i
            result.append(self.execute())

        print 'x win: %i, o win: %i, draw: %i' % (result.count(1), result.count(-1), result.count(0))
        
if __name__ == '__main__':
    start_time = time.time()
    ConnectFour().run(50)
    print("--- %s seconds ---" % (time.time() - start_time))
