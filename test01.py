import tkinter as tk
from tkinter import ttk
import winsound
import os


class EnhancedAnimationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("增强版互动展示游戏")

        # 初始化参数
        self.typing_interval = 100  # 文字显示间隔（毫秒）
        self.sound_effect = "type.wav"  # 默认音效文件
        self.current_animation = None
        self.animation_running = False

        # 创建界面布局
        self.create_left_panel()
        self.create_right_panel()

        # 绑定尺寸监控
        self.root.bind("<Configure>", self.track_dimensions)

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

        self.interval_scale = ttk.Scale(control_frame,
                                        from_=50,
                                        to=500,
                                        value=self.typing_interval,
                                        command=self.update_interval)
        self.interval_scale.pack(side=tk.LEFT, expand=True)

        sync_btn = ttk.Button(control_frame,
                              text="同步文字",
                              command=self.start_text_sync)
        sync_btn.pack(side=tk.RIGHT)

        # 动画选择按钮
        ttk.Label(self.left_frame, text="动画选择：").pack(pady=5)
        self.animation_btns = []
        for anim_file in self.get_animation_files():
            btn = ttk.Button(self.left_frame,
                             text=os.path.splitext(anim_file)[0],
                             command=lambda f=anim_file: self.load_animation(f))
            btn.pack(pady=2, fill=tk.X)
            self.animation_btns.append(btn)

    def create_right_panel(self):
        """创建右侧展示面板"""
        self.right_frame = ttk.Frame(self.root, padding=10)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # 创建带对话框的展示画布
        self.canvas = tk.Canvas(self.right_frame,
                                width=600,
                                height=400,
                                bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 绘制对话框背景
        self.dialog_bg = self.canvas.create_rectangle(
            50, 50, 550, 180,
            fill="#F0F0F0",
            outline="#808080",
            width=2
        )
        self.dialog_arrow = self.canvas.create_polygon(
            100, 180, 130, 180, 115, 190,
            fill="#F0F0F0",
            outline="#808080",
            width=2
        )
        self.text_item = self.canvas.create_text(
            100, 100,
            text="",
            font=("微软雅黑", 12),
            anchor=tk.NW,
            width=400
        )

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
            if self.current_pos % 3 == 0:
                self.play_sound()

            self.current_pos += 1
            self.typing_job = self.root.after(self.typing_interval, self.update_text_display)

    def update_interval(self, value):
        """更新文字显示间隔"""
        self.typing_interval = int(float(value))

    def play_sound(self):
        """播放音效"""
        if os.path.exists(self.sound_effect):
            try:
                winsound.PlaySound(self.sound_effect, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                print(f"音效播放失败: {str(e)}")

    def load_animation(self, filename):
        """加载外部动画文件（支持GIF）"""
        if self.animation_running:
            self.stop_animation()

        try:
            self.animation_frames = []
            frame_index = 0
            while True:
                frame = tk.PhotoImage(file=filename, format=f"gif -index {frame_index}")
                self.animation_frames.append(frame)
                frame_index += 1
        except tk.TclError:
            pass

        if self.animation_frames:
            self.current_frame = 0
            self.animation_item = self.canvas.create_image(300, 250, image=self.animation_frames[0])
            self.animate()

    def animate(self):
        """执行动画帧更新"""
        if self.animation_running:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.canvas.itemconfig(self.animation_item, image=self.animation_frames[self.current_frame])
            self.animation_job = self.root.after(100, self.animate)

    def track_dimensions(self, event):
        """实时输出界面尺寸"""
        left_width = self.left_frame.winfo_width()
        left_height = self.left_frame.winfo_height()
        right_width = self.right_frame.winfo_width()
        right_height = self.right_frame.winfo_height()

        print("\n当前界面尺寸：")
        print(f"左侧面板: {left_width} x {left_height}")
        print(f"右侧面板: {right_width} x {right_height}")
        print("-" * 30)

    def stop_animation(self):
        """停止当前动画"""
        if self.animation_running:
            self.root.after_cancel(self.animation_job)
            self.canvas.delete(self.animation_item)
            self.animation_running = False

    @staticmethod
    def get_animation_files():
        """获取动画文件列表（假设存放在animations目录）"""
        animation_dir = "animations"
        if os.path.exists(animation_dir):
            return [os.path.join(animation_dir, f)
                    for f in os.listdir(animation_dir)
                    if f.endswith(".gif")]
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedAnimationGame(root)
    root.mainloop()