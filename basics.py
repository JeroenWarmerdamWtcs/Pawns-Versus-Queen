from enum import IntEnum
from itertools import product

ranks = range(1, 9)
files = range(1, 9)


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

    @property
    def rank(self):
        return self.__rank


def _generate_all_valid_squares_a8_b8___h1():
    result = {}
    for rank in reversed(ranks):
        for file in files:
            result[file, rank] = Square(file, rank)
    return result


SQUARES = _generate_all_valid_squares_a8_b8___h1()


class Piece:
    def __init__(self, *square):
        self.__square = SQUARES[1, 1]
        self.move_to(*square)

    @property
    def square(self):
        return self.__square

    @property
    def file(self):
        return self.square.file

    @property
    def rank(self):
        return self.square.rank

    def move_to(self, *square):
        if len(square) == 1 and isinstance(square[0], Square):
            self.__square = square[0]
        elif len(square) == 2:
            file, rank = square
            self.__square = SQUARES[file, rank]
        else:
            assert False, "wrong argument"


class Pawn(Piece):
    def __init__(self, *square):
        super().__init__(*square)
        assert self.rank > 1

    def is_promoted(self):
        return self.rank == 8

    def is_blocked_by(self, square):
        return (self.file, self.rank + 1) == (square.file, square.rank)

    def is_backward_blocked_by(self, square):
        return (self.file, self.rank - 1) == (square.file, square.rank)

    def attacks(self, square):
        return ((self.file - 1, self.rank + 1) == (square.file, square.rank) or
                (self.file + 1, self.rank + 1) == (square.file, square.rank))

    def move(self):
        assert self.rank < 8
        self.move_to(self.file, self.rank + 1)

    def move_backwards(self):
        assert self.rank > 2
        self.move_to(self.file, self.rank - 1)

    def __str__(self):
        return f"{self.square}"


class Queen(Piece):
    DIRECTIONS = list(product([-1, 0, 1], [-1, 0, 1]))
    DIRECTIONS.remove((0, 0))

    def move(self, direction, nb_steps=1):
        delta_file, delta_rank = direction
        new_file = self.file + nb_steps * delta_file
        new_rank = self.rank + nb_steps * delta_rank
        if 1 <= new_file <= 8 and 1 <= new_rank <= 8:
            self.move_to(new_file, new_rank)
            return True
        else:
            return False

    def __str__(self):
        return f"Q{self.square}"
