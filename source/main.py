import ruleset
import renderer


board = ruleset.Board()
sides = ["", "white", "black"]

win = renderer.draw_board(board.get_graphics_board())
moves = board.get_valid_moves()
#print("moves[0]: " + str(moves[0]))
#board.make_move(moves[0])

    
def play_as_white():
    pass
    
def play_as_black():
    pass

def play_human(win, fog = True):
    render_mode = board.to_play
    #get 2 squares, instantly make move
    move_made = None
    last_squares = [None, None]
    renderer.update_board(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
    
    while move_made == None:
        # shift moves by 1, and exits once a valid move is made
        last_squares[0] = last_squares[1]
        
        last_squares[1] = renderer.get_update(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
        move_made = board.validate_move(last_squares)
        
        # purely for if there is a promotion made, otherwise move_made will be an array
        if move_made == "promote":
            promotion = renderer.get_promotion(win, board)
            move_made = board.validate_move(last_squares, promotion)
            renderer.update_board(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
    
    # black out screen
    if fog:
        renderer.clear_board(win)   # blank out the board and click to swap


while 1:
    """
    # purely for debugging, no functional purpose
    #side = sides[board.to_play]
    #print("\n\n" + side + " to play")
    #print("Valid Moves:")
    #print(board.to_algebraic_notation(board.get_valid_moves()))
    
    #useful code start
    render_mode = board.to_play
    #get 2 squares, instantly make move
    move_made = None
    last_squares = [None, None]
    renderer.update_board(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
    
    while move_made == None:
        # shift moves by 1, and exits once a valid move is made
        last_squares[0] = last_squares[1]
        
        last_squares[1] = renderer.get_update(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
        move_made = board.validate_move(last_squares)
        
        # purely for if there is a promotion made, otherwise move_made will be an array
        if move_made == "promote":
            promotion = renderer.get_promotion(win, board)
            move_made = board.validate_move(last_squares, promotion)
            renderer.update_board(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
        
    #here, the move has been made, insert an AI move
    """
    play_human(win)