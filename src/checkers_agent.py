import random, pygame, sys,math
from pygame.locals import *
import time

FPS = 5
# if you change the window height or width, you will need to recalculate the value for cell size
WINDOWWIDTH = 720
WINDOWHEIGHT = 720
CELLSIZE = 90
RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
# Calculate width and height for a 8x8 board
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
BGCOLOR = (255, 255, 255)
BLACK = (0, 0, 0)

BG_BOARD = pygame.image.load('../imgs/720x720_board.png')
RED = pygame.Color('#9c5359')
WHITE = pygame.Color('#d3bba2')
SQUARES = [['r','w','r','w','r','w','r','w'], ['w','r','w','r','w','r','w','r']] * 4


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Checkers')

    # showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                # save screenshot of the board
                if event.key == K_s:
                    pygame.image.save(DISPLAYSURF, '../imgs/screenshots/screenshot-' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.png')

                # exit game
                if event.key == K_ESCAPE:
                    terminate()

        DISPLAYSURF.blit(BG_BOARD, (0,0))

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


# Was used initially to draw to board before an image of the board was saved and loaded as the background
def drawSquares(array):
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            drawSquare(i, j, array[i][j])


def drawSquare(x, y, color):
    color = WHITE if color == 'w' else RED

    x = x * CELLSIZE
    y = y * CELLSIZE

    square = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, square)


if __name__ == '__main__':
    main()