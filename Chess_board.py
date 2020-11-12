from Square import *

class Chess_board:

    def __init__(self):
        self.board = [
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        []
                      ]
        color = "white"
        for i in range(8):
            for j in range(8):
                self.board[i].append(Square(j, i, 60, 60, color))
                if color == "black":
                    color = "white"
                else:
                    color = "black"
            if color == "black":
                color = "white"
            else:
                color = "black"
        print(self.board)

    def get_square(self, x, y):
        return self.board[y][x]

    def draw(self, screen):
        for row in self.board:
            for s in row:
                s.draw(screen)
