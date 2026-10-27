"""Basic usage of the wigxj package."""

from wigxj import clebsch_gordan, wigner3j, wigner6j

# Wigner 3j symbol
val = wigner3j(1, 1, 2, 0, 0, 0)
print(f"(1 1 2 / 0 0 0) = {val:.6f}")  # sqrt(2/15) ≈ 0.365148

# Clebsch-Gordan coefficient  <j1 m1 j2 m2 | j3 m3>
cg = clebsch_gordan(0.5, 0.5, 0.5, -0.5, 0, 0)
print(f"<1/2,1/2; 1/2,-1/2 | 0,0> = {cg:.6f}")  # 1/sqrt(2) ≈ 0.707107

# Wigner 6j symbol
val6 = wigner6j(0.5, 0.5, 1, 0.5, 0.5, 0)
print(f"{{1/2 1/2 1; 1/2 1/2 0}} = {val6:.6f}")  # 0.5
