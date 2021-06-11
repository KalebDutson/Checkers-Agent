import random, pygame, sys,math
from pygame.locals import *
import time
from Board import *

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
BRIGHT_RED = (255,   0,   0)
BGCOLOR = (50, 50, 50)
BLACK = (0, 0, 0)
GRAY = pygame.Color("#f9f9f9")
RED = pygame.Color('#9c5359')
WHITE = pygame.Color('#d3bba2')

# when true, allows for adding an removing of checkers with mouse
TEST_MODE = True

# Some debug information reported by the piece the mouse is over
PIECE_INFO = ""
# The piece that gave pieceInfo, so it's not polled every frame
INFO_PIECE = None

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
    global INFO_PIECE
    global PIECE_INFO

    board = Board()
    # can be value 'w' or 'r'
    turn = 'w'

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN and TEST_MODE:
                # right mouse click - add a WHITE checker
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    xIndex = math.floor(x / CELLSIZE)
                    yIndex = math.floor(y / CELLSIZE)
                    # don't compute clicks outside board
                    if xIndex < 8 and yIndex < 8:
                        # remove piece on second click
                        if board[xIndex][yIndex] == 'w':
                            board[xIndex][yIndex] = None
                        # add piece on empty square
                        elif board[xIndex][yIndex] == None:
                            board[xIndex][yIndex] = Checker(xIndex, yIndex, False)

                # middle mouse click
                if event.button == 2:
                    x, y = pygame.mouse.get_pos()
                    xIndex = math.floor(x / CELLSIZE)
                    yIndex = math.floor(y / CELLSIZE)
                    # don't compute clicks outside board
                    if xIndex < 8 and yIndex < 8:
                        print('Square')
                        print('(%s, %s)' % (xIndex, yIndex))
                        print('Board:')
                        print(board)

                # left mouse click - add a RED checker
                elif event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    xIndex = math.floor(x / CELLSIZE)
                    yIndex = math.floor(y / CELLSIZE)
                    # don't compute clicks outside board
                    if xIndex < 8 and yIndex < 8:
                        # remove piece on second click
                        if board[xIndex][yIndex] == 'r':
                            board[xIndex, yIndex] = None
                        # add piece on empty square
                        elif board[xIndex][yIndex] == None:
                            board[xIndex, yIndex] = Checker(xIndex, yIndex, True)

            elif event.type == KEYDOWN:
                # activate test mode
                if event.key == K_t:
                    TEST_MODE = not TEST_MODE
                # switch turn
                elif event.key == K_RETURN and TEST_MODE:
                    turn = 'r' if turn == 'w' else 'w'
                # Reset the board
                elif event.key == K_r and TEST_MODE:
                    board.reset()

                # end game
                elif event.key == K_q:
                    return
                # exit game
                elif event.key == K_ESCAPE:
                    terminate()

            elif event.type == MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                xIndex = math.floor(x / CELLSIZE)
                yIndex = math.floor(y / CELLSIZE)
                if xIndex < 8 and yIndex < 8:
                    piece = board[xIndex, yIndex]
                    if INFO_PIECE != piece:
                        INFO_PIECE = piece
                        if piece != None:
                            moves = piece.calculateMoves(board)                            

                            if len(moves):
                                PIECE_INFO =  "Potential score: %s" % max([m.score() for m in moves])
                                print("Moves:")
                                print([str(m) for m in moves])
                            else:
                                PIECE_INFO = "NO MOVES"

        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(BG_BOARD, (0,0))
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
            pygame.event.get() # clear event queue
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
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
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

        surf = font.render(PIECE_INFO, True, GRAY)
        rect = surf.get_rect()
        rect.bottomleft = (WINDOWWIDTH - 170, WINDOWHEIGHT - 620)
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

    xCenter = x * CELLSIZE + math.floor(CELLSIZE/2)
    yCenter = y * CELLSIZE + math.floor(CELLSIZE/2)
    spriteRect = sprite.get_rect()
    spriteRect.center = (xCenter, yCenter)
    DISPLAYSURF.blit(sprite, spriteRect)


if __name__ == '__main__':
    main()