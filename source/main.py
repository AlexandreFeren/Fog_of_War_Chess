import ruleset
import renderer


board = ruleset.Board()


win = renderer.draw_board(board.get_graphics_board())
while 1:
    render_mode = board.to_play
    #get 2 squares, instantly make move
    move_made = None
    last_squares = [None, None]
    renderer.update_board(win, board.get_graphics_board(), board.get_fog_squares(render_mode))

    while move_made == None:
        # shift moves by 1, and exits once a valid move is made
        last_squares[0] = last_squares[1]
        last_squares[1] = renderer.get_update(win, board.get_graphics_board(), board.get_fog_squares(render_mode))
        print(last_squares)
        move_made = board.make_move(last_squares)
#start game loop, then run an update until a valid move is made