"""Property-based tests: identities that must hold for every valid input.

Hypothesis generates the inputs; when a property fails it shrinks the
counterexample to the smallest one it can find.
"""

from hypothesis import assume, given, settings
from hypothesis import strategies as st
from sympy import Rational
from sympy.physics.wigner import wigner_3j, wigner_6j, wigner_9j

TOL = 1e-10

# j values 0, 1/2, 1, ..., 6: large enough to be interesting, small enough for sympy
half_int = st.integers(0, 12).map(lambda n: n / 2)


def _range(lo, hi):
    """lo, lo + 1, ..., hi (inclusive)."""
    return [lo + k for k in range(round(hi - lo) + 1)]


def _triad(a, b):
    """All c such that (a, b, c) satisfies the triangle and integer-sum rules."""
    return _range(abs(a - b), a + b)


@st.composite
def valid_3j(draw):
    j1, j2 = draw(half_int), draw(half_int)
    j3 = draw(st.sampled_from(_triad(j1, j2)))
    m1 = draw(st.sampled_from(_range(-j1, j1)))
    m2 = draw(st.sampled_from(_range(-j2, j2)))
    m3 = -m1 - m2
    assume(abs(m3) <= j3)
    return j1, j2, j3, m1, m2, m3


@st.composite
def valid_6j(draw):
    # {a b x; c d f}: triads (a, b, x), (a, d, f), (c, b, f), (c, d, x)
    a, b, c, d = (draw(half_int) for _ in range(4))
    xs = sorted(set(_triad(a, b)) & set(_triad(c, d)))
    fs = sorted(set(_triad(a, d)) & set(_triad(c, b)))
    assume(xs and fs)
    return a, b, c, d, xs, fs


def _sympy(x):
    return Rational(round(2 * x), 2)


# --- Orthogonality ----------------------------------------------------------


@given(data=st.data())
def test_cg_orthogonality(w, data):
    # sum_{m1} <j1 m1 j2 M-m1 | J M> <j1 m1 j2 M-m1 | J' M> = delta_{J J'}
    j1, j2 = data.draw(half_int), data.draw(half_int)
    J = data.draw(st.sampled_from(_triad(j1, j2)))
    Jp = data.draw(st.sampled_from(_triad(j1, j2)))
    lim = min(J, Jp)
    M = data.draw(st.sampled_from(_range(-lim, lim)))

    total = sum(
        w.clebsch_gordan(j1, m1, j2, M - m1, J, M)
        * w.clebsch_gordan(j1, m1, j2, M - m1, Jp, M)
        for m1 in _range(-j1, j1)
        if abs(M - m1) <= j2
    )
    assert abs(total - (J == Jp)) < TOL


@given(data=st.data())
def test_6j_orthogonality(w, data):
    # sum_x (2x+1)(2f+1) {a b x; c d f} {a b x; c d f'} = delta_{f f'}
    a, b, c, d, xs, fs = data.draw(valid_6j())
    f = data.draw(st.sampled_from(fs))
    fp = data.draw(st.sampled_from(fs))

    total = sum(
        (2 * x + 1)
        * (2 * f + 1)
        * w.wigner6j(a, b, x, c, d, f)
        * w.wigner6j(a, b, x, c, d, fp)
        for x in xs
    )
    assert abs(total - (f == fp)) < TOL


# --- Symmetries -------------------------------------------------------------


@given(args=valid_3j())
def test_3j_cyclic_permutation(w, args):
    # (j1 j2 j3 / m1 m2 m3) is invariant under cyclic permutation of columns
    j1, j2, j3, m1, m2, m3 = args
    assert abs(w.wigner3j(*args) - w.wigner3j(j2, j3, j1, m2, m3, m1)) < TOL


@given(args=valid_3j())
def test_3j_column_swap(w, args):
    # swapping two columns multiplies by (-1)^(j1+j2+j3)
    j1, j2, j3, m1, m2, m3 = args
    phase = (-1) ** round(j1 + j2 + j3)
    assert abs(w.wigner3j(j2, j1, j3, m2, m1, m3) - phase * w.wigner3j(*args)) < TOL


# --- Cross-check against sympy (exact rational arithmetic) ------------------


@settings(max_examples=50, deadline=None)
@given(args=valid_3j())
def test_3j_matches_sympy(w, args):
    expected = float(wigner_3j(*map(_sympy, args)))
    assert abs(w.wigner3j(*args) - expected) < TOL


@settings(max_examples=50, deadline=None)
@given(data=st.data())
def test_6j_matches_sympy(w, data):
    a, b, c, d, xs, fs = data.draw(valid_6j())
    x, f = data.draw(st.sampled_from(xs)), data.draw(st.sampled_from(fs))
    args = (a, b, x, c, d, f)
    expected = float(wigner_6j(*map(_sympy, args)))
    assert abs(w.wigner6j(*args) - expected) < TOL


@settings(max_examples=25, deadline=None)
@given(data=st.data())
def test_9j_matches_sympy(w, data):
    small = st.integers(0, 6).map(lambda n: n / 2)  # sympy's 9j is slow: keep j <= 3
    # {a b e; c d f; g h i}: rows and columns must all be valid triads
    a, b, c, d = (data.draw(small) for _ in range(4))
    e = data.draw(st.sampled_from(_triad(a, b)))
    f = data.draw(st.sampled_from(_triad(c, d)))
    g = data.draw(st.sampled_from(_triad(a, c)))
    h = data.draw(st.sampled_from(_triad(b, d)))
    i_values = sorted(set(_triad(e, f)) & set(_triad(g, h)))
    assume(i_values)
    i = data.draw(st.sampled_from(i_values))
    args = (a, b, e, c, d, f, g, h, i)
    expected = float(wigner_9j(*map(_sympy, args), prec=64))
    assert abs(w.wigner9j(*args) - expected) < TOL
