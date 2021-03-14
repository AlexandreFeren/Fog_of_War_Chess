from graphics import *

piece_set_path = "pieces/Maestro/"
light_color = "beige"
dark_color = "tan"
fog_color = "grey"
highlight_color = "orange"
fog = [i for i in range(32, 64)]

def draw_grid(win):
    rects = []
    
    for i in range(64):
        p1 = Point((i%8+1)*100, int(i/8+1)*100)
        p2 = Point(i%8*100, int(i/8)*100)
        rects.append(Rectangle(p1, p2))
        
        if i in fog:
            rects[-1].setFill(fog_color)
            rects[-1].setOutline(fog_color)
            rects[-1].draw(win)
        elif (int(i/8)+i%8)%2:
            rects[-1].setFill(light_color)
            rects[-1].setOutline(light_color)
            rects[-1].draw(win)
        else:
            rects[-1].setFill(dark_color)
            rects[-1].setOutline(dark_color)
            rects[-1].draw(win)
def draw_pieces(win, board):
    images = []
    for i in board:
        if not i[1] in fog:
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
    draw_grid(win)
    draw_pieces(win, board)
    while 1:
        pos = win.getMouse()
        draw_grid(win)  # redraw board to overwrite previous highlights

        rect = Rectangle(Point(int(pos.x/100 + 1)*100, int(pos.y/100 + 1)*100), 
                         Point(int(pos.x/100)*100, int(pos.y/100)*100))
        rect.setFill(highlight_color)
        rect.setOutline(highlight_color)

        rect.draw(win)  # draw highlight
        draw_pieces(win, board) # draw pieces on the board

    
    pos = win.getMouse()
