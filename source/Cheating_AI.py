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
        self.pgn_guess = []

    def evaluate(self):
        """
        central board evaluation function, takes in the guess about the current board state
        and evaluates what it thinks it is worth.
        """
        print(self)
        print("\n"*2)
        #print("test")
        
    '''
    def move(self):
        print("making move")
        return self.make_move(self.get_valid_moves()[0])
    '''