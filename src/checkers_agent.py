import random, pygame, sys,math
from pygame.locals import *
import time

FPS = 10
# if you change the window height or width, you will need to recalculate the value for cell size
WINDOWWIDTH = 720
WINDOWHEIGHT = 720
CELLSIZE = 90
# RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
# Calculate width and height for a 8x8 board
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

BGCOLOR = (255, 255, 255)
BLACK = (0, 0, 0)
RED = pygame.Color('#9c5359')
WHITE = pygame.Color('#d3bba2')


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
    board = [
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # right mouse click - add a WHITE checker
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    xIndex = math.floor(x / CELLSIZE)
                    yIndex = math.floor(y / CELLSIZE)
                    # remove piece on second click
                    if board[xIndex][yIndex] == 'w':
                        board[xIndex][yIndex] = ''
                    # add piece on empty square
                    elif board[xIndex][yIndex] == '':
                        board[xIndex][yIndex] = 'w'

                # middle mouse click
                if event.button == 2:
                    print('Board:')
                    for row in board:
                        print(row)

                # left mouse click - add a RED checker
                elif event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    xIndex = math.floor(x / CELLSIZE)
                    yIndex = math.floor(y / CELLSIZE)
                    # remove piece on second click
                    if board[xIndex][yIndex] == 'r':
                        board[xIndex][yIndex] = ''
                    # add piece on empty square
                    elif board[xIndex][yIndex] == '':
                        board[xIndex][yIndex] = 'r'

            elif event.type == KEYDOWN:
                # exit game
                if event.key == K_ESCAPE:
                    terminate()

        DISPLAYSURF.blit(BG_BOARD, (0,0))
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


def drawBoardState(board):
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] != '':
                drawChecker(i, j, board[i][j])


def drawChecker(x, y, piece):
    # piece is a king
    if piece.__contains__('k'):
        # sprite = RED_KING if p
        sprite = RED_KING if piece == 'rk' else WHITE_KING
    else:
        sprite = RED_PIECE if piece == 'r' else WHITE_PIECE

    xCenter = x * CELLSIZE + math.floor(CELLSIZE/2)
    yCenter = y * CELLSIZE + math.floor(CELLSIZE/2)
    spriteRect = sprite.get_rect()
    spriteRect.center = (xCenter, yCenter)
    DISPLAYSURF.blit(sprite, spriteRect)


if __name__ == '__main__':
    main()