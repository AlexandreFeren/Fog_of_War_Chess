import ruleset

board = ruleset.Board()
print(board.get_board_by_file())

import renderer

renderer.draw_board(board.get_board_by_file())