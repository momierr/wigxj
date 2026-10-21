# wigner

Fast Wigner 3j, 6j, 9j symbols and Clebsch-Gordan coefficients for Python.

Wraps [wigxjpf](https://github.com/nd-nuclear-theory/wigxjpf) (vendored, LGPL, see src/wigner/_ext/wigxjpf/COPYING.LESSER) for speed.
Falls back to a pure-Python implementation if no C compiler is available.

## Installation

```bash
pip install .
```

Requires a C compiler (GCC or Clang). To check which backend is active:

```python
import wigner
print(wigner._backend)  # "C" or "pure"
```

## API

```python
from wigner import wigner3j, wigner6j, wigner9j, clebsch_gordan
```

All functions accept integer or half-integer arguments as plain Python numbers.

| Function | Signature |
|---|---|
| `wigner3j` | `(j1, j2, j3, m1, m2, m3)` |
| `wigner6j` | `(j1, j2, j3, j4, j5, j6)` |
| `wigner9j` | `(j1, j2, j3, j4, j5, j6, j7, j8, j9)` |
| `clebsch_gordan` | `(j1, m1, j2, m2, j3, m3)` |

`wigner9j` requires the C extension. `clebsch_gordan` follows the convention:

$$\langle j_1 m_1 j_2 m_2 | j_3 m_3 \rangle = (-1)^{-j_1+j_2-m_3} \sqrt{2j_3+1} \begin{pmatrix} j_1 & j_2 & j_3 \\ m_1 & m_2 & -m_3 \end{pmatrix}$$

### Re-initializing for large j

The C backend initializes tables up to j=200 by default. For larger values:

```python
from wigner import init
init(500)  # extend tables to j=500
```

## Examples

See [`examples/`](examples/).

## License

MIT (this wrapper) + LGPL-3.0-or-later (vendored wigxjpf).
