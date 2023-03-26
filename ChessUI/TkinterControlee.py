import tkinter as tk
from .NativeAPI import EnableHighDPIMode, GetScreenResolution
import json
from .JSock import JSock
import time

# Preferences
highDPI = True
root = None
jsock = None
canvas = None

# Global Variables
halfGridSize = None
root = None
canvas = None
jsock = None
width = None
height = None


def CreateWindow(width, height, title):
    root = tk.Tk()
    root.geometry(str(width) + "x" + str(height) + "+10+10")
    root.title(title)
    return root


def CreateCanvas(root, x, y, width, height):
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.place(x=x, y=y)
    return canvas


def CreateCircle(canvas, x, y, width, fill, outline):
    tkOffsetBugfix = int(0.13 * width)
    canvas.create_oval(
        x + tkOffsetBugfix,
        y + tkOffsetBugfix,
        x + tkOffsetBugfix + width,
        y + tkOffsetBugfix + width,
        fill=fill, outline=outline
    )


def CreatePiece(canvas, i, j, halfGridSize, fill, outline):
    y = i
    x = j
    CreateCircle(canvas, x * 2 * halfGridSize, y * 2 * halfGridSize, int(0.85 * halfGridSize * 2), fill, outline)


def RedrawChessboard(canvas):
    canvas.delete("all")

    # Horizontal
    for dy in range(0, height):
        x1 = halfGridSize
        y1 = halfGridSize + dy * 2 * halfGridSize
        x2 = halfGridSize + (width - 1) * 2 * halfGridSize
        y2 = halfGridSize + dy * 2 * halfGridSize
        canvas.create_line(x1, y1, x2, y2)

    # Vertical
    for dx in range(0, width):
        x1 = halfGridSize + dx * 2 * halfGridSize
        y1 = halfGridSize
        x2 = halfGridSize + dx * 2 * halfGridSize
        y2 = halfGridSize + (height - 1) * 2 * halfGridSize
        canvas.create_line(x1, y1, x2, y2)


def MouseClickCallback(event):
    mx, my = event.x, event.y

    i = my // (2 * halfGridSize)
    j = mx // (2 * halfGridSize)
    # print(i, j)

    # CreatePiece(canvas, i, j, halfGridSize, fill="black", outline="black")
    jsock.SendStr("SetAction")
    jsock.SendStr(json.dumps(
        [i, j]
    ))


def IntervalFunction():

    # Close or Not
    jsock.SendStr("CloseOrNot")
    result = jsock.RecvStr()
    if result == "Yes":
        root.destroy()

    # GetState
    jsock.SendStr("GetState")
    result = jsock.RecvStr()
    if result != "NoNewState":
        RedrawChessboard(canvas)
        result = json.loads(result)
        for i in range(0, len(result)):
            for j in range(0, len(result[i])):
                if result[i][j] == 1:
                    CreatePiece(canvas, i, j, halfGridSize, fill="black", outline="black")
                elif result[i][j] == 2:
                    CreatePiece(canvas, i, j, halfGridSize, fill="white", outline="white")
                elif result[i][j] == 3:
                    CreatePiece(canvas, i, j, halfGridSize, fill="black", outline="red")
                elif result[i][j] == 4:
                    CreatePiece(canvas, i, j, halfGridSize, fill="white", outline="red")

    root.after(1, IntervalFunction)


def TkinterControlee():
    global highDPI, halfGridSize, root, canvas, jsock, width, height

    if highDPI:
        EnableHighDPIMode()

    screenResolution = GetScreenResolution()
    # print(screenResolution)

    # Get Chessboard Size
    jsock = JSock(debug_=False)
    jsock.Connect("127.0.0.1", 16521)
    width = None
    height = None
    while True:
        jsock.SendStr("GetSize")
        result = jsock.RecvStr()
        # print(result)
        if result != "NoNewSize":
            result = json.loads(result)
            width = result[0]
            height = result[1]
            break
        else:
            pass

    if highDPI:
        halfGridSize_Mode1 = int(0.03 * screenResolution[1])
        halfGridSize_Mode2 = int(0.5 * 0.95 * screenResolution[1] / height)
        halfGridSize_Mode3 = int(0.5 * 0.95 * screenResolution[0] / width)
        halfGridSize = min(halfGridSize_Mode1, halfGridSize_Mode2, halfGridSize_Mode3)
    else:
        halfGridSize = 15
    # print(halfGridSize)

    winWidth = width * 2 * halfGridSize
    winHeight = height * 2 * halfGridSize

    root = CreateWindow(winWidth, winHeight, "ChessUI")
    canvas = CreateCanvas(root, 0, 0, winWidth, winHeight)

    RedrawChessboard(canvas)

    canvas.bind("<Button-1>", MouseClickCallback)

    # Set Network Socket Interval
    root.after(1, IntervalFunction)

    root.mainloop()


if __name__ == "__main__":
    TkinterControlee()
