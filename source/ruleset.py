import numpy as np
import graphics
class Game:
    """
    representation of the board state, separate from Board to represent PGN more efficiently
    """

class Board:
    '''
    EMPTY:  0
    PAWN:   1
    ROOK:   2
    KNIGHT: 3
    BISHOP: 4
    QUEEN:  5
    KING:   6
    
    EMPTY:  0
    WHITE:  1
    BLACK:  2
    May implement fog of war as 3, it seems useful to implementation most likely
    '''
    def __init__(self):
        self.piece_colors = [" ", "w", "b"]
        self.piece_names = [" ", "P", "R", "N", "B", "Q", "K"]
        self.pieces = np.array([2, 3, 4, 5, 6, 4, 3, 2,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                2, 3, 4, 5, 6, 4, 3, 2])
    
        self.colors = np.array([2, 2, 2, 2, 2, 2, 2, 2,
                                2, 2, 2, 2, 2, 2, 2, 2,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1])

    def __str__(self):
        """
        string representation of the board, uses the standard piece letter notations
        """
        ret = ""
        for ind in range(64):
            if self.colors[ind] % 2:
                ret += self.piece_names[self.pieces[ind]]
            else:
                ret += self.piece_names[self.pieces[ind]].lower()
            if ind % 8 == 7:
                ret += "\n"
        return ret[:-1]

    
    def get_board(self, side):
        pass
    
    def get_board_by_file(self):
        ret = []
        for i in range(64):
            if self.pieces[i] != 0:
                ret.append(["", i])
                
                # currently the color return is being swapped because of a mismatch between
                # the board state arrays and the board display
                ret[-1][0] += self.piece_colors[self.colors[i]%2+1] # get 'b' or 'w'
                ret[-1][0] += self.piece_names[self.pieces[i]]  # get letter for piece
        return ret
        
    def export_fen(self):
        pass
    
    def export_pgn(self):
        pass