import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import main
from basics import *
from chess_board_frame import Board, WHITE_PAWN_CHARACTER, BLACK_QUEEN_CHARACTER, CHESS_FONT

root = tk.Tk()

pawns = {}  # dict from files to ranks. No pawn means not in dict
queen = None  # either none, or (f,r)

# status of the ui-board:
player = StringVar(value="pawns")  # or value="queen


def clear_board_and_set_pieces():
    board_frame.clear()
    for f, r in pawns.items():
        board_frame.set_white_pawn(f, r)
    if queen is not None:
        # noinspection PyArgumentList
        board_frame.set_black_queen(*queen)


def get_main_pawns():
    result = main.Pawns()
    for f, r in pawns.items():
        result.set(BOARD.get_square(f, r))
    return result


def evaluate_pawns_only_board():
    mp = get_main_pawns()

    # try queen on all empty squares
    for qf in FILES:
        for qr in RANKS:
            mq = Queen(BOARD.get_square(qf, qr))
            if not mp.occupy(mq):
                if player.get() == "pawns":
                    e = main.PosWhite(mp, mq).evaluate()
                else:
                    e = main.PosBlack(mp, mq).evaluate()

                if e is not None:
                    character = {Status.WIN: "+", Status.DRAW: "=", Status.LOSE: "-"}[e]
                    board_frame.set_text_on_square(qf, qr, character)


def evaluate_pawn_moves():
    assert queen is not None
    # noinspection PyArgumentList
    pos = main.PosWhite(get_main_pawns(), Queen(BOARD.get_square(*queen)))
    for new_pawn in pos.generate_moves():
        e = pos.get_position_after_move_pawn_forward(new_pawn).evaluate()
        if e is not None:
            character = {Status.WIN: "-", Status.DRAW: "=", Status.LOSE: "+"}[e]
            board_frame.set_text_on_square(new_pawn.file, new_pawn.rank, character)
            if e == Status.LOSE:
                board_frame.set_background_highlighted(new_pawn.file, new_pawn.rank)


def evaluate_queen_moves():
    assert queen is not None
    # noinspection PyArgumentList
    pos = main.PosBlack(get_main_pawns(), Queen(BOARD.get_square(*queen)))
    for new_queen in pos.generate_moves():
        e = pos.get_position_after_move_queen(new_queen).evaluate()
        if e is not None:
            if not pos.pawns.occupy(new_queen):
                character = {Status.WIN: "-", Status.DRAW: "=", Status.LOSE: "+"}[e]
                board_frame.set_text_on_square(new_queen.file, new_queen.rank, character)
            if e == Status.LOSE:
                board_frame.set_background_highlighted(new_queen.file, new_queen.rank)


def evaluate():
    clear_board_and_set_pieces()

    if queen is None:
        evaluate_pawns_only_board()
    elif player.get() == "pawns":
        evaluate_pawn_moves()
    else:
        evaluate_queen_moves()


def square_pressed(file, rank):
    global queen
    if not (file in FILES and rank in RANKS):
        return

    square = board_frame.squares[file, rank]

    if player.get() == "pawns":
        if rank in (1, 8):
            return

        if queen == (file, rank):
            queen = None

        if file not in pawns:
            pawns[file] = rank
            square.set_white_pawn()
        else:
            board_frame.squares[file, pawns[file]].clear()
            if rank != pawns[file]:
                pawns[file] = rank
                square.set_white_pawn()
            else:
                del pawns[file]

    else:
        if (file, rank) == queen:
            square.clear()
            queen = None
        else:
            if queen is not None:
                board_frame.squares[queen[0], queen[1]].clear()
            if pawns.get(file, -1) == rank:
                del pawns[file]
            square.set_black_queen()
            queen = (file, rank)

    evaluate()


board_frame = Board(root, square_pressed)
board_frame.grid(column=1, row=1)

turn_frame = tk.Frame(root)  # their units in pixels
turn_frame.grid(column=2, row=1)
turn_pawns = tk.Radiobutton(turn_frame, font=CHESS_FONT, text=WHITE_PAWN_CHARACTER, variable=player, value='pawns',
                            command=evaluate)
turn_pawns.grid(column=1, row=1)
turn_queen = tk.Radiobutton(turn_frame, font=CHESS_FONT, text=BLACK_QUEEN_CHARACTER, variable=player, value='queen',
                            command=evaluate)
turn_queen.grid(column=1, row=2)

ttk.Button(root, text="Quit", command=root.destroy).grid(column=2, row=2, sticky="E", padx=10, pady=10)

root.mainloop()
