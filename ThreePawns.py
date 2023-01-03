def queen_wins_against_three_pawns_in_adjacent_files_at_rank_5_or_lower():
    for s1 in SQUARES.values():
        if 2 <= s1.rank <= 5:
            print("***", s1)
            for s2 in SQUARES.values():
                if 2 <= s2.rank <= 5 and s1.file + 1 == s2.file:
                    for s3 in SQUARES.values():
                        if 2 <= s3.rank <= 5 and s2.file + 1 == s3.file:
                            for sq in SQUARES.values():
                                if str(sq) not in [str(s1), str(s2), str(s3)]:
                                    pawn1 = Pawn(s1.file, s1.rank)
                                    pawn2 = Pawn(s2.file, s2.rank)
                                    pawn3 = Pawn(s3.file, s3.rank)
                                    pawns = Pawns(pawn1, pawn2, pawn3)
                                    queen = Queen(sq.file, sq.rank)
                                    p = PosWhite(pawns, queen)
                                    if p.evaluate() != Status.WIN:
                                        print(p, p.evaluate())
                                    # if p.evaluate() != Status.LOSE:
                                    #    queen_always_loses = False
                                    #    break
                            # if queen_always_loses:
                            #    print(s1, s2)


for s1 in SQUARES.values():
    if 5 <= s1.rank <= 5:
        print("***", s1)
        for s2 in SQUARES.values():
            if 5 <= s2.rank <= 5 and s1.file + 1 == s2.file:
                for s3 in SQUARES.values():
                    if 5 <= s3.rank <= 5 and s2.file + 1 == s3.file:
                        queen_always_loses = True
                        for sq in SQUARES.values():
                            if sq not in [s1, s2, s3]:
                                pawn1 = Pawn(s1.file, s1.rank)
                                pawn2 = Pawn(s2.file, s2.rank)
                                pawn3 = Pawn(s3.file, s3.rank)
                                pawns = Pawns(pawn1, pawn2, pawn3)
                                queen = Queen(sq.file, sq.rank)
                                p = PosWhite(pawns, queen)
                                if p.evaluate() != Status.WIN:
                                    print(p, p.evaluate())
                                # if p.evaluate() != Status.LOSE:
                                #    queen_always_loses = False
                                #    break
                        # if queen_always_loses:
                        #    print(s1, s2)



