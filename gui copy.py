"""
Group: Keyboard Liberators
This program builds a graphical user interface for visualizing pose detection and user calibration.
When receiving function calls from the main loop, the GUI instance renders corresponding graphics to the screen.
"""

from context import Context
from time import time as tm
import pygame
import cv2
import sys
import ctypes


class GUI:
    """
    Graphical user interface built using Pygame.
    """
    def __init__(self, ctx: Context, reso: tuple, fps: float):
        self.ctx: Context = ctx
        ctx.gui = self
        self.reso: tuple = reso
        self.fps: float = fps

        pygame.init()
        self.caption = ctx.cfg.get("window", "caption")
        pygame.display.set_caption(self.caption)
        self.win_resolution = self.reso
        self.screen = pygame.display.set_mode(self.win_resolution)
        self.clock = pygame.time.Clock()
        
        # 设置窗口透明（仅Windows）
        self._set_window_transparency()

        self.show_caption_fps = ctx.cfg.getboolean('window', "show_caption_fps")
        self.delta_time: float = 0.0
        self.running_time: float = 0.0
        self._running_start_time: float = tm()
        self._fps_accum_target: int = ctx.cfg.getint('window', "smooth_fps_accum_frames")
        self._fps_accum_time: int = 0
        self._fps_accum_count: int = 0
        self._smoothed_fps: int = 0

    def _set_window_transparency(self):
        """
        Set window transparency on Windows platform.
        """
        if sys.platform == 'win32':
            try:
                # 获取窗口句柄
                hwnd = pygame.display.get_wm_info()['window']
                
                # Windows API 常量
                GWL_EXSTYLE = -20
                WS_EX_LAYERED = 0x80000
                LWA_ALPHA = 0x2
                LWA_COLORKEY = 0x1
                
                # 设置窗口为分层窗口
                _winlib = ctypes.windll.user32
                _winlib.SetWindowLongA(hwnd, GWL_EXSTYLE, 
                                      _winlib.GetWindowLongA(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
                
                # 色键透明：让黑色(0,0,0)完全透明
                colorkey = 0x000000  # 黑色 RGB(0,0,0)
                _winlib.SetLayeredWindowAttributes(hwnd, colorkey, 0, LWA_COLORKEY)
                
                print("窗口色键透明已启用 (黑色背景将完全透明)")
            except Exception as e:
                print(f"设置窗口透明失败: {e}")

    def clock_tick(self):
        """
        Update the clock and return the elapsed time in seconds.
        """
        self.running_time = tm() - self._running_start_time
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        if self.show_caption_fps:
            self.__calc_smooth_fps()
            caption = f"{self.caption}  FPS: {self._smoothed_fps}"
            pygame.display.set_caption(caption)
        return self.delta_time

    def __calc_smooth_fps(self):
        """
        Calculate the smoothed FPS based on the accumulated FPS values.
        """
        self._fps_accum_count += 1
        self._fps_accum_time += self.delta_time
        if self._fps_accum_count >= self._fps_accum_target:
            self._smoothed_fps = round(self._fps_accum_count / self._fps_accum_time)
            pygame.display.set_caption(f"{self.caption}  FPS: {self._smoothed_fps}")
            self._fps_accum_count = 0
            self._fps_accum_time = 0.0

    def clear_color(self):
        """
        Clear the screen with black (transparent when colorkey is enabled).
        """
        self.screen.fill((0, 0, 0))  # 黑色背景将完全透明

    @staticmethod
    def update_display():
        """
        Update the display with the rendered graphics.
        """
        pygame.display.flip()

    def render_webcam_capture(self, np_frame):
        """
        Visualize the webcam capture to the screen.
        """
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        self.screen.blit(frame, (0, 0))

    def render_pose_landmarks(self, landmarks):
        """
        Visualize the pose landmarks (links) to the screen.
        TODO: Given Mediapipe upper body pose landmarks, visualize the pose landmarks (links) to the screen.
        """

    def render_pose_features(self, features):
        """
        Visualize the pose features to the screen.
        TODO: Given PoseFeature instance, visualize the data on the screen
        """

    def render_game_controls(self, brake_pressure=0.0, throttle_pressure=0.0, 
                            handbrake_active=False):
        """
        Render game-style control UI elements in the bottom-right corner.
        Args:
            brake_pressure: 0.0-1.0, brake pedal pressure
            throttle_pressure: 0.0-1.0, throttle pedal pressure
            handbrake_active: bool, handbrake status
        """
        # 基础位置（右下角）
        base_x = self.win_resolution[0] - 250
        base_y = self.win_resolution[1] - 200
        
        # 1. 绘制左踏板（刹车）
        self._draw_pedal(base_x - 80, base_y, brake_pressure, (255, 100, 100), "Brake")
        
        # 2. 绘制右踏板（油门）
        self._draw_pedal(base_x + 20, base_y, throttle_pressure, (100, 255, 100), "Throttle")
        
        # 3. 绘制手刹指示器（中间的横条）
        handbrake_y = base_y + 120
        self._draw_handbrake(base_x - 30, handbrake_y, handbrake_active)
        
        # 4. 绘制按钮组（Y, X, B, A）
        button_x = base_x + 120
        button_y = base_y + 40
        self._draw_button_cluster(button_x, button_y)
    
    def _draw_pedal(self, x, y, pressure, color, label):
        """
        Draw a pedal with fill based on pressure.
        """
        pedal_width = 60
        pedal_height = 100
        
        # 背景（未按下部分）
        bg_rect = pygame.Rect(x, y, pedal_width, pedal_height)
        pygame.draw.rect(self.screen, (80, 80, 80), bg_rect, border_radius=10)
        
        # 填充（按下部分，从下往上填充）
        fill_height = int(pedal_height * pressure)
        if fill_height > 0:
            fill_rect = pygame.Rect(x, y + pedal_height - fill_height, 
                                    pedal_width, fill_height)
            pygame.draw.rect(self.screen, color, fill_rect, border_radius=10)
        
        # 边框
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 3, border_radius=10)
        
        # 标签
        font = pygame.font.Font(None, 20)
        text = font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(centerx=x + pedal_width // 2, y=y + pedal_height + 10)
        self.screen.blit(text, text_rect)
    
    def _draw_handbrake(self, x, y, active):
        """
        Draw handbrake indicator (horizontal bar).
        """
        bar_width = 120
        bar_height = 30
        
        color = (255, 200, 0) if active else (100, 100, 100)
        bar_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, color, bar_rect, border_radius=15)
        
        # 图标/文字
        font = pygame.font.Font(None, 24)
        text = font.render("HANDBRAKE" if active else "---", True, (0, 0, 0))
        text_rect = text.get_rect(center=bar_rect.center)
        self.screen.blit(text, text_rect)
    
    def _draw_button_cluster(self, x, y):
        """
        Draw Xbox-style button cluster (Y, X, B, A).
        """
        button_radius = 20
        button_spacing = 50
        
        buttons = [
            {'pos': (x, y - button_spacing), 'label': 'Y', 'color': (255, 215, 0)},  # 上
            {'pos': (x - button_spacing, y), 'label': 'X', 'color': (100, 150, 255)},  # 左
            {'pos': (x + button_spacing, y), 'label': 'B', 'color': (255, 100, 100)},  # 右
            {'pos': (x, y + button_spacing), 'label': 'A', 'color': (100, 255, 100)},  # 下
        ]
        
        for btn in buttons:
            # 外圈
            pygame.draw.circle(self.screen, (60, 60, 60), btn['pos'], button_radius + 3)
            # 按钮主体
            pygame.draw.circle(self.screen, btn['color'], btn['pos'], button_radius)
            # 字母
            font = pygame.font.Font(None, 28)
            text = font.render(btn['label'], True, (0, 0, 0))
            text_rect = text.get_rect(center=btn['pos'])
            self.screen.blit(text, text_rect)

    @staticmethod
    def handle_events() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    @staticmethod
    def quit():
        """
        Close the pygame window and release resources
        """
        pygame.quit()
