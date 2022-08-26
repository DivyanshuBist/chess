import os 


class Pieces:
    def __init__(self,name,color,value,texture=None,texture_rect=None):
        self.name=name
        self.color=color
        value_Sign=1 if color=='white' else -1
        self.moves=[]
        self.moved=False
        self.value=value*value_Sign
        self.texture=texture
        self.set_texture()
        self.texture_rect=texture_rect


    def set_texture(self,size=80):
        self.texture=os.path.join(
            f"../assets/images/imgs-{size}px/{self.color}_{self.name}.png"
        )
    def add_move(self,move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves=[]

class Pawn(Pieces):
    def __init__(self,color,val):           #updated
        self.dir=-1 if val==1 else 1
        self.en_passant=False
        super().__init__('pawn',color,1.0)

class Knight(Pieces):
    def __init__(self,color):
        super().__init__('knight',color,3.0)
        
class Bishop(Pieces):
    def __init__(self,color):
        super().__init__('bishop',color,3.001)

class Rook(Pieces):
    def __init__(self,color):
        super().__init__('rook',color,5.00)

class Queen(Pieces):
    def __init__(self,color):
        super().__init__('queen',color,9.00)

class King(Pieces):
    def __init__(self,color):
        self.left_rook=None
        self.right_rook=None
        super().__init__('king',color,10000.0)