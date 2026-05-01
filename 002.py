def is_prime(num):
    """判断一个数是否为质数"""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# 获取用户输入并验证
while True:
    try:
        n = int(input("请输入一个正偶数："))
        if n > 0 and n % 2 == 0:
            break
        else:
            print("错误：必须输入正偶数，请重新输入。")
    except ValueError:
        print("错误：输入的不是整数，请重新输入。")

result = []
for i in range(2, n // 2 + 1):
    if is_prime(i) and is_prime(n - i):
        result.append((i, n - i))

# 输出结果
if not result:
    print(f"{n} 无法分解为两个质数的和。")
else:
    print(f"{n} 可以分解为以下两个质数的和：")
    for pair in result:
        print(f"{pair[0]} + {pair[1]}")
