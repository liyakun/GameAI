import numpy as np
import os, random
from min_max_class import MinMax
import sys

class Helper:
    @staticmethod
    def check_for_streak(S, p, size):
        ctr = 0
        for r in S:
            ctr += sum([1 for a in np.split(r, np.where(np.diff(r) != 0)[0] + 1) if a[0] != 0 and len(a) == size])

        for c in S.T:
            ctr +=sum([1 for a in np.split(c, np.where(np.diff(c) != 0)[0] + 1) if a[0] == p and len(a) == size])

        for k in range(-3, 4):
            d = np.diag(S, k)
            ctr += sum([1 for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0 and len(a) == size])
        return ctr

    @staticmethod
    def is_valid_move(S, column):
        assert(column >= 0)
        #not sure if we need to check bigger than board size
        return S[0][column] == 0
    
    @staticmethod
    def move_was_winning_move(S, p):
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

        for k in range(-4,4):
            d = np.diag(S, k)
            tmp = [len(a) for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0]
            if len(tmp) > 0 and np.max(tmp) >= 4:
                return True

        return False
    
    @staticmethod
    def make_move(S, player, column):
        row = np.argmax(np.where(S[:, column] == 0))
        S[row][column] = player
    
    @staticmethod
    def evaluation(state, player):
        opponent = player * -1
        my_fours = Helper.check_for_streak(state, player, 4)
        my_threes = Helper.check_for_streak(state, player, 3)
        my_twos = Helper.check_for_streak(state, player, 2)
        my_ones = Helper.check_for_streak(state, player, 1)
        opp_fours = Helper.check_for_streak(state, opponent, 4)
        opp_threes = Helper.check_for_streak(state, opponent, 3)
        opp_twos = Helper.check_for_streak(state, opponent, 2)

        my_fives = Helper.check_for_streak(state, player, 5)
        my_sixes = Helper.check_for_streak(state, player, 6)
        opp_fives = Helper.check_for_streak(state, opponent, 5)
        opp_sixes = Helper.check_for_streak(state, opponent, 6)

        my_score = (my_fours + my_fives + my_sixes) * 100000 + my_threes * 100 + my_twos * 10 + my_ones
        opp_score = (opp_fours + opp_fives + opp_sixes) * 100000 + opp_threes * 100 + opp_twos * 10 

        if opp_fours > 0 or opp_fives > 0 or opp_sixes > 0:
            return -100000
        else:
            return -my_score + opp_score

class Player:
    def __init__(self, id, type='random'):
        self.id = id
        #random/optimal/manual
        self.type = type
    
    def is_valid_move(self, state, col):
        return 0 == state[0][col]

    def move(self, S, c=None):
        if self.type == 'random':
            self.move_random(S)
        elif self.type == 'heuristic':
            self.move_heuristic(S)
        elif self.type == 'manual':
            self.move_manual(S,c)
        elif self.type == 'minmax':
            self.move_minmax(S)
        else:
            print('Unknown Player Type')
            assert(False)

    def move_minmax(self, S):
        minmax = MinMax(Helper, 'connect_four', (-1)*self.id, 2, S)
        S_temp = minmax.run_min_max()
        subtracted = np.subtract(S_temp, S)
        np.nonzero( subtracted )
        S[np.nonzero( subtracted )] = self.id


    def move_heuristic(self, S):
        depth=1
        y = self.best_move(depth, S)
        x = np.argmax(np.where(S[:, y] == 0))
        S[x, y] = self.id

    def move_random(self, S):
        y = np.random.choice(np.where(S[0]==0)[0])
        x = np.argmax(np.where(S[:,y]==0))
        S[x,y] = self.id
    
    def move_manual(self, S, column):
        y = column
        x = np.argmax(np.where(S[:,y]==0))
        S[x,y] = self.id
    def best_move(self, depth, state):
        opponent = self.id * -1
        legal_moves = {}
        for col in range(7):  # enumerate all legal moves
            if self.is_valid_move(state, col):  # if column:col is a legal move`
                s_copy = np.copy(state)
                x = np.argmax(np.where(s_copy[:,col]==0))
                s_copy[x,col]=self.id
                legal_moves[col] = self.search(depth - 1, s_copy, self.id)  # get the min of opponent's heuristic
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



    def search(self, depth, state, player):
        opponent = player * -1
        legal_moves = []
        for i in range(7):  # enumerate all legal moves from this state
            if self.is_valid_move(state, i):  # if column is a legal move
                s_copy = np.copy(state)
                x = np.argmax(np.where(s_copy[:,i]==0))
                s_copy[x,i]=self.id
                legal_moves.append(s_copy)

        # if this node (state) is a terminal node or depth == 0
        if depth == 0 or len(legal_moves) == 0 or Helper.move_was_winning_move(state, player):
            return Helper.evaluation(state, player)  # return the heuristic value of node

        alpha = 99999999
        for child in legal_moves:
            if child is None:
                print "child == None (search)"
            alpha = min(alpha, self.search(depth - 1, child, opponent))  # get the min of opponent's heuristic

        return alpha

class ConnectFour:
    #0 is random, 1 is DeepAI, 2 is manual
    def __init__(self, columns = 7, rows = 6, p1type='random', p2type='random'):
        self.size = {'c' : columns, 'r': rows} # 7 columns x 6 rows
        self.gameState = np.zeros((6,7), dtype=int)

        self.player = 1
        self.mvcntr = 1
        self.noWinnerYet = True
        self.symbols = {1:'x', -1:'o', 0:' '}
        self.boardwidth = columns
        self.p1 = Player(1, p1type)
        self.p2 = Player(-1, p2type)



    def move_still_possible(self, S):
        return 0 in S[0]

    def drop(self, c=None):  # Drop a disc into a column
        if self.player == (1):
            self.p1.move(self.gameState, c)
        else:
            self.p2.move(self.gameState, c)
        return True

    def update_player(self):
        self.player = -1*self.player

    def search(self, depth, state, player):
        opponent = player * -1
        legal_moves = []
        for i in range(7):  # enumerate all legal moves from this state
            if self.is_valid_move(state, i):  # if column is a legal move
                s_copy = np.copy(state)
                self.make_move(s_copy, player, i)
                legal_moves.append(s_copy)

        # if this node (state) is a terminal node or depth == 0
        if depth == 0 or len(legal_moves) == 0 or Helper.move_was_winning_move(state, player):
            return Helper.evaluation(state, player)  # return the heuristic value of node

        alpha = 99999999
        for child in legal_moves:
            if child is None:
                print "child == None (search)"
            alpha = min(alpha, self.search(depth - 1, child, opponent))  # get the min of opponent's heuristic

        return alpha

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
