import numpy as np
#import graphics
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
        self.to_play = 1    # alternate between 1 and 2, refer to self.piece_colors
        self.piece_colors = [" ", "w", "b"]
        self.piece_names = [" ", "P", "R", "N", "B", "Q", "K"]
        
        # these will be flipped when displayed, since graphics.py displays starting from
        # the bottom left square. Also, I figure it makes sense for A1 to be index 0
        
        # castling (O-O w; O-O-O w; O-O b; O-O-O b; en passant file; 50-move rule)
        # en passant will be represented as an integer from -1 (not possible) to 7 (h file)
        # color shouldn't matter as it can be inferred: 3rd rank capture if black to play, 6th otherwise
        # threefold repetition not being implemented yet, but should be able to do by passing
        # in something like the game PGN
        self.meta_info = [1, 1, 1, 1, -1, 0]
        self.pieces = np.array([2, 3, 4, 5, 6, 4, 3, 2,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                2, 3, 4, 5, 6, 4, 3, 2])
    
        self.colors = np.array([1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                2, 2, 2, 2, 2, 2, 2, 2,
                                2, 2, 2, 2, 2, 2, 2, 2])
    
    def get_valid_moves(self):
        """
        Arguments:
            none, as board states are represented in self.
            uses self.meta_info, self.pieces, self.colors
        """
        
        moves = []
        
        return moves
    def make_move(self, squares, override = False):
        """
        Arguments:
            squares (int array): contains the square number for piece move (from and to)
            override (bool): for use with AI to remove need to check if the generated move is valid
        Returns:
            move (str): move made in the form of the 2 squares used. so 1. e4 would return e2e4
            
        castling is represented by selecting the king and then the rook.
        """
        
        '''
        #debug code to make a move whenever possible
        if (squares[0] != None):
            override = True
        '''
        ret = None
        if override:
            #only need to check for castling with the override
            #if it is a king and it is moving 2 laterally:
            if self.pieces[squares[0]] == 6 and abs(squares[0]%8 - squares[1]%8) == 2:
                #self.board[]
                print("CASTLE")
                ret = squares
            else:
                self.pieces[squares[1]] = self.pieces[squares[0]]
                self.colors[squares[1]] = self.colors[squares[0]]
                
                self.pieces[squares[0]] = 0
                self.colors[squares[0]] = 0
                ret = squares
            
            
        if squares[0] != None and self.pieces[squares[0]] != 0:
            self.pieces[squares[1]] = self.pieces[squares[0]]
            self.colors[squares[1]] = self.colors[squares[0]]
            
            self.pieces[squares[0]] = 0
            self.colors[squares[0]] = 0
            ret = squares
        
        if ret != None:
            # swap the player once a move is made
            self.to_play = self.to_play%2 + 1
        return ret
    
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

    def get_fog_squares(self, side = None):
        """
        Arguments:
            side (int, optional): can pass in 0, 1, 2
               0 - show full board
               1 - show white side
               2 - show black side
        Returns:
            fog (int array): all squares that are in the fog of war
        """
        if side == None:
            side = self.to_play
        fog = []
        if self.piece_colors[side] != " ":
            for i in range(len(self.colors)):
                if self.colors[i] != side:
                    fog.append(i)
        print(self.colors)
        print("FOG: " + str(fog))
        return fog
        
        
    def get_board(self, side):
        pass
    
    def get_graphics_board(self):
        ret = []
        fog = self.get_fog_squares(1)
        for i in range(64):
            if self.pieces[i] != 0:
                ret.append(["", i])
                
                # currently the color return is being swapped because of a mismatch between
                # the board state arrays and the board display
                ret[-1][0] += self.piece_colors[self.colors[i]] # get 'b' or 'w'
                ret[-1][0] += self.piece_names[self.pieces[i]]  # get letter for piece
        return ret
        
    def export_fen(self):
        pass
    
    def export_pgn(self):
        pass