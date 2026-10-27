try:
    from wigxj._wigner import clebsch_gordan, init, wigner3j, wigner6j, wigner9j

    _backend = "C"
except ImportError:
    from wigxj._pure import clebsch_gordan, wigner3j, wigner6j, wigner9j

    def init(max_j: int, /) -> None:
        pass  # pure backend has no precomputed tables

    _backend = "pure"

__all__ = ["clebsch_gordan", "init", "wigner3j", "wigner6j", "wigner9j"]
