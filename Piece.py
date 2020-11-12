import pygame
import os


class Piece:
    def __init__(self, square, player):
        self.square = square
        self.square.piece = self
        self.color = player.color
        self.player = player

    """Returns the squares in which the piece can move
        This method is overridden by every specific piece"""
    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        return legal_squares

    """Performs the actual move of the piece
        This method is the same for all the pieces"""
    def move(self, square, sim, board):
        if square.is_occupied():  # if the the square contains an enemy piece, it will be caught
            enemy_piece = square.piece
            enemy_piece.player.remove_piece(enemy_piece)
        self.square.piece = None
        self.square = square
        self.square.piece = self

        return False

    """Scans all the squares in diagonal depending on the direction and 
        returns all the empty ones and the ones with an enemy piece
        directions: NE, NW, SE, SW"""
    def diagonal_movement(self, x, y, board, direction):
        legal_squares = []
        if direction == 'SE':
            i = x + 1
            j = y + 1
            while i <= 7 and j <= 7:
                if board.get_square(i, j).is_occupied():
                    if board.get_square(i, j).piece.color != self.color:
                        legal_squares.append(board.get_square(i, j))
                    break
                legal_squares.append(board.get_square(i, j))
                i += 1
                j += 1
        if direction == 'NE':
            i = x + 1
            j = y - 1
            while i <= 7 and j >= 0:
                if board.get_square(i, j).is_occupied():
                    if board.get_square(i, j).piece.color != self.color:
                        legal_squares.append(board.get_square(i, j))
                    break
                legal_squares.append(board.get_square(i, j))
                i += 1
                j -= 1
        if direction == 'SW':
            i = x - 1
            j = y + 1
            while i >= 0 and j <= 7:
                if board.get_square(i, j).is_occupied():
                    if board.get_square(i, j).piece.color != self.color:
                        legal_squares.append(board.get_square(i, j))
                    break
                legal_squares.append(board.get_square(i, j))
                i -= 1
                j += 1
        if direction == 'NW':
            i = x - 1
            j = y - 1
            while i >= 0 and j >= 0:
                if board.get_square(i, j).is_occupied():
                    if board.get_square(i, j).piece.color != self.color:
                        legal_squares.append(board.get_square(i, j))
                    break
                legal_squares.append(board.get_square(i, j))
                i -= 1
                j -= 1
        return legal_squares

    """Scans all the squares in a strait line depending on the direction and 
        returns all the empty ones and the ones with an enemy piece
        directions: N, S, E, W"""
    def straight_movement(self, x, y, board, direction):
        legal_squares = []
        if direction == 'N':
            for j in range(y - 1, -1, -1):
                if board.get_square(x, j).is_occupied():
                    if board.get_square(x, j).piece.color != self.color:
                        legal_squares.append(board.get_square(x, j))
                    break
                legal_squares.append(board.get_square(x, j))
        if direction == 'E':
            for i in range(x + 1, 8):
                if board.get_square(i, y).is_occupied():
                    if board.get_square(i, y).piece.color != self.color:
                        legal_squares.append(board.get_square(i, y))
                    break
                legal_squares.append(board.get_square(i, y))
        if direction == 'S':
            for j in range(y + 1, 8):
                if board.get_square(x, j).is_occupied():
                    if board.get_square(x, j).piece.color != self.color:
                        legal_squares.append(board.get_square(x, j))
                    break
                legal_squares.append(board.get_square(x, j))
        if direction == 'W':
            for i in range(x - 1, -1, -1):
                if board.get_square(i, y).is_occupied():
                    if board.get_square(i, y).piece.color != self.color:
                        legal_squares.append(board.get_square(i, y))
                    break
                legal_squares.append(board.get_square(i, y))
        return legal_squares

    """Removes all the squares that would create a check if the piece moves into them and
        returns a new list"""
    def check(self, board, movement_squares, enemy):
        check_movements = []

        for s in movement_squares:  # simulates a movement and checks each time if there is a check
            previous_square = self.square
            enemy_piece = s.piece
            self.move(s, True, board)
            np_moves = []

            for p in enemy.pieces:
                np_moves.extend(p.legal_movements(board, enemy, False))

            if self.player.get_king().square not in np_moves:
                check_movements.append(s)

            self.move(previous_square, True, board)

            if enemy_piece is not None:
                enemy_piece.move(s, True, board)
                enemy.pieces.append(enemy_piece)

        return check_movements


class Pawn(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        if player.color == "black":
            self.initial_y = 1  # this is because the pawn needs to know if it is on the initial space
            self.dir = 1  # this is because the pawn can only move forward
            self.img = pygame.image.load(os.path.join("img", "pawn_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "pawn_w.png"))
            self.dir = -1
            self.initial_y = 6

    def move(self, square, sim, board):
        super().move(square, sim, board)

        if not sim:
            if self.square.index_y == self.initial_y + self.dir*6:
                return True

        return False

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        x = self.square.index_x
        y = self.square.index_y

        if y == self.initial_y:  # if the pawn is on the initial space  it can move 2 spaces forward
            if not board.get_square(x, y + self.dir*2).is_occupied():
                legal_squares.append(board.get_square(x, y + self.dir*2))

        if not board.get_square(x, y + self.dir*1).is_occupied():
            legal_squares.append(board.get_square(x, y + self.dir * 1))

        # catch. The pawn is the only piece that has a different way to move and catch
        if x - 1 >= 0 and y + self.dir >= 0:
            square = board.get_square(x - 1, y + self.dir)
            if square.is_occupied():
                if square.piece.color != self.color:
                    legal_squares.append(board.get_square(x - 1, y + self.dir))
        if x + 1 <= 7 and y + self.dir >= 0:
            square = board.get_square(x + 1, y + self.dir)
            if square.is_occupied():
                if square.piece.color != self.color:
                    legal_squares.append(board.get_square(x + 1, y + self.dir))

        # removes the spaces which would produce a check
        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)

        return legal_squares

    def promotion(self, piece):
        if piece == "knight":
            self.player.remove_piece(self)
            self.player.add_piece(Knight(self.square, self.player))
        if piece == "bishop":
            self.player.remove_piece(self)
            self.player.add_piece(Bishop(self.square, self.player))
        if piece == "rook":
            self.player.remove_piece(self)
            self.player.add_piece(Rook(self.square, self.player))
        if piece == "queen":
            self.player.remove_piece(self)
            self.player.add_piece(Queen(self.square, self.player))


class Knight(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        if player.color == "black":
            self.img = pygame.image.load(os.path.join("img", "knight_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "knight_w.png"))

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        x = self.square.index_x
        y = self.square.index_y

        # Encapsulating would be useless
        if y - 2 >= 0 and x + 1 <= 7:  # North
            square = board.get_square(x + 1, y - 2)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 1, y - 2))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 1, y - 2))

        if y - 2 >= 0 and x - 1 >= 0:
            square = board.get_square(x - 1, y - 2)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 1, y - 2))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 1, y - 2))

        ###############################################################################################################

        if x + 2 <= 7 and y + 1 <= 7:  # Est
            square = board.get_square(x + 2, y + 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 2, y + 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 2, y + 1))

        if x + 2 <= 7 and y - 1 >= 0:
            square = board.get_square(x + 2, y - 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 2, y - 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 2, y - 1))

        ###############################################################################################################

        if y + 2 <= 7 and x + 1 <= 7:  # South
            square = board.get_square(x + 1, y + 2)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 1, y + 2))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 1, y + 2))

        if y + 2 <= 7 and x - 1 >= 0:
            square = board.get_square(x - 1, y + 2)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 1, y + 2))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 1, y + 2))

        ###############################################################################################################

        if x - 2 >= 0 and y + 1 <= 7:  # West
            square = board.get_square(x - 2, y + 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 2, y + 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 2, y + 1))

        if x - 2 >= 0 and y - 1 >= 0:
            square = board.get_square(x - 2, y - 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 2, y - 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 2, y - 1))

        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)

        return legal_squares


class Bishop(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        if player.color == "black":
            self.img = pygame.image.load(os.path.join("img", "bishop_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "bishop_w.png"))

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def legal_movements(self, board, enemy, is_current):

        legal_squares = []

        x = self.square.index_x
        y = self.square.index_y

        legal_squares.extend(self.diagonal_movement(x, y, board, 'NE'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'SE'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'NW'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'SW'))

        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)

        return legal_squares


class Rook(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        self.moved = False
        if player.color == "black":
            self.img = pygame.image.load(os.path.join("img", "rook_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "rook_w.png"))

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def move(self, square, sim, board):
        super().move(square, sim, board)
        if not sim:
            self.moved = True

        return False

    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        x = self.square.index_x
        y = self.square.index_y

        legal_squares.extend(self.straight_movement(x, y, board, 'N'))
        legal_squares.extend(self.straight_movement(x, y, board, 'S'))
        legal_squares.extend(self.straight_movement(x, y, board, 'E'))
        legal_squares.extend(self.straight_movement(x, y, board, 'W'))

        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)

        return legal_squares


class Queen(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        if player.color == "black":
            self.img = pygame.image.load(os.path.join("img", "queen_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "queen_w.png"))

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        x = self.square.index_x
        y = self.square.index_y

        legal_squares.extend(self.diagonal_movement(x, y, board, 'NE'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'SE'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'NW'))
        legal_squares.extend(self.diagonal_movement(x, y, board, 'SW'))

        legal_squares.extend(self.straight_movement(x, y, board, 'N'))
        legal_squares.extend(self.straight_movement(x, y, board, 'S'))
        legal_squares.extend(self.straight_movement(x, y, board, 'E'))
        legal_squares.extend(self.straight_movement(x, y, board, 'W'))

        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)

        return legal_squares


class King(Piece):

    def __init__(self, square, player):
        super().__init__(square, player)
        self.moved = False
        if player.color == "black":
            self.img = pygame.image.load(os.path.join("img", "king_b.png"))
        else:
            self.img = pygame.image.load(os.path.join("img", "king_w.png"))

    """draws the piece on the chessBoard"""
    def draw(self, screen):
        screen.blit(self.img, self.square)

    def move(self, square, sim, board):
        if square.is_occupied():  # if the the square contains an enemy piece, it will be caught
            if square.piece.color == self.color:
                self.castling(square, board)
            else:
                enemy_piece = square.piece
                enemy_piece.player.remove_piece(enemy_piece)
                self.square.piece = None
                self.square = square
                self.square.piece = self
        else:
            self.square.piece = None
            self.square = square
            self.square.piece = self
        if not sim:
            self.moved = True

        return False

    def legal_movements(self, board, enemy, is_current):
        legal_squares = []
        x = self.square.index_x
        y = self.square.index_y

        if x + 1 <= 7 and y + 1 <= 7:
            square = board.get_square(x + 1, y + 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 1, y + 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 1, y + 1))

        if x + 1 <= 7:
            square = board.get_square(x + 1, y)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 1, y))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 1, y))

        if x + 1 <= 7 and y - 1 >= 0:
            square = board.get_square(x + 1, y - 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x + 1, y - 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x + 1, y - 1))

        ###########################################################################################################

        if y + 1 <= 7:
            square = board.get_square(x, y + 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x, y + 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x, y + 1))

        if x - 1 >= 0 and y + 1 <= 7:
            square = board.get_square(x - 1, y + 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 1, y + 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 1, y + 1))

        ###########################################################################################################

        if x - 1 >= 0:
            square = board.get_square(x - 1, y)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 1, y))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 1, y))

        if x - 1 >= 0 and y - 1 >= 0:
            square = board.get_square(x - 1, y - 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x - 1, y - 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x - 1, y - 1))

        if y - 1 >= 0:
            square = board.get_square(x, y - 1)
            if not square.is_occupied():
                legal_squares.append(board.get_square(x, y - 1))
            elif square.piece.color != self.color:
                legal_squares.append(board.get_square(x, y - 1))

        if is_current:
            legal_squares = self.check(board, legal_squares, enemy)
            legal_squares.extend(self.get_castling_squares(board, enemy))

        return legal_squares

    def get_castling_squares(self, board, enemy):
        y = self.square.index_y
        available_squares = []
        if not self.moved:
            print('King not moved')
            available_rooks = self.player.get_rooks()
            print(len(available_rooks))

            for r in available_rooks:
                print(r.square.index_x, r.square.index_y)
                if not r.moved:
                    is_free = True
                    first_square = None
                    second_square = None
                    if r.square.index_x < self.square.index_x:  # left rook
                        first_square = board.get_square(3, y)
                        second_square = board.get_square(4, y)
                        for i in range(1, 4):
                            if board.get_square(i, y).is_occupied():
                                is_free = False

                    elif r.square.index_x > self.square.index_x:
                        first_square = board.get_square(5, y)
                        second_square = board.get_square(6, y)
                        for i in range(5, 7):
                            if board.get_square(i, y).is_occupied():
                                is_free = False
                    if is_free:
                        c_square = [first_square, second_square]
                        np_moves = []
                        is_attacked = False
                        for p in enemy.pieces:
                            np_moves.extend(p.legal_movements(board, enemy, False))
                        for s in c_square:
                            if s in np_moves:
                                is_attacked = True
                        if not is_attacked:
                            available_squares.append(r.square)
        return available_squares



    def castling(self, square, board):
        y = self.square.index_y
        rook = square.piece
        if square.index_x < self.square.index_x: # left rook
            self.move(board.get_square(2, y), False, board)
            rook.move(board.get_square(3, y), False, board)
        else:
            self.move(board.get_square(6, y), False, board)
            rook.move(board.get_square(5, y), False, board)



