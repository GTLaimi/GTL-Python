# File: lorenz_animation.py
# Lorenz attractor animation with 3D trajectory + three projections
# Requires: numpy, matplotlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# ========== 参数 ==========
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0
dt = 0.01
total_steps = 5000          # 总模拟步数
steps_per_frame = 10        # 每帧添加的步数（越大动画越快）
interval = 30               # 帧间隔（毫秒）

# ========== 预计算轨迹 ==========
print("预计算轨迹...")
start_time = time.time()
xs = np.empty(total_steps)
ys = np.empty(total_steps)
zs = np.empty(total_steps)
x, y, z = 0.1, 0.0, 0.0
for i in range(total_steps):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    x += dx * dt
    y += dy * dt
    z += dz * dt
    xs[i] = x
    ys[i] = y
    zs[i] = z
elapsed_pre = time.time() - start_time
print(f"预计算完成，耗时 {elapsed_pre:.2f} 秒")

# ========== 创建画布 ==========
fig = plt.figure(figsize=(12, 10))
fig.suptitle("Lorenz Attractor – Dynamic Growth", fontsize=14, fontweight='bold')

# 3D 轨迹轴
ax3d = fig.add_subplot(2, 2, 1, projection='3d')
ax3d.set_xlim(xs.min()-1, xs.max()+1)
ax3d.set_ylim(ys.min()-1, ys.max()+1)
ax3d.set_zlim(zs.min()-1, zs.max()+1)
ax3d.set_xlabel('X'); ax3d.set_ylabel('Y'); ax3d.set_zlabel('Z')
line3d, = ax3d.plot([], [], [], lw=0.8, color='blue')
point3d, = ax3d.plot([], [], [], 'ro', markersize=4)  # 当前点

# 投影子图
ax_xy = fig.add_subplot(2, 2, 2)
ax_xy.set_xlim(xs.min()-1, xs.max()+1)
ax_xy.set_ylim(ys.min()-1, ys.max()+1)
ax_xy.set_xlabel('X'); ax_xy.set_ylabel('Y')
ax_xy.set_title('xOy Projection')
ax_xy.grid(True, alpha=0.3)
line_xy, = ax_xy.plot([], [], lw=0.5, color='blue')
point_xy, = ax_xy.plot([], [], 'ro', markersize=3)

ax_xz = fig.add_subplot(2, 2, 3)
ax_xz.set_xlim(xs.min()-1, xs.max()+1)
ax_xz.set_ylim(zs.min()-1, zs.max()+1)
ax_xz.set_xlabel('X'); ax_xz.set_ylabel('Z')
ax_xz.set_title('xOz Projection')
ax_xz.grid(True, alpha=0.3)
line_xz, = ax_xz.plot([], [], lw=0.5, color='green')
point_xz, = ax_xz.plot([], [], 'go', markersize=3)

ax_yz = fig.add_subplot(2, 2, 4)
ax_yz.set_xlim(ys.min()-1, ys.max()+1)
ax_yz.set_ylim(zs.min()-1, zs.max()+1)
ax_yz.set_xlabel('Y'); ax_yz.set_ylabel('Z')
ax_yz.set_title('yOz Projection')
ax_yz.grid(True, alpha=0.3)
line_yz, = ax_yz.plot([], [], lw=0.5, color='red')
point_yz, = ax_yz.plot([], [], 'ro', markersize=3)

# 时间显示文本
time_text = fig.text(0.02, 0.02, "", fontsize=9, family='monospace',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# ========== 动画初始化 ==========
def init():
    line3d.set_data([], [])
    line3d.set_3d_properties([])
    point3d.set_data([], [])
    point3d.set_3d_properties([])
    line_xy.set_data([], [])
    point_xy.set_data([], [])
    line_xz.set_data([], [])
    point_xz.set_data([], [])
    line_yz.set_data([], [])
    point_yz.set_data([], [])
    time_text.set_text("")
    return (line3d, point3d, line_xy, point_xy, line_xz, point_xz,
            line_yz, point_yz, time_text)

# ========== 动画更新函数 ==========
start_anim = time.time()    # 记录动画开始时间

def update(frame):
    # 当前已经绘制的点数
    end_idx = min((frame + 1) * steps_per_frame, total_steps)
    # 切片
    x_vals = xs[:end_idx]
    y_vals = ys[:end_idx]
    z_vals = zs[:end_idx]
    
    # 更新 3D 线
    line3d.set_data(x_vals, y_vals)
    line3d.set_3d_properties(z_vals)
    if end_idx > 0:
        point3d.set_data([x_vals[-1]], [y_vals[-1]])
        point3d.set_3d_properties([z_vals[-1]])
    
    # 更新投影线
    line_xy.set_data(x_vals, y_vals)
    point_xy.set_data([x_vals[-1]], [y_vals[-1]])
    
    line_xz.set_data(x_vals, z_vals)
    point_xz.set_data([x_vals[-1]], [z_vals[-1]])
    
    line_yz.set_data(y_vals, z_vals)
    point_yz.set_data([y_vals[-1]], [z_vals[-1]])
    
    # 计算已运行时间（从动画开始计时）
    elapsed = time.time() - start_anim
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    millis = int((elapsed - int(elapsed)) * 1000)
    time_str = f"{mins:02d}:{secs:02d}:{millis:03d}"
    
    # 当前点坐标
    if end_idx > 0:
        cx, cy, cz = x_vals[-1], y_vals[-1], z_vals[-1]
        pos_str = f"x={cx:.4f}, y={cy:.4f}, z={cz:.4f}"
    else:
        pos_str = "waiting..."
    
    info = (
        f"σ={sigma}  ρ={rho}  β={beta:.3f}  dt={dt}\n"
        f"Steps: {end_idx}/{total_steps}\n"
        f"Elapsed: {time_str}\n"
        f"Current: {pos_str}\n"
        f"dx/dt = σ(y-x)\n"
        f"dy/dt = x(ρ-z)-y\n"
        f"dz/dt = xy - βz"
    )
    time_text.set_text(info)
    
    return (line3d, point3d, line_xy, point_xy, line_xz, point_xz,
            line_yz, point_yz, time_text)

# ========== 运行动画 ==========
frames = int(np.ceil(total_steps / steps_per_frame))
ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                    interval=interval, blit=False, repeat=False)

plt.tight_layout()
plt.show()