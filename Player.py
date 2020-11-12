from Piece import *
from Chess_board import *


class Player():

    def __init__(self, color, board):
        self.color = color
        color_y = 7
        if color == "black":
            color_y = 0
        self.pieces = [Rook(board.get_square(0, color_y), self), Rook(board.get_square(7, color_y), self),
                    Knight(board.get_square(1, color_y), self), Knight(board.get_square(6, color_y), self),
                    Bishop(board.get_square(2, color_y), self), Bishop(board.get_square(5, color_y), self),
                    Queen(board.get_square(3, color_y), self), King(board.get_square(4, color_y), self)]
        color_y = 6
        if color == "black":
            color_y = 1

        for i in range(8):
            self.pieces.append(Pawn(board.get_square(i, color_y), self))

    """This method will be called after the player has selected a square
        return and draws all the squares in which the selected piece can move"""
    def select_piece(self, square, board, screen, enemy):
        movement_squares = []
        if square.is_occupied():
            if square.piece.color == self.color:
                movement_squares = square.piece.legal_movements(board, enemy, True)

                for s in movement_squares:
                    pygame.draw.circle(screen, (255, 0, 0), s.center, 3)
        return movement_squares

    """Moves the piece
        (this could be done directly by the piece but it's nicer to do it through the player)"""
    def move_piece(self, selected_piece, square, board):
        return selected_piece.move(square, False, board)

    """Removes the piece from the available pieces after it has been caught"""
    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def add_piece(self, piece):
        self.pieces.append(piece)

    """Returns the player's king"""
    def get_king(self):
        for p in self.pieces:
            if isinstance(p, King):
                return p
        return None

    def get_rooks(self):
        rook_list = []
        for p in self.pieces:
            if isinstance(p, Rook):
                rook_list.append(p)
        return rook_list
