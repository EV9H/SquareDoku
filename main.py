import pygame as p
import gameEngine

p.init()
wWIDTH = 2560
wHEIGHT = 1440
WIDTH = HEIGHT = 1080
DIMENSION = 9
SQ_SIZE = HEIGHT // DIMENSION
readySQ_SIZE = SQ_SIZE // 2
MAX_FPS = 60
IMAGES = {"arrow": p.transform.scale(p.image.load("Image/arrow.png"), (readySQ_SIZE * 2, readySQ_SIZE * 2))}


gs = gameEngine.GameState()
CENTEREDSHIFT_X = wWIDTH // 2 - WIDTH // 2
CENTEREDSHIFT_Y = 250

BOARDERWIDTH = 200

"""
def loadImages():
    pass
"""
R = 100
G = 50
B = 100
THEMECOLOR = p.Color(R, G, B, 255)

gameSurface = p.Surface((WIDTH, HEIGHT))
drawPhantom = False
phantomLoc = []
magicSelected = -1

def main():
    global gs
    screen = p.display.set_mode((0, 0), p.FULLSCREEN)

    clock = p.time.Clock()
    running = True

    global magicSelected
    magicSelected = -1
    while running:

        if gs.counter <= 0:
            gs.LOSE = True
            finalScore = gs.totalPoint

            screen.fill(p.Color(THEMECOLOR))
            drawReadyList(screen, gs)
            drawBlocks(screen, gs.board)  # the placed blocks and empty places
            drawText(screen, gs)
            #drawCountdown(screen, gs)
            drawMagicList(screen, gs)
            drawMagicCountdown(screen, gs)
            drawSections(screen)  # the underground section colors
            drawBoard(screen)  # the grids

            p.display.flip()
            waiting = True
            while waiting:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        gs.Music.stopBg()
                        waiting = False
                        running = False
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_r:
                            gs = gameEngine.GameState()
                            waiting = False

                        elif e.key == p.K_ESCAPE:
                            gs.Music.stopBg()
                            waiting = False
                            running = False

        if gs.counter <= 15:
            gs.Music.playCountdown()

        if gs.counter > 15:
            gs.Music.stopCountdown()

        RGBchanger()
        gs.maintainMagicList()

        for e in p.event.get():
            if e.type == p.QUIT:
                gs.Music.stopBg()
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if e.button == 1:
                    location = p.mouse.get_pos()  # (x,y) location of mouse
                    if magicSelected != -1:         # selected a magic
                        col = (location[0] - CENTEREDSHIFT_X) // SQ_SIZE
                        row = (location[1] - CENTEREDSHIFT_Y) // SQ_SIZE
                        if gs.magicList[gs.itemIdx] != "__":
                            point = gs.use_magic(gs.magicList[gs.itemIdx], gs.itemIdx, row,col)
                            gs.totalPoint += point


                        magicSelected = -1
                    else:
                        # place block
                        if CENTEREDSHIFT_X <= location[0] <= CENTEREDSHIFT_X + DIMENSION * SQ_SIZE and CENTEREDSHIFT_Y <= \
                                location[1] <= CENTEREDSHIFT_Y + DIMENSION * SQ_SIZE:
                            col = (location[0] - CENTEREDSHIFT_X) // SQ_SIZE
                            row = (location[1] - CENTEREDSHIFT_Y) // SQ_SIZE
                            if gs.readyList[gs.idx] != "__":
                                gs.placeBlock(gameEngine.Action(gs.readyList, gs.idx, [row, col]), gs.idx)
                                gs.FitList = gs.checkFit()
                                gs.Music.playPlacementSound()

                        # choose block
                        elif 0 <= location[0] < CENTEREDSHIFT_X and CENTEREDSHIFT_Y <= location[
                            1] <= CENTEREDSHIFT_Y + gs.readyboardH * readySQ_SIZE:
                            selectBlock(location)
                            gs.Music.playSelectSound()
                elif e.button == 4:  # scroll up
                    gs.idx = gs.seekClosestReadyIndex(-1)
                    gs.Music.playSelectSound()
                elif e.button == 5:  # scroll down
                    gs.idx = gs.seekClosestReadyIndex(1)
                    gs.Music.playSelectSound()

            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    gs.clearBoard()
                    drawGameState(screen, gs)
                elif e.key == p.K_z:
                    gs.undo()
                elif e.key == p.K_d or e.key == p.K_s:
                    gs.Music.mixer.stop()
                    gs.idx = gs.seekClosestReadyIndex(1)
                    gs.Music.playSelectSound()

                elif e.key == p.K_a or e.key == p.K_w:
                    gs.idx = gs.seekClosestReadyIndex(0)
                    gs.Music.playSelectSound()

                elif e.key == p.K_1:
                    if gs.magicList[0] != "__":
                        if magicSelected == 1:     #deselect
                            magicSelected = -1
                        else:
                            gs.itemIdx = 0
                            magicSelected = 1

                elif e.key == p.K_2:
                    if gs.magicList[1] != "__":
                        if magicSelected == 2:
                            magicSelected = -1
                        else:
                            gs.itemIdx = 1
                            magicSelected = 2

                elif e.key == p.K_3:
                    if gs.magicList[2] != "__":
                        if magicSelected == 3:
                            magicSelected = -1
                        else:
                            gs.itemIdx = 2
                            magicSelected = 3

                elif e.key == p.K_ESCAPE:
                    running = False

        drawGameState(screen, gs)



        dt = clock.tick(MAX_FPS) / 1000
        gs.counter -= dt
        gs.magicCounter -= dt


def drawGameState(screen, gs):
    screen.fill(p.Color(THEMECOLOR))

    drawReadyList(screen, gs)
    drawBlocks(screen, gs.board)  # the placed blocks and empty places



    drawText(screen, gs)
    drawCountdown(screen, gs)
    drawSelectArrow(screen, gs)
    drawMagicList(screen,gs)
    drawMagicCountdown(screen,gs)
    # Draw Phantom Block
    global magicSelected
    if magicSelected == -1:
        location = p.mouse.get_pos()
        if CENTEREDSHIFT_X <= location[0] <= CENTEREDSHIFT_X + DIMENSION * SQ_SIZE and CENTEREDSHIFT_Y <= location[
            1] <= CENTEREDSHIFT_Y + DIMENSION * SQ_SIZE:
            drawPhantomBlock(screen, gs, location[0], location[1])
    else:
        location = p.mouse.get_pos()
        if CENTEREDSHIFT_X <= location[0] <= CENTEREDSHIFT_X + DIMENSION * SQ_SIZE and CENTEREDSHIFT_Y <= location[
            1] <= CENTEREDSHIFT_Y + DIMENSION * SQ_SIZE:
            drawPhantomMagic(screen, gs, location[0], location[1])
    drawSections(screen)  # the underground section colors
    drawBoard(screen)  # the grids
    p.display.flip()

def drawSections(screen):
    for x in range(DIMENSION // 3):
        for y in range(DIMENSION // 3):
            if (x + y) % 2 == 1:
                rect = p.Rect(CENTEREDSHIFT_X + x * 3 * SQ_SIZE, CENTEREDSHIFT_Y + y * 3 * SQ_SIZE, 3 * SQ_SIZE,
                              3 * SQ_SIZE)
                shape_surf = p.Surface(rect.size, p.SRCALPHA)
                p.draw.rect(shape_surf, (255, 255, 255, 45), shape_surf.get_rect())
                screen.blit(shape_surf, rect)


def drawCountdown(screen, gs):
    counter = round(gs.counter, 1)
    p.time.set_timer(p.USEREVENT, 1000)
    size = wHEIGHT // 20
    fontTimer = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size)
    digit = fontTimer.render(str(counter).rjust(3), 1, (255, 255, 255)) if counter > 0 else fontTimer.render(
        "Game Over", 1, (255, 255, 255))

    fontTimer = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size // 3)
    timeLabel = fontTimer.render("Timer".rjust(5), 1, (255, 255, 255)) if counter > 0 else fontTimer.render(" ", 1, (
        255, 255, 255))

    screen.blit(digit, (CENTEREDSHIFT_X + SQ_SIZE - 30, CENTEREDSHIFT_Y - size))
    screen.blit(timeLabel, (CENTEREDSHIFT_X + SQ_SIZE * 1.4 -30, CENTEREDSHIFT_Y - size * 1.5))


def drawText(screen, gs):
    size = wHEIGHT // 20
    score = gs.getTotalPoint()
    largeFont = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size)  # Font object
    scoreDigit = largeFont.render(str(score), 1, (255, 255, 255))  # create our text

    largeFont = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size // 3)
    scoreLabel = largeFont.render("Score".rjust(5), 1, (255, 255, 255))

    screen.blit(scoreDigit, (CENTEREDSHIFT_X + SQ_SIZE * 4.3, CENTEREDSHIFT_Y - size))  # draw the text to the screen
    screen.blit(scoreLabel, (CENTEREDSHIFT_X + SQ_SIZE * 4.15, CENTEREDSHIFT_Y - size * 1.5))

def drawMagicCountdown(screen,gs):
    counter = round(gs.magicCounter, 1)
    p.time.set_timer(p.USEREVENT, 1000)
    size = wHEIGHT // 20
    fontTimer = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size)
    digit = fontTimer.render(str(counter).rjust(3), 1, (255, 255, 255)) if counter > 0 else fontTimer.render(
        "0", 1, (255, 255, 255))

    fontTimer = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size // 3)
    timeLabel = fontTimer.render("Next magic in".rjust(5), 1, (255, 255, 255)) if counter > 0 else fontTimer.render(" ", 1, (
        255, 255, 255))

    screen.blit(digit, (CENTEREDSHIFT_X + 9*SQ_SIZE - 270, CENTEREDSHIFT_Y - size))
    screen.blit(timeLabel, (CENTEREDSHIFT_X + 9*SQ_SIZE - 270, CENTEREDSHIFT_Y - size * 1.5))

def drawReadyList(screen, gs):
    fitList = gs.FitList
    for r in range(gs.readyboardH):
        for c in range(gs.readyboardW):
            section = r // (len(gs.readyBoard) // 3)
            if fitList[section]:
                if gs.readyBoard[r][c] != "__":
                    p.draw.rect(screen, p.Color("blue"),
                                p.Rect(BOARDERWIDTH + c * readySQ_SIZE, r * readySQ_SIZE + CENTEREDSHIFT_Y,
                                       readySQ_SIZE, readySQ_SIZE))
                else:
                    p.draw.rect(screen, THEMECOLOR,
                                p.Rect(BOARDERWIDTH + c * readySQ_SIZE, r * readySQ_SIZE + CENTEREDSHIFT_Y,
                                       readySQ_SIZE, readySQ_SIZE))
            else:
                if gs.readyBoard[r][c] != "__":
                    p.draw.rect(screen, p.Color("red"),
                                p.Rect(BOARDERWIDTH + c * readySQ_SIZE, r * readySQ_SIZE + CENTEREDSHIFT_Y,
                                       readySQ_SIZE, readySQ_SIZE))
                else:
                    p.draw.rect(screen, THEMECOLOR,
                                p.Rect(BOARDERWIDTH + c * readySQ_SIZE, r * readySQ_SIZE + CENTEREDSHIFT_Y,
                                       readySQ_SIZE, readySQ_SIZE))
    for r in range(gs.readyboardH):
        for c in range(gs.readyboardW):
            p.draw.rect(screen, p.Color(200, 200, 200, 0),
                        p.Rect(BOARDERWIDTH + c * readySQ_SIZE, r * readySQ_SIZE + CENTEREDSHIFT_Y, readySQ_SIZE,
                               readySQ_SIZE), 1)


def drawMagicList(screen,gs):
    l = gs.magicList
    for i in range(len(l)):
        if l[i] != "__":
            size = 50
            font = p.font.Font('Fonts/AstroSpace-eZ2Bg.ttf', size)  # Font object

            temp = str(i+1) + ":  " + str(gs.M.magicDictionary[gs.magicList[i]][0]) + " x " + str(gs.M.magicDictionary[gs.magicList[i]][1])

            magicText = font.render(temp, 1, (255, 0, 255))  # create our text

            screen.blit(magicText, (CENTEREDSHIFT_X + SQ_SIZE * 10, CENTEREDSHIFT_Y + SQ_SIZE+i * 3 * SQ_SIZE))

def drawBoard(screen):
    colors = (p.Color("white"), p.Color("light gray"))
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (r // 3 + c // 3) % 2 == 1:
                p.draw.rect(screen, colors[1],
                            p.Rect(CENTEREDSHIFT_X + c * SQ_SIZE, CENTEREDSHIFT_Y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)
            else:
                p.draw.rect(screen, colors[0],
                            p.Rect(CENTEREDSHIFT_X + c * SQ_SIZE, CENTEREDSHIFT_Y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)
    '''
    lineColor = p.Color("dark gray")
    p.draw.line(screen, lineColor, (3 * SQ_SIZE, 0), (3 * SQ_SIZE, HEIGHT), 5)
    p.draw.line(screen, lineColor, (3 * SQ_SIZE * 2, 0), (3 * SQ_SIZE * 2, HEIGHT), 5)
    p.draw.line(screen, lineColor, (0, 3 * SQ_SIZE), (WIDTH, 3 * SQ_SIZE), 5)
    p.draw.line(screen, lineColor, (0, 3 * SQ_SIZE * 2), (WIDTH, 3 * SQ_SIZE * 2), 5)
    '''


def drawBlocks(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = board[r][c]
            if square != "__":
                p.draw.rect(screen, p.Color("blue"),
                            p.Rect(CENTEREDSHIFT_X + c * SQ_SIZE, CENTEREDSHIFT_Y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, THEMECOLOR,
                            p.Rect(CENTEREDSHIFT_X + c * SQ_SIZE, CENTEREDSHIFT_Y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawSelectArrow(screen, gs):
    index = gs.idx
    posX = BOARDERWIDTH + 6 * readySQ_SIZE
    posY = CENTEREDSHIFT_Y + index * 6 * readySQ_SIZE + 2 * readySQ_SIZE
    image = IMAGES["arrow"]
    screen.blit(image, (posX, posY))


def drawPhantomBlock(screen, gs, x, y):
    block = gs.readyList[gs.idx]
    width = block.info[1]
    height = block.info[0]

    col = (x - CENTEREDSHIFT_X) // SQ_SIZE
    row = (y - CENTEREDSHIFT_Y) // SQ_SIZE

    fit = gs.checkFitForCurrentSquare(block, row, col)
    if col + width <= DIMENSION and row + height <= DIMENSION and fit:
        cnt = 2
        for r in range(height):
            for c in range(width):
                if block.info[r * width + c + 2] == 1:
                    p.draw.rect(screen, p.Color(125, 25, 255, 0), p.Rect(CENTEREDSHIFT_X + col * SQ_SIZE + c * SQ_SIZE,
                                                                         CENTEREDSHIFT_Y + row * SQ_SIZE + r * SQ_SIZE,
                                                                         SQ_SIZE, SQ_SIZE), 0)


def drawPhantomMagic(screen, gs, x, y):
    name = gs.magicList[gs.itemIdx]
    if name != "__":
        height = gs.M.magicDictionary[name][0]
        width = gs.M.magicDictionary[name][1]

        col = (x - CENTEREDSHIFT_X) // SQ_SIZE
        row = (y - CENTEREDSHIFT_Y) // SQ_SIZE

        if gs.validateMagic(name, row, col):
            for r in range(height):
                for c in range(width):
                    p.draw.rect(screen, p.Color(0,0,0), p.Rect(CENTEREDSHIFT_X + col * SQ_SIZE + c * SQ_SIZE,
                                                                             CENTEREDSHIFT_Y + row * SQ_SIZE + r * SQ_SIZE,
                                                                             SQ_SIZE, SQ_SIZE), 0)


def selectBlock(location):
    changed = False
    original = gs.idx

    y = location[1]
    x = location[0]

    selectedBlock = (y - CENTEREDSHIFT_Y) // readySQ_SIZE // 6
    gs.idx = selectedBlock


def gameOverScreen(screen, gs):
    largeFont = p.font.SysFont('comicsans', 30)  # Font object
    text = largeFont.render('"Game Over": ', 1, (255, 255, 255))  # create our text
    screen.blit(text, (WIDTH / 3, HEIGHT + 100))


def RGBchanger():
    global THEMECOLOR
    if gs.counter <= 0:
        THEMECOLOR = p.Color(0, 0, 0, 255)
    else:
        R = int(gs.counter * 2) if gs.counter <= 255 else 255
        G = int(gs.counter) if gs.counter <= 255 else 255
        B = int(gs.counter * 2) if gs.counter <= 255 else 255
        print(R, G, B)

        R = min(R, 255)
        G = min(G, 255)
        B = min (B, 255)
        THEMECOLOR = p.Color(R, G, B, 255)


if __name__ == "__main__":
    main()
