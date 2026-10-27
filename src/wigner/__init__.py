try:
    from wigner._wigner import clebsch_gordan, init, wigner3j, wigner6j, wigner9j

    _backend = "C"
except ImportError:
    from wigner._pure import clebsch_gordan, wigner3j, wigner6j

    def wigner9j(
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        j7: float,
        j8: float,
        j9: float,
        /,
    ) -> float:
        raise NotImplementedError(
            "wigner9j requires the C extension — reinstall with a C compiler available"
        )

    def init(max_j: int, /) -> None:
        pass  # pure backend has no precomputed tables

    _backend = "pure"

__all__ = ["clebsch_gordan", "init", "wigner3j", "wigner6j", "wigner9j"]
