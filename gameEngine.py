import math
import random

import mediaEngine

#

placementTimerIncrement = 0
eraseTimerIncrementMultiplier = 1.5
readyBoardWIDTH = 6

readyBoardHEIGHT = 18


class GameState:
    Music = mediaEngine.MusicPlayer()

    idx = -1
    itemIdx = 0
    readyRemain = 3

    def __init__(self):
        self.counter = 40      # time count

        self.M = Magic()
        self.magicCounter = 30

        self.placementCount = 0
        self.eraseCount = 0
        self.totalPoint = 0
        self.readyList = [Block(), Block(), Block()]

        self.magicList = ["__", "__","__"]

        self.board = [
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__", "__"]
        ]

        self.readyboardW = 6
        self.readyboardH = 18
        self.readyBoard = [
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__"]

        ]
        self.maintainReadyList(0, True)
        self.idx = self.getFirstAvailableReadyIndex()
        self.LOSE = False
        self.FitList = self.checkFit()
        self.Music.playBg()

    """ board function """

    def placeBlock(self, action, index):
        if self.idx == -1 or self.readyList[self.idx] == "__":
            return
        p = 0
        p2 = 0
        if self.validateAction(action):
            self.Music.playPlacementSound()
            # basic Info
            row = action.targetRow
            col = action.targetCol

            # draw
            for w in range(action.info[1]):
                for h in range(action.info[0]):
                    if action.info[2 + h * action.info[1] + w] != 0:
                        self.board[row + h][col + w] = "**"

            self.readyRemain -= 1

            self.maintainReadyList(index)
            if (not self.readyListIsFull()):
                if (self.idx >= len(self.readyList) // 2):
                    if self.idx <= self.getFirstAvailableReadyIndex():
                        self.idx = self.seekClosestReadyIndex(1)
                    else:
                        self.idx = self.seekClosestReadyIndex(0)
                else:
                    self.idx = self.seekClosestReadyIndex(1)

            # Point Update
            p2 = self.boardUpdate(action)
            p = self.getPlacementPoint(action.blockType)
            self.totalPoint += p2 + p

            # Timer Update
            self.counter += placementTimerIncrement

    def boardUpdate(self, action):
        p = 0
        info = action.info
        targetCol = action.targetCol
        targetRow = action.targetRow

        potentialCol = []
        potentialRow = []
        potentialSquare = []

        for row in range(0, info[0]):
            potentialRow.append(row + targetRow)

        for col in range(0, info[1]):
            potentialCol.append(col + targetCol)

        for row in potentialRow:
            for col in potentialCol:
                potentialSquare.append([row // 3, col // 3])

        temp = []
        for elem in potentialSquare:
            if elem not in temp:
                temp.append(elem)
        potentialSquare = temp

        # line Erase: [[x,y,direction = 0 (horizontal) ], [x,y, direction = 1(vertical) ]]
        lineErase = []

        # square Erase: [[x,y] left-top, count by 3*3 square not pixel]
        squareErase = []

        # row check
        for row in potentialRow:
            erase = True
            for i in range(9):
                if self.board[row][i] == "__":
                    erase = False
                    break
            if erase:
                lineErase.append([row, 0])

        # col check
        for col in potentialCol:
            erase = True
            for i in range(9):
                if self.board[i][col] == "__":
                    erase = False
                    break
            if erase:
                lineErase.append([col, 1])

        # 3*3 check
        for square in potentialSquare:
            # left top pixel [x,y]
            x = square[1] * 3
            y = square[0] * 3

            erase = True
            for i in range(3):
                for j in range(3):
                    if self.board[y + i][x + j] == "__":
                        erase = False

            if erase:
                squareErase.append((x, y))

        exp = len(lineErase) + len(squareErase)
        basePoint = 8 * len(lineErase) + 9 * len(squareErase)
        p = pow(basePoint, math.sqrt(exp))

        if exp > 0:
            degree = exp if exp <= 4 else 4
            self.Music.playEraseSound(degree)
        # Erase

        for k in lineErase:
            dir = k[1]
            l = k[0]
            if dir == 0:  # row erase
                for i in range(9):
                    self.board[l][i] = "__"

            else:
                for i in range(9):
                    self.board[i][l] = "__"

        for k in squareErase:
            x = k[1]
            y = k[0]

            for i in range(3):
                for j in range(3):
                    self.board[x + i][y + j] = "__"

        if p == 1:
            return 0
        else:
            self.counter += basePoint * eraseTimerIncrementMultiplier
            foundEmptySlot = False
            for i in range(len(self.magicList)):
                if self.magicList[i] == "__":
                    self.magicList[i] = self.M.getMagic(exp)
                    foundEmptySlot = True
                    break
            if not foundEmptySlot:
                replace = random.randint(0,2)
                self.magicList[replace] = self.M.getMagic(exp)
            return int(p)

    """ validate function """

    def checkFit(self):
        fitList = []
        for i in range(len(self.readyList)):
            fit = False
            readyBlock = self.readyList[i]
            if readyBlock != "__":  # need to check fit, not fit = gray.
                info = readyBlock.getInfo()
                blockRow = info[0]
                blockCol = info[1]
                for r in range(len(self.board)):
                    for c in range(len(self.board[0])):
                        if self.board[r][c] == "__":
                            tempFit = True
                            for i in range(blockRow):
                                for j in range(blockCol):
                                    if r + i >= len(self.board) or c + j >= len(self.board):
                                        tempFit = False
                                        break
                                    if info[2 + i * blockCol + j] == 1:
                                        if self.board[r + i][c + j] != "__":
                                            tempFit = False
                                    if not tempFit:
                                        break
                            if tempFit:
                                fit = True
                                break
            fitList.append(fit)

        return fitList

    def validateAction(self, action):
        valid = True
        # basic Info
        row = action.targetRow
        col = action.targetCol
        info = action.info
        height = info[0]
        width = info[1]
        cnt = 2
        # seek board
        for r in range(row, row + height):
            for c in range(col, col + width):
                if r >= len(self.board) or c >= len(self.board[0]):
                    valid = False
                    break

                if self.board[r][c] != "__" and info[cnt] == 1:
                    valid = False
                    break
                cnt += 1
        return valid

    def checkFitForCurrentSquare(self, block, r, c):
        action = Action(self.readyList, self.idx, (r, c))
        if self.validateAction(action):
            return True
        else:
            return False

    """ Ready List Function """

    def maintainReadyList(self, blockPlaced, new=False):

        if new:
            for i in range(len(self.readyList)):
                self.readyList[i] = Block(random.choice(list(Block.blockDictionary.keys())))
        else:

            self.readyList[blockPlaced] = "__"
            # clear readyBoard for this blockPlaced Index

            if self.readyRemain == 0:
                GameState.idx = -1
                for i in range(len(self.readyList)):
                    self.readyList[i] = Block(random.choice(list(Block.blockDictionary.keys())))
                self.readyRemain = 3
        self.FitList = self.checkFit()
        self.readyBoardUpdate(blockPlaced)

    def readyBoardUpdate(self, index):
        for k in range(len(self.readyBoard)):
            for j in range(len(self.readyBoard[0])):
                if self.readyBoard[k][j] != "__":
                    self.readyBoard[k][j] = "__"

        for idx in range(len(self.readyList)):
            if self.readyList[idx] != "__":
                info = self.readyList[idx].info

                # CENTERING
                width = info[1]
                height = info[0]

                x_offset = (readyBoardWIDTH // 2 - width // 2) if (
                        readyBoardWIDTH // 2 - width // 2 + width <= 6) else 0
                y_offset = (readyBoardHEIGHT // 2 // 3 - height // 2) if (
                        readyBoardHEIGHT // 3 // 2 - height // 2 + height <= 6) else 0

                for c in range(info[1]):
                    for r in range(info[0]):

                        if info[2 + r * info[1] + c] != 0:
                            self.readyBoard[y_offset + r + idx * 6][x_offset + c] = "**"
                        else:
                            self.readyBoard[y_offset + r + idx * 6][x_offset + c] = "__"

    def readyListIsFull(self):
        for b in self.readyList:
            if b == "__":
                return False
        return True

    """ Magic/ Item Function"""

    def use_magic(self, name, idx, row, col):
        return self.bomb(name, idx, row, col)

    def bomb(self, name, idx, row, col):
        point = 0
        if name == "__":
            return

        if self.validateMagic(name,row, col):
            self.magicList[idx] = "__"
            eraseWidth = Magic.magicDictionary[name][1]
            eraseHeight = Magic.magicDictionary[name][0]

            for i in range(eraseWidth):
                for j in range(eraseHeight):
                    if self.board[row + j][col + i] != "__":
                        self.board[row + j][col + i] = "__"
                        point += 1
        return point

    def validateMagic(self, name, row, col):
        b = self.board
        magicDimension = Magic.magicDictionary[name]
        width = magicDimension[1]
        height = magicDimension[0]
        if 0 <= row + height <= len(b) and 0 <= col + width <= len(b[0]):
            return True
        else:
            return False

    def maintainMagicList(self):
        if self.magicCounter <= 0 and len(self.magicList) <= 3:
            self.magicCounter = 30

            for i in range(len(self.magicList)):
                if self.magicList[i] == "__":
                    self.magicList[i] = self.M.getMagic(0)
                    break
        self.FitList = self.checkFit()


    """
    Other Helper Function
    """

    def clearBoard(self):
        self.__init__()

    def undo(self):
        pass

    ## helper functions
    def getTotalPoint(self):
        return self.totalPoint

    def getPlacementPoint(self, BlockType):
        n = Block.blockPoint[BlockType]
        return n

    def addErasePoint(self, n):
        self.eraseCount += n

    def setPlacementTimeIncrement(self, n):
        placementTimerIncrement = n

    def setEraseTimeIncrementMultiplier(self, p):
        eraseTimerIncrementMultiplier = p

    def getFirstAvailableReadyIndex(self):
        cnt = 0
        for b in self.readyList:
            if b != "__":
                return cnt
            cnt += 1

        return cnt

    def seekClosestReadyIndex(self, dir):
        res = self.idx
        if dir == 1:
            if self.idx == len(self.readyList) - 1:
                res = self.idx
            else:
                for b in range(self.idx + 1, len(self.readyList)):
                    if self.readyList[b] != "__":
                        res = b
                        break
        else:
            if self.idx == 0:
                res = self.idx
            else:
                for b in range(self.idx - 1, -1, -1):

                    if self.readyList[b] != "__":
                        res = b
                        break
        return res


class Action:
    def __init__(self, readyList, index, location):
        self.targetRow = location[0]
        self.targetCol = location[1]
        self.block = readyList[index]
        self.blockType = self.block.getType()
        self.dimension = (self.block.getInfo()[0], self.block.getInfo()[1])
        self.info = self.block.getInfo()


class Block:
    # block type indexed in GameState
    blockDictionary = {"square": (2, 2, 1, 1, 1, 1), "Z": (2, 3, 1, 1, 0, 0, 1, 1), "rZ": (2, 3, 0, 1, 1, 1, 1, 0),
                       "I2": [2, 1, 1, 1], "I3": [3, 1, 1, 1, 1], "-2": [1, 2, 1, 1], "-3": [1, 3, 1, 1, 1],
                       "dot": [1, 1, 1], "T": [3,3,1,1,1,0,1,0,0,1,0], "vZ": [3,2,1,0,1,1,0,1],
                       "vrz":[3,2,0,1,1,1,1,0], "+": [3,3,0,1,0,1,1,1,0,1,0],
                       "L": [3,2,1,0,1,0,1,1], "rL": [3,2,0,1,0,1,1,1], "iL":[3,2,1,1,1,0,1,0], "irL": [3,2,1,1,0,1,0,1],
                       "vL": [2,3,1,0,0,1,1,1], "vrL": [2,3,0,0,1,1,1,1],"ivL": [2,3,1,1,1,1,0,0], "irvL":[2,3,1,1,1,0,0,0,1]

                       }
    blockPoint = {"square": 4, "Z": 4, "rZ": 4, "I2": 2, "I3": 3, "-2": 2, "-3": 3, "dot": 1, "T": 5, "vZ": 4, "vrz": 4,
                  "+": 5, "L": 4, "rL":4, "iL": 4, "irL":4, "vL" : 4, "vrL":4, "ivL":4, "irvL":4 }

    def __init__(self, blockType="I2"):
        self.blockType = blockType
        self.info = Block.blockDictionary[blockType]
        self.x_len = self.info[1]
        self.y_len = self.info[0]

    def getInfo(self):
        return self.info

    def getType(self):
        return self.blockType


class Magic:
    magicDictionary = {}
    rarity = {}

    def __init__(self):

        for i in range(1,6):
            for j in range(1,6):
                s = str(i) + str(j)
                self.magicDictionary[s] = [i, j]

        for i in range(5):
            self.rarity[i] = []

        for name in self.magicDictionary.keys():
            info = self.magicDictionary[name]
            area = info[0] * info[1]
            if area <= 1:
                self.rarity[0].append(name)
            elif area <= 4:
                self.rarity[1].append(name)
            elif area <= 9:
                self.rarity[2].append(name)
            elif area <= 16:
                self.rarity[3].append(name)
            elif area <= 25:
                self.rarity[4].append(name)
        print(self.rarity)
    def getMagic(self, rarity):
        name = random.choice(self.rarity[rarity])
        return name

    def getBombDimension(self, name):
        return [self.magicDictionary[name][0], self.magicDictionary[name][1]]
