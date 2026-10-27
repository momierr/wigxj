import math
import warnings
from fractions import Fraction

import numpy as np


def _f(x):
    # Exact factorial; arguments are always whole numbers here (half-integers cancel)
    return math.factorial(round(x))


def _delta2(a, b, c):
    # Triangle coefficient squared, as an exact fraction
    if a + b < c or a + c < b or b + c < a or (a + b + c) % 1:
        return Fraction(0)
    return Fraction(_f(a + b - c) * _f(a - b + c) * _f(-a + b + c), _f(a + b + c + 1))


def wigner3j(j1, j2, j3, m1, m2, m3):
    j123 = np.array([j1, j2, j3])
    m123 = np.array([m1, m2, m3])

    if (j123 < 0).any():
        warnings.warn("All j values must be >= 0")
        return 0
    if any(v % 0.5 for v in j123) or any(v % 0.5 for v in m123):
        warnings.warn("Arguments must be integer or half-integer")
        return 0
    if any((j123 - m123) % 1):
        warnings.warn("j's and m's must be congruent mod 1")
        return 0
    if j3 > j1 + j2 or j3 < abs(j1 - j2) or m1 + m2 + m3 != 0 or any(abs(m123) > j123):
        return 0

    t1 = j2 - m1 - j3
    t2 = j1 + m2 - j3
    t3 = j1 + j2 - j3
    t4 = j1 - m1
    t5 = j2 + m2

    tmin = round(max(0, t1, t2))
    tmax = round(min(t3, t4, t5))

    phase = (-1) ** round(j1 - j2 - m3)

    sq2 = (
        _f(j1 - m1)
        * _f(j1 + m1)
        * _f(j2 - m2)
        * _f(j2 + m2)
        * _f(j3 - m3)
        * _f(j3 + m3)
    )
    s = sum(
        Fraction(
            (-1) ** k,
            _f(k)
            * _f(j3 - j2 + k + m1)
            * _f(j3 - j1 + k - m2)
            * _f(j1 + j2 - j3 - k)
            * _f(j1 - k - m1)
            * _f(j2 - k + m2),
        )
        for k in range(tmin, tmax + 1)
    )
    # Exact up to here: a single rounding to float at the very end
    return phase * math.copysign(math.sqrt(_delta2(j1, j2, j3) * sq2 * s * s), s)


def clebsch_gordan(j1, m1, j2, m2, j3, m3):
    phase = (-1) ** round(-j1 + j2 - m3)
    return phase * math.sqrt(2 * j3 + 1) * wigner3j(j1, j2, j3, m1, m2, -m3)


def wigner6j(j1, j2, j3, j4, j5, j6):

    t1 = j1 + j2 + j3
    t2 = j1 + j5 + j6
    t3 = j4 + j2 + j6
    t4 = j4 + j5 + j3

    inf_ = round(max(t1, t2, t3, t4))

    t5 = j1 + j2 + j4 + j5
    t6 = j2 + j3 + j5 + j6
    t7 = j3 + j1 + j6 + j4

    sup_ = round(min(t5, t6, t7))

    d2 = (
        _delta2(j1, j2, j3)
        * _delta2(j1, j5, j6)
        * _delta2(j4, j2, j6)
        * _delta2(j4, j5, j3)
    )
    if d2 == 0:
        return 0

    s = sum(
        Fraction(
            (-1) ** k * _f(k + 1),
            _f(k - t1)
            * _f(k - t2)
            * _f(k - t3)
            * _f(k - t4)
            * _f(t5 - k)
            * _f(t6 - k)
            * _f(t7 - k),
        )
        for k in range(inf_, sup_ + 1)
    )
    return math.copysign(math.sqrt(d2 * s * s), s)


def wigner9j(a, b, c, d, e, f, g, h, i):
    # 9j as a sum over x of products of three 6j symbols
    lo = max(abs(a - i), abs(d - h), abs(b - f))
    hi = min(a + i, d + h, b + f)
    return sum(
        (-1) ** round(2 * x)
        * (2 * x + 1)
        * wigner6j(a, b, c, f, i, x)
        * wigner6j(d, e, f, b, x, h)
        * wigner6j(g, h, i, x, a, d)
        for x in (lo + k for k in range(round(hi - lo) + 1))
    )
