import chess
from PIL import ImageTk, Image

colors = {'light_blue': '#8ad6ff',
          'dark_blue': '#619eff',
          'black': '#000',
          'light_red': '#d14747',
          'light_yellow': '#fffa75',
          'white': '#fff'}

square_map = {(0, 0): chess.A8,
              (0, 1): chess.A7,
              (0, 2): chess.A6,
              (0, 3): chess.A5,
              (0, 4): chess.A4,
              (0, 5): chess.A3,
              (0, 6): chess.A2,
              (0, 7): chess.A1,
              (1, 0): chess.B8,
              (1, 1): chess.B7,
              (1, 2): chess.B6,
              (1, 3): chess.B5,
              (1, 4): chess.B4,
              (1, 5): chess.B3,
              (1, 6): chess.B2,
              (1, 7): chess.B1,
              (2, 0): chess.C8,
              (2, 1): chess.C7,
              (2, 2): chess.C6,
              (2, 3): chess.C5,
              (2, 4): chess.C4,
              (2, 5): chess.C3,
              (2, 6): chess.C2,
              (2, 7): chess.C1,
              (3, 0): chess.D8,
              (3, 1): chess.D7,
              (3, 2): chess.D6,
              (3, 3): chess.D5,
              (3, 4): chess.D4,
              (3, 5): chess.D3,
              (3, 6): chess.D2,
              (3, 7): chess.D1,
              (4, 0): chess.E8,
              (4, 1): chess.E7,
              (4, 2): chess.E6,
              (4, 3): chess.E5,
              (4, 4): chess.E4,
              (4, 5): chess.E3,
              (4, 6): chess.E2,
              (4, 7): chess.E1,
              (5, 0): chess.F8,
              (5, 1): chess.F7,
              (5, 2): chess.F6,
              (5, 3): chess.F5,
              (5, 4): chess.F4,
              (5, 5): chess.F3,
              (5, 6): chess.F2,
              (5, 7): chess.F1,
              (6, 0): chess.G8,
              (6, 1): chess.G7,
              (6, 2): chess.G6,
              (6, 3): chess.G5,
              (6, 4): chess.G4,
              (6, 5): chess.G3,
              (6, 6): chess.G2,
              (6, 7): chess.G1,
              (7, 0): chess.H8,
              (7, 1): chess.H7,
              (7, 2): chess.H6,
              (7, 3): chess.H5,
              (7, 4): chess.H4,
              (7, 5): chess.H3,
              (7, 6): chess.H2,
              (7, 7): chess.H1,
              }


# assign images
black = dict()
white = dict()
created_images = False

board_size = 600
square_size = board_size // 8
flipped = False


def get_square(x, y):
    square_x, square_y = (x - 3) // square_size, (y - 3) // square_size
    if flipped:
        square_y = 7 - square_y

    return square_x, square_y


class ChessPiece:
    def __init__(self, canvas, color, piece_type, piece_x, piece_y, img):
        self.color = color
        self.type = piece_type
        self.img = img
        self.x = piece_x
        self.y = piece_y
        self.id = canvas.create_image(piece_x, piece_y, image=img)

        self.square = square_map[get_square(self.x, self.y)]

        return

    def update_square(self, x, y):
        self.x = x
        self.y = y
        self.square = square_map[get_square(self.x, self.y)]

    def get_coords(self):
        return get_square(self.x, self.y)

    def __str__(self):
        return f'{self.color}, {self.type}, {self.square}'

def create_images():
    black['rook'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rdt60.png'))
    black['knight'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_ndt60.png'))
    black['bishop'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_bdt60.png'))
    black['queen'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_qdt60.png'))
    black['king'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_kdt60.png'))
    black['pawn'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_pdt60.png'))
    white['rook'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rlt60.png'))
    white['knight'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_nlt60.png'))
    white['bishop'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_blt60.png'))
    white['queen'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_qlt60.png'))
    white['king'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_klt60.png'))
    white['pawn'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_plt60.png'))
    created_images = True


def draw_pieces(tkCanvas):

    pieces = dict()

    if not created_images:
        create_images()

    pieces['r1'] = ChessPiece(tkCanvas, 'black', 'r', 39, 39, black['rook'])
    pieces['n1'] = ChessPiece(tkCanvas, 'black', 'n', square_size + 39, 39, black['knight'])
    pieces['b1'] = ChessPiece(tkCanvas, 'black', 'b', square_size * 2 + 39, 39, black['bishop'])
    pieces['q'] = ChessPiece(tkCanvas, 'black', 'q', square_size * 3 + 39, 39, black['queen'])
    pieces['k'] = ChessPiece(tkCanvas, 'black', 'k', square_size * 4 + 39, 39, black['king'])
    pieces['b2'] = ChessPiece(tkCanvas, 'black', 'b', square_size * 5 + 39, 39, black['bishop'])
    pieces['n2'] = ChessPiece(tkCanvas, 'black', 'n', square_size * 6 + 39, 39, black['knight'])
    pieces['r2'] = ChessPiece(tkCanvas, 'black', 'r', square_size * 7 + 39, 39, black['rook'])
    for i in range(8):
        pieces[f'p{i}'] = ChessPiece(tkCanvas, 'black', 'p', square_size * i + 39, square_size + 39, black['pawn'])

    pieces['R1'] = ChessPiece(tkCanvas, 'white', 'R', 39, square_size * 7 + 39, white['rook'])
    pieces['N1'] = ChessPiece(tkCanvas, 'white', 'N', square_size + 39, square_size * 7 + 39, white['knight'])
    pieces['B1'] = ChessPiece(tkCanvas, 'white', 'B', square_size * 2 + 39, square_size * 7 + 39, white['bishop'])
    pieces['Q'] = ChessPiece(tkCanvas, 'white', 'Q', square_size * 3 + 39, square_size * 7 + 39, white['queen'])
    pieces['K'] = ChessPiece(tkCanvas, 'white', 'K', square_size * 4 + 39, square_size * 7 + 39, white['king'])
    pieces['B2'] = ChessPiece(tkCanvas, 'white', 'B', square_size * 5 + 39, square_size * 7 + 39, white['bishop'])
    pieces['K2'] = ChessPiece(tkCanvas, 'white', 'N', square_size * 6 + 39, square_size * 7 + 39, white['knight'])
    pieces['R2'] = ChessPiece(tkCanvas, 'white', 'R', square_size * 7 + 39, square_size * 7 + 39, white['rook'])
    for i in range(8):
        pieces[f'P{i}'] = ChessPiece(tkCanvas, 'white', 'P', square_size * i + 39, square_size * 6 + 39, white['pawn'])

    return pieces
