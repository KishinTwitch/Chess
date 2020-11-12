import pygame
BLACK = (209, 139, 71)

WHITE = (255, 206, 158)

RED = (255, 0, 0)

class Square(pygame.Rect):

    def __init__(self, x, y, w, h, color):
        super().__init__(50 + 60*x, 50 + y*60, w, h)
        self.index_x = x
        self.index_y = y
        self.piece = None
        self.color = color
        self.selected = False

    def is_occupied(self):
        return self.piece is not None

    def draw(self, screen):
        if not self.selected:
            if self.color == "black":
                pygame.draw.rect(screen, BLACK, self)
            else:
                pygame.draw.rect(screen, WHITE, self)
        else:
            pygame.draw.rect(screen, RED, self)
