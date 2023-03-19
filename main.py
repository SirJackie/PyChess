from ChessUI.ChessUI import ChessUI
import time


class ChessBoard:
    iMax = None
    jMax = None
    state = None
    enableUI = False
    ui = None

    def __init__(self, i, j, enableUI=False):  # i行, j列; width=j, height=i
        self.iMax = i
        self.jMax = j
        self.state = [[0 for j in range(0, self.jMax)] for i in range(0, self.iMax)]
        self.enableUI = enableUI

        if enableUI:
            self.ui = ChessUI(i, j)

    def Inspect(self):
        for i in range(0, self.iMax):
            for j in range(0, self.jMax):
                print(self.state[i][j], end="")
            print("\n", end="")

    def Draw(self):
        self.ui.SetState(self.state)

    def MakePieceFall(self, iP, jP):
        pass

    def SimulateGravity(self, jColumn):
        for i in range(self.iMax - 1, -1, -1):
            if self.state[i][jColumn] != 0:
                # Full Grid
                pass
            else:
                # Empty Grid, Find one above to make it fall
                for iPrime in range(i - 1, -1, -1):
                    if self.state[iPrime][jColumn] != 0:
                        # Found the Piece to Fall
                        break
                    else:
                        # Continue the Finding Process
                        pass
                self.state[i][jColumn] = self.state[iPrime][jColumn]
                self.state[iPrime][jColumn] = 0

    def MakeMove(self):
        i, j = self.ui.GetAction()
        self.state[i][j] = 1
        self.SimulateGravity(j)
        self.Draw()
        self.Inspect()


cb = ChessBoard(9, 9, enableUI=True)

while True:
    cb.MakeMove()
