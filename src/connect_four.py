import numpy as np


class ConnectFour:
    
    def __init__(self, isAtRandom, columns = 7, rows = 6):
        self.size = {'c' : columns, 'r': rows} # 7 columns x 6 rows       
        self.gameState = np.zeros((6,7), dtype=int)
        self.player = 1
        self.mvcntr = 1
        self.noWinnerYet = True
        self.symbols = {1:'x', -1:'o', 0:' '}
        self.isAtRandom = isAtRandom


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


    def drop(self, column): # Drop a disc into a column
        if( self.isAtRandom ):
            self.gameState = self.move_at_random(self.gameState, self.player)
        else:
            # print(sum( self.gameState[:,column] == 0))
            if(sum( self.gameState[:,column] == 0) == 0):
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
        count = 0
        for r in S:
            ctr+= sum([1 for a in np.split(r, np.where(np.diff(r) != 0)[0] + 1) if a[0] != 0 and len(a) == size])

        for c in S.T:
            ctr+=sum([1 for a in np.split(c, np.where(np.diff(c) != 0)[0] + 1) if a[0] == p and len(a) == size])

        for k in range(-3,4):
            d = np.diag(S, k)
            ctr += sum([1 for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0 and len(a) == size])
        return count

    # print game state matrix using symbols
    def print_game_state(self, S):
        os.system([ 'clear', 'cls' ][ os.name == 'nt' ])
        print("I want to play a game o_O")
        print("")
        B = np.copy(S).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = symbols[n]
        print B
        print("")
