import json
from JSock import JSock

jsock = JSock()
jsock.Connect("127.0.0.1", 16521)

# jsock.SendStr("CloseOrNot")
# print(jsock.RecvStr())

# jsock.SendStr("GetState")
# print(jsock.RecvStr())

# jsock.SendStr("SetAction")
# jsock.SendStr(json.dumps(
#     [2, 5]
# ))

jsock.SendStr("GetSize")
print(jsock.RecvStr())
