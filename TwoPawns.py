from main import *


def queen_wins_against_two_pawns_at_most_one_at_rank_6():
    print("checking queen_wins_against_two_pawns_at_most_one_at_rank_6")
    for s1 in [sq for sq in BOARD.squares if 2 <= sq.rank <= 6]:
        for s2 in [sq for sq in BOARD.squares if 2 <= sq.rank <= 6]:
            if (s1.rank < 6 or s2.rank < 6) and s1.file < s2.file:
                for sq in BOARD.squares:
                    if sq not in [s1, s2]:
                        pos = PosBlack(Pawns(s1, s2), Queen(sq))
                        assert pos.evaluate() == Status.WIN


def queen_loses_against_two_pawns_at_rank_7():
    print("checking queen_loses_against_two_pawns_at_rank_7")
    for f1 in FILES:
        s1 = BOARD.get_square(f1, 7)
        for f2 in FILES:
            if f1 < f2:
                s2 = BOARD.get_square(f2, 7)
                for sq in BOARD.squares:
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(s1, s2), Queen(sq))
                        assert p.evaluate() == Status.LOSE, p


def queen_loses_against_defended_pawn_at_rank_7():
    print("checking queen_loses_against_defended_pawn_at_rank_7")
    for f1 in FILES:
        s1 = BOARD.get_square(f1, 7)
        for f2 in FILES:
            if abs(f1 - f2) == 1:
                s2 = BOARD.get_square(f2, 6)  # s2 defends s1
                for sq in BOARD.squares:
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(s1, s2), Queen(sq))
                        assert p.evaluate() == Status.LOSE, p


def queen_wins_against_two_isolated_pawns_at_rank_6():
    #  NOT TRUE
    print("checking queen_wins_against_two_isolated_pawns_at_rank_6")
    for f1 in FILES:
        s1 = BOARD.get_square(f1, 6)
        for f2 in FILES:
            if f2 > f1 + 1:
                s2 = BOARD.get_square(f2, 6)
                for sq in BOARD.squares:
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(s1, s2), Queen(sq))
                        if p.evaluate() == Status.LOSE:
                            print(p)
                        if sq.rank >= 6:
                            # queen can move to or stay on 7th rank
                            assert p.evaluate() == Status.WIN, p
                        elif abs(sq.file - f1) > 1 and abs(sq.file - f2) > 1:
                            # queen can move vertically to 7th rank
                            assert p.evaluate() == Status.WIN, p
                        elif sq.file in [f1, f2]:
                            # queen can move vertically so it diagonally attacks square in front of other
                            # if it does already, she can move horizontally to file of other square
                            # Only exception are pawns on a6 and h6. Then a1 is not low enough.
                            # Still, on most square the queen can move to the 7th rank. Except for square a1 and h1
                            if not ([f1, f2] == [1, 8] and sq.rank == 1):
                                assert p.evaluate() == Status.WIN, p


def pawns_win_often_with_defended_pawn_at_rank_6():
    print("checking pawns_win_often_with_defended_pawn_at_rank_6")
    for f1 in FILES:
        s1 = BOARD.get_square(f1, 6)
        for f2 in FILES:
            if abs(f1 - f2) == 1:
                s2 = BOARD.get_square(f2, 5)  # s2 defends s1
                for sq in BOARD.squares:
                    if sq not in [s1, s2]:
                        pos = PosWhite(Pawns(s1, s2), Queen(sq))
                        if pos.is_valid():
                            if sq.file == f1:
                                # win pawn 1 whether it moves or not
                                assert pos.evaluate() == Status.LOSE, pos
                            elif (f2 - f1) * (7 - sq.rank) == sq.file - f1:
                                # queen on diagonal through squares in front of the pawns:
                                # take pawn that moves
                                assert pos.evaluate() == Status.LOSE, pos
                            elif sq.rank == 8 and sq.file == f2:
                                # queen on diagonal through squares in front of the pawns:
                                # capture pawn that moves
                                assert pos.evaluate() == Status.LOSE, pos
                            elif sq.rank == 7 and sq.file == f2 + f2 - f1:
                                # capture pawn that moves
                                assert pos.evaluate() == Status.LOSE, pos
                            elif sq.rank == 6 and sq.file == f1 + f1 - f2:
                                # capture pawn that moves
                                assert pos.evaluate() == Status.LOSE, pos
                            else:
                                assert pos.evaluate() == Status.WIN, pos


def check_lower_rank_push_mandatory():
    print("checking ")
    i = 0
    for gap in range(5):
        print(gap)
        for p1 in range(2, 8):
            for p2 in range(2, 8):
                for p3 in range(2, 8):
                    for p4 in range(2, 8):
                        for qf in range(4):
                            for qr in range(2, 8):
                                i = i + 1

    print(i)

    for s1 in [sq for sq in BOARD.squares if 3 <= sq.rank <= 6]:
        for s2 in [sq for sq in BOARD.squares if 2 <= sq.rank < s1.rank and s1.file != sq.file]:
            for sq in [sq for sq in BOARD.squares if sq.file not in [s1.file, s2.file] and sq.rank not in [1, 8]]:
                pos = PosWhite(Pawns(s1, s2), Queen(sq))
                if pos.evaluate() == Status.WIN:
                    s1_push = BOARD.get_square(s1.file, s1.rank + 1)
                    pos2 = PosBlack(Pawns(s1_push, s2), Queen(sq))
                    if pos2.evaluate() == Status.WIN:
                        if abs(s1.file - s2.file) > 1:
                            print(f'"{str(pos).replace(" ", ",")}",')


queen_wins_against_two_pawns_at_most_one_at_rank_6()
queen_loses_against_two_pawns_at_rank_7()
queen_loses_against_defended_pawn_at_rank_7()
queen_wins_against_two_isolated_pawns_at_rank_6()
pawns_win_often_with_defended_pawn_at_rank_6()
check_lower_rank_push_mandatory()
