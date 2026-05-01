from fractions import Fraction
import math

def bernoulli(n):
    """返回 B_0..B_n(伯努利数,B_1 = +1/2)"""
    B = [Fraction(1, 1)]
    for m in range(1, n + 1):
        s = Fraction(0, 1)
        for k in range(m):
            s += Fraction(math.comb(m + 1, k)) * B[k]
        B.append(-s / (m + 1))
    B[1] = Fraction(1, 2)   # 采用 B_1 = +1/2
    return B

p = int(input("epxt: "))
n = int(input("n: "))

B = bernoulli(p)
coeffs = []
for k in range(p + 1):
    coeffs.append(Fraction(math.comb(p + 1, k), p + 1) * B[k])

# 输出多项式
print(f"1^{p} + 2^{p} + ... + n^{p} =")
terms = []
for k, c in enumerate(coeffs):
    if c == 0:
        continue
    power = p + 1 - k
    term = f"({c}) * n" if power == 1 else f"({c}) * n^{power}"
    terms.append(term)
print(" + ".join(terms))

# 验证数值
total = Fraction(0, 1)
for k, c in enumerate(coeffs):
    total += c * (n ** (p + 1 - k))
print(f"n={n} → 求和 = {total}")