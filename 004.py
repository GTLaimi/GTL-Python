def f(x):
    return 50*x+0.2*x**2

list_cost = []                     # 移到这里，收集全部合法成本
for a in range(40,101):
    list=[100]
    list.append(180-a)
    for b in range(100-a,min(list)+1):
        c=180-a-b
        if c < 40 or c > 100:     # 确保第三季度产量合法
            continue
        cost=0
        cost+=f(a)+f(b)+f(c)
        cost+=4*(a-40)+4*(a+b-100)
        list_cost.append(cost)    # 现在每次循环都会把成本加进去

final_cost=min(list_cost)         # 此时才是所有组合中的真正最小值

for a in range(40,101):
    list=[100]
    list.append(180-a)
    for b in range(100-a,min(list)+1):
        c=180-a-b
        if c < 40 or c > 100:
            continue
        cost=0
        cost+=f(a)+f(b)+f(c)
        cost+=4*(a-40)+4*(a+b-100)
        if cost==final_cost :
            print("""
第一季度应产""",a,"台","""
第二季度应产""",b,"台","""
第三季度应产""",c,"台")
            break
        else:
            continue #这是一个注释awa