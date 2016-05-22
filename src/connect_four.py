import numpy as np
import os, random

class ConnectFour:

    #0 is random, 1 is DeepAI, 2 is manual
    def __init__(self, columns = 7, rows = 6, gameType=None):
        self.size = {'c' : columns, 'r': rows} # 7 columns x 6 rows
        self.gameState = np.zeros((6,7), dtype=int)
        self.player = 1
        self.mvcntr = 1
        self.noWinnerYet = True
        self.symbols = {1:'x', -1:'o', 0:' '}
        self.gameType = gameType
        self.symbols = {1: 'x', -1: 'o', 0: ' '}
        self.boardwidth = columns

    def is_valid_move(self, S, column):
        if column < 0 or column >= (self.boardwidth) or S[0][column] != 0:
            return False
        return True

    def make_move(self, S, player, column):
        row = np.argmax(np.where(S[:, column] == 0))
        S[row][column] = player


    def move_still_possible(self, S):
        return 0 in S[0]

    def update_player(self):
        self.player *= (-1)

    def move_at_random(self, S, p):
        y = np.random.choice(np.where(S[0]==0)[0])
        x = np.argmax(np.where(S[:,y]==0))
        S[x,y] = p
        return S

    def move_desired(self, S, p, column):
        y = column
        x = np.argmax(np.where(S[:,y]==0))
        S[x,y] = p
        return S

    def drop(self, column):  # Drop a disc into a column
        if self.gameType == 0:
            self.gameState = self.move_at_random(self.gameState, self.player)
        elif self.gameType ==1:
            self.gameState = self.move_min_max(self.gameState, self.player, 2)
        else:
            # print(sum( self.gamestate[:,column] == 0))
            if sum(self.gameState[:,column] == 0) == 0:
                return False
            self.gameState = self.move_desired(self.gameState, self.player, column)

        return True

    def move_was_winning_move(self, S, p):
        # we do not need to check the sign of the largest stroke because we do
        # the check after our own move and only we can win here

        for r in S:
            tmp = [len(a) for a in np.split(r, np.where(np.diff(r) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) == 4:
                return True

        for c in S.T:
            tmp = [len(a) for a in np.split(c, np.where(np.diff(c) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) == 4:
                return True

        for k in range(-3,4):
            d = np.diag(S, k)
            tmp = [len(a) for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) == 4:
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

    def search(self, depth, state, player):
        opponent = player * -1
        legal_moves = []
        for i in range(7):  # enumerate all legal moves from this state
            if self.is_valid_move(state, i):  # if column is a legal move
                s_copy = np.copy(state)
                self.make_move(s_copy, player, i)
                legal_moves.append(s_copy)

        # if this node (state) is a terminal node or depth == 0
        if depth == 0 or len(legal_moves) == 0 or self.move_was_winning_move(state, player):
            return self.evaluation(state, player)  # return the heuristic value of node

        alpha = 99999999
        for child in legal_moves:
            if child is None:
                print "child == None (search)"
            alpha = min(alpha, self.search(depth - 1, child, opponent))  # get the min of opponent's heuristic

        return alpha

    def best_move(self, depth, state, player):
        opponent = player * -1
        legal_moves = {}
        for col in range(7):  # enumerate all legal moves
            if self.is_valid_move(state, col):  # if column:col is a legal move`
                s_copy = np.copy(state)
                self.make_move(s_copy, player, col)
                legal_moves[col] = self.search(depth - 1, s_copy, player)  # get the min of opponent's heuristic
        best_alpha = -99999999
        best_move_ = None
        moves = legal_moves.items()
        print moves
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move_ = move
        return best_move_  # return the column for best move

    def move_min_max(self, S, p, depth):
        y = self.best_move(depth, S, p)
        x = np.argmax(np.where(S[:, y] == 0))
        S[x, y] = p
        return S, y

    def evaluation(self, state, player):
        opponent = player * -1
        my_fours = self.check_for_streak(state, player, 4)
        my_threes = self.check_for_streak(state, player, 3)
        my_twos = self.check_for_streak(state, player, 2)
        my_ones = self.check_for_streak(state, player, 1)
        opp_fours = self.check_for_streak(state, opponent, 4)
        opp_threes = self.check_for_streak(state, opponent, 3)
        opp_twos = self.check_for_streak(state, opponent, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos * 10

    # print game state matrix using symbols
    def print_game_state(self, S):
        os.system([ 'clear', 'cls' ][ os.name == 'nt' ])
        print("I want to play a game o_O")
        print("")
        B = np.copy(S).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = self.symbols[n]
        print B
        print("")
