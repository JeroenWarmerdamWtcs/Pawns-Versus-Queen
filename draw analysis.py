from main import *


def analyse_draw():
    print("Analyse draw")
    # draw in 0
    draw = [[]]
    for square in SQUARES.values():
        if 2 <= square.rank < 8:
            pawn = Pawn(square.file, square.rank)
            pawns = Pawns(pawn)
            p = PosWhite(pawns, Queen(square.file, square.rank+1))
            assert p.evaluate() == Status.DRAW
            draw[0].append(p)
    print(f"- draw by definition: number positions = {len(draw[0])}")
    assert len(draw[0]) == 48

    while draw[-1]:
        # draw in n -> draw in n+1
        draw.append([])
        for p in draw[-2]:
            for q in p.generate_prev_positions():
                if q not in draw[-1]:
                    if q.evaluate() == Status.DRAW:
                        draw[-1].append(deepcopy(q))
        print(f"- draw in {len(draw)-1}: number positions = {len(draw[-1])}", end="")
        if 0 < len(draw[-1]) < 10:
            print(" ", draw[-1])
        else:
            print("")

    input("ready")


analyse_draw()
