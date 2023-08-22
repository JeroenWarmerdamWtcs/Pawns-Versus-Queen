from pyscreenshot import grab
from tkinter import ttk
import tkinter as tk
from chess_board_frame import Board

positions = ["a2, b2, c2, d2, e2, f2, g2, h2, Qd8  # initial position",
             "d4, Qc6, ad5, bd6, ce4, de6  # queen can avoid being captured",
             "Qa3, b6, d6  # draw in 3",
             "d7, Qa5, Qa8, Qb6, Qb8, Qf6, Qf8, Qg5, Qg8, Qh4, Qh8  # draw in 1",
             "a6, g6, Qa1, Qd4, Qg1  # two pawns on 6th rank",
             "a6, h6, Qa1, Qb2, Qg2, Qh1  # two pawns: on a6 and h6",
             "a6, g6, Qb3, Qf3, Qh5  # two pawns: on a6 and g6",
             "a6, f6, Qb4, Qg5  # two pawns on a6 and f6",
             "b6, g6, Qa5, Qc4, Qf4, Qh5  # two pawns: on b6 and g6",
             "a6, e6, Qd1, Qf1  # two pawns: on a6 and e6",
             "b6, f6, Qa1, Qc1, Qe1, Qg1  # two pawns: on b6 and f6",
             "a6, d6, Qc1, Qe1, Qe2  # two pawns: on a6 and d6",
             "b6, e6, Qa2, Qd1, Qd2, Qf1, Qf2  # two pawns: on b6 and e6",
             "c6, f6, Qb2, Qd1, Qe1, Qg2  # two pawns: on c6 and f6",
             "a6, c6, Qd1, =d3  # two pawns: on a6 and c6",
             "b6, d6, Qe1, =a3, =e3  # two pawns: on b6 and d6",
             "c6, e6, Qf1, =b3, =f3  # two pawns: on b6 and d6",
             "a6, h5, Qg2  # h6 is only winning move",
             "b6, g5, Qf4  # g6 is only winning move",
             "b6, f5, Qe5  # Qe7 wins, f6 loses to Qd5, b7 loses to qb8. Why interesting?",
             "a6, c2, e2, g5, Qh1  # g6 wins, all pawns essential",
             "a6, c4, e2, g5, Qh1  # queen wins",
             "d6, e7  # queen win",
             "d5, e7  # queen must capture",
             "d4, e7  # queen must capture",
             "d6, e6  # queen must capture",
             "d5, e6, •c5, •d6, •f6 # queen wins",
             "a6, g6, Qd4",
             "b6, f6, Qd5",
             "c6, e6, Qd6, Qd8",
             "h6,g5,Qd7",
             "e5,f6,Qa2, Qb3,Qc4,Qd5,Qd7,Qg6",
             "a6,h5,Qg2",
             "b6,h5,Qg3",
             "c6,h5,Qg4",
             "f6,a5,Qb4",
             "g6,a5,Qb3",
             "g6,b5,Qc4",
             "h6,a5,Qb2",
             "h6,b5,Qc3",
             "a6, c5, Qd5, •c6, •a5 # also +1",
             "a6, e5, Qd5, •e6, •c5 # also + 1",
             "a6, e5, Qf3, •e6, •e3",
             "a6, f5, Qe4, •f6, •h7",
             "a6, f5, Qg2, •f6, •f2",
             "b6, d5, f5, Qg3"
             ]

root = tk.Tk()


def create_image():
    filename = "position.png"
    f = 1.25
    print(board_frame.winfo_width())
    img = grab(bbox=(
        int((board_frame.winfo_rootx() + 20) * f),
        int((board_frame.winfo_rooty() + 20) * f),
        int((board_frame.winfo_rootx() + board_frame.winfo_width() - 20) * f),
        int((board_frame.winfo_rooty() + board_frame.winfo_height() - 20) * f)))

    # board_frame = 300 x 300, i.e. squares of 30 x 30 and border of 30 on all sides
    # bbox = 260 x 260, i.e. squares of 30 x 30 and border of 10 on all sides
    img = img.resize((200, 200))
    img.save(filename)

    import os
    os.startfile(filename)


def create_image_small():
    filename = "position.png"
    f = 1.25
    img = grab(bbox=(
        int((board_frame.winfo_rootx() + 90) * f),
        int((board_frame.winfo_rooty() + 20) * f),
        int((board_frame.winfo_rootx() + board_frame.winfo_width() - 90) * f),
        int((board_frame.winfo_rooty() + 180) * f)))

    img = img.resize((90, 120))
    img.save(filename)

    import os
    os.startfile(filename)


def show(pos_str):
    if "#" in pos_str:
        title.configure(text=pos_str.split("#")[1].strip())
        pos_str = pos_str.split("#")[0]
    else:
        title.configure(text="")
    board_frame.clear()
    for square in pos_str.split(","):
        square = square.strip()
        character = square[:-2]
        file = "abcdefgh".find(square[-2]) + 1
        rank = int(square[-1])
        if character == "Q":
            board_frame.set_black_queen(file, rank)
        elif character == "":
            board_frame.set_white_pawn(file, rank)
        else:
            board_frame.set_text_on_square(file, rank, character)


def show_next():
    global positions
    positions = positions[1:] + positions[:1]
    show(positions[0])


def show_prev():
    global positions
    positions = positions[-1:] + positions[:-1]
    show(positions[0])


title = tk.Label(root, text="title")
title.grid(column=1, row=0)
board_frame = Board(root, lambda x: None)
board_frame.grid(column=1, row=1)

turn_frame = tk.Frame(root)  # their units in pixels
turn_frame.grid(column=2, row=1)

ttk.Button(turn_frame, text="Prev", command=show_prev).grid(column=1, row=1, sticky="E", padx=10, pady=10)
ttk.Button(turn_frame, text="Next", command=show_next).grid(column=1, row=2, sticky="E", padx=10, pady=10)
ttk.Button(turn_frame, text="Capture all", command=create_image).grid(column=1, row=3, sticky="E", padx=10, pady=10)
ttk.Button(turn_frame, text="Capture part", command=create_image_small).grid(column=1, row=4, sticky="E", padx=10,
                                                                             pady=10)

ttk.Button(root, text="Quit", command=root.destroy).grid(column=2, row=2, sticky="E", padx=10, pady=10)

show(positions[0])

root.mainloop()
