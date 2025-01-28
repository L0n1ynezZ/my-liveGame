# game_ui.py
import os
import tkinter as tk
from tkinter import ttk
from utils.file_utils import get_resource_path
import pygame


class GameUI:
    def __init__(self, root, animation_manager):
        self.root = root
        self.animation_manager = animation_manager
        self.typing_interval = 100  # 默认文字间隔
        self.sound_effect = get_resource_path("../assets/sounds/type.mp3")

        # 初始化 pygame 混音器
        pygame.mixer.init()

        # 初始化界面组件
        self.create_left_panel()
        self.create_right_panel()

        # 绑定尺寸监控
        # self.root.bind("<Configure>", self.track_dimensions)

    def create_left_panel(self):
        """创建左侧控制面板"""
        self.left_frame = ttk.Frame(self.root, padding=10, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 文字输入组件
        self.text_input = ttk.Entry(self.left_frame, width=20)
        self.text_input.pack(pady=5, fill=tk.X)

        # 同步控制组件
        control_frame = ttk.Frame(self.left_frame)
        control_frame.pack(pady=5, fill=tk.X)

        self.interval_scale = ttk.Scale(
            control_frame,
            from_=50,
            to=500,
            value=self.typing_interval,
            command=self.update_interval
        )
        self.interval_scale.pack(side=tk.LEFT, expand=True)

        sync_btn = ttk.Button(
            control_frame,
            text="同步文字",
            command=self.start_text_sync
        )
        sync_btn.pack(side=tk.RIGHT)

        # 动画选择按钮
        ttk.Label(self.left_frame, text="动画选择：").pack(pady=5)
        self.animation_btns = []
        for anim_file in self.get_animation_files():
            btn = ttk.Button(
                self.left_frame,
                text=os.path.splitext(anim_file)[0],
                command=lambda f=anim_file: self.animation_manager.load_animation(f)
            )
            btn.pack(pady=2, fill=tk.X)
            self.animation_btns.append(btn)

    def create_right_panel(self):
        """创建右侧展示面板"""
        self.right_frame = ttk.Frame(self.root, padding=10)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # 获取动画管理器的画布引用
        self.canvas = self.animation_manager.canvas
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 初始化对话框
        self.init_dialog_box()

    def init_dialog_box(self):
        """初始化对话框样式"""
        # 对话框背景
        self.dialog_bg = self.canvas.create_rectangle(
            50, 50, 550, 180,
            fill="#F0F0F0",
            outline="#808080",
            width=2
        )
        # 对话框箭头
        self.dialog_arrow = self.canvas.create_polygon(
            100, 180, 130, 180, 115, 190,
            fill="#F0F0F0",
            outline="#808080",
            width=2
        )
        # 文字显示区域
        self.text_item = self.canvas.create_text(
            100, 100,
            text="",
            font=("微软雅黑", 12),
            anchor=tk.NW,
            width=400
        )

    def update_interval(self, value):
        """更新文字显示间隔"""
        self.typing_interval = int(float(value))

    def start_text_sync(self):
        """启动文字同步动画"""
        if hasattr(self, 'typing_job'):
            self.root.after_cancel(self.typing_job)
        self.sync_text = self.text_input.get()
        self.current_pos = 0
        self.canvas.itemconfig(self.text_item, text="")
        self.update_text_display()

    def update_text_display(self):
        """更新文字显示（逐字动画）"""
        if self.current_pos < len(self.sync_text):
            displayed_text = self.sync_text[:self.current_pos + 1]
            self.canvas.itemconfig(self.text_item, text=displayed_text)

            # 播放音效（每隔3个字符播放一次）
            if self.current_pos % 3 == 0 and os.path.exists(self.sound_effect):
                self.play_sound()

            self.current_pos += 1
            self.typing_job = self.root.after(
                self.typing_interval,
                self.update_text_display
            )

    def play_sound(self):
        """播放音效"""
        try:
            # 加载音效文件
            sound = pygame.mixer.Sound(self.sound_effect)
            # 播放音效
            sound.play()
        except Exception as e:
            print(f"音效播放失败: {str(e)}")

    def track_dimensions(self, event):
        """监控界面尺寸变化"""
        left_width = self.left_frame.winfo_width()
        left_height = self.left_frame.winfo_height()
        right_width = self.right_frame.winfo_width()
        right_height = self.right_frame.winfo_height()

        print("\n当前界面尺寸：")
        print(f"左侧面板: {left_width}x{left_height}")
        print(f"右侧面板: {right_width}x{right_height}")
        print("-" * 30)

    def get_animation_files(self):
        """获取动画文件列表"""
        anim_dir = get_resource_path("animations")
        if os.path.exists(anim_dir):
            return [
                os.path.join(anim_dir, f)
                for f in os.listdir(anim_dir)
                if f.endswith(".gif")
            ]
        return []

# game_ui.py这一块还有很多问题：
# 1.最终面板呈现的效果是上下分层，而不是我预期的左右分层
# 2.我希望你能把对话框的箭头朝上摆放，或者在新代码中详细告诉我你的对话框设计思路，并教我如何修改
# 3.同步文字的音效播放异常，我的声音持续时间1秒，我希望你在选择文字同步速度的时候，能详细讲清楚文字同步的速度，并添加一个按钮展开一个下拉框，方便我选择声音
# 4.对话框我只希望我在点击同步文字之后才会出现，并且我希望有一个追加文字的按钮和结束对话的按钮。追加文字按钮负责在现有内容的基础上另起一行同步内容，但是不能超出对话框背景（原代码文字显示区域没有限制好）。结束对话按钮负责让对话框消失