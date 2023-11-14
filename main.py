import pygame, sys, random
from pygame.locals import *


COLUMNS = 4
ROWS = 4
BOX = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOTPINK = (255, 105, 180)
CYAN = (0, 100, 100)

bgcolor = HOTPINK
boxcolor = CYAN
textcolor = WHITE
BORDERCOLOR = BLACK

textcolor = BLACK
messagecolor = BLACK

POS_X = int((WINDOWWIDTH - (BOX * COLUMNS + (COLUMNS - 1))) / 2)
POS_Y = int((WINDOWHEIGHT - (BOX * ROWS + (ROWS - 1))) / 2)

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def main():
    global clock, WIN, font_type, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT

    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("4X4 Puzzle")
    font_type = pygame.font.Font(None, 30)

    RESET_SURF, RESET_RECT = makeText(
        "Reset", textcolor, boxcolor, WINDOWWIDTH - 120, WINDOWHEIGHT - 90
    )
    NEW_SURF, NEW_RECT = makeText(
        "New Game", textcolor, boxcolor, WINDOWWIDTH - 120, WINDOWHEIGHT - 60
    )

    mainBoard, solution = spawnNewPuzzle(80)
    solvedboard = getStartingBoard()
    allMoves = []

    while True:  # main game loop
        movement = None
        text = "Play with the arrow keys."
        if mainBoard == solvedboard:
            text = "Congratulations!"

        drawBoard(mainBoard, text)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solution = spawnNewPuzzle(80)
                        allMoves = []

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and is_move(mainBoard, LEFT):
                    movement = LEFT
                elif event.key in (K_RIGHT, K_d) and is_move(mainBoard, RIGHT):
                    movement = RIGHT
                elif event.key in (K_UP, K_w) and is_move(mainBoard, UP):
                    movement = UP
                elif event.key in (K_DOWN, K_s) and is_move(mainBoard, DOWN):
                    movement = DOWN

        if movement:
            animate(mainBoard, movement, "Play with the arrow keys.", 8)
            makeMove(mainBoard, movement)
            allMoves.append(movement)
        pygame.display.update()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def getStartingBoard():
    count = 1
    board = []
    for x in range(COLUMNS):
        column = []
        for y in range(ROWS):
            column.append(count)
            count += COLUMNS
        board.append(column)
        count -= COLUMNS * (ROWS - 1) + COLUMNS - 1

    board[COLUMNS - 1][ROWS - 1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(COLUMNS):
        for y in range(ROWS):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = (
            board[blankx][blanky + 1],
            board[blankx][blanky],
        )
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = (
            board[blankx][blanky - 1],
            board[blankx][blanky],
        )
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = (
            board[blankx + 1][blanky],
            board[blankx][blanky],
        )
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = (
            board[blankx - 1][blanky],
            board[blankx][blanky],
        )


def is_move(board, move):
    blankx, blanky = getBlankPosition(board)
    return (
        (move == UP and blanky != len(board[0]) - 1)
        or (move == DOWN and blanky != 0)
        or (move == LEFT and blankx != len(board) - 1)
        or (move == RIGHT and blankx != 0)
    )


def getRandomMove(board, lastMove=None):
    moves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not is_move(board, DOWN):
        moves.remove(DOWN)
    if lastMove == DOWN or not is_move(board, UP):
        moves.remove(UP)
    if lastMove == LEFT or not is_move(board, RIGHT):
        moves.remove(RIGHT)
    if lastMove == RIGHT or not is_move(board, LEFT):
        moves.remove(LEFT)
    return random.choice(moves)


def getLeftTopOfbox(boxX, boxY):
    left = POS_X + (boxX * BOX) + (boxX - 1)
    top = POS_Y + (boxY * BOX) + (boxY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for boxX in range(len(board)):
        for boxY in range(len(board[0])):
            left, top = getLeftTopOfbox(boxX, boxY)
            boxRect = pygame.Rect(left, top, BOX, BOX)
            if boxRect.collidepoint(x, y):
                return (boxX, boxY)
    return (None, None)


def drawbox(boxx, boxy, number, adjx=0, adjy=0):
    left, top = getLeftTopOfbox(boxx, boxy)
    pygame.draw.rect(WIN, boxcolor, (left + adjx, top + adjy, BOX, BOX))
    textSurf = font_type.render(str(number), True, textcolor)
    textRect = textSurf.get_rect()
    textRect.center = left + int(BOX / 2) + adjx, top + int(BOX / 2) + adjy
    WIN.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    textSurf = font_type.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    WIN.fill(bgcolor)
    if message:
        textSurf, textRect = makeText(message, messagecolor, bgcolor, 5, 5)
        WIN.blit(textSurf, textRect)

    for boxx in range(len(board)):
        for boxy in range(len(board[0])):
            if board[boxx][boxy]:
                drawbox(boxx, boxy, board[boxx][boxy])

    left, top = getLeftTopOfbox(0, 0)
    width = COLUMNS * BOX
    height = ROWS * BOX
    pygame.draw.rect(WIN, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    WIN.blit(RESET_SURF, RESET_RECT)
    WIN.blit(NEW_SURF, NEW_RECT)


def animate(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    base = WIN.copy()

    moveLeft, moveTop = getLeftTopOfbox(movex, movey)
    pygame.draw.rect(base, bgcolor, (moveLeft, moveTop, BOX, BOX))

    for i in range(0, BOX, animationSpeed):
        checkForQuit()
        WIN.blit(base, (0, 0))
        if direction == UP:
            drawbox(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawbox(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawbox(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawbox(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        clock.tick(FPS)


def spawnNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, "")
    pygame.display.update()
    pygame.time.wait(1500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        animate(board, move, "", animationSpeed=int(BOX / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        animate(board, oppositeMove, "", animationSpeed=int(BOX / 2))
        makeMove(board, oppositeMove)


if __name__ == "__main__":
    main()
