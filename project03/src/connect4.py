import time
import numpy as np
from min_max_class import MinMax
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


class EvaluationTable:

    def __init__(self, columns=7, rows=6):
        self.columns, self.rows = columns, rows
        self.evaluationTable = [[0 for col in range(self.columns)] for row in range(self.rows)]

    def vertical_check(self):
        for j in range(self.rows):
                if j+3 < self.rows:
                    for i in range(4):
                        for index, item in enumerate(self.evaluationTable[j+i]):
                            self.evaluationTable[j+i][index] += 1
                else:
                    break

    def horizontal_check(self):
        for j in range(self.columns):
                if j+3 < self.columns:
                    for i in range(4):
                        for row in self.evaluationTable:
                            row[j+i] += 1
                else:
                    break

    def diagonal_check(self):
        for row in range(self.rows):
            if row + 3 < self.rows:
                # check for diagonals with positive slope
                for col in range(self.columns):
                    if col + 3 < self.columns:
                        for i in range(4):
                            self.evaluationTable[row+i][col+i] += 1
                    else:
                        break
                # check for diagonals with negative slope
                for col in range(self.columns-1, -1, -1):
                    if col - 3 >= 0:
                        for i in range(4):
                            self.evaluationTable[row+i][col-i] += 1
                    else:
                        break

    def color_map(self, map):
        fig = plt.figure(figsize=(6, 3.2))

        ax = fig.add_subplot(111)
        ax.set_title('Board ')
        plt.imshow(map)
        ax.set_aspect('equal')

        cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical')
        plt.show()

    def evaluate_board(self):
        self.vertical_check()
        self.horizontal_check()
        self.diagonal_check()
        return self.evaluationTable

evaluate = EvaluationTable()
evaluationTable = evaluate.evaluate_board()
#for row in evaluationTable:
#    print row
#evaluate.color_map(evaluate.evaluationTable)

#evaluationTable = [[3, 4, 5, 7, 5, 4, 3], [4, 6, 8, 10, 8, 6, 4], [5, 8, 11, 13, 11, 8, 5], [5, 8, 11, 13, 11, 8, 5],
#                   [4, 6, 8, 10, 8, 6, 4], [3, 4, 5, 7, 5, 4, 3]]
#evaluate.color_map(np.array(oldTable))


class ConnectFour:

    def __init__(self, columns=7, rows=6):
        self.size = {'c': columns, 'r': rows}  # 7 columns x 6 rows
        self.gameState = np.zeros((6, 7), dtype=int)
        self.player = 1
        self.mvcntr = 1
        self.noWinnerYet = True
        self.symbols = {1: 'x', -1: 'o', 0: ' '}
        self.boardwidth = columns

    def box_plot_with_special_point(self, equal_list, equal_special_list, str_):
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        # plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')

        # get all the variance value w.r.t equal_list(random_list)
        randomDists = ['depth 2', 'depth 3', 'depth 4']

        y = np.transpose(np.array(equal_list)).mean(axis=0)
        x = np.array([i + 1 for i in range(y.size)])
        plt.plot(x, y, 'b-')
        bp_0 = ax.boxplot(equal_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        plt.setp(xticksNames, fontsize=12)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="median")
            else:
                median.set(color='#b2df8a', linewidth=2)

        dash_line = mlines.Line2D([], [], color='purple', label='mean', linestyle='--')
        median_line = mlines.Line2D([], [], color='#b2df8a', label='median', linestyle='-')
        ax.set_xlabel('Depth')
        ax.set_ylabel('Wining Frequency')
        ax.set_ylim([35, 55])
        # Put a legend below current axis
        f1 = plt.legend(handles=[dash_line, median_line], loc=2, prop={'size': 10})
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
        ax = plt.gca().add_artist(f1)
        plt.show()

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

        for k in range(-3, 4):
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
        new_state = minmax.run_min_max()
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

    def execute(self, depth=2):
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
                game_state = self.move_min_max(game_state, player, depth)
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

    def run(self, times, depth=2):
        result = []
        for i in range(times):
            result.append(self.execute(depth))

        print 'x win: %i, o win: %i, draw: %i' % (result.count(1), result.count(-1), result.count(0))
        return result.count(1)

    def experiment(self, times, running, depth):
        result_all = []
        #time_all = []
        for i in range(times):
            start_time = time.time()
            result_all.append(self.run(running, depth))
            #self.run(running, depth)
            #time_all.append(time.time() - start_time)
            print("--- %s seconds ---" % (time.time() - start_time))
        return result_all

if __name__ == '__main__':
    time2 = ConnectFour().experiment(5, 50, 2)
    time3 = ConnectFour().experiment(5, 50, 3)
    time4 = ConnectFour().experiment(5, 50, 4)
    ConnectFour().box_plot_with_special_point([time2, time3, time4], [], '')

