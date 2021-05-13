import ruleset

class AIBoard(ruleset.GeneralBoard):
    """
    board representation for the AI, keeps track of a separate board for what it believes is the board state
    needs the move gen functions to search for what moves may have been made in the future of implementation
    ideally shouldn't have access to general board, but for now I am ignoring that it has theoretical access
        
    Implements:
        GeneralBoard
    """
    def __init__(self):
        """
        initialization, still uses the same board representation, but repurposed to be a guess.
        there may be some need to 
        """
        super().__init__()
        
        
        #representation of the moves that the AI thinks have been made
        self.moves_guess = []

    def make_move(self, move):
        super().make_move(move)
        #add the expected move, if opponent made move, can't know by default
        #since this is the cheating AI, it will know the move
        self.moves_guess.append(move)

    def evaluate(self):
        """
        central board evaluation function, takes in the guess about the current board state
        and evaluates what it thinks it is worth.
        """
        value = 0
        piece_values = [0, 1, 5, 3, 3, 9, 200]
        color_values = [0, 1, -1]
        move_scalar = .1
        # add some value to mobility (.1 per move seems common)
        self.swap_side()
        moves = self.get_valid_moves()
        value += len(moves)*move_scalar*color_values[self.to_play]
        self.swap_side()
        moves = self.get_valid_moves()
        value += len(moves)*move_scalar*color_values[self.to_play]
        
        for i in range(64):
            value += piece_values[self.pieces[i]]*color_values[self.colors[i]]

        return value
        
    def search(self, depth = 2):
        """
        search for good moves based on the evaluation function
        should randomly choose between good options if there are similar values
        """
        count = 0
        best_val = None
        best_move = None
        
        for move in self.get_valid_moves():
            #check value of the move
            self.make_move(move)

            if depth <= 0:
                value = self.evaluate()
            else:
                temp = self.search(depth - 1)
                value = temp[1]
                count += temp[2] + 1
            self.unmake_move(move)
            
            if best_val == None:
                best_val = value
                best_move = move

            #check against the best value
            elif ((self.to_play == 1 and value > best_val) or
                    (self.to_play == 2 and value < best_val)):
                
                best_val = value
                best_move = move
                
        #return value and move for simplicity of return values
        return [best_move, best_val, count]