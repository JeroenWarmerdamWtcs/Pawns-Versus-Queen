import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import main

files = range(1, 9)
ranks = range(1, 9)

pawns = {}  # dict from files to ranks. No pawn means not in dict

sq = {}  # dict of (files, ranks) to Square class


root = tk.Tk()
# noinspection SpellCheckingInspection
pawn_image = tk.PhotoImage(file=r"C:\Users\jhawa\Documents\Jeroen\Diverse Code\PawnsVsQueen\pawn.png")


def eval():
    for qr in ranks:
        for qf in files:
            s = main.SetUp()
            for pf in pawns:
                s.set_pawn((pf, pawns[pf]))
            e = main.evaluate(s, qf, qr)
            sq[(qf, qr)]._btn.config(text=e)


def square_pressed(file, new_rank):
    if not (file in files and
            new_rank in ranks and
            new_rank > 1):
        return

    if file not in pawns:
        pawns[file] = new_rank
        sq[(file, new_rank)].set_pawn()
    else:
        old_rank = pawns[file]
        sq[(file, old_rank)].remove_pawn()
        if new_rank != old_rank:
            pawns[file] = new_rank
            sq[(file, new_rank)].set_pawn()
        else:
            del pawns[file]

    eval()


class Square(ttk.Frame):
    def __init__(self, parent, file, rank):
        self.file = file
        self.rank = rank
        ttk.Frame.__init__(self, parent, height=20, width=20, style="Square.TFrame")

        self.pack_propagate(0)
        self._btn = tk.Button(self,
                              command=lambda: square_pressed(self.file, self.rank),
                              bd=0)
        if file % 2 == rank % 2:
            self._btn.config(activebackground='#b7f731')
            self._btn.config(bg='#b7f731')
        self._btn.pack(fill=tk.BOTH, expand=1)

    def set_pawn(self):
        self._btn.configure(image=pawn_image)

    def remove_pawn(self):
        self._btn.configure(image="")


frm = ttk.Frame(root, padding=10)
frm.grid()
board = ttk.Frame(frm, padding=10)
board.grid(column=1, row=1, rowspan=2)

for f in files:
    for r in ranks:
        sq[(f, r)] = Square(board, f, r)
        sq[(f, r)].grid(column=f, row=9 - r)

tk.Button(frm, text="Quit", command=root.destroy).grid(column=9, row=2)
root.mainloop()
