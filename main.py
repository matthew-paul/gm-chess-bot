import chess
from stockfish import Stockfish
from tkinter import *
from helper import *

board = chess.Board()

selected_square = None
selected_piece = None

stockfish = Stockfish('C:/Users/matth/Documents/Chess/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe', parameters={"Minimum Thinking Time": 1000})

# functions


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key
    return None


def get_piece_from_square(square):
    for k, piece in pieces.items():
        if piece.square == square:
            return piece
    return None


def reset_colors():
    for i in range(8):
        for j in range(8):
            canvas.itemconfig(squares[i][j], fill=colors['light_blue'] if (i + j) % 2 == 0 else colors['dark_blue'])


def move(square1, square2):
    global selected_square, selected_piece
    selected_square = None
    selected_piece = None

    attempted_move = chess.Move(from_square=square1, to_square=square2)
    board.push(attempted_move)

    piece1 = get_piece_from_square(square1)
    print(f'Piece to move: {piece1}')
    piece2 = get_piece_from_square(square2)
    old_x, old_y = piece1.x, piece1.y

    if not piece2:
        # move image to square 2
        new_x, new_y = get_key(square_map, square2)
        new_x = square_size * new_x + 39
        new_y = square_size * new_y + 39
        canvas.move(piece1.id, new_x - old_x, new_y - old_y)

        # update piece 1
        piece1.x = new_x
        piece1.y = new_y
        piece1.update_square()


    else:
        new_x, new_y = piece2.x, piece2.y
        canvas.delete(piece2.id)
        del pieces[get_key(pieces, piece2)]

        # move image to square 2
        canvas.move(piece1.id, new_x - old_x, new_y - old_y)

        # update piece 1
        piece1.x = new_x
        piece1.y = new_y
        piece1.update_square()

    stockfish.set_fen_position(board.fen())


def automove():
    best_move = stockfish.get_best_move()
    square_1_str, square_2_str = best_move[0:2], best_move[2:]
    square_1_x, square_1_y = ord(square_1_str[0]) - ord('a'), 8 - int(square_1_str[1])
    square_2_x, square_2_y = ord(square_2_str[0]) - ord('a'), 8 - int(square_2_str[1])

    #print(f'({square_1_x}, {square_1_y})')
    #print(f'({square_2_x}, {square_2_y})')

    square1 = square_map[(square_1_x, square_1_y)]
    square2 = square_map[(square_2_x, square_2_y)]



    move(square1, square2)



def mouse_clicked(eventorigin):
    global selected_square, selected_piece
    mouse_x = eventorigin.x
    mouse_y = eventorigin.y

    square_x, square_y = get_square(mouse_x, mouse_y)

    if 0 <= square_x <= 7 and 0 <= square_y <= 7:

        # no piece selected
        if selected_square is None and get_piece_from_square(square_map[(square_x, square_y)]) is not None:
            canvas.itemconfig(squares[square_x][square_y], fill=colors['light_yellow'])
            selected_square = square_map[(square_x, square_y)]
            selected_piece = get_piece_from_square(square_map[(square_x, square_y)])

        # piece selected
        else:
            new_square = square_map[(square_x, square_y)]

            # unselect if clicked again
            if new_square == selected_square:
                canvas.itemconfig(squares[square_x][square_y],
                                  fill=colors['light_blue'] if (square_x + square_y) % 2 == 0 else colors['dark_blue'])
            # attempt to move
            elif selected_piece is not None:
                # do move
                move(selected_square, new_square)
                automove()

                # reset colors
                reset_colors()

            selected_square = None
            selected_piece = None


# gui stuff
board_gui = Tk()
board_gui.title("Chess Bot")
board_gui.minsize(board_size + 5, board_size + 5)
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
        square_row.append(canvas.create_rectangle(x, y, x + square_size, y + square_size,
                                                  fill=colors['light_blue'] if toggle else colors['dark_blue'],
                                                  outline=colors['white']))
        toggle = not toggle
        y += square_size
    squares.append(square_row)
    x += square_size

# draw pieces

pieces = draw_pieces(canvas)

# bind mouse click
board_gui.bind("<Button 1>", mouse_clicked)


board_gui.mainloop()


