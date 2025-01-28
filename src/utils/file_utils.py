import os

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets"))
    return os.path.join(base_path, relative_path)

def load_animation_frames(filename):
    """加载动画帧"""
    frames = []
    try:
        frame_index = 0
        while True:
            frame = tk.PhotoImage(file=filename, format=f"gif -index {frame_index}")
            frames.append(frame)
            frame_index += 1
    except tk.TclError:
        pass
    return frames