from itertools import product, dropwhile, combinations


# We generate all 256 combinations of files that are filled with pawns.
# First comes the combination with no files filled,
# next those with one file filled,
# next those with two files filled,
# until the last combination with all files filled.
# If one combination can be obtained by another by moving all filled files to the right
# we generate them next after each other.

# The are two method for generation, each having another presentation.
# The first generates the numbers of the files that contains columns, like
#   (3, 4, 6)
# The other generates eight boolean that specify whether the file is filed, like
#   (False, False, True, True, False, True, False, False)
#

def generate():
    yield []
    for nb in range(1, 9):
        comb_list = list(combinations(range(1, 9), nb))
        comb_list.sort(key=lambda e: list(map(lambda v: v - e[0], e)))
        for c in comb_list:
            yield c


def generate2():

    def drop_while_false(comb):
        return list(dropwhile(lambda value: not value, comb))

    comb_list = list(product([True, False], repeat=8))
    comb_list.sort(key=lambda e: drop_while_false(e), reverse=True)
    comb_list.sort(key=lambda e: e.count(True))

    for c in comb_list:
        yield c


def check_two_methods_equivalent():

    def is_equivalent(x, y):
        for i, value in enumerate(y):
            if value != (i+1 in x):
                return False
        return True

    assert is_equivalent((2, 3, 5), (False, True, True, False, True, False, False, False))

    for c1, c2 in zip(generate(), generate2()):
        assert is_equivalent(c1, c2)


check_two_methods_equivalent()
