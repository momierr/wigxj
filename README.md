# wigxj

[![CI](https://github.com/momierr/wigxj/actions/workflows/ci.yml/badge.svg)](https://github.com/momierr/wigxj/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Fast Wigner 3j, 6j, 9j symbols and Clebsch-Gordan coefficients for Python.

- **Fast**: a CPython extension around [wigxjpf](https://github.com/nd-nuclear-theory/wigxjpf)
  (exact prime-factorisation arithmetic), about 0.3 µs per symbol for small j.
- **Simple**: pass spins as plain numbers (`0.5`, `1`, `1.5`); no doubled integers, no manual setup.
- **Always works**: if the C extension cannot be built, a pure-Python backend with
  exact integer arithmetic takes over, with the same API.
- **Typed**: ships type stubs (`py.typed`).

## Installation

```bash
pip install wigxj
```

Building from source needs a C compiler (GCC, Clang or MSVC). Without one, installation
still succeeds and wigxj uses the pure-Python backend. To check which backend is active:

```python
import wigxj

print(wigxj._backend)  # "C" or "pure"
```

## Quick start

```python
from wigxj import clebsch_gordan, wigner3j, wigner6j, wigner9j

wigner3j(1, 1, 2, 0, 0, 0)  # 0.3651... = sqrt(2/15)
wigner6j(1, 1, 0, 1, 1, 0)  # 0.3333... = 1/3
clebsch_gordan(0.5, 0.5, 0.5, -0.5, 0, 0)  # 0.7071... = 1/sqrt(2)  (spin singlet)
wigner9j(1, 1, 1, 1, 1, 1, 1, 1, 0)  # 0.0555... = 1/18
```

## API

All functions take integer or half-integer arguments and return a `float`.
Arguments that violate the selection rules (triangle conditions, `m1 + m2 + m3 != 0`, ...)
return `0.0`.

| Function         | Signature                              | Symbol                                      |
| ---------------- | -------------------------------------- | ------------------------------------------- |
| `wigner3j`       | `(j1, j2, j3, m1, m2, m3)`             | (j1 j2 j3 / m1 m2 m3)                        |
| `wigner6j`       | `(j1, j2, j3, j4, j5, j6)`             | {j1 j2 j3 / j4 j5 j6}                        |
| `wigner9j`       | `(j1, j2, j3, j4, j5, j6, j7, j8, j9)` | {j1 j2 j3 / j4 j5 j6 / j7 j8 j9}             |
| `clebsch_gordan` | `(j1, m1, j2, m2, j3, m3)`             | ⟨j1 m1 j2 m2 \| j3 m3⟩                       |
| `init`           | `(max_j)`                              | resize the C backend's tables (see below)   |

`clebsch_gordan` uses the Condon-Shortley convention:

$$\langle j_1 m_1 j_2 m_2 | j_3 m_3 \rangle = (-1)^{-j_1+j_2-m_3} \sqrt{2j_3+1} \begin{pmatrix} j_1 & j_2 & j_3 \\ m_1 & m_2 & -m_3 \end{pmatrix}$$

### Large j

The C backend precomputes tables for j up to 200. Larger values raise a `ValueError`
until you extend the tables:

```python
from wigxj import init, wigner3j

init(500)  # tables for j up to 500
wigner3j(400, 400, 0, 0, 0, 0)
```

The pure-Python backend has no tables and no limit on j.

## Performance

Time per call (best of 5, single machine, Python 3.15):

| Symbol                         | wigxj (C) | wigxj (pure) | `sympy.physics.wigner` |
| ------------------------------ | --------: | -----------: | ---------------------: |
| 3j, small (2 2 2 / 1 -1 0)     |   0.27 µs |        17 µs |                  22 µs |
| 3j, j = 50 (50 50 50 / 0 0 0)  |    6.2 µs |       218 µs |                 180 µs |
| 6j, small {2 2 2 / 2 2 2}      |   0.34 µs |       8.6 µs |                 122 µs |
| 6j, j = 30 {30 30 30 / 30 30 30} |  5.2 µs |       103 µs |                 427 µs |

## Why wigxj?

| Package                                                        | When to use it                                                                                       |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **wigxj**                                                      | Fast floating-point 3j/6j/9j/Clebsch-Gordan with a plain-number API.                                 |
| [pywigxjpf](https://pypi.org/project/pywigxjpf/)               | wigxjpf's own binding: same core, but arguments are doubled integers and tables are set up manually. |
| [sympy.physics.wigner](https://docs.sympy.org/latest/modules/physics/wigner.html) | You need **exact** symbolic results (rationals and square roots), and speed does not matter.  |
| [wigner](https://pypi.org/project/wigner/)                     | You need Wigner d-functions.                                                                         |

## Examples

See [`examples/`](examples/), e.g. a dipole matrix element calculation.

## Development

The development environment is managed with [pixi](https://pixi.sh):

```bash
pixi run test          # build the C extension, run the tests on both backends
pixi run lint          # ruff
pixi run format-check  # ruff format
pixi run typecheck     # mypy
```

The tests run every check against both the C and the pure-Python backend, and use
[Hypothesis](https://hypothesis.readthedocs.io) to verify orthogonality relations, symmetries
and agreement with sympy's exact results on random inputs.

## License

wigxj is MIT-licensed (see [`LICENSE`](LICENSE)). It bundles
[wigxjpf](https://github.com/nd-nuclear-theory/wigxjpf) 1.15 by H. T. Johansson and
C. Forssén, licensed under LGPL-3.0-or-later (see
[`src/wigxj/_ext/wigxjpf/COPYING.LESSER`](src/wigxj/_ext/wigxjpf/COPYING.LESSER)).

If you use wigxj in your research, please cite wigxjpf:
H. T. Johansson and C. Forssén, *Fast and Accurate Evaluation of Wigner 3j, 6j, and 9j
Symbols Using Prime Factorization and Multiword Integer Arithmetic*,
SIAM J. Sci. Comput. **38**, A376 (2016), [doi:10.1137/15M1021908](https://doi.org/10.1137/15M1021908).
