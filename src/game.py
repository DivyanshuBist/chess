import os
import pygame
from dragger import Dragger
from board import Board
from settings import *
from sound import Sound
class Game:
    def __init__(self):
        self.next_player='white'
        self.board=Board()
        self.dragger=Dragger()
        self.sound=Sound()

    def show_bg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(row+col)%2==0:
                    color=(234,235,200)
                else:
                    color=(119,154,88)
                rect=(col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece()==True:
                    piece=self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img=pygame.image.load(piece.texture)
                        img_center=col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2
                        piece.texture_rect=img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)

    def show_moves(self,surface):
        if self.dragger.dragging:
            piece=self.dragger.piece

            for move in piece.moves:
                color="#C86464" if (move.final.row+move.final.col)%2==0 else "#C84646"

                rect=(move.final.col*SQSIZE,move.final.row*SQSIZE,SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)
    def show_last_move(self,surface):
        if self.board.last_move:
            initial=self.board.last_move.initial
            final=self.board.last_move.final
            for pos in [initial,final]:
                color=(244,247,166) if (pos.row+pos.col)%2==0 else (172,195,51)

                rect=(pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)

    def next_turn(self):
        self.next_player='white' if self.next_player=='black' else 'black'

    def sound_effect(self,capture=False):
        if capture:
            self.sound.capture_sound()
        else:
            self.sound.move_sound()
        
    def new_game(self):
        self.__init__()
            