# File: bifurcation_matplotlib.py
# Logistic map bifurcation diagram with matplotlib

import numpy as np
import matplotlib.pyplot as plt
import time

# ========== 参数设置 ==========
r_min = 2.5               # 参数 r 起始值
r_max = 4.0               # 参数 r 结束值
r_points = 2000           # r 轴采样点数（越高图像越精细）
transient = 500           # 跳过暂态迭代次数
plot_points = 200         # 每个 r 绘制的稳定点个数
x0 = 0.5                  # 初始值

# ========== 计算分叉图 ==========
print("正在计算分叉图...")
start_time = time.time()

# 生成 r 数组
r_vals = np.linspace(r_min, r_max, r_points)
# 结果数组：每一行是一个 r，每一列是一个稳定点
x_vals = np.zeros((r_points, plot_points))

for i, r in enumerate(r_vals):
    x = x0
    # 跳过暂态
    for _ in range(transient):
        x = r * x * (1 - x)
    # 收集稳定点
    for j in range(plot_points):
        x = r * x * (1 - x)
        x_vals[i, j] = x

elapsed = time.time() - start_time
print(f"计算完成，耗时 {elapsed:.2f} 秒")

# ========== 绘图 ==========
plt.figure(figsize=(12, 8))
# 将每个 r 对应的 plot_points 个点全部画出
for i in range(r_points):
    plt.plot(np.full(plot_points, r_vals[i]), x_vals[i, :], 
             ',', color='black', alpha=0.1)

plt.xlabel('r', fontsize=14)
plt.ylabel('x', fontsize=14)
plt.title('Logistic Map Bifurcation Diagram', fontsize=16)
plt.xlim(r_min, r_max)
plt.ylim(-0.05, 1.05)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()