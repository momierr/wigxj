import pytest

from wigner import _backend, init, wigner3j

c_only = pytest.mark.skipif(_backend != "C", reason="C backend only")


def test_init_importable():
    init(10)  # no-op on pure backend, must not raise


@c_only
def test_beyond_table_raises():
    init(200)
    with pytest.raises(ValueError, match="init"):
        wigner3j(250, 250, 0, 0, 0, 0)


@c_only
def test_init_extends_table():
    init(300)
    assert isinstance(wigner3j(250, 250, 0, 0, 0, 0), float)
    init(200)  # restore default so other tests aren't affected


@c_only
def test_init_negative_raises():
    with pytest.raises(ValueError):
        init(-1)
