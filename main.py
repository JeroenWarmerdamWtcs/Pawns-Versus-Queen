from itertools import product
from enum import IntEnum
from copy import deepcopy

# This is a Python script for solving the game "queen vs pawns":
# The game start with the white pawns and the black queen
# on the usual initial squares and those are the only pieces.
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


#       So positions have
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

files = range(1, 8 + 1)
ranks = range(1, 8 + 1)


class Player(IntEnum):
    WHITE = 1
    BLACK = -1


class Status(IntEnum):
    WIN = 1
    DRAW = 0
    LOSE = -1


class Square:
    def __init__(self, file, rank):
        assert 1 <= file <= 8
        assert 1 <= rank <= 8
        self.__file = file
        self.__rank = rank

    def __str__(self):
        # noinspection SpellCheckingInspection
        return "_abcdefgh"[self.file] + str(self.rank)

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        assert 1 <= value <= 8
        self.__file = value

    def _get_rank(self):
        return self.__rank

    def _set_rank(self, value):
        assert 1 <= value <= 8, value
        self.__rank = value

    rank = property(_get_rank, _set_rank)


def generate_all_valid_squares_a8_b8___h1():
    for rank in reversed(ranks):
        for file in files:
            yield Square(file, rank)


class Pawn(Square):
    def __init__(self, file, rank):
        assert rank > 1
        super().__init__(file, rank)

    def _set_rank(self, value):
        assert value != 1
        super()._set_rank(value)

    def is_promoted(self):
        return self.rank == 8

    def is_blocked(self, square):
        return self.file == square.file and self.rank + 1 == square.rank

    def attacks(self, square):
        return abs(self.file - square.file) == 1 and self.rank + 1 == square.rank

    def move(self):
        assert self.rank < 8
        self.rank += 1


class Queen(Square):
    DIRECTIONS = list(product([-1, 0, 1], [-1, 0, 1]))
    DIRECTIONS.remove((0, 0))

    def move(self, direction, nb_steps=1):
        delta_file, delta_rank = direction
        new_file = self.file + nb_steps * delta_file
        new_rank = self.rank + nb_steps * delta_rank
        if 1 <= new_file <= 8 and 1 <= new_rank <= 8:
            self.file = new_file
            self.rank = new_rank
            return True
        else:
            return False


class Pawns:
    def __init__(self, *pawns):
        self.__pawns = {}  # __pawns[file] == None or __pawns[file].file == file
        for pawn in pawns:
            self.set(pawn)

    def __str__(self):
        return " ".join(map(str, self.pawns))

    def set(self, pawn):
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

    def occupy(self, square):
        if square.file in self.__pawns:
            return self.__pawns[square.file].rank == square.rank
        else:
            return False

    def attack(self, square):
        if square.rank == 1:
            return False
        if square.file < 8:
            if self.occupy(Square(square.file + 1, square.rank - 1)):
                return True
        if square.file > 1:
            if self.occupy(Square(square.file - 1, square.rank - 1)):
                return True

    def pawn_in_file(self, file):
        return self.__pawns.get(file, None)


# ######################## QUEEN MOVES ##########################


class Position:
    def __init__(self, pawns, queen):
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
                elif self.pawns.occupy(Square(f, r)):
                    result += " p"
                else:
                    result += " ."
            result += "\n"
        result += "  a b c d e f g h\n"
        return result

    def player(self):
        assert False, f"abstract method called on {self}"

    def is_lost_by_definition(self):
        assert False, f"abstract method called on {self}"

    def generate_next_positions(self):
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
        return f"{self.pawns} Q{self.queen}"

    def __str__(self):
        return self.__repr__()

    def get_position_after_move_pawn_forward(self, pawn, twice=False):
        pawns = deepcopy(self.pawns)
        up = (0, 1)
        pawn.move()
        if twice:
            pawn.move(up)
        return PosBlack(pawns, self.queen)

    def generate_next_positions(self):
        for pawn in self.pawns.pawns:
            if not pawn.is_promoted() and not pawn.is_blocked(self.queen):
                yield self.get_position_after_move_pawn_forward(pawn)
                if pawn.rank == 2 and (pawn.file, 4) != (self.queen.file, self.queen.rank):
                    yield self.get_position_after_move_pawn_forward(pawn, twice=True)


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
        return f"Q{self.queen} {self.pawns}"

    def __str__(self):
        return self.__repr__()

    def get_position_after_move_queen(self, destination):
        pawns = deepcopy(self.pawns)
        pawns.empty_square(destination)
        return PosWhite(pawns, destination)

    def generate_next_positions(self):
        for d in Queen.DIRECTIONS:
            new_queen = deepcopy(self.queen)
            new_queen.move(d)
            while new_queen.move(d):
                if not self.pawns.attack(new_queen):
                    yield self.get_position_after_move_queen(new_queen)
                if self.pawns.occupy(new_queen):
                    break


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
        print("Number: ", sum([len(x) for x in self.store]))
        for n in range(9):
            if len(self.store[n]) > 0:
                print("  ", n, ": ", len(self.store[n]))

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

    p = PosBlack(Pawns(Pawn(2, 8)), Queen(2, 3))
    assert p.evaluate() == Status.LOSE

    p = PosWhite(Pawns(Pawn(2, 7)), Queen(4, 8))
    assert p.evaluate() == Status.WIN

    p = PosWhite(Pawns(Pawn(2, 7)), Queen(2, 8))
    assert p.evaluate() == Status.DRAW

    p = PosBlack(Pawns(Pawn(2, 6)), Queen(2, 8))
    assert p.evaluate() == Status.WIN


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
    for queen in generate_all_valid_squares_a8_b8___h1():
        assert PosWhite(Pawns(), queen).evaluate() == Status.LOSE


def generate_and_evaluate_all_positions_with_one_pawn():
    for pawn in generate_all_valid_squares_a8_b8___h1():
        if pawn.rank > 1:
            pawns = Pawns()
            pawns.set(pawn)
            for queen in generate_all_valid_squares_a8_b8___h1():
                p = PosWhite(pawns, queen)
                if p.is_valid():
                    p.evaluate()
                p = PosBlack(pawns, queen)
                if p.is_valid():
                    p.evaluate()


def generate_and_evaluate_all_positions_with_two_pawns():
    for pawn1 in generate_all_valid_squares_a8_b8___h1():
        for pawn2 in generate_all_valid_squares_a8_b8___h1():
            if pawn1.rank > 1 and pawn2.rank > 1 and pawn1.file < pawn2.file:
                pawns = Pawns()
                pawns.set(pawn1)
                pawns.set(pawn2)
                for queen in generate_all_valid_squares_a8_b8___h1():
                    p = PosWhite(pawns, queen)
                    if p.is_valid():
                        p.evaluate()
                    p = PosBlack(pawns, queen)
                    if p.is_valid():
                        p.evaluate()


def generate_and_evaluate_all_positions_with_three_pawns():
    for pawn1 in generate_all_valid_squares_a8_b8___h1():
        for pawn2 in generate_all_valid_squares_a8_b8___h1():
            for pawn3 in generate_all_valid_squares_a8_b8___h1():
                if (pawn1.rank > 1 and pawn2.rank > 1 and pawn3.rank > 1 and
                        pawn1.file < pawn2.file < pawn3.file):
                    pawns = Pawns()
                    pawns.set(pawn1)
                    pawns.set(pawn2)
                    pawns.set(pawn3)
                    for queen in generate_all_valid_squares_a8_b8___h1():
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
    assert len(evaluation_store.store[0]) == 64
    generate_and_evaluate_all_positions_with_one_pawn()
    # white to play:
    #  6 + 6 rook pawns each with 62 queen positions
    #  6 * 6 other pawns each with 61 queen positions
    # so 2 * 6 * 62 + 6 * 6 * 61
    # black to play:
    #  8 * 7 pawn positions and 63 queen position
    # no pawns: 64
    print(len(evaluation_store.store[1]))
    print(2 * 6 * 62 + 6 * 6 * 61 + 8 * 7 * 63)
    assert len(evaluation_store.store[1]) == 2 * 6 * 62 + 6 * 6 * 61 + 8 * 7 * 63
    evaluation_store.print_stats()
    generate_and_evaluate_all_positions_with_two_pawns()
    evaluation_store.print_stats()
    generate_and_evaluate_all_positions_with_three_pawns()
    evaluation_store.print_stats()


def do_example():
    pawns = Pawns()
    pawns.set(Square(4, 5))
    # pawns.set(Square((5, 5))

    for r in reversed(ranks):
        print(r, end="")
        for f in files:
            print(' ', end="")
            queen = Square(f, r)
            print(evaluate(pawns, queen), end="")
        print()


if __name__ == "__main__":
    unit_test()
    generate_and_evaluate()
    do_example()

# evaluation_white = {}
# evaluation_black = {}
#
# for q in squares():
#     p = Position(queen=q)
#     code = p.id()
#     evaluation_white[code] = "lose"
#     evaluation_black[code] = "invalid"
#
# assert len(evaluation_white) == len(evaluation_black) == 64
#
# count = 0
# for s in squares():
#     pawn_file, pawn_rank = s
#     if valid_pawn_rank(pawn_rank):
#         for q in squares():
#             if s != q:
#                 p = Position(queen=q)
#                 p.set_pawn(s)
#                 code = p.id()
#                 if pawn_rank == 8:
#                     evaluation_white[code] = "invalid"
#                     evaluation_black[code] = "lose"
#                 elif p.attacked_by_pawn(q):
#                     evaluation_white[code] = "win"
#                     evaluation_black[code] = "win"
#                 else:
#                     evaluation_white[code] = "unknown"
#                     evaluation_black[code] = "unknown"
#
# assert len(evaluation_white) == len(evaluation_black) == 64 + 56 * 63
#
# for code in evaluation_white:
#     if evaluation_white[code] == "unknown":
#         position = Position(code=code)
#         move_found = False
#         all_moves_are_losing = True
#         some_moves_are_winning = False
#         for p in position.generate_next_positions_after_a_pawn_move():
#             move_found = True
#             eval_black_to_play = evaluation_black[p.id()]
#             if eval_black_to_play == "lose":
#                 some_moves_are_winning = True
#                 break
#             if eval_black_to_play == "unknown":
#                 all_moves_are_losing = False
#         if not move_found:
#             evaluation_white[code] = "draw"
#         elif some_moves_are_winning:
#             evaluation_white[code] = "win"
#         elif all_moves_are_losing:
#             evaluation_white[code] = "lose"
#
#
#
#
#
#
#
# exit()
#
# evaluation = {}
# new_work = []
# # evaluation[position] = n means:
# #   with white-to-play in position it can guarantee a win in n moves
#
# # initialisation: evaluation[position] = 1
#
#
# def init_evaluation():
#     for queen_square in product(files, ranks):
#         for pawn_file in files:
#             pawn_square = (pawn_file, LAST_RANK - 1)
#             pawn_square_next = (pawn_file, LAST_RANK)
#             if queen_square not in [pawn_square, pawn_square_next]:
#                 position = Position(queen=queen_square)
#                 position.set_pawn(pawn_square)
#                 if not position.attacked_by_pawn(queen_square):
#                     evaluation[position.id()] = 1
#
#
# def get_evaluation(position):
#     for nb_pawns in range(1, 9):  # 0 pawns will not win
#         for selection in combinations(range(8), nb_pawns):
#             less_pawns = Position(queen=position.queen)
#             valid = True
#             for file in selection:
#                 if position.pawns[file] > 0:
#                     less_pawns.set_pawn((file, position.pawns[file]))
#                 else:
#                     valid = False
#                     break
#             if valid:
#                 result = evaluation.get(less_pawns.id(), None)
#                 if result is not None:
#                     return result
#     return None
#
#
# def generate_new_evaluations(position):
#     found = str(position) == "Q: c3 p: c6 d4 f5"
#
#     for prev in position.generate_prev_positions_before_a_queen_move():
#         if found:
#             print("prev", prev)
#         best_nb = 0
#         winning = True
#         for _next in prev.generate_next_positions_after_a_queen_move():
#             _evaluation = get_evaluation(_next)
#             if found:
#                 print("_next", _next)
#             if get_evaluation(_next) is None:
#                 if found:
#                     print("None")
#                 winning = False
#                 break
#             best_nb = max(best_nb, _evaluation)
#         if winning:
#             for prev_prev in prev.generate_prev_positions_before_a_pawn_move():
#                 if get_evaluation(prev_prev) is None:
#                     prev_prev_id = prev_prev.id()
#                     evaluation[prev_prev_id] = best_nb + 1
#                     new_work.append(prev_prev_id)
#
#
# def main():
#     global new_work
#     init_evaluation()
#     assert len(evaluation) == 482
#     new_work = list(evaluation.keys())
#     while new_work:
#         print(len(new_work))
#         input("press enter to continue")
#         work = new_work
#         new_work = []
#         for p in work:
#             generate_new_evaluations(Position(code=p))
#         for p in new_work:
#             position = Position(code=p)
#             print(evaluation[p], position)
#
#
# main()
