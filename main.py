import chess
from tkinter import *
from helper import draw_pieces

board = chess.Board()
flipped = False

# functions


def mouse_clicked(eventorigin):
    mouse_x = eventorigin.x
    mouse_y = eventorigin.y

    square_x, square_y = (mouse_x - 5) // square_size, (mouse_y - 5) // square_size

    print(mouse_x, mouse_y)
    print(square_x, square_y)


# gui stuff
board_size = 600
square_size = board_size // 8

light_blue = '#8ad6ff'
dark_blue = '#619eff'

board_gui = Tk()
board_gui.title("Chess Bot")
board_gui.minsize(board_size + 5, board_size + 10)
board_gui.resizable(0, 0)

frame = Frame(board_gui)
frame.pack()

canvas = Canvas(frame, width=board_size, height=board_size, bg='white')
canvas.pack(fill=BOTH, expand=True)

# draw squares
squares = []


toggle = flipped  # top left color based on whether board is flipped
for x in range(2, board_size, square_size):
    toggle = not toggle
    square_row = []
    for y in range(2, board_size, square_size):
        square_row.append(canvas.create_rectangle(x, y, x + square_size, y + square_size, fill=light_blue if toggle else dark_blue, outline='#000'))
        toggle = not toggle
        y += square_size
    squares.append(square_row)
    x += square_size

# draw pieces

black_pieces = {}
white_pieces = {}

draw_pieces(canvas, black_pieces, white_pieces, square_size)

# bind mouse click
board_gui.bind("<Button 1>", mouse_clicked)

draw_pieces(canvas, black_pieces, white_pieces, square_size)
board_gui.mainloop()

