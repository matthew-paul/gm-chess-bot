import chess
from stockfish import Stockfish
from tkinter import *
from helper import *
from time import sleep

board = chess.Board()

selected_square = None
selected_piece = None
castling_rights = {'white': [True, True], 'black': [True, True]}

stockfish = Stockfish('C:/Users/matth/Documents/Chess/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2.exe', parameters={"Threads": 4, "Ponder": True, "Minimum Thinking Time": 10000})

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


def move_piece(square1, square2):
    piece1 = get_piece_from_square(square1)

    if not piece1:
        return

    old_x, old_y = piece1.x, piece1.y
    new_x, new_y = get_key(square_map, square2)
    new_x = square_size * new_x + 39
    new_y = square_size * new_y + 39

    canvas.move(piece1.id, new_x - old_x, new_y - old_y)

    piece1.update_square(new_x, new_y)


def move(square1, square2):
    global selected_square, selected_piece

    selected_square = None
    selected_piece = None
    stockfish.set_fen_position(board.fen())

    piece1 = get_piece_from_square(square1)
    piece2 = get_piece_from_square(square2)

    old_x, old_y = piece1.get_coords()
    new_x, new_y = get_key(square_map, square2)

    x_dist = abs(new_x - old_x)
    y_dist = abs(new_y - old_y)

    if piece1.type in ['r', 'R']:
        if piece1.type == 'r':
            if (old_x, old_y) == (0, 0):
                castling_rights['black'][0] = False
            elif (old_x, old_y) == (7, 0):
                castling_rights['black'][1] = False
        else:
            if (old_x, old_y) == (0, 7):
                castling_rights['white'][0] = False
            elif (old_x, old_y) == (7, 7):
                castling_rights['white'][1] = False

    if piece1.type in ['k', 'K']:  # check for castling
        if x_dist == 2 and y_dist == 0:
            if piece1.type == 'k' and (old_x, old_y) == (4, 0) and (new_x, new_y) == (6, 0) and castling_rights['black'][1]:  # kingside castle
                castling_rights['black'][1] = False

                move_piece(square1, square2)
                move_piece(square_map[(7, 0)], square_map[(5, 0)])

            if piece1.type == 'k' and (old_x, old_y) == (4, 0) and (new_x, new_y) == (2, 0) and castling_rights['black'][0]:  # queenside castle
                castling_rights['black'][0] = False

                move_piece(square_map[(4, 0)], square_map[(2, 0)])
                move_piece(square_map[(0, 0)], square_map[(3, 0)])

            if piece1.type == 'K' and (old_x, old_y) == (4, 7) and (new_x, new_y) == (6, 7) and castling_rights['white'][1]:  # kingside castle
                castling_rights['white'][1] = False

                move_piece(square_map[(4, 7)], square_map[(6, 7)])
                move_piece(square_map[(7, 7)], square_map[(5, 7)])

            if piece1.type == 'K' and (old_x, old_y) == (4, 7) and (new_x, new_y) == (2, 7) and castling_rights['white'][0]:  # queenside castle
                castling_rights['white'][0] = False

                move_piece(square_map[(4, 7)], square_map[(2, 7)])
                move_piece(square_map[(0, 7)], square_map[(3, 7)])

        else:
            move_piece(square1, square2)
            castling_rights['black' if piece1.type == 'k' else 'white'] = [False, False]

    if piece2:
        canvas.delete(piece2.id)
        del pieces[get_key(pieces, piece2)]

    move_piece(square1, square2)


def automove():
    best_move = stockfish.get_best_move()
    square_1_str, square_2_str = best_move[0:2], best_move[2:]
    square_1_x, square_1_y = ord(square_1_str[0]) - ord('a'), 8 - int(square_1_str[1])
    square_2_x, square_2_y = ord(square_2_str[0]) - ord('a'), 8 - int(square_2_str[1])


    square1 = square_map[(square_1_x, square_1_y)]
    square2 = square_map[(square_2_x, square_2_y)]

    attempted_move = chess.Move(from_square=square1, to_square=square2)
    board.push(attempted_move)
    move(square1, square2)


def is_legal_move(old_square, new_square):
    piece1 = get_piece_from_square(old_square)
    piece2 = get_piece_from_square(new_square)

    old_x, old_y = piece1.get_coords()
    new_x, new_y = get_key(square_map, new_square)

    y_dist = abs(old_y - new_y)
    x_dist = abs(old_x - new_x)

    print(f'({old_x}, {old_y}) -> ({new_x}, {new_y})')

    if piece2 and piece2.color == piece1.color:  # can't move to a square with a friendly piece
        return False

    if piece1.type in ['p', 'P']:  # pawn
        if piece1.type == 'P':  # white pawn
            if new_x - old_x == 0 and (old_y - new_y) in [1, 2]:  # moving piece forward 1 or 2 squares
                if old_y - new_y == 2 and old_y != 6:  # don't allow moving forward 2 squares unless pawn hasn't moved yet
                    return False

                if not piece2:  # nothing in front of pawn
                    return True
                else:
                    return False
            elif abs(new_x - old_x) == 1 and old_y - new_y == 1:  # moving piece diagonally
                if not piece2 or piece2.color != 'black':  # must have black piece on new square
                    return False

            else:
                return False
        elif piece1.type == 'p':  # black pawn
            if new_x - old_x == 0 and (new_y - old_y) in [1, 2]:  # moving piece forward 1 or 2 squares
                if new_y - old_y == 2 and old_y != 1:  # don't allow moving forward 2 squares unless pawn hasn't moved yet
                    return False

                if not piece2:  # nothing in front of pawn
                    return True
                else:
                    return False
            elif abs(new_x - old_x) == 1 and new_y - old_y == 1:  # moving piece diagonally
                if not piece2 or piece2.color != 'white':  # must have white piece on new square
                    return False

            else:
                return False
    elif piece1.type in ['n', 'N']:  # knight
        if y_dist != 0 and x_dist != 0 and y_dist + x_dist == 3:
            return True
        else:
            return False
    elif piece1.type in ['b', 'B']:  # bishop
        if x_dist == y_dist:  # moving diagonally
            # check for any pieces in between
            for i, j in get_squares_between(old_x, old_y, new_x, new_y):
                square = square_map[(i, j)]
                if get_piece_from_square(square):
                    return False

            return True
        else:
            return False
    elif piece1.type in ['r', 'R']:  # rook
        if x_dist != 0 and y_dist != 0:
            return False

        # check for any pieces in between
        for i, j in get_squares_between(old_x, old_y, new_x, new_y):
            square = square_map[(i, j)]
            if get_piece_from_square(square):
                return False
    elif piece1.type in ['k', 'K']:  # king
        if x_dist > 1 or y_dist > 1:
            if x_dist == 2 and y_dist == 0:
                # check for each type of castling
                if piece1.type == 'k' and (old_x, old_y) == (4, 0) and (castling_rights['black'][0] and (new_x, new_y) == (2, 0)) or (castling_rights['black'][1] and (new_x, new_y) == (6, 0)):
                    return True
                elif piece1.type == 'K' and (old_x, old_y) == (4, 7) and (castling_rights['white'][0] and (new_x, new_y) == (2, 7)) or (castling_rights['white'][1] and (new_x, new_y) == (6, 7)):
                    return True
                else:
                    return False
            return False
        return True
    elif piece1.type in ['q', 'Q']:  # queen

        if x_dist != y_dist and x_dist != 0 and y_dist != 0:
            return False

        for i, j in get_squares_between(old_x, old_y, new_x, new_y):
            # print(f'{i}, {j}')
            square = square_map[(i, j)]
            if get_piece_from_square(square):
                print(f'piece on square {i}, {j}')
                return False



    return True


def get_squares_between(old_x, old_y, new_x, new_y):
    result = []


    # remove starting and ending points
    if old_x < new_x:
        old_x += 1
    elif old_x > new_x:
        old_x -= 1

    if old_y < new_y:
        old_y += 1
    elif old_y > new_y:
        old_y -= 1


    if new_x == old_x:
        print(f'vertical')
        for j in range(old_y, new_y, 1 if old_x < new_x else -1):
            result.append((old_x, j))
    elif new_y == old_y:
        print(f'horizontal')
        for i in range(old_x, new_x, 1 if old_y < new_y else -1):
            result.append((i, old_y))
    elif abs(new_y - old_y) == abs(new_x - old_x):
        for i, j in zip(range(old_x, new_x, -1 if new_x < old_x else 1), range(old_y, new_y, -1 if new_y < old_y else 1)):
            result.append((i, j))

    return result


def mouse_clicked(eventorigin):
    global selected_square, selected_piece
    mouse_x = eventorigin.x
    mouse_y = eventorigin.y

    square_x, square_y = get_square(mouse_x, mouse_y)

    if 0 <= square_x <= 7 and 0 <= square_y <= 7:

        # no square selected yet
        if selected_square is None and get_piece_from_square(square_map[(square_x, square_y)]) is not None:
            canvas.itemconfig(squares[square_x][square_y], fill=colors['light_yellow'])
            selected_square = square_map[(square_x, square_y)]
            selected_piece = get_piece_from_square(square_map[(square_x, square_y)])

        # square already selected
        else:
            new_square = square_map[(square_x, square_y)]

            # unselect if clicked again
            if new_square == selected_square:
                canvas.itemconfig(squares[square_x][square_y],
                                  fill=colors['light_blue'] if (square_x + square_y) % 2 == 0 else colors['dark_blue'])
            # attempt to move
            elif selected_piece is not None:
                if is_legal_move(selected_square, new_square):
                    print(f'Legal move')
                    attempted_move = chess.Move(from_square=selected_square, to_square=new_square)
                    board.push(attempted_move)
                    if board.is_valid():
                        print(f'Valid move')
                        move(selected_square, new_square)
                        automove()
                    else:
                        print(f'Not valid move')
                        board.pop()
                else:
                    print(f'Illegal move')



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


