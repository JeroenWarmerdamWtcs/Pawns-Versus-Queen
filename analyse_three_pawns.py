from main import *


def check_pawns_win_against_queen_on_all_legal_squares(pawns):
    for sq in BOARD.squares:
        queen = Queen(sq)
        if sq not in [p.square for p in pawns.squares]:
            pos = PosWhite(pawns, queen)
            if pos.is_valid():
                assert pos.evaluate() == Status.WIN, pos


def check_queen_wins_on_all_legal_squares(pawns):
    for square in filter(lambda sq: sq not in pawns, BOARD.squares):
        pos = PosBlack(pawns, Queen(sq))
        if pos.is_valid():
            assert pos.evaluate() == Status.WIN, pos


def queen_wins_against_three_pawns_in_adjacent_files_at_rank_5_or_lower():
    print("checking queen_wins_against_three_pawns_in_adjacent_files_at_rank_5_or_lower", end="")
    for f1 in range(1, 7):
        for r1 in range(2, 6):
            s1 = BOARD.get_square(f1, r1)
            print(f" {s1}", end="")
            for r2 in range(2, 6):
                s2 = BOARD.get_square(f1 + 1, r2)
                print(f" {s2}", end="")
                for r3 in range(2, 6):
                    s3 = BOARD.get_square(f1 + 2, r3)
                    print(f" {s3}", end="")
                    pawns = Pawns(s1, s2, s3)
                    check_queen_wins_on_all_legal_squares(pawns)
                    print("\b" * len(f" {s3}"), end="")
                print("\b" * len(f" {s2}"), end="")
            print("\b" * len(f" {s1}"), end="")
    print(" OK")


def three_pawns_one_isolated():
    print("checking three pawn, one isolated ", end="")
    for f1 in FILES:
        s1 = BOARD.get_square(f1, 6)
        print(s1, end="")
        for f2 in [f for f in FILES if abs(f - f1) == 1]:
            s2 = BOARD.get_square(f2, 5)
            for f3 in [f for f in FILES if abs(f - f1) > 1 and abs(f - f2) > 1]:
                for r3 in range(2, 7):
                    s3 = BOARD.get_square(f3, r3)
                    pawns = Pawns(s1, s2, s3)
                    if abs(f3 - f2) == 3 and abs(f3 - f1) == 4 and r3 == 2:
                        # Exceptional case I
                        for sq in [sq for sq in BOARD.squares if sq not in [s1, s2, s3]]:
                            pos = PosWhite(pawns, Queen(sq))
                            if pos.is_valid():
                                if sq != BOARD.get_square(f3, 3):
                                    assert pos.evaluate() == Status.LOSE, pos
                                else:
                                    assert pos.evaluate() == Status.WIN, pos
                    elif abs(f3 - f2) == 2 and abs(f3 - f1) == 3 and r3 <= 3:
                        # Exceptional case II
                        for sq in BOARD.squares:
                            if sq not in [s1, s2, s3]:
                                pos = PosWhite(pawns, Queen(sq))
                                if pos.is_valid():
                                    if (f2 - f1) * (7 - sq.rank) == sq.file - f1:
                                        assert pos.evaluate() == Status.LOSE, pos
                                    elif sq.file == f1 and sq.rank in [1, 4]:
                                        assert pos.evaluate() == Status.LOSE, pos
                                    else:
                                        assert pos.evaluate() == Status.WIN, pos
                    else:
                        # General
                        check_pawns_win_against_queen_on_all_legal_squares(pawns)

        print("\b" * len(str(s1)), end="")
    print("OK")


def three_pawns_xxx():
    print("checking three_pawns_xxx ", end="")
    for s1 in [s for s in BOARD.squares if 1 < s.rank < 5]:
        print(s1, end="")
        for s2 in [s for s in BOARD.squares if 1 < s.rank < 5 and s1.file < s.file]:
            print(s2, end="")
            for s3 in [s for s in BOARD.squares if 1 < s.rank < 5 and s2.file < s.file]:
                print(s3, end="")
                pawns = Pawns(s1, s2, s3)
                check_queen_wins_on_all_legal_squares(pawns)
                print("\b" * len(str(s3)), end="")
            print("\b" * len(str(s2)), end="")
        print("\b" * len(str(s1)), end="")
    print("OK")


def try_something():
    s1 = BOARD.get_square(3, 5)
    s2 = BOARD.get_square(4, 4)
    s3 = BOARD.get_square(6, 4)
    for sq in BOARD.squares:
        if sq not in [s1, s2, s3]:
            pos = PosWhite(Pawns(s1, s2, s3), Queen(sq))
            if pos.is_valid() and pos.evaluate() != Status.WIN:
                print(pos, pos.evaluate())


# queen_wins_against_three_pawns_in_adjacent_files_at_rank_5_or_lower()
# three_pawns_one_isolated()
try_something()
three_pawns_xxx()
