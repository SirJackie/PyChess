from .JSock import JSock
import _thread
import json
import time


state = None
hasNewState = False
action = None
hasNewAction = False

wannaClose = False
closeBridgeServer = False

size = None
hasNewSize = False


def ControllerServer():
    global state, hasNewState, action, hasNewAction, size, hasNewSize
    global closeBridgeServer, wannaClose

    jsock = JSock(debug_=False)
    jsock.StartServer(16520)

    while True:
        # noinspection PyBroadException
        try:
            while True:
                jsock.AcceptClient()

                while True:
                    msg = jsock.RecvStr()

                    if msg == "SetState":
                        state = json.loads(jsock.RecvStr())
                        hasNewState = True
                        # print(state)

                    elif msg == "SetSize":
                        size = json.loads(jsock.RecvStr())
                        hasNewSize = True
                        # print("Size:", size)

                    elif msg == "GetAction":
                        if hasNewAction:
                            jsock.SendStr(json.dumps(action))
                            hasNewAction = False
                        else:
                            jsock.SendStr("NoNewAction")

        except BaseException:
            # print("An Error Occurred in Controller Server, Controller Client Might Be Closed.")
            wannaClose = True  # Set the wannaClose, wait for the Controlee to set closeBridgeServer
            pass


def ControleeServer():
    global state, hasNewState, action, hasNewAction, size, hasNewSize
    global closeBridgeServer, wannaClose

    jsock = JSock(debug_=False)
    jsock.StartServer(16521)

    while True:
        # noinspection PyBroadException
        try:
            while True:
                jsock.AcceptClient()

                # If the code runs till here ( AcceptClient() is a blocking function ),
                # The Tkinter Controlee Client may have been connected.

                while True:
                    msg = jsock.RecvStr()

                    if msg == "CloseOrNot":
                        if wannaClose is True:
                            jsock.SendStr("Yes")
                            closeBridgeServer = True
                        else:
                            jsock.SendStr("No")

                    elif msg == "GetState":
                        if hasNewState:
                            jsock.SendStr(json.dumps(state))
                            hasNewState = False
                        else:
                            jsock.SendStr("NoNewState")

                    elif msg == "GetSize":
                        if hasNewSize:
                            jsock.SendStr(json.dumps(size))
                            hasNewSize = False
                        else:
                            jsock.SendStr("NoNewSize")

                    elif msg == "SetAction":
                        action = json.loads(jsock.RecvStr())
                        hasNewAction = True
                        # print(action)

        except BaseException:
            # print("An Error Occurred in Controlee Server, Controlee Client Might Be Closed.")
            wannaClose = True  # Set the wannaClose
            closeBridgeServer = True  # Don't need to wait for the Controller, just set closeBridgeServer
            pass


def BridgeServer():

    # Start Server Threads
    _thread.start_new_thread(ControllerServer, ())
    _thread.start_new_thread(ControleeServer, ())

    # Main Loop
    while not closeBridgeServer:
        time.sleep(1)


if __name__ == "__main__":
    BridgeServer()
