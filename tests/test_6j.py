import pytest

TOL = 1e-10


@pytest.mark.parametrize(
    "args,expected",
    [
        # {1/2 1/2 1; 1/2 1/2 0} = 1/2  (zero-j6 reduction formula)
        ((0.5, 0.5, 1, 0.5, 0.5, 0), 0.5),
        # {1 1 0; 1 1 0} = 1/3
        ((1, 1, 0, 1, 1, 0), 1.0 / 3.0),
    ],
)
def test_known_values(w, args, expected):
    assert abs(w.wigner6j(*args) - expected) < TOL


@pytest.mark.parametrize(
    "args",
    [
        # triangle violation in first triad
        (1, 1, 5, 1, 1, 1),
        # half-integer triad sum: 5 + 3.5 + 4 = 12.5
        (5, 4.5, 3.5, 2, 3.5, 4),
    ],
)
def test_triangle_gives_zero(w, args):
    assert w.wigner6j(*args) == 0


def test_symmetry_column_swap(w):
    # {j1 j2 j3; j4 j5 j6} = {j2 j1 j3; j5 j4 j6}
    j1, j2, j3, j4, j5, j6 = 1, 2, 1, 1, 2, 2
    assert (
        abs(w.wigner6j(j1, j2, j3, j4, j5, j6) - w.wigner6j(j2, j1, j3, j5, j4, j6))
        < TOL
    )
