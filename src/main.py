import pygame,sys
from move import Move
from settings import *
from game import Game
from square import Square
class Main:
    def __init__(self):

        pygame.init()
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,HEIGHT))
        pygame.display.set_caption("Chess")
        self.game=Game()

    def mainloop(self):
        game=self.game
        screen=self.screen
        dragger=self.game.dragger
        board=self.game.board
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    # print(event.pos)
                    clicked_row=dragger.mouseY//SQSIZE
                    clicked_col=dragger.mouseX//SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece()==True:
                        piece=board.squares[clicked_row][clicked_col].piece
                        if piece.color==game.next_player:
                            board.calc_move(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)


                elif event.type==pygame.MOUSEMOTION:
                    # print(dragger.dragging,"\n")
                    if dragger.dragging==True:
                        pos=event.pos
                        dragger.update_mouse(pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)


                elif event.type==pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row=dragger.mouseY//SQSIZE
                        released_col=dragger.mouseX//SQSIZE

                        initial=Square(dragger.initial_row,dragger.initial_col)
                        final=Square(released_row,released_col)
                        move=Move(initial,final)
                        if board.valid_move(dragger.piece,move):
                            capture=board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece,move)

                            board.set_true_en_passant(dragger.piece)
                            #sound
                            game.sound_effect(capture)
                            #show 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            #turn 
                            game.next_turn()
                        dragger.undrag_piece()
                #key_press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        game.new_game()
                        screen=self.screen
                        board=self.game.board
                        dragger=self.game.dragger


                elif event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main=Main()
main.mainloop()