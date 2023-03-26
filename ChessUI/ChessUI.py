import os
import json
from .JSock import JSock
import time
from multiprocessing import Process
from .BridgeServer import BridgeServer
from .TkinterControlee import TkinterControlee


class ChessUI:

    jsock = None
    bridgeServer = None
    tkinterControlee = None

    def __init__(self, i, j):  # i行, j列; width=j, height=i
        # Start Bridge Server and Tkinter Controlee Processes
        # os.system("start .\\ChessUI\\Launcher1.vbs")
        # os.system("start .\\ChessUI\\Launcher2.vbs")

        self.bridgeServer = Process(target=BridgeServer)
        self.bridgeServer.start()

        self.tkinterControlee = Process(target=TkinterControlee)
        self.tkinterControlee.start()

        # Connect to the Bridge Server
        self.jsock = JSock(debug_=False)
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
                pass
            else:
                break

        action = json.loads(result)
        return action[0], action[1]

    def SetState(self, state):
        self.jsock.SendStr("SetState")
        self.jsock.SendStr(json.dumps(
            state
        ))
