import sys

from setuptools import Extension, setup

_ext_dir = "src/wigner/_ext"
_wig_dir = f"{_ext_dir}/wigxjpf"

ext = Extension(
    "wigner._wigner",
    sources=[
        f"{_ext_dir}/_wigner_ext.c",
        f"{_wig_dir}/src/prime_factor.c",
        f"{_wig_dir}/src/calc.c",
        f"{_wig_dir}/src/trivial_zero.c",
        f"{_wig_dir}/src/c_wrap.c",
        f"{_wig_dir}/src/wigxjpf_error.c",
    ],
    include_dirs=[
        f"{_wig_dir}/inc",
        f"{_wig_dir}/cfg",
        f"{_wig_dir}/src",
    ],
    libraries=[] if sys.platform == "win32" else ["m"],
    extra_compile_args=["-O3"],
    optional=True,
)


setup(
    package_dir={"": "src"},
    ext_modules=[ext],
)
