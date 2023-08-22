from enum import IntEnum, Enum, unique
from typing import Dict, Tuple
from copy import copy

RANKS = range(1, 9)
FILES = range(1, 9)


class Player(IntEnum):
    WHITE = 1
    BLACK = -1


class Status(IntEnum):
    WIN = 1
    DRAW = 0
    LOSE = -1

    def __str__(self):
        return {Status.WIN: "+", Status.DRAW: '=', Status.LOSE: "-"}[self]


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


@unique
class Direction(IntEnum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


@unique
class DirectionVector(Enum):
    N = (0, 1)
    NE = (1, 1)
    E = (1, 0)
    SE = (1, -1)
    S = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (-1, 1)


def _generate_all_valid_squares_a8_b8___h1() -> Dict[Tuple[int, int], Square]:
    result = {}
    for rank in reversed(RANKS):
        for file in FILES:
            result[file, rank] = Square(file, rank)
    return result


def _generate_neighbours(squares: Dict[Tuple[int, int], Square]) -> Dict[Square, Dict[Direction, Square]]:
    result = {sq: {d: None for d in Direction} for sq in squares.values()}
    for d in Direction:
        df, dr = DirectionVector[d.name].value
        for sq in squares.values():
            f = sq.file + df
            r = sq.rank + dr
            result[sq][d] = squares.get((f, r), None)
    return result


class Board:
    def __init__(self):
        self._square_dict = _generate_all_valid_squares_a8_b8___h1()
        self._neighbours = _generate_neighbours(self._square_dict)
        self._pawn_squares = [sq for sq in self.squares if sq.rank > 1]

    def get_square(self, file, rank):
        return self._square_dict[file, rank]

    @property
    def squares(self):
        return self._square_dict.values()

    def get_neighbour(self, square: Square, direction: Direction) -> Square:
        return self._neighbours[square][direction]

    @property
    def pawn_squares(self):
        return self._pawn_squares


class Piece:
    def __init__(self, square):
        self.__square = square

    def __deepcopy__(self, _):
        return copy(self)

    @property
    def square(self):
        return self.__square

    @property
    def file(self):
        return self.square.file

    @property
    def rank(self):
        return self.square.rank

    def move_to(self, square):
        assert isinstance(square, Square)
        self.__square = square

    def move(self, direction: Direction) -> bool:
        square = BOARD.get_neighbour(self.__square, direction)
        if square is None:
            return False
        else:
            self.__square = square
            return True


class Pawn(Piece):
    def __init__(self, square):
        super().__init__(square)
        assert self.rank > 1

    def is_promoted(self):
        return self.rank == 8

    def __str__(self):
        return f"{self.square}"


class Queen(Piece):
    def __str__(self):
        return f"Q{self.square}"


BOARD = Board()
