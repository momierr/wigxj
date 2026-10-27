import pytest

from wigxj import _backend, clebsch_gordan, init, wigner3j, wigner6j, wigner9j

c_only = pytest.mark.skipif(_backend != "C", reason="C backend only")


def test_init_importable():
    init(10)  # no-op on pure backend, must not raise


@c_only
@pytest.mark.parametrize(
    "fn,args",
    [
        (wigner3j, (250, 250, 0, 0, 0, 0)),
        (wigner6j, (250, 250, 0, 250, 250, 0)),
        (wigner9j, (250, 250, 0, 250, 250, 0, 0, 0, 0)),
        (clebsch_gordan, (250, 0, 250, 0, 0, 0)),
    ],
)
def test_beyond_table_raises(fn, args):
    init(200)
    with pytest.raises(ValueError, match="init"):
        fn(*args)


@c_only
def test_init_extends_table():
    init(300)
    assert isinstance(wigner3j(250, 250, 0, 0, 0, 0), float)
    init(200)  # restore default so other tests aren't affected


@c_only
def test_init_negative_raises():
    with pytest.raises(ValueError):
        init(-1)
