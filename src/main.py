import random, pygame, sys, math
from pygame.locals import *
import time
from Board import *
from Checker import Checker

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
TEST_MODE = True


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

    # showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global TEST_MODE

    board = Board()

    # can be value 'w' or 'r'
    turn = 'r'
    selectedChecker = None
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
                        if point.x < 8 and point.y < 8:
                            piece = board[point]
                            # add piece on empty square
                            if piece is None:
                                board[point] = Checker(point.x, point.y, False)
                            # remove piece on second click
                            elif not piece.red:
                                board[point] = None

                    # left mouse click - add a RED checker
                    elif event.button == 1:
                        point = getPointAtMouse()
                        # don't compute clicks outside board
                        if point.x < 8 and point.y < 8:
                            piece = board[point]
                            # add piece on empty square
                            if piece is None:
                                board[point] = Checker(point.x, point.y, True)
                                # remove piece on second click
                            elif piece.red:
                                board[point] = None

                elif event.type == KEYDOWN:
                    # switch turn
                    if event.key == K_RETURN:
                        turn = 'r' if turn == 'w' else 'w'
                    # reset board
                    elif event.key == K_r:
                        board.reset()
                    # clear board of all pieces
                    elif event.key == K_c:
                        board.clear()
                    # king / un-king the piece at the mouse location
                    elif event.key == K_k:
                        point = getPointAtMouse()
                        # only check squares on board
                        if point.x < 8 and point.y < 8:
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
                                print("Moves:")
                                print([str(m) for m in moves])
                                
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
                    if event.button == 1 and turn == 'r' and point.x < 8 and point.y < 8:
                        # select a checker at the mouse location
                        if board.occupied(point):
                            if board[point].red:
                                highlightMoves = []
                                if selectedChecker != board[point]:
                                    selectedChecker = board[point]
                                    moves, multiJumps = selectedChecker.calculateMoves(board)
                                    for m in moves:
                                        highlightMoves.append(m)
                                else:
                                    selectedChecker = None

                        # move checker
                        # TODO: add logic to remove jumped checkers
                        else:
                            validMove = None
                            for m in highlightMoves:
                                if point.x == m.dst.x and point.y == m.dst.y:
                                    validMove = m
                                    break
                            if validMove and selectedChecker is not None:
                                highlightMoves = []
                                selectedChecker.move(validMove, board)
                                selectedChecker = None

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

        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(BG_BOARD, (0, 0))
        drawHighlightPoints(highlightMoves)
        drawMsgTitle()
        drawStatus(turn)
        drawBoardState(board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, RED)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
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


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 120)
    gameSurf = gameOverFont.render('Game Over', True, WHITE, RED)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)

    DISPLAYSURF.blit(gameSurf, gameRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawMsgTitle():
    surf = BASICFONT.render('Status:', True, REAL_WHITE)
    rect = surf.get_rect()
    rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 695)
    DISPLAYSURF.blit(surf, rect)


def drawStatus(turn):
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
    rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 670)
    DISPLAYSURF.blit(surf, rect)

    if TEST_MODE:
        surf = font.render('Testing Mode active', True, BRIGHT_RED)
        rect = surf.get_rect()
        rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 645)
        DISPLAYSURF.blit(surf, rect)

        surf = font.render('Square at Mouse', True, REAL_WHITE)
        rect = surf.get_rect()
        rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 595)
        DISPLAYSURF.blit(surf, rect)

        # show square index at mouse position
        x, y = pygame.mouse.get_pos()
        xIndex = math.floor(x / CELLSIZE)
        yIndex = math.floor(y / CELLSIZE)
        letters = "ABCDEFGH"
        # don't compute clicks outside board
        if xIndex < 8 and yIndex < 8:
            surf = font.render('%s%s | Index: (%s, %s)' % (letters[xIndex], yIndex, xIndex, yIndex), True, REAL_WHITE)
            rect = surf.get_rect()
            rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 570)
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


# takes an array of Points and highlights the boarders of the square at each point
def drawHighlightPoints(moves):
    # gradient of colors
    colors = [(117, 207, 255), (108, 194, 241), (99, 182, 226), (90, 169, 212), (81, 157, 198), (72, 145, 184),
              (63, 133, 171),(54, 121, 157), (45, 109, 144), (36, 98, 131), (45, 109, 144), (54, 121, 157),
              (63, 133, 171),(72, 145, 184), (81, 157, 198), (90, 169, 212), (99, 182, 226), (108, 194, 241)]
    # lower rate increases the speed at which the color changes along the gradient
    rate = 150
    index = (pygame.time.get_ticks() // rate) % len(colors)
    for m in moves:
        xCenter = m.dst.x * CELLSIZE + math.floor(CELLSIZE / 2)
        yCenter = m.dst.y * CELLSIZE + math.floor(CELLSIZE / 2)
        pygame.draw.circle(DISPLAYSURF, colors[index], (xCenter, yCenter), radius=25)


if __name__ == '__main__':
    main()
