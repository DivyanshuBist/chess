class Square:
    def __init__(self,row,col,piece=None):
        self.row=row
        self.col=col
        self.piece=piece
    
    def __eq__(self,other):
        return self.row==other.row and self.col==other.col

    def has_piece(self):
        return self.piece!=None
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isEmpty_or_enemy(self,color):
        return (not self.has_piece()) or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg<0 or arg>7:
                # print(arg,"\t")
                return False
        # print("\n")
        return True