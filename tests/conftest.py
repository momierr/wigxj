import importlib
from types import ModuleType

import pytest

import wigner._pure as pure

c_ext: ModuleType | None
try:
    c_ext = importlib.import_module("wigner._wigner")
except ImportError:
    c_ext = None


@pytest.fixture(params=["C", "pure"], scope="module")
def w(request):
    if request.param == "C":
        if c_ext is None:
            pytest.skip("C extension not built")
        return c_ext
    return pure
