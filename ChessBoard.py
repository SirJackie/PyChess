from ChessUI.ChessUI import ChessUI
import time


animationDuration = 0.02  # seconds


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
        # Will Create Latency to UI, Use It Carefully
        for i in range(0, self.iMax):
            for j in range(0, self.jMax):
                print(self.state[i][j], end="")
            print("\n", end="")

    def Draw(self):
        self.ui.SetState(self.state)

    def FallingAnimation(self, jColumn, iTop, iBottom):
        self.Draw()
        for i in range(iTop, iBottom):
            self.state[i+1][jColumn] = self.state[i][jColumn]
            self.state[i][jColumn] = 0
            self.Draw()
            if i == iBottom - 1:
                pass
            else:
                time.sleep(animationDuration)

    def SimulateGravity(self, jColumn):
        for i in range(self.iMax - 1, -1, -1):
            if self.state[i][jColumn] != 0:
                # Full Grid
                pass
            else:
                # Empty Grid, Find one above to make it fall
                for iPrime in range(i - 1, -1, -1):
                    if self.state[iPrime][jColumn] != 0:
                        # Found the Piece to Fall, then Make the Piece Fall
                        self.FallingAnimation(jColumn, iTop=iPrime, iBottom=i)
                        break
                    else:
                        # Continue the Finding Process
                        pass

    def MakeMove(self):
        i, j = self.ui.GetAction()
        i = 0  # You can only put new piece in the top girds
        self.state[i][j] = 1
        self.SimulateGravity(j)
        self.Draw()
