import pygame
import sys
from Piece import *
from Square import *
from Chess_board import *
from Player import *


class Game:

    def __init__(self):
        self.width = 580
        self.height = 580
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Chess_board()
        self.player_b = Player("black", self.board)
        self.player_w = Player("white", self.board)

    """Game loop"""
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        selected_square = None

        promotion_message = pygame.Rect(50, 50, 400, 300)

        promotion_squares = [pygame.Rect(50, 50, 60, 60), pygame.Rect(50, 50, 60, 60),
                             pygame.Rect(50, 50, 60, 60), pygame.Rect(50, 50, 60, 60)]

        promotion_pieces = ["knight", "bishop", "rook", "queen"]

        for i in range(len(promotion_squares)):
            newX = 90 + 32*(i+1) + i*60 + 30
            promotion_squares[i].center = (newX, self.height/2)
        
        promotion_message.center = (self.width/2, self.height/2)

        movement_squares = []  # the list of squares in which the current player can click and move the selected piece

        current_player = self.player_w

        next_player = self.player_b

        pawn_promotion = False

        promoting_pawn = None

        sysfont = pygame.font.SysFont(pygame.font.get_default_font(), 30)

        while True:
            possible_movements = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # detects the mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if pawn_promotion:
                        for i in range(len(promotion_squares)):
                            if promotion_squares[i].collidepoint(mouse_x, mouse_y):
                                promoting_pawn.promotion(promotion_pieces[i])
                                pawn_promotion = False
                                promoting_pawn = None
                                temp = current_player
                                current_player = next_player
                                next_player = temp
                                for p in current_player.pieces:
                                    possible_movements.extend(p.legal_movements(self.board, next_player, True))
                                if len(possible_movements) == 0:
                                    print('Check mate!')
                    else:
                        for row in self.board.board:
                            for s in row:
                                if s.collidepoint(mouse_x, mouse_y):
                                    if selected_square is not None:
                                        if s == selected_square:  # if the player selects the selected square it will be deselected
                                            s.selected = False
                                            selected_square = None
                                            print('None')
                                        elif s in movement_squares:
                                            """if the player selected a piece, the squares in which it can move will be 
                                                highlighted and if the selected square is one of those squares
                                                the piece will perform the move and the turn will end making the enemy
                                                the current player"""
                                            selected_piece = selected_square.piece
                                            pawn_promotion = current_player.move_piece(selected_square.piece, s, self.board)
                                            if pawn_promotion:
                                                promoting_pawn = selected_piece
                                            else:
                                                temp = current_player
                                                current_player = next_player
                                                next_player = temp
                                                for p in current_player.pieces:
                                                    possible_movements.extend(p.legal_movements(self.board, next_player, True))
                                                if len(possible_movements) == 0:
                                                    print('Check mate!')
                                        else:  # if the player selects different square from the selected square
                                            selected_square.selected = False
                                            s.selected = True
                                            selected_square = s
                                    else:  # if there is not any square selected, simply selects one
                                        s.selected = True
                                        selected_square = s

            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            # draws the pieces in the pieces list of each player
            for w in self.player_w.pieces:
                w.draw(self.screen)
            for b in self.player_b.pieces:
                b.draw(self.screen)
            if pawn_promotion:
                pygame.draw.rect(self.screen, (0, 0, 0), promotion_message)
                message = sysfont.render("Choose one of the following pieces", True, (255, 255, 255))
                r = message.get_rect()
                r.center = (self.width/2, 200)
                self.screen.blit(message, r)
                for i in range(len(promotion_squares)):
                    pygame.draw.rect(self.screen, (255, 255, 255), promotion_squares[i])
                    if current_player.color == 'black':
                        self.screen.blit(pygame.image.load(os.path.join("img", promotion_pieces[i] + "_b.png")),
                                         promotion_squares[i])
                    else:
                        self.screen.blit(pygame.image.load(os.path.join("img", promotion_pieces[i] + "_w.png")),
                                         promotion_squares[i])

            if selected_square is not None:
                movement_squares = current_player.select_piece(selected_square, self.board, self.screen, next_player)

            pygame.display.flip()
            clock.tick(60)
