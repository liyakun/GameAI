import numpy as np


def move_still_possible(S):
    return 0 in S[0]


def move_at_random(S, p):
    y = np.random.choice(np.where(S[0]==0)[0])
    x = np.argmax(np.where(S[:,y]==0))
    S[x,y] = p
    return S


def move_was_winning_move(S, p):
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


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B


if __name__ == '__main__':
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((6,7), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True

    # game running
    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        gameState = move_at_random(gameState, player)

        # print current game state
        print_game_state(gameState)

        # evaluate game state
        if move_was_winning_move(gameState, player):
            print 'player %s wins after %d moves' % (name, mvcntr)
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1

    if noWinnerYet:
        print 'game ended in a draw'
