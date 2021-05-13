import game
import AI
import Cheating_AI
import renderer
import random
import chess
import chess.engine

def play_as_white(render_mode = 1):
    """
    Play as white against a computer opponent
    Arguments:
        render_mode: the mode in which to render the board, can put in 0 for debugging
    Returns:
        won (int/None): the win condition, if any. 1 for white wins, 2 for black wins
    """
    won = human_move(render_mode)
    if won != None:
        return won
    won = AI_move()
    if won != None:
        return won

def play_as_black(render_mode = 2):
    """
    Play as black against a computer opponent
    Arguments:
        render_mode: the mode in which to render the board, can put in 0 for debugging
    Returns:
        won (int/None): the win condition, if any. 1 for white wins, 2 for black wins
    """
    won = AI_move()
    if won != None:
        return won
    won = human_move(render_mode)
    if won != None:
        return won

def play_human(render_mode = 1):
    """
    Play against a human opponent
    Arguments
        fog (bool): whether or not fog of war should be displayed
    Returns:
        won (int/None): the win condition, if any. 1 for white wins, 2 for black wins
    """
    
    won = human_move(render_mode)
    if won != None:
        return won
        
    if render_mode != 0:
        render_mode = render_mode%2 + 1
    won = human_move(render_mode)
    if won != None:
        return won
        
def get_move_input(render_mode = None):
    """
    Helper function to avoid duplicate code, makes a move for the player based on their input
    Arguments:
        render_mode (int): 1 for white, 2 for black, 0 for unobscured
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
            #print("MOVE MADE", move_made)
            renderer.update_board(win, board.get_graphics_board(), board.get_visible_squares(render_mode))
    return move_made

def human_move(render_mode = None):
    print(board.export_fen())
    if render_mode == None:
        render_mode = board.to_play
    move = get_move_input(render_mode)
    if move[2] == 6:
        print("King captured")
        return board.to_play
    else:
        won = None
    AI_board.make_move(move)
    board.make_move(move)
    #print(move)
    
def AI_move():
    """
    #get move from AI
    board.export_fen()
    """
    #move = random.choice(board.get_valid_moves())
    print(board.export_fen())
    chess_board = chess.Board(board.export_fen())
    print(chess.Board())
    print(chess_board)
    try:
        move = board.move_from_san(engine.analyse(chess_board, chess.engine.Limit(time=.1))["pv"][0])
    except:
        # while this block can definitely be reached on not moving the king out of danger,
        # there may be other, unintended ways to get here that I do not fully understand
        print("stupid move")
        return board.to_play
    
    
    #move = AI_board.search()[0]
    if move[2] == 6:
        print("King captured")
        return board.to_play
    else:
        won = None
    AI_board.make_move(move)
    board.make_move(move)
    AI_board.evaluate()

    
    
def test_unmake():

    test = input("test unmake?")
    if test == "y":
        for move in board.get_valid_moves():
            board.make_move(move)
            renderer.update_board(win, board.get_graphics_board(), [i for i in range(64)])
            input("move made")
            board.unmake_move(move)
            renderer.update_board(win, board.get_graphics_board(), [i for i in range(64)])
            input()
    #get and make a move for player
    move = get_move_input(0)
    board.make_move(move)
    

board = game.Board()
engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
chess_board = chess.Board()


AI_board = Cheating_AI.AIBoard()
sides = ["", "white", "black"]

win = renderer.draw_board(board.get_graphics_board())
moves = board.get_valid_moves()

won = None
ply = 0

while 1:
    
    won = play_as_black(0)
    #won = play_human(0)
    if won != None:
        print(sides[won], "Won the game")
        break