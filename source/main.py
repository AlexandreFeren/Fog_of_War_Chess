import ruleset
import renderer
    
def play_as_white(win, fog = True):
    """
    Play as white against a computer opponent
    Arguments:
        fog (bool): whether or not fog of war should be displayed
    Returns:
        None
    """
    render_mode = 1
    get_move_input(render_mode)
    #here the AI move would be done
    raise NotImplementedError("play_as_white not implemented yet")
    
def play_as_black(win, fog = True):
    """
    Play as black against a computer opponent
    Arguments:
        fog (bool): whether or not fog of war should be displayed
    Returns:
        None
    """
    render_mode = 2
    get_move_input(render_mode)   
    #here the AI move would be done
    raise NotImplementedError("play_as_black not implemented yet")

def play_human(win, fog = True):
    """
    Play against a human opponent, with the option of playing unobscured (though this will still allow for normally illegal king moves)
    Arguments
        fog (bool): whether or not fog of war should be displayed
    Returns:
        None
    """
    render_mode = board.to_play # render the side that is to play
    
    won = get_move_input(render_mode)
    
    if won != None:
        return won
    # black out screen
    if fog:
        renderer.clear_board(win)   # blank out the board and click to swap

def get_move_input(render_mode):
    """
    
    """
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
    if move_made[2] == 6:
        print("King captured")
        return board.to_play

board = ruleset.Board()
sides = ["", "white", "black"]

win = renderer.draw_board(board.get_graphics_board())
moves = board.get_valid_moves()

while 1:
    won = play_human(win)
    if won != None:
        break