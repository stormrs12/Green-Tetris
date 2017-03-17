from pygame.locals import *
import pygame
import math
import random
import sys

running = True

WIDTH = 800
HEIGHT = 600

color_pelette = [
    (15, 56, 15),
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15),
    (170, 170, 170)
]

def C(c):
    return color_pelette[c]

def pieceFall(cell, downCount, startPoint):
    newCell = cell

    for i in xrange(startPoint, 0, -1):
    #for i in xrange(len(newCell) - 1, 0, -1):
        for j in xrange(len(newCell[i]) - 1, -1, -1):
            if newCell[i][j]:
                newCell[i][j] = 0
                if i + downCount >= len(newCell):
                    newCell[len(newCell) - 1][j] = 1
                else:
                    if newCell[i + downCount][j]:
                        newCell[i + downCount - 1][j] = 1
                    else:
                        newCell[i + downCount][j] = 1
    return newCell

pieces = [
    [ # T-Piece
        [
            (0, 0, 0, 0),
            (0, 1, 1, 1),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 1, 1, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ]
    ],

    [ # J-Piece
        [
            (0, 0, 0, 0),
            (0, 1, 1, 1),
            (0, 0, 0, 1),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 1),
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 1, 0, 0),
            (0, 1, 1, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 1, 1, 0),
            (0, 0, 0, 0)
        ]
    ],

    [ # L-Piece
        [
            (0, 0, 0, 0),
            (0, 1, 1, 1),
            (0, 1, 0, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 0, 1),
            (0, 1, 1, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ]
    ],

    [ # Z-Piece
        [
            (0, 0, 0, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 0, 1),
            (0, 0, 1, 1),
            (0, 0, 1, 0),
            (0, 0, 0, 0)
        ]
    ],

    [ # S-Piece
        [
            (0, 0, 0, 0),
            (0, 0, 1, 1),
            (0, 1, 1, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
            (0, 0, 0, 0)
        ]
    ],

    [ # L-Piece
        [
            (0, 0, 0, 0),
            (1, 1, 1, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        [
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 0)
        ]
    ],

    [ # O-Piece
        [
            (0, 0, 0, 0),
            (0, 1, 1, 0),
            (0, 1, 1, 0),
            (0, 0, 0, 0)
        ]
    ],
]

piece = random.randint(0, len(pieces) - 1)
nextRandomPiece = random.randint(0, len(pieces) - 1)
pieceOrient = 0
piecePosition = (3, -1)

slideDown = False

rw = pygame.display.set_mode((WIDTH, HEIGHT), \
     pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

pygame.display.set_caption("Green Tetris")

pygame.font.init()

clock = pygame.time.Clock()

cellWidth = 10
cellHeight = 15

cells = [[0 for i in xrange(0, cellWidth)] for i in xrange(0, cellHeight)]

blockDelay = 1000
pygame.time.set_timer(pygame.USEREVENT, blockDelay)

SLIDEDOWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SLIDEDOWN_EVENT, 50)

pygame.time.set_timer(pygame.USEREVENT + 2, 500)
blinking = True

mainFont = pygame.font.Font("Assets/FreePixel.ttf", 30)
gameOverFont = pygame.font.Font("Assets/FreePixel.ttf", 60)
gameTitleFont = pygame.font.Font("Assets/FreePixel.ttf", 100)

blockSize = 35

score = 0
level = -2

scoreFieldWidth = WIDTH - (WIDTH * 0.7)
scoreFieldHeight = HEIGHT - (HEIGHT * 0.7)

scoreField = (WIDTH * 0.7, 0, scoreFieldWidth, scoreFieldHeight)

fieldWidth = blockSize * len(cells[0])
fieldHeight = blockSize * len(cells)

fieldHeightDifference = HEIGHT - fieldHeight
fieldWidthDifference = scoreField[0] - fieldWidth

playField = (fieldWidthDifference / 2, fieldHeightDifference / 2, fieldWidth, fieldHeight)

scores = []

prompt = ""

scoreFile = open("Assets/scores.txt")

for s in scoreFile:
    ss = s.split(":")
    scores.append([ss[0], int(ss[1].strip('\n'))])

scoreFile.close()

def scoreKeys(item):
    return item[1]

scores = sorted(scores, key=scoreKeys, reverse=True)

highscore = scores[0][1]

debug_mode = False

while running:
    orientBlock = False
    leftBlock = False
    rightBlock = False
    verticalBlock = False

    nextPiece = pieces[piece][(pieceOrient + 1) % len(pieces[piece])]
    for i in xrange(0, len(nextPiece)):
        for j in xrange(0, len(nextPiece[i])):
            if (nextPiece[i][j]):

                piecePos = (
                    playField[0] + piecePosition[0] * blockSize + j * blockSize,
                    playField[1] + piecePosition[1] * blockSize + i * blockSize
                )

                pygame.draw.rect(rw, (255, 0,0),
                (piecePos[0], piecePos[1], blockSize, blockSize))

                if piecePos[0] < playField[0] or piecePos[0] >= playField[0] + fieldWidth:
                    orientBlock = True
                if piecePos[1] + blockSize >= playField[1] + fieldHeight:
                    orientBlock = True
                if (piecePosition[1] + i < len(cells) and piecePosition[0] + j < len(cells[0])):
                    if cells[piecePosition[1] + i][piecePosition[0] + j]:
                        orientBlock = True


    currentPiece = pieces[piece][pieceOrient]

    for i in xrange(0, len(currentPiece)):
        for j in xrange(0, len(currentPiece[i])):
            if (currentPiece[i][j]):
                piecePos = (
                    playField[0] + piecePosition[0] * blockSize + j * blockSize,
                    playField[1] + piecePosition[1] * blockSize + i * blockSize
                )
                if (piecePosition[0] + j - 1) <= len(cells[0]):
                    if piecePos[0] <= playField[0] or\
                       cells[piecePosition[1] + i][piecePosition[0] + j - 1]:
                        leftBlock = True

                if piecePos[0] + blockSize >= playField[0] + fieldWidth or\
                   cells[piecePosition[1] + i][piecePosition[0] + j + 1]:
                    rightBlock = True

                if piecePosition[1] + i >= len(cells) - 1:
                    verticalBlock = True
                else:
                    if cells[piecePosition[1] + i + 1][piecePosition[0] + j]:
                        verticalBlock = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT + 2:
            blinking = not blinking
        if event.type == pygame.USEREVENT:
            pygame.display.set_caption("Green Tetris - " + str(int(clock.get_fps())))

            if level < 1:
                break

            if not verticalBlock:
                piecePosition = (piecePosition[0], piecePosition[1] + 1)
            else:
                for i in xrange(0, len(currentPiece)):
                    for j in xrange(0, len(currentPiece[i])):
                        piecePos = (
                            playField[0] + piecePosition[0] * blockSize + j * blockSize,
                            playField[1] + piecePosition[1] * blockSize + i * blockSize
                        )

                        if piecePos[1] < playField[1]:
                            level = -1

                        if (currentPiece[i][j]):
                            cells[piecePosition[1] + i][piecePosition[0] + j] = 1

                lowestPoint = len(cells)

                downCount = 0
                for i in xrange(0, len(cells)):
                    if 0 not in cells[i]:
                        cells[i] = [0 for j in xrange(0, cellWidth)]

                        score += 500 * level

                        if (score >= 1000 * level * 5):
                            level += 1

                            if blockDelay > 100:
                                blockDelay -= 100
                                pygame.time.set_timer(pygame.USEREVENT, blockDelay)

                        downCount += 1
                        if i < lowestPoint: lowestPoint = i

                cells = pieceFall(cells, downCount, lowestPoint) if downCount > 0 else cells

                piecePosition = (3, -1)
                pieceOrient = 0

                piece = nextRandomPiece
                nextRandomPiece = random.randint(0, len(pieces) - 1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not leftBlock:
                    piecePosition = (piecePosition[0] - 1, piecePosition[1])
            if event.key == pygame.K_RIGHT:
                if not rightBlock:
                    piecePosition = (piecePosition[0] + 1, piecePosition[1])
            if event.key == pygame.K_UP:
                if not orientBlock:
                    pieceOrient = (pieceOrient + 1) % len(pieces[piece])
            if level == -1:
                if event.key >= K_a and event.key <= K_z or\
                event.key >= K_0 and event.key <= K_9:
                    key = pygame.key.get_pressed()
                    if key[K_LSHIFT] or key[K_RSHIFT]:
                        prompt += pygame.key.name(event.key).upper()
                    else:
                        prompt += pygame.key.name(event.key)
                if event.key == K_SPACE:
                    prompt += " "
                if event.key == pygame.K_BACKSPACE:
                    promptBackspace = True
                    prompt = prompt[:-1]
                if event.key == pygame.K_RETURN and prompt is not "":
                    scoreFile = open("Assets/scores.txt", "a")
                    scoreFile.write("\n" + prompt + ":" + str(score))
                    scoreFile.close()

                    scoreFile = open("Assets/scores.txt")
                    scores = []

                    for s in scoreFile:
                        ss = s.split(":")
                        scores.append([ss[0], int(ss[1].strip('\n'))])

                    scoreFile.close()

                    scores = sorted(scores, key=scoreKeys, reverse=True)

                    score = 0
                    cells = [[0 for i in xrange(0, cellWidth)] for i in xrange(0, cellHeight)]
                    prompt = ""

                    level = -2
                    break
            if level == -2:
                if event.key == pygame.K_RETURN :
                    level = 1

        if event.type == SLIDEDOWN_EVENT:
            if slideDown:
                currentPiece = pieces[piece][pieceOrient]

                for i in xrange(0, len(currentPiece)):
                    for j in xrange(0, len(currentPiece[i])):
                        if (currentPiece[i][j]):
                            piecePos = (
                                playField[0] + piecePosition[0] * blockSize + j * blockSize,
                                playField[1] + piecePosition[1] * blockSize + i * blockSize
                            )
                            if (piecePosition[0] + j - 1) <= len(cells[0]):
                                if piecePos[0] <= playField[0] or\
                                   cells[piecePosition[1] + i][piecePosition[0] + j - 1]:
                                    leftBlock = True

                            if piecePos[0] + blockSize >= playField[0] + fieldWidth or\
                               cells[piecePosition[1] + i][piecePosition[0] + j + 1]:
                                rightBlock = True

                            if piecePosition[1] + i >= len(cells) - 1:
                                verticalBlock = True
                            else:
                                if cells[piecePosition[1] + i + 1][piecePosition[0] + j]:
                                    verticalBlock = True

                if not verticalBlock:
                    piecePosition = (piecePosition[0], piecePosition[1] + 1)

    key = pygame.key.get_pressed()

    rw.fill(C(3))

    if level == -2:
        titleText = "Green Tetris"
        ttSurface = gameTitleFont.render(titleText, 0, C(4))
        ttPos = (WIDTH / 2 - (ttSurface.get_width() / 2), HEIGHT * 0.15)

        ttBgRect = (
            ttPos[0] - ttSurface.get_width() / 2,
            ttPos[1],
            ttSurface.get_width() * 2,
            ttSurface.get_height()
        )

        pygame.draw.rect(rw, C(1), ttBgRect)

        rw.blit(ttSurface, ttPos)

        ttText2 = "Press ENTER"

        tt2Surf = gameOverFont.render(ttText2, 0, C(1))
        tt2Surf.set_alpha(255 * int(blinking))
        tt2Pos = (
            WIDTH / 2 - tt2Surf.get_width() / 2,
            HEIGHT * 0.5
        )

        rw.blit(tt2Surf, tt2Pos)

        tt3 = "Top Scores:"
        tt3Surf = mainFont.render(tt3, 0, C(1))

        tt3Pos = (
            WIDTH / 2 - tt3Surf.get_width() / 2,
            HEIGHT * 0.7
        )

        rw.blit(tt3Surf, tt3Pos)

        for so in xrange(0, len(scores) - (len(scores) - 3)):

            tmpScoreNameTxt = scores[so][0] + ': ' + str(scores[so][1])

            tsnRender = mainFont.render(tmpScoreNameTxt, 0, C(1))

            tsnPos = (
                tt3Pos[0],
                tt3Pos[1]+ tt3Surf.get_height() + tsnRender.get_height() * so
            )

            rw.blit(tsnRender, tsnPos)

        pygame.display.flip()
        clock.tick(60)
        continue

    if level == -1:
        gameOverText = "Game Over"
        gotSurface = gameOverFont.render(gameOverText, 0, C(4))
        gotPos = ((WIDTH / 2) - gotSurface.get_width() / 2, HEIGHT * 0.1)

        pygame.draw.rect(rw, C(1), \
        (gotPos[0] - gotSurface.get_width() / 2, gotPos[1], \
        gotSurface.get_width() * 2, \
        gotSurface.get_height()))

        rw.blit(gotSurface, gotPos)

        yourScoreSurf = gameOverFont.render("Your score: "+ str(score), 0, C(4))
        ysPos = ((WIDTH / 2) - yourScoreSurf.get_width() / 2, HEIGHT / 2,\
        yourScoreSurf.get_width(), yourScoreSurf.get_height())

        pygame.draw.rect(rw, C(1), ysPos)

        rw.blit(yourScoreSurf, ((WIDTH / 2) - yourScoreSurf.get_width() / 2, HEIGHT / 2))

        hsText = ""

        if score > highscore:
            hsText = "New Highscore!"

        hsSurf = gameTitleFont.render(hsText, 0, C(1))
        hsPos = ((WIDTH / 2) - hsSurf.get_width() / 2, HEIGHT * 0.3)
        rw.blit(hsSurf, hsPos)

        # -- Name Prompt --

        npText = "Enter your name: "
        npSurf = gameOverFont.render(npText, 0, C(3))

        npPos = (
            0,
            HEIGHT * 0.7,
            WIDTH,
            yourScoreSurf.get_height() * 2
        )

        pygame.draw.rect(rw, C(1), npPos)

        npNameText = gameOverFont.render(prompt, 0, C(3))

        rw.blit(npSurf, (npPos[0], npPos[1]))
        rw.blit(npNameText, (npPos[0], npPos[1] + npPos[3] / 2))

        pygame.display.flip()
        clock.tick(60)
        continue

    slideDown = key[pygame.K_DOWN]

    pygame.draw.line(rw, C(1), (WIDTH * 0.7, 0), (WIDTH * 0.7, HEIGHT), 5)

    scoreText = mainFont.render("Score:", 0, C(1))
    scoreNumberText = mainFont.render(str(score), 0, C(1))
    rw.blit(scoreText, (scoreField[0] + (scoreFieldWidth / 2) - scoreText.get_width() / 2, 50))
    rw.blit(scoreNumberText, \
    (scoreField[0] + (scoreFieldWidth / 2) - scoreNumberText.get_width() / 2,
    80))

    levelText = mainFont.render("Level:", 0, C(1))
    levelNumberText = mainFont.render(str(level), 0, C(1))
    rw.blit(levelText, (scoreField[0] + (scoreFieldWidth / 2) - levelText.get_width() / 2, 150))
    rw.blit(levelNumberText, \
    (scoreField[0] + (scoreFieldWidth / 2) - levelNumberText.get_width() / 2,
    180,
    ))

    pygame.draw.rect(rw, C(1), playField, 1)

    for i in xrange(0, len(cells)):
        for j in xrange(0, len(cells[i])):
            if cells[i][j]:
                oneRect = (playField[0] + j * blockSize, playField[1] + i * blockSize,\
                 blockSize, blockSize)

                pygame.draw.rect(rw, C(1), oneRect)

    currentPiece = pieces[piece][pieceOrient]

    for i in xrange(0, len(currentPiece)):
        for j in xrange(0, len(currentPiece[i])):
            if currentPiece[i][j]:
                partRect = (playField[0] + piecePosition[0] * blockSize + j * blockSize, \
                playField[1] + piecePosition[1] * blockSize + i * blockSize, \
                blockSize, blockSize)

                pygame.draw.rect(rw, C(1), partRect)

    nrpText = "Next:"
    nptSurf = mainFont.render(nrpText, 0, C(1))

    nptPos = (
        scoreField[0] + scoreFieldWidth / 2 - nptSurf.get_width() / 2,
        280
    )

    rw.blit(nptSurf, nptPos)

    nrPiece = pieces[nextRandomPiece][0]
    for i in xrange(0, len(nrPiece)):
        for j in xrange(0, len(nrPiece[1])):
            if (nrPiece[i][j]):
                pt = (
                    nptPos[0] + j * blockSize - blockSize,
                    nptPos[1] + i * blockSize,
                    blockSize, blockSize
                )

                pygame.draw.rect(rw, C(1), pt)

    if debug_mode:
        nextPiece = pieces[piece][(pieceOrient + 1) % len(pieces[piece])]

        for i in xrange(0, len(nextPiece)):
            for j in xrange(0, len(nextPiece[i])):
                if (nextPiece[i][j]):
                    piecePos = (
                        playField[0] + piecePosition[0] * blockSize + j * blockSize,
                        playField[1] + piecePosition[1] * blockSize + i * blockSize
                    )
                    pygame.draw.rect(rw, (255, 0,0), (piecePos[0], piecePos[1], 10, 10))

    pygame.display.flip()
    clock.tick(60)

sys.exit()
