from copy import deepcopy
from basics import *

# This is a Python script for solving the game "queen vs pawns":
# The game start with the white pawns and the black queen
# on the usual initial squares and those are the only pieces.
#
#       -----------------
#    8 | . . . q . . . . |
#    7 | . . . . . . . . |
#    6 | . . . . . . . . |
#    5 | . . . . . . . . |
#    4 | . . . . . . . . |
#    3 | . . . . . . . . |
#    2 | p p p p p p p p |
#    1 | . . . . . . . . |
#       -----------------
#      a b c d e f g h
#
# White's goal is to promote a pawn. Capturing the queen is also a win.
# Black's goal is to capture all pawns before any promotes.
# The position is draw if there is no legal move, i.e. queen blocks last pawn.

# We might restrict queen moves, not to go to an attacked square.
#    There will always be legal moves left for the queen. Assume not, then:
#       - It cannot be on rank 1 as on rank 1 it can freely move
#       - The square below the queen must be under attack
#         by a pawn in a neighbouring file and two ranks lower
#       - Let us call the rank of the pawn r, one higher s and two higher t,
#       - Let us call the file of the queen x, of the pawn y
#
#               t    Q .             t    . Q
#               s    . .      or     s    . .
#               r    . p             r    p .
#
#                    x y                  y x

#       - The queen might go to the squares ys and yt.
#       - So these squares are under attack by one pawn in the file of the queen (x)
#         and one pawn on the other side of the pawn. Let us call that file z

#               t    Q . .             t    . . Q
#               s    . . .      or     s    . . .
#               r    . p .             r    . p .
#
#                    x y z                  z y x

#       - The queen might go to zr and zt. It cannot be blocked, as ys and yt are empty
#       (as y has a pawn already on r)
#       - Those squares cannot be attacked from the y file, as the pawn in the y file does not
#         attack these squares
#
#       - So we must have two attacking squares in other file next to z. Contradiction.


# So positions have
#       - at most one pawn in each file, ranks between 2 and 8
#       - one queen, not on the same square as a pawn
#       - when white-to-play
#         - no queen on an attacked square
#         - no pawn on rank 8
#         - no pawn at all is possible ==> lost
#       - when black-to-play
#         - at least one pawn
#         - at most one pawn at rank 8 ==> lost
#
# How many positions are possible with white-to-play:
#   rank 2, 3, ..., 7 for each pawn and an additional "rank" for not present. That gives
#   7^8 = 5,764,801 positions
#   For the queen 64 squares when there is no pawn at all.
#   On the other hand, if we have 8 pawn and all attack different squares, then only 64 - 6*3 - 2*2 = 42 are left
#   So a lower bound is 7^8 * 42 = 242,121,642 positions

# It is too much to consider each position and store its value (win, lose, draw, how many moves).
# In cases white wins, some pawns might be irrelevant. For instance: white-to-play with pawns on a6 an b6,
# is a win. We do not need to evaluate all situation for additional pawns in the other files.
# However, additional pawns might give a win in less moves. So we will not store and optimise the number
# of moves till win.  ??????
# For any winning positions for white, it will eventually result in a promotion,
# so we should be able to generate those positions backwards.

# When is a position with white-to-play a win in n moves:
# - n=1: pawn on seventh rank not blocked by the queen
# - n>1: the is a legal pawn move, such that every legal queen-move next
#         results in a position with white to play and win in at most n-1 moves

# We can generate 'all' positions with white to play and win in n moves as follows:
# - n=1: pawn on seventh rank not blocked by the queen
# - n -> n+1: take a position winning position white to play in n moves
#             generate all possible previous positions with white to play
#               do a reverse queen move:
#                   if queen was in a file without pawns, consider with and without pawn on the place of the queen
#                   queen can come from any place, not occupied or block, but it might be attacked by one pawn (not two)
#
#               consider alternative queen moves:
#                   evaluate by taking all subsets of pawns
#               if for all alternative queen moves, there is a pawn subset such that
#                   the position is winning for white
#               then the position is losing for black

#               Then do a reverse pawn move:
#                   if the queen is attacked by one pawn consider only reverse move by that pawn
#                   if not attacked, consider all reverse pawn move, but avoid pawn on queen
#
#               Store this position is win in n+1 unless it is stored already

#   consider [1] a pawn on a6 and a queen on f1. White to play wins in 2 moves.
#   now consider [2] a pawn on a5 and a queen on g2, pawns on g3, f3 and e2. White to play wins in 3 moves,
#   as the queen is blocked to all good squares.
#   From [1] we can do the reverse move Qf1g2. Now we need to add all these pawns
#   to make it winning for the pawns.


# ######################## POSITIONS ##########################


class Pawns:
    def __init__(self, *pawns):
        self.__pawns = {}  # __pawns[file] == None or __pawns[file].file == file
        for pawn in pawns:
            assert isinstance(pawn, Pawn)
            self.set(pawn)

    def __str__(self):
        return " ".join(map(str, self.pawns))

    def set(self, pawn):
        assert isinstance(pawn, Pawn)
        self.__pawns[pawn.file] = pawn  # this will automatically remove any other pawns in this file

    def empty_file(self, file):
        self.__pawns.pop(file, None)

    def empty_square(self, square):
        if self.occupy(square):
            self.empty_file(square.file)

    def count(self):
        return len(self.__pawns)

    @property
    def pawns(self):
        return self.__pawns.values()

    def get_highest_rank(self):
        return max([pawn.file for pawn in self.pawns], default=0)

    def get_nb_promoted(self):
        return sum([pawn.is_promoted() for pawn in self.pawns])

    def get_promoted_pawn(self):
        return next(filter(lambda pawn: pawn.is_promoted(), self.pawns), None)

    def occupy(self, square):
        if square.file in self.__pawns:
            return self.__pawns[square.file].rank == square.rank
        else:
            return False

    def attack(self, square):
        if square.rank == 1:
            return False
        if square.file < 8:
            if self.occupy(SQUARES[square.file + 1, square.rank - 1]):
                return True
        if square.file > 1:
            if self.occupy(SQUARES[square.file - 1, square.rank - 1]):
                return True
        return False

    def pawn_in_file(self, file):
        return self.__pawns.get(file, None)


# ######################## QUEEN MOVES ##########################


class Position:
    def __init__(self, pawns, queen):
        assert isinstance(pawns, Pawns)
        assert isinstance(queen, Queen)
        self.pawns = deepcopy(pawns)
        self.queen = queen

    def is_valid(self):
        return not self.pawns.occupy(self.queen)

    def get_board_as_string(self):
        result = ""
        for r in reversed(ranks):
            result += str(r)
            for f in files:
                if (f, r) == self.queen:
                    result += " Q"
                elif self.pawns.occupy(SQUARES(f, r)):
                    result += " p"
                else:
                    result += " ."
            result += "\n"
        result += "  a b c d e f g h\n"
        return result

    def player(self) -> Player:
        assert False, f"abstract method called on {self}"
        # noinspection PyUnreachableCode
        return Player.WHITE

    def is_lost_by_definition(self):
        assert False, f"abstract method called on {self}"

    def generate_next_positions(self):
        assert False, f"abstract method called on {self}"
        # noinspection PyUnreachableCode
        return []

    def generate_prev_positions(self):
        assert False, f"abstract method called on {self}"
        # noinspection PyUnreachableCode
        return []

    def evaluate(self):
        result = evaluation_store[self]
        if result is not None:
            return result

        if self.is_lost_by_definition():
            evaluation_store.save(self, Status.LOSE)
            return Status.LOSE

        best = Status.LOSE
        stalemate = True
        for next_pos in self.generate_next_positions():
            stalemate = False
            new_eval = next_pos.evaluate()
            if new_eval == Status.LOSE:
                evaluation_store.save(self, Status.WIN)
                return Status.WIN
            if new_eval == Status.DRAW:
                best = Status.DRAW

        if stalemate:
            assert self.player() == Player.WHITE
            evaluation_store.save(self, Status.DRAW)
            return Status.DRAW

        evaluation_store.save(self, best)
        return best


# ######################## EVALUATION ##########################

class PosWhite(Position):
    def player(self):
        return Player.WHITE

    def is_valid(self):
        return (super().is_valid() and
                self.pawns.get_nb_promoted() == 0 and
                not self.pawns.attack(self.queen))

    def is_lost_by_definition(self):
        return self.pawns.count() == 0

    def __repr__(self):
        return f"{self.pawns} {self.queen}"

    def __str__(self):
        return self.__repr__()

    def get_position_after_move_pawn_forward(self, pawn_file, twice=False):
        pawns = deepcopy(self.pawns)
        pawn = pawns.pawn_in_file(pawn_file)
        pawn.move()
        if twice:
            pawn.move()
        return PosBlack(pawns, self.queen)

    def generate_next_positions(self):
        for pawn in self.pawns.pawns:
            if not pawn.is_promoted() and not pawn.is_blocked_by(self.queen):
                yield self.get_position_after_move_pawn_forward(pawn.file)
                if pawn.rank == 2 and (pawn.file, 4) != (self.queen.file, self.queen.rank):
                    yield self.get_position_after_move_pawn_forward(pawn.file, twice=True)

    def get_position_after_move_backwards_queen(self, origin):
        pawns = deepcopy(self.pawns)
        return PosBlack(pawns, origin)

    def generate_prev_positions(self):
        queen_might_have_captured_a_pawn = \
            self.pawns.pawn_in_file(self.queen.file) is None and 2 <= self.queen.rank <= 7

        for d in Queen.DIRECTIONS:
            new_queen = deepcopy(self.queen)
            while new_queen.move(d):
                if self.pawns.occupy(new_queen):
                    break
                yield self.get_position_after_move_backwards_queen(new_queen)
                if queen_might_have_captured_a_pawn:
                    pawn = Pawn(self.queen.square)
                    position = self.get_position_after_move_backwards_queen(new_queen)
                    position.pawns.set(pawn)
                    yield position


class PosBlack(Position):
    def player(self):
        return Player.BLACK

    def is_valid(self):
        return (super().is_valid() and
                self.pawns.count() >= 1 and
                self.pawns.get_nb_promoted() <= 1)

    def is_lost_by_definition(self):
        return self.pawns.get_nb_promoted() > 0

    def __repr__(self):
        return f"{self.queen} {self.pawns}"

    def __str__(self):
        return self.__repr__()

    def get_position_after_move_queen(self, destination):
        pawns = deepcopy(self.pawns)
        pawns.empty_square(destination)
        return PosWhite(pawns, destination)

    def generate_next_positions(self):
        for d in Queen.DIRECTIONS:
            new_queen = deepcopy(self.queen)
            while new_queen.move(d):
                if not self.pawns.attack(new_queen):
                    yield self.get_position_after_move_queen(new_queen)
                if self.pawns.occupy(new_queen):
                    break

    def get_position_after_move_pawn_backwards(self, pawn_file, twice=False):
        pawns = deepcopy(self.pawns)
        pawn = pawns.pawn_in_file(pawn_file)
        pawn.move_backwards()
        if twice:
            pawn.move()
        return PosWhite(pawns, self.queen)

    def generate_prev_positions(self):
        promoted_pawn = self.pawns.get_promoted_pawn()
        if promoted_pawn:
            assert self.pawns.get_nb_promoted() == 1
            yield self.get_position_after_move_pawn_backwards(promoted_pawn.file)
            return

        for pawn in self.pawns.pawns:
            if pawn.rank > 2 and not pawn.is_backward_blocked_by(self.queen):
                yield self.get_position_after_move_pawn_backwards(pawn.file)
                if pawn.rank == 4 and (pawn.file, 2) != (self.queen.file, self.queen.rank):
                    yield self.get_position_after_move_pawn_backwards(pawn.file, twice=True)


class EvaluationStore:
    def __init__(self):
        self.store = {Player.WHITE: [{} for _ in range(9)],
                      Player.BLACK: [{} for _ in range(9)]}
        # i.e. store[p][n] contains positions with n pawns and p to play

    def save(self, position, evaluation):
        assert isinstance(position, Position)
        assert isinstance(evaluation, Status)
        p = position.player()
        n = position.pawns.count()
        code = self.position_to_code(position)
        assert code not in self.store[p][n], f"position already in store: {position}"
        self.store[p][n][code] = evaluation

    def __getitem__(self, position):
        assert isinstance(position, Position)
        assert isinstance(position.pawns, Pawns)
        n = position.pawns.count()
        code = self.position_to_code(position)
        return self.store[position.player()][n].get(code, None)

    def print_stats(self):
        for p in Player:
            print(f"Player: {p.name}")
            print(f"  Number of valid position: {sum([len(x) for x in self.store[p]])}")
            for n in range(9):
                if len(self.store[p][n]) > 0:
                    print(f"    Number of valid positions with {n} pawns: {len(self.store[p][n])}", end=" (")
                    print(f"W={list(self.store[p][n].values()).count(Status.WIN)}", end=" ")
                    print(f"D={list(self.store[p][n].values()).count(Status.DRAW)}", end=" ")
                    print(f"L={list(self.store[p][n].values()).count(Status.LOSE)})")

        for code in self.store[Player.BLACK][2]:
            if self.store[Player.BLACK][2][code] == Status.DRAW:
                print(code)

    @staticmethod
    def position_to_code(position):
        result = [position.queen.file, position.queen.rank]
        for f in files:
            pawn = position.pawns.pawn_in_file(f)
            if pawn is None:
                result += [f, -1]
            else:
                result += [f, pawn.rank]
        return tuple(result)


evaluation_store = EvaluationStore()


def unit_test():
    p = PosWhite(Pawns(), Queen(4, 5))
    assert p.evaluate() == Status.LOSE

    p = PosBlack(Pawns(Pawn(SQUARES[2, 8])), Queen(2, 3))
    assert p.evaluate() == Status.LOSE

    p = PosWhite(Pawns(Pawn(2, 7)), Queen(4, 8))
    assert p.evaluate() == Status.WIN

    p = PosWhite(Pawns(Pawn(2, 7)), Queen(2, 8))
    assert p.evaluate() == Status.DRAW

    p = PosBlack(Pawns(Pawn(2, 6)), Queen(2, 8))
    assert p.evaluate() == Status.WIN


unit_test()


status_char_for_black = {
    (None, Status.WIN): "+", (None, Status.DRAW): "=", (None, Status.LOSE): "-",
    (Status.WIN, Status.WIN): "+", (Status.WIN, Status.DRAW): "D", (Status.WIN, Status.LOSE): "-",
    (Status.DRAW, Status.WIN): "B", (Status.DRAW, Status.DRAW): "E", (Status.DRAW, Status.LOSE): "H",
    (Status.LOSE, Status.WIN): "w", (Status.LOSE, Status.DRAW): "F", (Status.LOSE, Status.LOSE): "z"}


def evaluate(pawns, queen):
    if pawns.occupy(queen):
        return 'p'

    eval_black_to_play = PosBlack(pawns, queen).evaluate()
    eval_white_to_play = None
    p = PosWhite(pawns, queen)
    if p.is_valid():
        eval_white_to_play = p.evaluate()

    return status_char_for_black[(eval_white_to_play, eval_black_to_play)]


evaluation_store = EvaluationStore()


# def print_stats():
#     stat = {}
#     for code in evaluation_store:
#         p = Position(code=code)
#         t = p.turn
#         nb = p.get_nb_pawns()
#         if nb not in stat:
#             stat[nb] = {Player.WHITE: {}, Player.BLACK: {}}
#         d = stat[nb][t]
#         ev = evaluation_store[code]
#         d[ev] = d.get(ev, 0) + 1
#
#     for nb in stat:
#         print(nb, "w", end=" ")
#         for key in stat[nb][Player.WHITE]:
#             print(key.name, stat[nb][Player.WHITE][key], end=" ")
#         print()
#         print(nb, "b", end=" ")
#         for key in stat[nb][Player.BLACK]:
#             print(key.name, stat[nb][Player.BLACK][key], end=" ")
#         print()


def generate_and_evaluate_all_positions_without_pawns():
    for queen in SQUARES.values():
        assert PosWhite(Pawns(), Queen(queen.file, queen.rank)).evaluate() == Status.LOSE


def generate_and_evaluate_all_positions_with_one_pawn():
    for square in SQUARES.values():
        if square.rank > 1:
            pawn = Pawn(square.file, square.rank)
            pawns = Pawns(pawn)
            for queen in SQUARES.values():
                p = PosWhite(pawns, Queen(queen.file, queen.rank))
                if p.is_valid():
                    p.evaluate()
                p = PosBlack(pawns, Queen(queen.file, queen.rank))
                if p.is_valid():
                    p.evaluate()


def generate_and_evaluate_all_positions_with_two_pawns():
    for pawn1 in SQUARES.values():
        for pawn2 in SQUARES.values():
            if pawn1.rank > 1 and pawn2.rank > 1 and pawn1.file < pawn2.file:
                pawns = Pawns(Pawn(pawn1.file, pawn1.rank), Pawn(pawn2.file, pawn2.rank))
                for queen in SQUARES.values():
                    p = PosWhite(pawns, Queen(queen.file, queen.rank))
                    if p.is_valid():
                        p.evaluate()
                    p = PosBlack(pawns, Queen(queen.file, queen.rank))
                    if p.is_valid():
                        p.evaluate()


def generate_and_evaluate_all_positions_with_three_pawns():
    for pawn1 in SQUARES.values():
        for pawn2 in SQUARES.values():
            for pawn3 in SQUARES.values():
                if (pawn1.rank > 1 and pawn2.rank > 1 and pawn3.rank > 1 and
                        pawn1.file < pawn2.file < pawn3.file):
                    pawns = Pawns()
                    pawns.set(pawn1)
                    pawns.set(pawn2)
                    pawns.set(pawn3)
                    for queen in SQUARES.values():
                        p = PosWhite(pawns, queen)
                        if p.is_valid():
                            p.evaluate()
                        p = PosBlack(pawns, queen)
                        if p.is_valid():
                            p.evaluate()


def generate_and_evaluate_all_positions_with(nb_pawns):
    pass


def generate_and_evaluate():
    generate_and_evaluate_all_positions_without_pawns()
    assert len(evaluation_store.store[Player.WHITE][0]) == 64, len(evaluation_store.store[Player.WHITE][0])
    generate_and_evaluate_all_positions_with_one_pawn()
    # white to play:
    #  6 + 6 rook pawns each with 62 queen positions
    #  6 * 6 other pawns each with 61 queen positions
    # so 2 * 6 * 62 + 6 * 6 * 61
    print(len(evaluation_store.store[Player.WHITE][1]))
    print(2 * 6 * 62 + 6 * 6 * 61)
    assert len(evaluation_store.store[Player.WHITE][1]) == 2 * 6 * 62 + 6 * 6 * 61
    # black to play:
    #  8 * 7 pawn positions and 63 queen position
    # no pawns: 64
    print(len(evaluation_store.store[Player.BLACK][1]))
    print(8 * 7 * 63)
    assert len(evaluation_store.store[Player.BLACK][1]) == 8 * 7 * 63
    evaluation_store.print_stats()
    generate_and_evaluate_all_positions_with_two_pawns()
    evaluation_store.print_stats()
    generate_and_evaluate_all_positions_with_three_pawns()
    evaluation_store.print_stats()


def do_example():
    pawns = Pawns()
    pawns.set(SQUARES(4, 5))
    # pawns.set(Square((5, 5))

    for r in reversed(ranks):
        print(r, end="")
        for f in files:
            print(' ', end="")
            queen = SQUARES(f, r)
            print(evaluate(pawns, queen), end="")
        print()


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


if __name__ == "__main__":
    analyse_draw()
    unit_test()
    generate_and_evaluate()
    do_example()
