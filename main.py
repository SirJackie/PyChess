from ChessBoard import ChessBoard


if __name__ == "__main__":
    cb = ChessBoard(9, 9, enableUI=True)

    while True:
        cb.MakeMove()
