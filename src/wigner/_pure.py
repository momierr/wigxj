import math
import warnings

import numpy as np


def delta(a, b, c):
    if a + b < c or a + c < b or b + c < a:
        return 0
    return math.sqrt(
        math.factorial(round(a + b - c))
        * math.factorial(round(a - b + c))
        * math.factorial(round(-a + b + c))
        / math.factorial(round(a + b + c + 1))
    )


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

    tmin = int(round(max(0, t1, t2)))
    tmax = int(round(min(t3, t4, t5)))

    phase = (-1) ** int(round(j1 - j2 - m3))
    d = delta(j1, j2, j3)

    sq = math.sqrt(
        math.exp(math.lgamma(j1 - m1 + 1))
        * math.exp(math.lgamma(j1 + m1 + 1))
        * math.exp(math.lgamma(j2 - m2 + 1))
        * math.exp(math.lgamma(j2 + m2 + 1))
        * math.exp(math.lgamma(j3 - m3 + 1))
        * math.exp(math.lgamma(j3 + m3 + 1))
    )

    s = 0.0
    for k in range(tmin, tmax + 1):
        X = (
            math.exp(math.lgamma(k + 1))
            * math.exp(math.lgamma(j3 - j2 + k + m1 + 1))
            * math.exp(math.lgamma(j3 - j1 + k - m2 + 1))
            * math.exp(math.lgamma(j1 + j2 - j3 - k + 1))
            * math.exp(math.lgamma(j1 - k - m1 + 1))
            * math.exp(math.lgamma(j2 - k + m2 + 1))
        )
        s += ((-1) ** k) / X

    return phase * d * sq * s


def clebsch_gordan(j1, m1, j2, m2, j3, m3):
    phase = (-1) ** int(round(-j1 + j2 - m3))
    return phase * math.sqrt(2 * j3 + 1) * wigner3j(j1, j2, j3, m1, m2, -m3)


def wigner6j(j1, j2, j3, j4, j5, j6):
    t1 = j1 + j2 + j3
    t2 = j1 + j5 + j6
    t3 = j4 + j2 + j6
    t4 = j4 + j5 + j3

    inf_ = int(round(max(t1, t2, t3, t4)))

    t5 = j1 + j2 + j4 + j5
    t6 = j2 + j3 + j5 + j6
    t7 = j3 + j1 + j6 + j4

    sup_ = int(round(min(t5, t6, t7)))

    if (
        delta(j1, j2, j3) == 0
        or delta(j1, j5, j6) == 0
        or delta(j4, j2, j6) == 0
        or delta(j4, j5, j3) == 0
    ):
        return 0

    d = delta(j1, j2, j3) * delta(j1, j5, j6) * delta(j4, j2, j6) * delta(j4, j5, j3)
    s = 0.0
    for k in range(inf_, sup_ + 1):
        X = (
            math.exp(math.lgamma(k - t1 + 1))
            * math.exp(math.lgamma(k - t2 + 1))
            * math.exp(math.lgamma(k - t3 + 1))
            * math.exp(math.lgamma(k - t4 + 1))
            * math.exp(math.lgamma(t5 - k + 1))
            * math.exp(math.lgamma(t6 - k + 1))
            * math.exp(math.lgamma(t7 - k + 1))
        )
        s += (-1) ** k * math.exp(math.lgamma(k + 2)) / X

    return d * s
