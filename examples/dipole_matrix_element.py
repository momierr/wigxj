"""
Reduced dipole matrix element via Wigner-Eckart theorem.

For an electric dipole transition |J, mJ> -> |J', mJ'>,
the matrix element factors as:

  <J' mJ'| T^1_q |J mJ> ∝ (-1)^(J-mJ) * wigner3j(J, 1, J', mJ, q, -mJ')

with the selection rule mJ' = mJ + q.
"""

from wigxj import wigner3j

J = 1  # initial state
J_prime = 2  # final state

# mJ values: -J, -J+1, ..., J (works for integer and half-integer J)
mJ_values = [J - k for k in range(round(2 * J) + 1)]

print(f"3j angular factors for J={J} -> J'={J_prime} (E1)\n")
print(f"{'mJ':>4}  {'q':>4}  {'mJ_prime':>8}  {'3j':>12}")
print("-" * 36)

for mJ in mJ_values:
    for q in (-1, 0, 1):
        mJ_prime = mJ + q
        if abs(mJ_prime) > J_prime:
            continue
        # 3j selection rule: mJ + q + (-mJ') = 0  =>  mJ' = mJ + q  ✓
        val = wigner3j(J, 1, J_prime, mJ, q, -mJ_prime)
        if val != 0:
            print(f"{mJ:>4.1f}  {q:>4}  {mJ_prime:>8.1f}  {val:>12.6f}")
