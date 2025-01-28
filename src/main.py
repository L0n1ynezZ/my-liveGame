import tkinter as tk
from tkinter import ttk
from game_ui import GameUI
from animation_manager import AnimationManager


class LiveGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Game")

        # 创建画布
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 初始化管理器
        self.animation_manager = AnimationManager(self.canvas)

        # 创建界面
        self.ui = GameUI(root, self.animation_manager)


if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGame(root)
    root.mainloop()