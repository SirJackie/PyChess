def printf(sth):
    print(sth, end="")


class ChessBoard:
    info = None
    width = None
    height = None

    def Inspect(self):
        print(self.width, self.height, self.info)

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.info = [[0 for i in range(0, w)] for i in range(0, h)]

    def Draw(self):
        for y in range(0, self.height):
            printf("-" * (1 + 4 * self.width))
            printf("\n")
            printf("| ")
            for x in range(0, self.width):
                printf(self.info[y][x])
                printf(" | ")
            printf("\n")
        printf("-" * (1 + 4 * self.width))


cb = ChessBoard(5, 5)
# cb.Inspect()
cb.Draw()
