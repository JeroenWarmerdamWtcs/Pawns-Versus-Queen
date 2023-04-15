from basics import *
from functools import partial
import tkinter as tk

PIECES = u"\u2654\u2655\u2656\u2657\u2658\u2659\u265A\u265B\u265C\u265D\u265E\u265F"
WHITE_PAWN_CHARACTER = PIECES[5]
BLACK_QUEEN_CHARACTER = PIECES[7]
CHESS_FONT = ('Segoe UI Symbol', 20)


class Square(tk.Frame):
    def __init__(self, parent, is_dark_square, call_back):
        super().__init__(parent, width=30, height=30)
        self.is_dark_square = is_dark_square
        self.grid_propagate(False)  # disables resizing of frame
        self.columnconfigure(0, weight=1)  # enables button to fill frame
        self.rowconfigure(0, weight=1)  # any positive number would do the trick
        self.square_button = tk.Button(
            self,
            font=CHESS_FONT,
            command=call_back,
            relief=tk.FLAT)
        self.square_button.grid(sticky="wens")  # makes the button expand
        self.clear()

    def clear(self):
        self.set_text("")
        self.set_background_normal()

    def set_text(self, text):
        self.square_button.configure(text=text)

    def set_white_pawn(self):
        self.set_text(WHITE_PAWN_CHARACTER)

    def set_black_queen(self):
        self.set_text(BLACK_QUEEN_CHARACTER)

    def __set_background(self, color):
        self.square_button.configure(bg=color, activebackground=color)

    def set_background_normal(self):
        self.__set_background("lightgray" if self.is_dark_square else "white")

    def set_background_highlighted(self):
        self.__set_background("light green" if self.is_dark_square else "#D3FFD8")


class Board(tk.Frame):
    def __init__(self, parent, call_back):
        super().__init__(parent, padx=30, pady=30)
        self.square_pressed = call_back
        self.squares = {}

        for file in files:
            for rank in ranks:
                is_dark_square = file % 2 == rank % 2
                self.squares[file, rank] = Square(self, is_dark_square, partial(self.square_pressed, file, rank))
                self.squares[file, rank].grid(row=8-rank, column=file)  # put frame where the button should be

    def set_text_on_square(self, file, rank, text):
        self.squares[file, rank].set_text(text)

    def set_white_pawn(self, file, rank):
        self.squares[file, rank].set_white_pawn()

    def set_black_queen(self, file, rank):
        self.squares[file, rank].set_black_queen()

    def set_background_normal(self, file, rank):
        self.squares[file, rank].set_background_normal()

    def set_background_highlighted(self, file, rank):
        self.squares[file, rank].set_background_highlighted()

    def clear(self):
        for file in files:
            for rank in ranks:
                self.squares[file, rank].clear()
