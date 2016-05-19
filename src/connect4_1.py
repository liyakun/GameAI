# Four-In-A-Row (a Connect Four clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, pygame
import numpy as np
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

DIFFICULTY = 2  # how many moves to look ahead. (>2 is usually too much)

SPACESIZE = 50  # size of the tokens and individual board spaces in pixels

FPS = 30  # frames per second to update the screen
WINDOWWIDTH = 640  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

BRIGHTBLUE = (0, 100, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'


def move_still_possible(S):
    return 0 in S[0]


def move_at_random(S, p):
    y = np.random.choice(np.where(S[0] == 0)[0])
    x = np.argmax(np.where(S[:, y] == 0))
    S[x, y] = p
    return S, y, x


# get the number of streak in block (i, 6) within column col
def vertical_streak(row, col, state, streak):
    consecutive_count = 0
    for i in range(row, 6):
        if state[i][col] == state[row][col]:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


# get the number of streak in block (j, 7) within row row
def horizontal_streak(row, col, state, streak):
    consecutive_count = 0
    for j in range(col, 7):
        if state[row][j] == state[row][col]:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


# get the number of streak in block (i, j) within diagonal
def diagonal_streak(row, col, state, streak):
    total = 0
    # check for diagonals with positive slope
    consecutive_count = 0
    j = col
    for i in range(row, 6):
        if j > 6:
            break
        elif state[i][j] == state[row][col]:
            consecutive_count += 1
        else:
            break
        j += 1

    if consecutive_count >= streak:
        total += 1

    # check for diagonals with negative slope
    consecutive_count = 0
    j = col
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif state[i][j] == state[row][col]:
            consecutive_count += 1
        else:
            break

        j += 1  # increment column when row is incremented

    if consecutive_count >= streak:
        total += 1

    return total


def check_four_streak(state, player, streak):
    count = 0
    # for each piece in the board
    for i in range(6):
        for j in range(7):
            # check the player number
            if state[i][j] == player:
                count += vertical_streak(i, j, state, streak)
                count += horizontal_streak(i, j, state, streak)
                count += diagonal_streak(i, j, state, streak)
    return count


def heuristic(state, player):
    opponent = player * -1

    my_fours = check_four_streak(state, player, 4)
    my_threes = check_four_streak(state, player, 3)
    my_twos = check_four_streak(state, player, 2)
    my_ones = check_four_streak(state, player, 1)
    opp_fours = check_four_streak(state, opponent, 4)
    opp_threes = check_four_streak(state, opponent, 3)
    opp_twos = check_four_streak(state, opponent, 2)
    print opp_fours, opp_threes, opp_twos

    if opp_fours > 0:
        return -100000
    else:
        return my_fours * 100000 + my_threes * 100 + my_twos * 10 + my_ones


def state_to_board(S):
    board = [['red' if item is 1 else 'black' if item is -1 else EMPTY for item in items] for items in S.tolist()]
    return map(list, map(None, *board))  # transpose the 2d list


def board_to_state(board):
    state = [[1 if item is 'red' else -1 if item is 'black' else 0 for item in items] for items in board]
    return np.transpose(np.array(state))


def search(depth, state, player):
    opponent = player * -1
    legal_moves = []
    for i in range(7):  # enumerate all legal moves from this state
        temp = state_to_board(state)
        if isValidMove(temp, i):  # if column is a legal move
            x = np.argmax(np.where(state[:, i] == 0))
            makeMove(temp, opponent, i, x)
            for i in range(len(temp)):
                for j in range(len(temp[0])):
                    if temp[i][j] == -1:
                        temp[i][j] = 'black'
                    elif temp[i][j] == 1:
                        temp[i][j] = 'red'
            legal_moves.append(board_to_state(temp))

    # if this node (state) is a terminal node or depth == 0
    if depth == 0 or len(legal_moves) == 0 or move_was_winning_move(state, player):
        return heuristic(state, player)  # return the heuristic value of node

    alpha = 99999999
    for child in legal_moves:
        if child is None:
            print "child == None (search)"
        alpha = min(alpha, search(depth-1, child, opponent))  # get the min of opponent's heuristic

    return alpha


def best_move(depth, state, player):
    opponent = player * -1
    legal_moves = {}
    for col in range(7):  # enumerate all legal moves
        temp = state_to_board(state)
        if isValidMove(temp, col):  # if column:col is a legal move`
            x = np.argmax(np.where(state[:, col] == 0))
            makeMove(temp, player, col, x)  # make the move in column:'col', row:'x' for current player
            for i in range(len(temp)):
                for j in range(len(temp[0])):
                    if temp[i][j] == -1:
                        temp[i][j] = 'black'
                    elif temp[i][j] == 1:
                        temp[i][j] = 'red'
            legal_moves[col] = search(depth-1, board_to_state(temp), player)  # get the min of opponent's heuristic
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


# set default search depth is DIFFICULTY
def move_min_max(S, p, depth):
    y = best_move(depth, S, p)
    x = np.argmax(np.where(S[:, y] == 0))
    S[x, y] = p
    return S, y, x


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

    for k in range(-3, 4):
        d = np.diag(S, k)
        tmp = [len(a) for a in np.split(d, np.where(np.diff(d) != 0)[0] + 1) if a[0] != 0]
        if len(tmp) > 0 and np.max(tmp) >= 4:
            return True

    return False


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1: 'x', -1: 'o', 0: ' '}


# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B == n] = symbols[n]
    print B


def main():
    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
    global BLACKTOKENIMG, BOARDIMG, HUMANWINNERIMG
    global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Four in a Row')

    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    REDTOKENIMG = pygame.image.load('4row_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('4row_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('4row_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

    HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
    COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
    TIEWINNERIMG = pygame.image.load('4row_tie.png')
    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    while True:
        runGame()


def runGame():

    if random.randint(0, 1) == 0:
        turn = COMPUTER
        player = 1
    else:
        turn = HUMAN
        player = -1
    mvcntr = 1
    noWinnerYet = True

    # Set up a blank board data structure.
    mainBoard = getNewBoard()
    matrixMainBoard = np.zeros((6, 7), dtype=int)
    first = -1

    # while True: # main game loop
    while move_still_possible(matrixMainBoard) and noWinnerYet:
        name = symbols[player]
        print '%s moves' % name
        if player == 1:
            matrixMainBoard, column, row = move_min_max(matrixMainBoard, player, 2)
        else:
            if first == -1 and matrixMainBoard[5][3] != 1:  # if human play first, then put the red in the central
                matrixMainBoard[5][3] = -1
                column, row = 3, 5
                first = 0
            else:
                matrixMainBoard, column, row = move_min_max(matrixMainBoard, player, 2)
        if player == -1:
            color = RED
        else:
            color = BLACK
        animateComputerMoving(mainBoard, column, row, color)
        makeMove(mainBoard, color, column, row)
    
        print_game_state(matrixMainBoard)

        # evaluate game state
        if move_was_winning_move(matrixMainBoard, player):
            print 'player %s wins after %d moves' % (player, mvcntr)
            if player == -1:
                winnerImg = HUMANWINNERIMG
            else:
                winnerImg = COMPUTERWINNERIMG
            noWinnerYet = False
        else:
            winnerImg = TIEWINNERIMG

        # switch player and increase move counter
        player *= -1
        mvcntr += 1

    while True:
        # Keep looping until player clicks the mouse or quits.
        drawBoard(mainBoard)
        DISPLAYSURF.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def makeMove(board, player, column, row):
    # lowest = getLowestEmptySpace(board, column)
    # if lowest != -1:
    board[column][row] = player


def drawBoard(board, extraToken=None):
    DISPLAYSURF.fill(BGCOLOR)

    # draw tokens
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:
                DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

    # draw the extra token
    if extraToken != None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # draw board over the tokens
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect)

    # draw the red and black tokens off to the side
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right


def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)
    return board


def animateDroppingToken(board, column, row, color):
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE
    dropSpeed = 1.0

    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()


def animateComputerMoving(board, column, row, color):
    if(color == BLACK):
        x = BLACKPILERECT.left
        y = BLACKPILERECT.top
    else:
        x = REDPILERECT.left
        y = REDPILERECT.top
    speed = 1.0
    # moving the black tile up
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = YMARGIN - SPACESIZE
    speed = 1.0
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    animateDroppingToken(board, column, row, color)


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def isValidMove(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


if __name__ == '__main__':
    main()
