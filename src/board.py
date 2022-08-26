from move import Move
from settings import *
from square import Square
from pieces import *
import random
import pygame
import copy
from sound import Sound
class Board:
    def __init__(self):
        self.squares=[[0,0,0,0,0,0,0,0] for col in range(COLS) ]
        self.last_move=None
        self.val=bool(random.randint(0,1)) 
        self.p1_color='black' if self.val==1 else 'white'
        self._create()
        self._add_pieces('white',not self.val)              
        self._add_pieces('black',self.val)  

    def move(self,piece,move,testing=False):
        initial=move.initial
        final=move.final
        en_passant_empty= not self.squares[final.row][final.col].has_piece()

        self.squares[initial.row][initial.col].piece=None
        self.squares[final.row][final.col].piece=piece

        #pawn promotion
        if isinstance(piece,Pawn):
            diff=final.col-initial.col
            if diff!=0 and en_passant_empty:
                self.squares[initial.row][initial.col+diff].piece=None
                self.squares[final.row][final.col].piece=piece
                if not testing:
                    sound=Sound()
                    sound.capture_sound()

            else: self.check_promotion(piece,final)
        
        #castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved=True

        piece.clear_moves()

        self.last_move=move


    def valid_move(self,piece,move):
    
        return move in piece.moves

    def check_promotion(self,piece,final):
        
        if final.row==0 or final.row==7: 
            while True:
                pygame.init()
                for event in pygame.event.get(): 
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_q:
                            self.squares[final.row][final.col].piece=Queen(piece.color)
                            return 
                        elif event.key == pygame.K_b:
                            self.squares[final.row][final.col].piece=Bishop(piece.color)
                            return 
                        elif event.key == pygame.K_r:
                            self.squares[final.row][final.col].piece=Rook(piece.color)
                            return 
                        elif event.key == pygame.K_k:
                            self.squares[final.row][final.col].piece=Knight(piece.color)
                            return 
                    else :
                        continue


    def castling(self,initial,final):
        return abs(initial.col-final.col)==2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move,testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_move(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True
        
    def calc_move(self,piece,row,col,bool=True):

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isEmpty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].has_piece()==False:
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            #en_passant
            r=3 if(piece.color==self.p1_color) else 4
            fr=2 if piece.color==self.p1_color else 5
            #left en passant
            if Square.in_range(col-1) and row==r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p=self.squares[row][col-1].piece
                    if isinstance(p,Pawn):
                        if p.en_passant:
                            initial=Square(row,col)
                            final=Square(fr,col-1,p)
                        
                            move=Move(initial,final)

                            if bool :
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else :
                                piece.add_move(move)
            #right en_passant
            if Square.in_range(col+1) and row==r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p=self.squares[row][col+1].piece
                    if isinstance(p,Pawn):
                        if p.en_passant:
                            initial=Square(row,col)
                            final=Square(fr,col+1,p)
                        
                            move=Move(initial,final)

                            if bool :
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else :
                                piece.add_move(move)
        def straightlinemoves(incrs):
            for incr in incrs:
                row_incr,col_incr=incr
                possible_move_row=row+row_incr
                possible_move_col=col+col_incr

                while True:
                
                    if Square.in_range(possible_move_row,possible_move_col):

                        initial=Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final=Square(possible_move_row,possible_move_col,final_piece)

                        move =Move(initial,final)

                        if not self.squares[possible_move_row][possible_move_col].has_piece():
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:break

                    possible_move_row=possible_move_row+row_incr
                    possible_move_col=possible_move_col+col_incr

                    

        def king_moves():
            adjs=[(row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            for possible_move in adjs:
                possible_move_row,possible_move_col=possible_move
                #normal moves
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isEmpty_or_enemy(piece.color):
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)
                        move=Move(initial,final)
                        
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

            if not piece.moved:
                #queen castling
                left_rook=self.squares[row][0].piece
                if isinstance(left_rook,Rook) and left_rook.moved==False:
                    for c in range(1,4):
                        if self.squares[row][c].has_piece():
                            break
                        if c==3:
                            piece.left_rook=left_rook

                            #move rook
                            initial=Square(row,0)
                            final=Square(row,3)
                            moveR=Move(initial,final)
    
                            #move king
                            initial=Square(row,col)
                            final=Square(row,2)
                            moveK=Move(initial,final)
                            

                            if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                            else:
                                # append new move to rook
                                left_rook.add_move(moveR)
                                # append new move king
                                piece.add_move(moveK)
                                
                        
                #king castling
                right_rook=self.squares[row][7].piece
                if isinstance(right_rook,Rook) and right_rook.moved==False:
                    for c in range(5,7):
                        if self.squares[row][c].has_piece():
                            break
                        if c==6:
                            piece.right_rook=right_rook

                            #move rook
                            initial=Square(row,7)
                            final=Square(row,5)
                            moveR=Move(initial,final)
        
                            #move king
                            initial=Square(row,col)
                            final=Square(row,6)
                            moveK=Move(initial,final)
                            
                            if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                            else:
                                # append new move to rook
                                right_rook.add_move(moveR)
                                # append new move king
                                piece.add_move(moveK)

        if isinstance(piece,Pawn): pawn_moves()

        elif isinstance(piece,Knight): knight_moves()

        elif  isinstance(piece,Bishop): straightlinemoves(
            [(-1,-1),
            (-1,1),
            (1,-1),
            (1,1)]
        )
        
        elif isinstance(piece,Rook): straightlinemoves(
            [(-1,0),
            (1,0),
            (0,-1),
            (0,1)]
        )

        elif isinstance(piece,Queen): straightlinemoves(
            [(-1,-1),
            (-1,1),
            (1,-1),
            (1,1),
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
            ]
        )
    
        elif isinstance(piece,King): king_moves()
        

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col]= Square(row,col)
                
    def _add_pieces(self,color,val):
        
        row_other,row_pawn=(7,6) if val==1 else (0,1)
        #pawn
        for cols in range(COLS):
            self.squares[row_pawn][cols]=Square(row_pawn,cols,Pawn(color,val))
        #knight
            self.squares[row_other][1]=Square(row_other,1,Knight(color))
            self.squares[row_other][6]=Square(row_other,6,Knight(color))
        #Bishop
            self.squares[row_other][2]=Square(row_other,2,Bishop(color))
            self.squares[row_other][5]=Square(row_other,5,Bishop(color))
        #Rook
            self.squares[row_other][0]=Square(row_other,0,Rook(color))
            self.squares[row_other][7]=Square(row_other,7,Rook(color))
        
            if (val==1 and color=='black') or (val==0 and color=='white'):
                #Queen
                    self.squares[row_other][4]=Square(row_other,4,Queen(color))
                #King
                    self.squares[row_other][3]=Square(row_other,3,King(color))
            else:  
                #Queen
                    self.squares[row_other][3]=Square(row_other,3,Queen(color))
                #King
                    self.squares[row_other][4]=Square(row_other,4,King(color))