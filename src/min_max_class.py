import numpy as np
from games import TicTacToe
#from connect_four import ConnectFour

class MinMax:

    def __init__(self, game, game_name, player, level, state):
        self.game = game
        self.game_name = game_name
        self.player = player
        self.level = level
        self.state = state
        self.nodeDict, self.nodeSuccDict, self.nodeUtilDict, self.nodeMinMaxDict = {}, {}, {}, {}

    def min_node_util(self, node):
        if node in self.nodeUtilDict:
            self.nodeMinMaxDict[node] = self.nodeUtilDict[node]
            return self.nodeMinMaxDict[node]
        mmv = np.inf
        for s in self.nodeSuccDict[node]:
            mmv = min(mmv, self.max_node_util(s))
        self.nodeMinMaxDict[node] = mmv
        return mmv

    def max_node_util(self, node):
        if node in self.nodeUtilDict:
            self.nodeMinMaxDict[node] = self.nodeUtilDict[node]
            return self.nodeMinMaxDict[node]
        mmv = -np.inf
        for s in self.nodeSuccDict[node]:
            mmv = max(mmv, self.min_node_util(s))
        self.nodeMinMaxDict[node] = mmv
        return mmv

    def next_step_ttt(self, player, state, succ):
        rs, cs = np.where(state == 0)
        for j in range(rs.size):
            ss_copy = np.copy(state)
            ss_copy[rs[j], cs[j]] = player

            newnode = max(self.nodeDict.keys()) + 1
            self.nodeDict[newnode] = ss_copy

            succ.append(newnode)

    def next_step_connect4(self, player, state, succ):
        for i in range(7):  # enumerate all legal moves from this state
            if self.game.is_valid_move(state, i):  # if column is a legal move
                ss_copy = np.copy(state)
                self.game.make_move(ss_copy, player, i)

                newnode = max(self.nodeDict.keys()) + 1
                self.nodeDict[newnode] = ss_copy

                succ.append(newnode)

    def build_tree(self, state, player, node, level):
        succ = []

        # if state is not terminal: switch player & compute successors
        if level == 0 or self.game.move_was_winning_move(state, player):
            self.nodeUtilDict[node] = self.game.evaluation(state, player)
        else:
            player *= -1
            if self.game_name is 'ttt':
                self.next_step_ttt(player, state, succ)
            elif self.game_name is 'connect_four':
                self.next_step_connect4(player, state, succ)
            else:
                raise ValueError("Game name is not as expected!")

        self.nodeSuccDict[node] = succ

        for s in succ:
            self.build_tree(self.nodeDict[s], player, s, level - 1)

    def run_min_max(self):

        # build tree
        node = 0
        self.nodeDict[node] = self.state
        state, player, level = self.state, self.player, self.level
        self.build_tree(state, player, node, level)
        print(self.state)
        print(self.level)
        print(self.player)
        print(self.node)
        # as here 'player' is actually our opponent, we want his min
        mmv = self.min_node_util(node)
        for succ in self.nodeSuccDict[node]:
            print(self.nodeDict[succ])
        return next(self.nodeDict[succ] for succ in self.nodeSuccDict[node] if self.nodeMinMaxDict[succ] is mmv), mmv


if __name__ == '__main__':
    ttt = TicTacToe()
    state = np.array([
        [-1, 0, 1],
        [0, 1, 0],
        [0, 0, 0]
    ])
    player = 1
    level = 2
    minmax = MinMax(ttt, 'ttt', player, level, state)
    print minmax.run_min_max()
    connect4 = ConnectFour(7, 6)
    state = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, -1, 1, 0, 0, 0],
        [0, 0, -1, 1, 0, 0, 0]
    ])
    player = 1
    level = 2
    minmax = MinMax(connect4, 'connect_four', player, level, state)
    print minmax.run_min_max()
