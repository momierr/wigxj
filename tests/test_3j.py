import math

import pytest

from wigner import _backend, wigner3j
from wigner._pure import wigner3j as wigner3j_pure

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
def test_known_values(args, expected):
    assert abs(wigner3j(*args) - expected) < TOL


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
def test_selection_rules(args):
    assert wigner3j(*args) == 0


def test_symmetry_time_reversal():
    # (j1 j2 j3 / m1 m2 m3) = (-1)^(j1+j2+j3) (j1 j2 j3 / -m1 -m2 -m3)
    j1, j2, j3, m1, m2, m3 = 2, 1, 2, 1, 0, -1
    phase = (-1) ** int(j1 + j2 + j3)
    assert (
        abs(
            wigner3j(j1, j2, j3, m1, m2, m3)
            - phase * wigner3j(j1, j2, j3, -m1, -m2, -m3)
        )
        < TOL
    )


def test_c_matches_pure():
    if _backend != "C":
        pytest.skip("C extension not available")
    from wigner._wigner import wigner3j as wigner3j_c

    cases = [
        (1, 1, 2, 0, 0, 0),
        (2, 2, 2, 1, -1, 0),
        (0.5, 0.5, 1, 0.5, -0.5, 0),
        (3, 2, 1, -1, 0, 1),
    ]
    for args in cases:
        assert abs(wigner3j_c(*args) - wigner3j_pure(*args)) < TOL, (
            f"mismatch at {args}"
        )
