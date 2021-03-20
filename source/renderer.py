from graphics import *

piece_set_path = "pieces/Maestro/"
# index 0 is out of fog, index 1 is in fog
light_colors = ["beige", "grey"]
dark_colors = ["tan", "black"]
# color to indicate that a square has been highlighted
highlight_color = "orange"

# graphics are a bit slow, but it should be passable. each update undraws and redraws all items.
# could possibly be made faster by 

def draw_grid(win, visible):
    rects = []
    
    for i in range(64):
        p1 = Point((i%8+1)*100, int(i/8+1)*100)
        p2 = Point(i%8*100, int(i/8)*100)
        rects.append(Rectangle(p1, p2))
        visible_square = 0
        if not i in visible:
            visible_square = 1

        if (int(i/8)+i%8)%2:
            rects[-1].setFill(light_colors[visible_square])
            rects[-1].setOutline(light_colors[visible_square])
            rects[-1].draw(win)
        else:
            rects[-1].setFill(dark_colors[visible_square])
            rects[-1].setOutline(dark_colors[visible_square])
            rects[-1].draw(win)
            
def draw_pieces(win, board, visible):
    images = []
    for i in board:
        if i[1] in visible:
            p1 = Point((i[1]%8)*100 + 50, int(i[1]/8)*100 + 50)
            
            images.append(Image(p1, piece_set_path + i[0] + ".png"))
            images[-1].draw(win)
        
def draw_board(board):
    """
    Arguments:
        board: get from the return value of the board state
    """
    win = GraphWin('Draw a Triangle', 800, 800, autoflush = False)
    win.setCoords(0, 0, 799, 799)
    win.setBackground('beige')
    
    # render the squares and pieces
    draw_grid(win, [i for i in range(16,64)])
    draw_pieces(win, board, [i for i in range(16,64)])
    return win
    
def update_board(win, board, fog):
    # convert x and y positions to a single square value
    
    for item in win.items[:]:
        item.undraw()
    draw_grid(win, fog)  # redraw board to overwrite previous highlights
    draw_pieces(win, board, fog) # draw pieces on the board
    
    
def get_update(win, board, fog = []):
    """
    Arguments:
        board ([str, int] array): the true state of the board, in the form of an array of file names and index
        fog (int array): the squares that are not visible to the current player.
    Returns:
        square (int): selected square
    """
    
    pos = win.getMouse()
    # convert x and y positions to a single square value
    square = int(pos.x/100) + int(pos.y/100)*8
    
    for item in win.items[:]:
        item.undraw()
    update_board(win, board, fog)

    rect = Rectangle(Point(int(pos.x/100 + 1)*100, int(pos.y/100 + 1)*100), 
                     Point(int(pos.x/100)*100, int(pos.y/100)*100))
    rect.setFill(highlight_color)
    rect.setOutline(highlight_color)

    rect.draw(win)  # draw highlight
    draw_pieces(win, board, fog) # draw pieces on the board
    return square

def get_promotion(win, board):
    """
    Arguments:
        side, to appropriately display the piece color
    Returns:
        piece (int): piece to promote to
            1: =R
            2: =N
            3: =B
            4: =Q
    """
    piece = None
    side = board.to_play
    image_name = ""
    if side == 1:
        image_name += "w"
    else:
        image_name += "b"
    
    # draw images to the screen
    images = []
    images.append(Image(Point(300, 400), piece_set_path + image_name + "R.png"))
    images.append(Image(Point(400, 400), piece_set_path + image_name + "N.png"))
    images.append(Image(Point(500, 400), piece_set_path + image_name + "B.png"))
    images.append(Image(Point(600, 400), piece_set_path + image_name + "Q.png"))
    for i in images:
        i.draw(win)
    
    
    while piece == None:    #loop to avoid needing to run down the board again
        pos = win.getMouse()
        if (int(pos.y/100 - .5)) == 3:
            if (int(pos.x/100 -.5)) == 2:
                # promoting to Rook
                piece = 1
            elif (int(pos.x/100 -.5)) == 3:
                # promoting to Knight
                piece = 2
            elif (int(pos.x/100 -.5)) == 4:
                # promoting to Bishop
                piece = 3
            elif (int(pos.x/100 -.5)) == 5:
                # promoting to Queen
                piece = 4
            else:
                print("no piece selected")

    return piece