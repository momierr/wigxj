try:
    from wigner._wigner import clebsch_gordan, init, wigner3j, wigner6j, wigner9j

    _backend = "C"
except ImportError:
    from wigner._pure import clebsch_gordan, wigner3j, wigner6j

    def wigner9j(*args, **kwargs):
        raise NotImplementedError(
            "wigner9j requires the C extension — reinstall with a C compiler available"
        )

    _backend = "pure"

__all__ = ["wigner3j", "wigner6j", "wigner9j", "clebsch_gordan"]
