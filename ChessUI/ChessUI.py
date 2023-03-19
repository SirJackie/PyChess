import os
import json
from ChessUI.JSock import JSock
import time


class ChessUI:

    jsock = None

    def __init__(self, i, j):  # i行, j列; width=j, height=i
        # Start Bridge Server and Tkinter Controlee Processes
        os.system("start .\\ChessUI\\Launcher1.vbs")
        os.system("start .\\ChessUI\\Launcher2.vbs")

        # Connect to the Bridge Server
        self.jsock = JSock()
        self.jsock.Connect("127.0.0.1", 16520)

        # Send SetSize Request
        self.jsock.SendStr("SetSize")
        self.jsock.SendStr(json.dumps(
            [j, i]  # width=j, height=i
        ))

    def GetAction(self):
        # Send GetAction Request Repeatedly, Until Gotten
        while True:
            self.jsock.SendStr("GetAction")
            result = self.jsock.RecvStr()
            if result == "NoNewAction":
                time.sleep(0.01)
            else:
                break

        action = json.loads(result)
        return action[0], action[1]

    def SetState(self, state):
        self.jsock.SendStr("SetState")
        self.jsock.SendStr(json.dumps(
            state
        ))
