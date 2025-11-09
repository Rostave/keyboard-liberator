"""
Test GUI controls visualization
"""
import pygame
import cv2
import numpy as np
import sys
import os

# 添加父目录到路径，以便导入主目录的模块
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# 创建一个简单的 Context mock
class MockConfig:
    def get(self, section, key):
        defaults = {
            'caption': 'Game Controls Test',
            'smooth_fps_accum_frames': '10'
        }
        return defaults.get(key, 'default')
    
    def getboolean(self, section, key):
        return True
    
    def getint(self, section, key):
        return 10

class MockContext:
    def __init__(self):
        self.cfg = MockConfig()
        self.gui = None

# 导入 GUI 类
from context import Context
# 如果上面导入失败，使用 mock
try:
    ctx = Context()
except:
    ctx = MockContext()

# 导入 GUI
import importlib.util
gui_demo_path = os.path.join(parent_dir, "gui_demo.py")
spec = importlib.util.spec_from_file_location("gui", gui_demo_path)
gui_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gui_module)

GUI = gui_module.GUI

# 初始化 GUI
gui = GUI(ctx, reso=(500, 400), fps=60)

# 创建一个虚拟的摄像头画面（纯色背景）
def create_dummy_frame(width=640, height=480):
    """创建一个渐变色的虚拟画面"""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # 创建渐变背景
    for i in range(height):
        frame[i, :] = [50 + i//3, 100 + i//4, 150 + i//5]
    return frame

# 模拟变量
brake = 0.0
throttle = 0.0
handbrake = False
left_turn = 0.0
right_turn = 0.0
time_counter = 0

print("GUI 半透明测试启动！")
print("操作说明：")
print("  W键: 油门加速")
print("  S键: 刹车减速")
print("  A键: 左转")
print("  D键: 右转")
print("  空格键: 切换手刹")
print("  ESC: 退出")
print("\n提示：窗口是半透明的，可以透过看到后面的桌面或应用！")

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                handbrake = not handbrake
    
    # 键盘控制
    keys = pygame.key.get_pressed()
    
    # 油门控制（W键）
    if keys[pygame.K_w]:
        throttle = min(1.0, throttle + 0.02)
    else:
        throttle *= 0.95  # 自然衰减
    
    # 刹车控制（S键）
    if keys[pygame.K_s]:
        brake = min(1.0, brake + 0.02)
    else:
        brake *= 0.95  # 自然衰减
    
    # 左转控制（A键）
    if keys[pygame.K_a]:
        left_turn = min(1.0, left_turn + 0.02)
    else:
        left_turn *= 0.95  # 自然衰减
    
    # 右转控制（D键）
    if keys[pygame.K_d]:
        right_turn = min(1.0, right_turn + 0.02)
    else:
        right_turn *= 0.95  # 自然衰减
    
    # 清屏（黑色背景会完全透明）
    gui.clear_color()
    
    # 不渲染摄像头画面，保持背景透明
    # gui.render_webcam_capture(dummy_frame)  # 注释掉
    
    # 绘制游戏控制UI
    gui.render_game_controls(
        brake_pressure=brake,
        throttle_pressure=throttle,
        handbrake_active=handbrake,
        left_pressure=left_turn,
        right_pressure=right_turn
    )
    
    # 更新显示
    gui.update_display()
    gui.clock_tick()
    
    time_counter += 1

# 退出
gui.quit()
print("GUI 测试结束")
