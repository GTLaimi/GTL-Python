import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

def solve_all_n_queens(n=8):
    """返回八皇后问题所有解（每行皇后列索引）"""
    solutions = []
    board = [-1] * n

    def is_safe(row, col):
        for r in range(row):
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def backtrack(row):
        if row == n:
            solutions.append(board.copy())
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

    backtrack(0)
    return solutions

class QueenVisualizer:
    def __init__(self, solutions):
        self.solutions = solutions
        self.n = len(solutions[0]) if solutions else 8
        self.current_idx = 0
        self.total = len(solutions)

        # 创建图形，预留底部空间用于按钮和序号
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.18, top=0.92)  # 底部留出更多空间

        # 绘制棋盘底色
        self.chessboard = np.zeros((self.n, self.n))
        self.chessboard[1::2, ::2] = 1
        self.chessboard[::2, 1::2] = 1
        self.ax.matshow(self.chessboard, cmap='gray', extent=[0, self.n, 0, self.n])

        # 网格线
        for i in range(self.n + 1):
            self.ax.axhline(i, color='black', linewidth=1)
            self.ax.axvline(i, color='black', linewidth=1)

        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # 顶部坐标文本（仅显示坐标）
        self.coord_text = self.ax.text(
            0.5, 1.02, "", transform=self.ax.transAxes,
            ha='center', va='bottom', fontsize=11, family='monospace'
        )

        # 底部序号文本（使用 figure 坐标，放在按钮上方）
        self.index_text = self.fig.text(
            0.5, 0.12, "", ha='center', va='center', fontsize=12
        )

        # 皇后文本容器
        self.queen_texts = []

        # 绘制初始解
        self.update_display()

        # 创建按钮
        ax_prev = plt.axes([0.3, 0.05, 0.15, 0.05])
        ax_next = plt.axes([0.55, 0.05, 0.15, 0.05])
        self.btn_prev = Button(ax_prev, 'Previous')
        self.btn_next = Button(ax_next, 'Next')

        self.btn_prev.on_clicked(self.prev_solution)
        self.btn_next.on_clicked(self.next_solution)

        # 键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def index_to_chess_notation(self, row, col):
        """将(行,列)转为国际象棋坐标，如 (0,0) -> 'a8', (7,7) -> 'h1'"""
        file_char = chr(ord('a') + col)          # 列: a-h
        rank_num = self.n - row                  # 行: 8-1
        return f"{file_char}{rank_num}"

    def get_solution_coords(self, solution):
        """生成当前解的坐标字符串，按行顺序列出"""
        coords = []
        for row, col in enumerate(solution):
            coords.append(self.index_to_chess_notation(row, col))
        return "♛ " + ", ".join(coords)

    def update_display(self):
        # 清除旧皇后
        for txt in self.queen_texts:
            txt.remove()
        self.queen_texts.clear()

        solution = self.solutions[self.current_idx]

        # 绘制新皇后
        for row in range(self.n):
            col = solution[row]
            y_center = self.n - row - 0.5
            x_center = col + 0.5
            bg_color = self.chessboard[row, col]
            color = 'red' if bg_color == 0 else 'darkred'
            txt = self.ax.text(x_center, y_center, '♛',
                               fontsize=28, ha='center', va='center',
                               color=color)
            self.queen_texts.append(txt)

        # 更新顶部坐标文本
        coord_str = self.get_solution_coords(solution)
        self.coord_text.set_text(coord_str)

        # 更新底部序号文本
        self.index_text.set_text(f"Solution {self.current_idx + 1} of {self.total}")

        self.fig.canvas.draw_idle()

    def prev_solution(self, event):
        self.current_idx = (self.current_idx - 1) % self.total
        self.update_display()

    def next_solution(self, event):
        self.current_idx = (self.current_idx + 1) % self.total
        self.update_display()

    def on_key_press(self, event):
        if event.key == 'left':
            self.prev_solution(None)
        elif event.key == 'right':
            self.next_solution(None)

if __name__ == "__main__":
    all_solutions = solve_all_n_queens(8)
    print(f"Total solutions found: {len(all_solutions)}")

    if all_solutions:
        viz = QueenVisualizer(all_solutions)
        plt.show()
    else:
        print("No solution found.")