import math

import pytest

TOL = 1e-10


@pytest.mark.parametrize(
    "a,b,e,c,d,f",
    [
        (1, 1, 1, 1, 1, 1),
        (0.5, 0.5, 1, 0.5, 0.5, 1),
        (2, 1, 2, 1, 2, 1),
        (3, 2, 2, 2, 3, 2),
    ],
)
def test_zero_reduces_to_6j(w, a, b, e, c, d, f):
    # {a b e; c d e; f f 0} = (-1)^(b+c+e+f) / sqrt((2e+1)(2f+1)) {a b e; d c f}
    phase = (-1) ** round(b + c + e + f)
    expected = (
        phase / math.sqrt((2 * e + 1) * (2 * f + 1)) * w.wigner6j(a, b, e, d, c, f)
    )
    assert abs(w.wigner9j(a, b, e, c, d, e, f, f, 0) - expected) < TOL


def test_symmetry_transpose(w):
    # the 9j symbol is invariant under transposition
    j = (1, 2, 2, 1.5, 0.5, 1, 1.5, 2.5, 3)
    t = (j[0], j[3], j[6], j[1], j[4], j[7], j[2], j[5], j[8])
    assert abs(w.wigner9j(*j) - w.wigner9j(*t)) < TOL


def test_symmetry_row_swap(w):
    # an odd permutation of rows multiplies by (-1)^(sum of all nine j)
    j = (1, 2, 2, 1.5, 0.5, 1, 1.5, 2.5, 3)
    swapped = j[3:6] + j[0:3] + j[6:9]
    phase = (-1) ** round(sum(j))
    assert abs(w.wigner9j(*swapped) - phase * w.wigner9j(*j)) < TOL


def test_triangle_gives_zero(w):
    # first row (1, 1, 3) violates the triangle condition
    assert w.wigner9j(1, 1, 3, 1, 1, 1, 1, 1, 1) == 0
