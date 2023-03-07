def printf(sth):
    print(sth, end="")


class ChessBoard:
    info = None
    width = None
    height = None

    def Inspect(self):
        print(self.width, self.height, self.info)

    def __init__(self):
        # self.info = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.info = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.width = 3
        self.height = 3

    def Draw(self):
        for y in range(0, self.height):
            printf("-------------")
            printf("\n")
            printf("| ")
            for x in range(0, self.width):
                printf(self.info[y][x])
                printf(" | ")
            printf("\n")
        printf("-------------")


cb = ChessBoard()
# cb.Inspect()
cb.Draw()
