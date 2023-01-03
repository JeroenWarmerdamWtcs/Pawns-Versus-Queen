from main import *


def queen_wins_against_two_pawns_at_most_one_at_rank_6():
    print("checking queen_wins_against_two_pawns_at_most_one_at_rank_6")
    for s1 in [sq for sq in SQUARES.values() if 2 <= sq.rank <= 6]:
        for s2 in [sq for sq in SQUARES.values() if 2 <= sq.rank <= 6]:
            if (s1.rank < 6 or s2.rank < 6) and s1.file < s2.file:
                for sq in SQUARES.values():
                    if sq not in [s1, s2]:
                        pos = PosBlack(Pawns(Pawn(s1), Pawn(s2)), Queen(sq))
                        assert pos.evaluate() == Status.WIN


def queen_loses_against_two_pawns_at_rank_7():
    print("checking queen_loses_against_two_pawns_at_rank_7")
    for f1 in files:
        s1 = SQUARES[f1, 7]
        for f2 in files:
            if f1 < f2:
                s2 = SQUARES[f2, 7]
                for sq in SQUARES.values():
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(Pawn(s1), Pawn(s2)), Queen(sq))
                        assert p.evaluate() == Status.LOSE, p


def queen_loses_against_defended_pawn_at_rank_7():
    print("checking queen_loses_against_defended_pawn_at_rank_7")
    for f1 in files:
        s1 = SQUARES[f1, 7]
        for f2 in files:
            if abs(f1 - f2) == 1:
                s2 = SQUARES[f2, 6]  # s2 defends s1
                for sq in SQUARES.values():
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(Pawn(s1), Pawn(s2)), Queen(sq))
                        assert p.evaluate() == Status.LOSE, p


def queen_wins_against_two_isolated_pawns_at_rank_6():
    print("checking queen_wins_against_two_isolated_pawns_at_rank_6")
    for f1 in files:
        s1 = SQUARES[f1, 6]
        for f2 in files:
            if f2 > f1 + 1:
                s2 = SQUARES[f2, 6]
                for sq in SQUARES.values():
                    if sq not in [s1, s2]:
                        p = PosBlack(Pawns(Pawn(s1), Pawn(s2)), Queen(sq))
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


queen_wins_against_two_pawns_at_most_one_at_rank_6()
queen_loses_against_two_pawns_at_rank_7()
queen_loses_against_defended_pawn_at_rank_7()
queen_wins_against_two_isolated_pawns_at_rank_6()
