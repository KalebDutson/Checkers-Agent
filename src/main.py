import random, pygame, sys, math
from pygame.locals import *
import time
from Board import *
from Checker import Checker
from CheckersPlayer import CheckersPlayer
from Move import Move

# A global constant for controlling debug prints
DEBUG = True

FPS = 10
# if you change the window height or width, you will need to recalculate the value for cell size
WINDOWWIDTH = 900
WINDOWHEIGHT = 720
# cell size makes the actual board 720x720. Allows for extra black space in window for messages
CELLSIZE = 90

# RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
# Calculate width and height for a 8x8 board
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

REAL_WHITE = (255, 255, 255)
BRIGHT_RED = (255, 0, 0)
BGCOLOR = (50, 50, 50)
BLACK = (0, 0, 0)
GRAY = pygame.Color("#f9f9f9")
RED = pygame.Color('#9c5359')
WHITE = pygame.Color('#d3bba2')

# when true, allows for adding an removing of checkers with mouse
TEST_MODE = False
# When true, both players are AI and move as fast as possible.
# Good for debugging.
AUTO_PLAY = False

def autoPlay(humanPlayer, agentPlayer, turn):
    player = humanPlayer if turn == 'r' else agentPlayer
    opponent = humanPlayer if turn == 'w' else agentPlayer
    if not player.defeated():
        player.executeBestMove(opponent)
    return 'r' if turn == 'w' else 'w'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BG_BOARD, RED_PIECE, RED_KING, WHITE_PIECE, WHITE_KING

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Checkers')

    BG_BOARD = pygame.image.load('../imgs/720x720_board.png')
    RED_PIECE = pygame.image.load('../imgs/red_piece.png').convert_alpha()
    RED_KING = pygame.image.load('../imgs/red_king.png').convert_alpha()
    WHITE_PIECE = pygame.image.load('../imgs/white_piece.png').convert_alpha()
    WHITE_KING = pygame.image.load('../imgs/white_king.png').convert_alpha()

    while True:
        msg, autoPlay = runGame()
        showGameOverScreen(msg, autoPlay)

def runGame():
    global TEST_MODE
    global AUTO_PLAY
    # A number of frames to be skipped before the next auto play turn is taken.
    # This makes the game visible for humans.
    autoPlayDelay = 0

    board = Board()

    humanPlayer = CheckersPlayer(board, red=True, human=True)
    agentPlayer = CheckersPlayer(board, red=False, human=False)

    # can be value 'w' or 'r'
    turn = 'r'
    # updated to true if the human or agent makes a move. Updates the turn at the end of event loop
    turnOver = False
    # number of millis the agent has to wait before moving a piece
    turnDelay = 700

    # selected checker of the human player
    selected = None
    highlightMoves = []

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()

            # test mode event handling
            if TEST_MODE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # right mouse click - add a WHITE checker
                    if event.button == 3:
                        point = getPointAtMouse()
                        # don't compute clicks outside board
                        if board.onBoard(point):
                            piece = board[point]
                            # add piece on empty square
                            if not board.occupied(point):
                                board.addChecker(Checker(point.x, point.y, False))
                            # remove piece on second click
                            elif not piece.red:
                                board.remove(point)

                    # left mouse click - add a RED checker
                    elif event.button == 1:
                        point = getPointAtMouse()
                        # don't compute clicks outside board
                        if point.x < 8 and point.y < 8:
                            piece = board[point]
                            # add piece on empty square
                            if piece is None:
                                board.addChecker(Checker(point.x, point.y, True))
                                # remove piece on second click
                            elif piece.red:
                                board.remove(point)

                    # middle mouse click - display info of checker at mouse
                    elif event.button == 2:
                        point = getPointAtMouse()
                        if board.onBoard(point):
                            if board.occupied(point):
                                checker = board[point]
                                print('Checker Info')
                                print('Pos: %s | Player: %s | King: %s' % (
                                    str(checker.position),
                                    'Red' if checker.red else 'White',
                                    checker.kinged
                                ))
                            else:
                                print('No checker here')

                elif event.type == KEYDOWN:
                    # switch turn
                    if event.key == K_RETURN:
                        turn = 'r' if turn == 'w' else 'w'
                    # Toggle auto play
                    elif event.key == K_a:
                        AUTO_PLAY = not AUTO_PLAY
                    # reset board
                    elif event.key == K_r:
                        board.reset()
                    # clear board of all pieces
                    elif event.key == K_c:
                        board.clear()
                    # king / un-king the piece at the mouse location
                    elif event.key == K_k:
                        point = getPointAtMouse()
                        if board.onBoard(point):
                            if board.occupied(point):
                                checker = board[point]
                                if checker.kinged:
                                    checker.deKing()
                                else:
                                    checker.becomeKing()
                    elif event.key == K_p:
                        point = getPointAtMouse()
                        # only check squares on board
                        if point.x < 8 and point.y < 8:
                            if board.occupied(point):
                                checker = board[point]
                                moves = checker.calculateMoves(board)
                                pieceString = ("red %s" if checker.red else "white %s") % ("king" if checker.kinged else "piece")
                                print("Moves for %s at %s%s:" % (pieceString, "ABCDEFGH"[checker.position.x], checker.position.y))
                                print([str(m) for m in moves])
                    # execute the best move for player of current turn
                    elif event.key == K_SPACE:
                        turn = autoPlay(humanPlayer, agentPlayer, turn)

                    elif event.key == K_b:
                        print('Board:')
                        print(board)

                    # Reset the board
                    elif event.key == K_r:
                        board.reset()

            elif not TEST_MODE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = getPointAtMouse()
                    # left mouse button
                    if event.button == 1 and turn == 'r' and board.onBoard(point):
                        # human player selects a checker at the mouse location
                        if board.occupied(point):
                            if board[point].red:
                                highlightMoves = []
                                # if checker clicked is not currently selected
                                if selected != board[point]:
                                    # select checker at point
                                    selected = board[point]
                                    moves = selected.calculateMoves(board)
                                    # moves is unpacked by default so this is inclusive
                                    # of all move options.
                                    highlightMoves += moves

                                # unselect selected checker
                                else:
                                    selected = None

                        # move or jump human player's checker to empty square
                        else:
                            validMove = None

                            # check if human clicked a valid move
                            for m in highlightMoves:
                                if point.x == m.dst.x and point.y == m.dst.y:
                                    validMove = m
                                    break
                            # Move selected checker and end turn
                            if validMove and selected is not None:
                                highlightMoves = []
                                humanPlayer.moveChecker(selected, validMove)
                                selected = None
                                turnOver = True

            if event.type == KEYDOWN:
                # activate test mode
                if event.key == K_t:
                    TEST_MODE = not TEST_MODE
                # end game
                elif event.key == K_q:
                    return
                # exit game
                elif event.key == K_ESCAPE:
                    terminate()

        # Allow agent to play on White player's turn
        if turn == 'w' and not TEST_MODE and not AUTO_PLAY:
            assert not agentPlayer.defeated()
            # wait before executing agent's turn
            pygame.time.delay(turnDelay)
            agentPlayer.executeBestMove(humanPlayer)
            turnOver = True

        # switch turn to other player
        if turnOver:
            turn = endTurn(turn)
            turnOver = False

        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(BG_BOARD, (0, 0))
        drawHighlightPoints(highlightMoves, selected)
        drawMsgTitle()
        drawStatus(turn, board)
        drawBoardState(board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        # Determine if game is over
        # return game state upon game end
        gom = gameOverMsg(humanPlayer, agentPlayer, turn)
        if gom is not None and not TEST_MODE:
            return gom, AUTO_PLAY
        
        if AUTO_PLAY:
            if autoPlayDelay > 0:
                autoPlayDelay -= 1
            else:
                turn = autoPlay(humanPlayer, agentPlayer, turn)            
                autoPlayDelay = 2

# Return a message for who won
# Returns None if a tie or win is not found
# Assumes that the human player is RED and the agent player is WHITE
# turn is required to avoid giving a game over message before a final
# move has been played.
def gameOverMsg(human, agent, turn):
    msg = None
    if human.defeated() and agent.defeated():
        msg = 'Illegal'
    elif human.defeated():
        msg = 'White Wins'
    elif agent.defeated():
        msg = 'Red Wins'
    elif not human.canMove() and not agent.canMove():
        msg = 'Draw'
    return msg

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, BRIGHT_RED)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 75)
    titleSurf1 = titleFont.render('Checkers', True, WHITE, RED)

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        rect1 = titleSurf1.get_rect()
        rect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(titleSurf1, rect1)
        drawPressKeyMsg()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def terminate():
    pygame.quit()
    sys.exit()


def showGameOverScreen(msg, autoPlay):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 30)
    gameSurf = gameOverFont.render(msg, True, BRIGHT_RED)
    gameRect = gameSurf.get_rect()
    gameRect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 500)
    DISPLAYSURF.blit(gameSurf, gameRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    if autoPlay:
        time.sleep(1.5)
        return
    else:
        while True:
            if checkForKeyPress():
                pygame.event.get()  # clear event queue
                return


def drawMsgTitle():
    surf = BASICFONT.render('Status:', True, REAL_WHITE)
    rect = surf.get_rect()
    rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 695)
    DISPLAYSURF.blit(surf, rect)


def drawStatus(turn, board):
    yDist = 670  # initial distance to subtract from WINDOWHEIGHT to put messages in left corner
    yInc = 25  # y difference for each subsequent message

    font = pygame.font.Font('freesansbold.ttf', 16)
    s = 'no one\'s turn'
    color = REAL_WHITE
    if turn == 'r':
        s = 'Red player\'s turn'
        color = RED
    elif turn == 'w':
        s = 'White player\'s turn'
        color = WHITE

    surf = font.render(s, True, color)
    rect = surf.get_rect()
    rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - yDist)
    DISPLAYSURF.blit(surf, rect)

    if TEST_MODE:
        yDist -= yInc  # increment y distance for message
        surf = font.render('Testing Mode active', True, BRIGHT_RED)
        rect = surf.get_rect()
        rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - yDist)
        DISPLAYSURF.blit(surf, rect)

        yDist -= yInc  # increment y distance for message
        surf = font.render('Square at Mouse', True, REAL_WHITE)
        rect = surf.get_rect()
        rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - yDist)
        DISPLAYSURF.blit(surf, rect)

        # show square index at mouse position
        point = getPointAtMouse()
        letters = "ABCDEFGH"
        # don't compute outside board
        if board.onBoard(point):
            yDist -= yInc  # increment y distance for message
            # display the index of the square at the mouse location
            surf = font.render('%s%s | Index: (%s, %s)' % (letters[point.x], point.y + 1, point.x, point.y), True, REAL_WHITE)
            rect = surf.get_rect()
            rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - yDist)
            DISPLAYSURF.blit(surf, rect)

def drawBoardState(board):
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j]:
                drawChecker(i, j, board[i][j])


def drawChecker(x, y, piece):
    # piece is a king
    if piece.kinged:
        # sprite = RED_KING if p
        sprite = RED_KING if piece.red else WHITE_KING
    else:
        sprite = RED_PIECE if piece.red else WHITE_PIECE

    xCenter = x * CELLSIZE + math.floor(CELLSIZE / 2)
    yCenter = y * CELLSIZE + math.floor(CELLSIZE / 2)
    spriteRect = sprite.get_rect()
    spriteRect.center = (xCenter, yCenter)
    DISPLAYSURF.blit(sprite, spriteRect)


def endTurn(turn):
    return 'r' if turn == 'w' else 'w'


def getPointAtMouse():
    x, y = pygame.mouse.get_pos()
    xIndex = math.floor(x / CELLSIZE)
    yIndex = math.floor(y / CELLSIZE)
    return Point(xIndex, yIndex)

# Takes an array of Moves and highlights the square at each point
def drawHighlightPoints(moves, selected):
    if len(moves) < 1:
        return
    # gradient of colors
    colors = [(117, 207, 255), (108, 194, 241), (99, 182, 226), (90, 169, 212), (81, 157, 198), (72, 145, 184),
              (63, 133, 171),(54, 121, 157), (45, 109, 144), (36, 98, 131), (45, 109, 144), (54, 121, 157),
              (63, 133, 171),(72, 145, 184), (81, 157, 198), (90, 169, 212), (99, 182, 226), (108, 194, 241)]
    darkIndex = 8
    # lower rate increases the speed at which the color changes along the gradient
    rate = 150
    index = (pygame.time.get_ticks() // rate) % len(colors)
    for m in moves:
        assert isinstance(m, Move), '%s of type %s is not type %s' % (m, type(m), type(Move))
        xCenter = m.dst.x * CELLSIZE + math.floor(CELLSIZE / 2)
        yCenter = m.dst.y * CELLSIZE + math.floor(CELLSIZE / 2)
        pygame.draw.circle(DISPLAYSURF, colors[index], (xCenter, yCenter), radius=25)

    if selected is not None:
        x = selected.position.x * CELLSIZE
        y = selected.position.y * CELLSIZE
        pygame.draw.rect(DISPLAYSURF, colors[darkIndex], (x, y, CELLSIZE, CELLSIZE))


if __name__ == '__main__':
    main()
