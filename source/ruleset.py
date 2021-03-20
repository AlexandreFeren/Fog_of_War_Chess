import numpy as np

"""
tests to make:
    working:
        pawn move obstructed
        double pawn move obstructed
        pawn captures
    untested
        capture en passant
        capture en passant after another move
        castle after rook captured, but king and rook haven't moved
        desync of color and piece type (if one board is 0, so should be the other)

"""


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
        
        #dictionary mapping piece names to functions for move generation
        self.piece_move_functions = {1: self.get_pawn_moves, 2: self.get_rook_moves, 3: self.get_knight_moves, 
                                     4: self.get_bishop_moves, 5: self.get_queen_moves, 6: self.get_king_moves}
        
        # these will be flipped when displayed, since graphics.py displays starting from
        # the bottom left square. Also, I figure it makes sense for A1 to be index 0
        
        # castling (O-O w; O-O-O w; O-O b; O-O-O b; en passant file; 50-move rule)
        # en passant will be represented as an integer from -1 (not possible) to 7 (h file)
        # color shouldn't matter as it can be inferred: 3rd rank capture if black to play, 6th otherwise
        # threefold repetition not being implemented yet, but should be able to do by passing
        # in something like the game PGN
        #                   K   Q   k   q   en-passant file   50-move rule
        self.meta_info = [  1,  1,  1,  1,  -1,               0]
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
    
    
    def validate_move(self, squares, promotion = None):
        """
        Used to validate that a move from the user would be legal in the position
        
        Arguments:
            squares (int array): contains the square number for piece move (from and to)
                                 since moves need to be reversible, this only will be able to match
                                 the first 2 elements of a move
        Returns:
            move (str): move made in the form of the 2 squares used. so 1. e4 would return e2e4
            
        castling is represented by selecting the king and then the rook.
        """
        ret = None
        #check that 2 squares have been selected
        if squares[0] != None and self.pieces[squares[0]] != 0:
            #if the move is legal, find out by comparing to the first 2 elements of each move
            for i in self.get_valid_moves():
                if squares == i[:2]:
                    if i[3] == 1 or i[3] == 2 or i[3] == 3 or i[3] == 4:
                        #give option for promotion
                        if promotion == None:
                            ret = "promote"
                            return ret      # need to avoid swapping side
                        else:
                            # if the move has the same promotion value, make it
                            if i[3] == promotion:
                                ret = self.make_move(i)
                    else:
                        ret = self.make_move(i)
        
        if ret != None:
            # swap the player once a move is made
            self.to_play = self.to_play%2 + 1
        
        return ret
        
        
    def make_move(self, move):
        """
            Called by validate_move or by the AI when making a move will make a move with no validation
            
            Arguments:
                move (int array): validated move in the form of [int, int, int] where the ints are the squares to be moved to/from,
                                     and the piece to be promoted to if relevant
            Returns:
                modifies the state of the board to fit the given move
        """
        #if the selected square is a king and it is moving over by 2
        ret = None
        print("make_move start")
        print(self.meta_info)
        #self.meta_info[4] = -1  #reset en passant tracker, needed info is stored in move[3]
        
        if move[3] == 0:    # no special work to be done
            self.pieces[move[1]] = self.pieces[move[0]]
            self.colors[move[1]] = self.to_play
            
            self.pieces[move[0]] = 0
            self.colors[move[0]] = 0
            ret = move
            self.meta_info[4] = -1 # reset en passant

            
        elif move[3] < 5:   # promoting a pawn
            self.pieces[move[1]] = move[3] + 1  # add 1 because the move info is shifted by 1 (no pawn promotion)
            self.colors[move[1]] = self.to_play
            
            self.pieces[move[0]] = 0
            self.colors[move[0]] = 0
            ret = move
            self.meta_info[4] = -1 # reset en passant

        elif move[3] == 5:
            # takes en passant
            self.pieces[move[1]] = self.pieces[move[0]]
            self.colors[move[1]] = self.to_play
            
            if self.to_play == 1:
                self.pieces[move[1] - 8] = 0
                self.colors[move[1] - 8] = 0
            else:
                self.pieces[move[1] + 8] = 0
                self.colors[move[1] + 8] = 0
            
            self.pieces[move[0]] = 0
            self.colors[move[0]] = 0

            
            #raise NotImplementedError("en passant not implemented")
            
            
            ret = move
            self.meta_info[4] = -1 # reset en passant

        elif move[3] == 6:
            # makes en passant possible, so add the file the pawn moved on to the en passant meta info
            print("en passant possible", move[0])            # note that it is possible to take en passant this turn

            self.meta_info[4] = move[0]%8

            self.pieces[move[1]] = self.pieces[move[0]]
            self.colors[move[1]] = self.to_play
            
            self.pieces[move[0]] = 0
            self.colors[move[0]] = 0
            ret = move
            
        elif move[3] == 7:
            # castle short
            raise NotImplementedError("short castle not implemented")
            ret = move
            self.meta_info[4] = -1 # reset en passant

        elif move[3] == 8:
            # castle long
            raise NotImplementedError("long castle not implemented")
            ret = move
            self.meta_info[4] = -1 # reset en passant

        else:
            # doesn't catch negative values, and will assume it is a pawn promotion
            raise ValueError("Invalid move information in move[3]")
            ret = move
            
        return ret
        
    def get_valid_moves(self):
        """
        Arguments:
            none, as board states are represented in self.
            uses self.meta_info, self.pieces, self.colors
        Returns:
            moves (2D int array): each element is a move.
                [0]: move from  (0-63)
                [1]: move to    (0-63)
                [2]: captured piece type (0-6)
                    0: no capture
                    1: Pawn
                    2: Rook
                    3: Knight
                    4: Bishop
                    5: Queen
                    6: King
                [3]: promotion/other information
                    0: no other information
                    1: =R
                    2: =N
                    3: =B
                    4: =Q
                    5: takes en passant
                    6: makes en passant possible
                    7: O-O
                    8: O-O-O
        """
        
        moves = []
        #check all squares
        for i in range(64):
            # if the piece belongs to the person that is to play
            if self.colors[i] == self.to_play:
                for move in self.piece_move_functions[self.pieces[i]](i):
                    if len(move) != 4:
                        print("Bad move input")
                    moves.append(move)
                    
        return moves
    
    def to_algebraic_notation(self, moves = None, move = None):
        """
        Arguments:
            moves (2D int array): moves to convert in the form of [int, int, int, int] where these are the board coords from 0-63,
                                  the piece captured (if any), and the piece promoted to (if any)
        returns:
            algebraic (string array): moves in algebraic notation ie) Nf3, e4, ...
            if ambiguous, clear up ambiguity line Nef3 or maybe even Ne1f3 if necessary
        """
        
        algebraic = []
        for i in moves:
            algebraic.append(self._to_algebraic_notation(i))    
        
        return algebraic
        
    def _to_algebraic_notation(self, move):
        """
        Helper function so that single moves may be generated as well
        
        Arguments:
            move (int array): single move to convert into algebraic notation
        Returns:
            ret (string): move to be made, in algebraic notation
        """
    
        ret = ""
        # piece name
        if self.pieces[move[0]] >= 2:
            ret += self.piece_names[self.pieces[move[0]]]
        
        # optional specification for disambiguation. for now, just specifying for anything that
        # is not a pawn, and files always because of possible ambiguous pawn captures
        if True:
            # if another piece of this type could move to that square from a different file
            ret += chr(move[0]%8 + ord("a"))
        if ret != "":
            # if another piece of this type could move to that square from a different rank
            # and the file doesn't disambiguate it
            ret += str(int(move[0]/8) + 1)
        
        # optional x for takes
        if self.pieces[move[1]] != 0:
            ret += "x"
        
        ret += chr(move[1]%8 + ord("a"))
        ret += str(int(move[1]/8) + 1)
        
        # in standard chess, here there is +, ++, and #, but these are being omitted
        # since checks don't matter, and # just denotes the end of a game
        return ret
    
    def get_pawn_moves(self, square):
        """
        Arguments:
            square (int): the square that the pawn lies on
        returns:
            moves (2D int array): all legal moves for the given pawn, in the form noted in get_valid_moves
        """
        # moves in the form of move =[square 1, square 2]
        moves = []
        if self.to_play == 1: # white to move
            if int(square/8) == 4:
                # check for en passant
                # will be on neighboring files, so if difference in mods is 1
                if self.meta_info[4] >= 0:

                    # en passant possible somewhere
                    if abs(self.meta_info[4] - square%8) == 1:
                        #                     en passant file + shift to piece to take
                        moves.append([ square, self.meta_info[4] + 40,
                                       1, 5])
            
            #single pawn move and path not obstructed
            if self.pieces[square + 8] == 0:
                # double pawn move, no need to check for promotions
                if (int(square/8) == 1 and                  # if on the second rank
                        self.pieces[square + 16] == 0):     # and 2 squares forward is empty
                    moves.append([square, square + 16, 0, 6])
                    #self.meta_info[4] = square%8
                if (square/8) == 6: # promoting, add all promotion types
                    for i in range(1, 5):
                        moves.append([square, square + 8, 0, i])
                else:   # not promoting, already checked that path not obstructed
                    moves.append([square, square + 8, 0, 0])
            
            # can't take to the left is on A file
            if (square%8 != 0 and 
                    self.pieces[square + 7] != 0):
                if int(square/8) == 6:          # takes with promotion
                    for i in range(1, 5):
                        moves.append([square, square + 7, self.pieces[square + 7], i])
                else:
                    moves.append([square, square + 7, self.pieces[square + 7], 0])
                
            # can't take to the right if on the H file
            if (square%8 != 7 and 
                    self.pieces[square + 9] != 0):
                if int(square/8) == 6:          # takes with promotion
                    for i in range(1, 5):
                        moves.append([square, square + 9, self.pieces[square + 9], i])
                else:
                    moves.append([square, square + 9, self.pieces[square + 9], 0])
            
        else:   # black to move
            if int(square/8) == 3:
                # check for en passant
                # will be on neighboring files, so if difference in mods is 1
                if self.meta_info[4] >= 0:

                    # en passant possible somewhere
                    if abs(self.meta_info[4] - square%8) == 1:
                        #                     en passant file + shift to piece to take
                        moves.append([ square, self.meta_info[4] + 16,
                                       1, 5])
            
            #single pawn move and path not obstructed
            if self.pieces[square - 8] == 0:
                # double pawn move, no need to check for promotions
                if (int(square/8) == 6 and                  # if on the seventh rank
                        self.pieces[square - 16] == 0):     # and 2 squares forward is empty
                    moves.append([square, square - 16, 0, 6])   
                    #self.meta_info[4] = square%8
                if (square/8) == 1: # promoting, add all promotion types
                    for i in range(1, 5):
                        moves.append([square, square - 8, 0, i])
                else:   # not promoting, already checked that path not obstructed
                    moves.append([square, square - 8, 0, 0])
            
            # can't take to the left is on A file
            if (square%8 != 0 and 
                    self.pieces[square - 9] != 0):
                if int(square/8) == 1:          # takes with promotion
                    for i in range(1, 5):
                        moves.append([square, square - 9, self.pieces[square - 9], i])
                else:
                    moves.append([square, square - 9, self.pieces[square - 9], 0])
                
            # can't take to the right if on the H file
            if (square%8 != 7 and 
                    self.pieces[square - 7] != 0):
                if int(square/8) == 6:          # takes with promotion
                    for i in range(1, 5):
                        moves.append([square, square - 7, self.pieces[square - 7], i])
                else:
                    moves.append([square, square - 7, self.pieces[square - 7], 0])

        return moves
        #raise NotImplementedError("pawn moves not implemented yet")
    
    def get_rook_moves(self, square):
        """
        Arguments:
            square (int): the square that the rook lies on
        returns:
            moves (2D int array): all legal moves for the given rook, in the form noted in get_valid_moves
        """
        moves = []
        #moves.append([square, -1, -1, -1])
        return moves
        #raise NotImplementedError("rook moves not implemented yet")
        
    def get_knight_moves(self, square):
        """
        Arguments:
            square (int): the square that the knight lies on
        returns:
            moves (2D int array): all legal moves for the given knight, in the form noted in get_valid_moves
        """
        moves = []
        #moves.append([square, -1, -1, -1])
        return moves
        #raise NotImplementedError("knight moves not implemented yet")
    
    def get_bishop_moves(self, square):
        """
        Arguments:
            square (int): the square that the bishop lies on
        returns:
            moves (2D int array): all legal moves for the given bishop, in the form noted in get_valid_moves
        """
        moves = []
        #moves.append([square, -1, -1, -1])
        return moves
        #raise NotImplementedError("bishop moves not implemented yet")
        
    def get_queen_moves(self, square):
        """
        Arguments:
            square (int): the square that the queen lies on
        returns:
            moves (2D int array): all legal moves for the given queen, in the form noted in get_valid_moves
        """
        moves = []
        #moves.append([square, -1, -1, -1])
        return moves
        #raise NotImplementedError("queen moves not implemented yet")
        
    def get_king_moves(self, square):
        """
        Arguments:
            square (int): the square that the king lies on
        returns:
            moves (2D int array): all legal moves for the given king, in the form noted in get_valid_moves
        """
        moves = []
        #moves.append([square, -1, -1, -1])
        return moves
        #raise NotImplementedError("king moves not implemented yet")
    
    
    
    
    
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

    def get_visible_squares(self, side = None):
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
            
        visible = []
        for i in self.get_valid_moves():
            if not i[0] in visible:
                visible.append(i[0])
            if not i[1] in visible:
                visible.append(i[1])
        for i in range(64):
            if self.pieces[i] != 0 and self.colors[i] == self.to_play and not i in visible:
                visible.append(i)

        return visible
        
        
    def get_board(self, side):
        pass
    
    def get_graphics_board(self):
        ret = []
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