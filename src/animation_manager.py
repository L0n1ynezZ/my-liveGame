import tkinter as tk
from utils.file_utils import load_animation_frames


class AnimationManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.current_animation = None
        self.animation_running = False

    def load_animation(self, filename):
        """加载并播放动画"""
        if self.animation_running:
            self.stop_animation()

        self.animation_frames = load_animation_frames(filename)
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

    def stop_animation(self):
        """停止当前动画"""
        if self.animation_running:
            self.root.after_cancel(self.animation_job)
            self.canvas.delete(self.animation_item)
            self.animation_running = False