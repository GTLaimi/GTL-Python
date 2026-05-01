from fractions import Fraction

def combination(n, k):
    """计算组合数 C(n, k)，返回整数"""
    if k < 0 or k > n:
        return 0
    # 用下降阶乘 // 阶乘，保证整除
    k = min(k, n - k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result

def falling_factorial(z, y):
    """下降阶乘 z*(z-1)*...*(z-y+1)，y 项；y=0 时返回 1"""
    d = 1
    for i in range(y):
        d *= z - i
    return d

ε = int(input("epxt: "))
n = int(input("n: "))

# 已知 ξ_{ε+1}
xi_high = Fraction(1, ε + 1)

# 存放 ξ_ε, ξ_{ε-1}, ..., ξ_1（按此顺序）
coeffs = []

for x in range(1, ε + 1):
    # 第一项求和：Σ_{δ=0}^{ε-x} (-1)^δ C(ε-x, δ) (ε-x-δ)^ε
    term1 = Fraction(0, 1)
    for δ in range(ε - x + 1):
        sign = (-1) ** δ
        comb = combination(ε - x, δ)
        term1 += sign * comb * ((ε - x - δ) ** ε)

    # 第二项求和：Σ_{i=0}^{x-1} ξ_{ε+1-i} * Σ_{δ=0}^{ε+1-x} (-1)^δ C(ε+1-x, δ) (ε+1-x-δ)^{ε+1-i}
    term2 = Fraction(0, 1)
    for i in range(x):  # 注意 i=0 ~ x-1
        # 选择对应的 ξ_{ε+1-i}
        if i == 0:
            xi = xi_high          # ξ_{ε+1}
        else:
            xi = coeffs[i - 1]    # ξ_ε 对应 i=1, ξ_{ε-1} 对应 i=2 等等

        inner_sum = 0
        for δ in range(ε + 1 - x + 1):  # δ=0 ~ ε+1-x
            sign = (-1) ** δ
            comb = combination(ε + 1 - x, δ)
            inner_sum += sign * comb * ((ε + 1 - x - δ) ** (ε + 1 - i))
        term2 += xi * inner_sum

    numerator = term1 - term2
    denominator = falling_factorial(ε + 1 - x, ε + 1 - x)  # 即 (ε+1-x)!
    a = numerator / denominator
    coeffs.append(a)

# 此时的 coeffs = [ξ_ε, ξ_{ε-1}, ..., ξ_1]
# 公式给出的是 Σ_{k=1}^{n-1} k^ε，我们要 Σ_{k=1}^{n} k^ε，所以 ξ_ε 要 +1
coeffs[0] += 1

# 输出公式
print(f"1^{ε} + 2^{ε} + ... + n^{ε} =")
formula_parts = []
# 最高次项 ξ_{ε+1} n^{ε+1}
formula_parts.append(f"{xi_high} * n^{ε + 1}")

# 其余项
for idx, coeff in enumerate(coeffs):
    power = ε - idx
    formula_parts.append(f"{coeff} * n^{power}")
print(" + ".join(formula_parts))

# 代入 n 计算总和
total = xi_high * (n ** (ε + 1))
for idx, coeff in enumerate(coeffs):
    total += coeff * (n ** (ε - idx))
print(f"n={n} → 求和 = {total}")