import math

import pytest

TOL = 1e-10


@pytest.mark.parametrize(
    "args,expected",
    [
        # spin singlet: <1/2 1/2 1/2 -1/2 | 0 0> = -<1/2 -1/2 1/2 1/2 | 0 0> = 1/sqrt(2)
        ((0.5, 0.5, 0.5, -0.5, 0, 0), 1.0 / math.sqrt(2)),
        ((0.5, -0.5, 0.5, 0.5, 0, 0), -1.0 / math.sqrt(2)),
        # spin triplet: <1/2 1/2 1/2 -1/2 | 1 0> = 1/sqrt(2)
        ((0.5, 0.5, 0.5, -0.5, 1, 0), 1.0 / math.sqrt(2)),
        # two spin-1: <1 1 1 -1 | 0 0> = 1/sqrt(3), <1 0 1 0 | 0 0> = -1/sqrt(3)
        ((1, 1, 1, -1, 0, 0), 1.0 / math.sqrt(3)),
        ((1, 0, 1, 0, 0, 0), -1.0 / math.sqrt(3)),
        # <1 1 1 0 | 2 1> = 1/sqrt(2), <1 0 1 1 | 1 1> = -1/sqrt(2)
        ((1, 1, 1, 0, 2, 1), 1.0 / math.sqrt(2)),
        ((1, 0, 1, 1, 1, 1), -1.0 / math.sqrt(2)),
    ],
)
def test_known_values(w, args, expected):
    assert abs(w.clebsch_gordan(*args) - expected) < TOL


@pytest.mark.parametrize("j1,j2", [(0.5, 0.5), (1, 2), (3.5, 1.5), (10, 7), (60, 40)])
def test_stretched_state(w, j1, j2):
    # <j1 j1 j2 j2 | j1+j2 j1+j2> = 1 for any j1, j2
    assert abs(w.clebsch_gordan(j1, j1, j2, j2, j1 + j2, j1 + j2) - 1.0) < TOL


@pytest.mark.parametrize(
    "args",
    [
        # m1 + m2 != M
        (1, 1, 1, 0, 2, 0),
        # triangle violation
        (1, 0, 1, 0, 3, 0),
    ],
)
def test_selection_rules(w, args):
    assert w.clebsch_gordan(*args) == 0
