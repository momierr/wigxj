import math

import pytest

TOL = 1e-10


@pytest.mark.parametrize(
    "args,expected",
    [
        # trivial: (0 0 0 / 0 0 0) = 1
        ((0, 0, 0, 0, 0, 0), 1.0),
        # (1 1 0 / 1 -1 0) = 1/sqrt(3)
        ((1, 1, 0, 1, -1, 0), 1.0 / math.sqrt(3)),
        # (1 1 2 / 0 0 0) = sqrt(2/15)
        ((1, 1, 2, 0, 0, 0), math.sqrt(2.0 / 15.0)),
        # (2 2 2 / 1 -1 0) = 1/sqrt(70)  — exercises the tmin=max(...) fix
        ((2, 2, 2, 1, -1, 0), 1.0 / math.sqrt(70.0)),
        # half-integer: (1/2 1/2 1 / 1/2 -1/2 0) = 1/sqrt(6)
        ((0.5, 0.5, 1, 0.5, -0.5, 0), 1.0 / math.sqrt(6.0)),
    ],
)
def test_known_values(w, args, expected):
    assert abs(w.wigner3j(*args) - expected) < TOL


@pytest.mark.parametrize(
    "args",
    [
        # m sum != 0
        (1, 1, 2, 1, 0, 0),
        # triangle violation
        (1, 1, 3, 0, 0, 0),
        # |m| > j
        (1, 1, 2, 2, 0, -2),
    ],
)
def test_selection_rules(w, args):
    assert w.wigner3j(*args) == 0


def test_symmetry_time_reversal(w):
    # (j1 j2 j3 / m1 m2 m3) = (-1)^(j1+j2+j3) (j1 j2 j3 / -m1 -m2 -m3)
    j1, j2, j3, m1, m2, m3 = 2, 1, 2, 1, 0, -1
    phase = (-1) ** int(j1 + j2 + j3)
    assert (
        abs(
            w.wigner3j(j1, j2, j3, m1, m2, m3)
            - phase * w.wigner3j(j1, j2, j3, -m1, -m2, -m3)
        )
        < TOL
    )


@pytest.mark.parametrize("j", [10, 12, 20, 150])
def test_large_j_closed_form(w, j):
    # (j j 0 / 0 0 0) = (-1)^j / sqrt(2j+1); the old vendored wigxjpf hung for j >= 12
    assert abs(w.wigner3j(j, j, 0, 0, 0, 0) - (-1) ** j / math.sqrt(2 * j + 1)) < TOL
