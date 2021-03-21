from PIL import ImageTk, Image


def draw_pieces(tkCanvas, black, white, square_size):
    black['rook1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rdt60.png'))
    tkCanvas.create_image(39, 39, image=black['rook1'])

    black['knight1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_ndt60.png'))
    tkCanvas.create_image(square_size + 39, 39, image=black['knight1'])

    black['bishop1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_bdt60.png'))
    tkCanvas.create_image(square_size * 2 + 39, 39, image=black['bishop1'])

    black['queen'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_qdt60.png'))
    tkCanvas.create_image(square_size * 3 + 39, 39, image=black['queen'])

    black['king'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_kdt60.png'))
    tkCanvas.create_image(square_size * 4 + 39, 39, image=black['king'])

    black['bishop2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_bdt60.png'))
    tkCanvas.create_image(square_size * 5 + 39, 39, image=black['bishop2'])

    black['knight2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_ndt60.png'))
    tkCanvas.create_image(square_size * 6 + 39, 39, image=black['knight2'])

    black['rook2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rdt60.png'))
    tkCanvas.create_image(square_size * 7 + 39, 39, image=black['rook2'])

    for i in range(8):
        black[f'pawn{i}'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_pdt60.png'))
        tkCanvas.create_image(square_size * i + 39, square_size + 39, image=black[f'pawn{i}'])


    white['rook1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rlt60.png'))
    tkCanvas.create_image(39, square_size * 7 + 39, image=white['rook1'])

    white['knight1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_nlt60.png'))
    tkCanvas.create_image(square_size + 39, square_size * 7 + 39, image=white['knight1'])

    white['bishop1'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_blt60.png'))
    tkCanvas.create_image(square_size * 2 + 39, square_size * 7 + 39, image=white['bishop1'])

    white['queen'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_qlt60.png'))
    tkCanvas.create_image(square_size * 3 + 39, square_size * 7 + 39, image=white['queen'])

    white['king'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_klt60.png'))
    tkCanvas.create_image(square_size * 4 + 39, square_size * 7 + 39, image=white['king'])

    white['bishop2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_blt60.png'))
    tkCanvas.create_image(square_size * 5 + 39, square_size * 7 + 39, image=white['bishop2'])

    white['knight2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_nlt60.png'))
    tkCanvas.create_image(square_size * 6 + 39, square_size * 7 + 39, image=white['knight2'])

    white['rook2'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_rlt60.png'))
    tkCanvas.create_image(square_size * 7 + 39, square_size * 7 + 39, image=white['rook2'])

    for i in range(8):
        white[f'pawn{i}'] = ImageTk.PhotoImage(Image.open('resources/pieces/Chess_plt60.png'))
        tkCanvas.create_image(square_size * i + 39, square_size * 6 + 39, image=white[f'pawn{i}'])
