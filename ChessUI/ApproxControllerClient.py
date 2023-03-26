import json
from JSock import JSock
import time

jsock = JSock()
jsock.Connect("127.0.0.1", 16520)

# jsock.SendStr("CloseServer")


def GetAction():
    result = None
    while True:
        jsock.SendStr("GetAction")
        result = jsock.RecvStr()
        if result == "NoNewAction":
            time.sleep(0.01)
        else:
            break
    return result


# print(GetAction())

# jsock.SendStr("SetState")
# jsock.SendStr(json.dumps(
#     [[0, 1, 2], [11, 12, 6], [7, 8, 9]]
# ))

jsock.SendStr("SetSize")
jsock.SendStr(json.dumps(
    [5, 3]
))
time.sleep(10000)
