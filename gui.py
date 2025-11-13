"""
Group: Keyboard Liberators
This program builds a graphical user interface for visualizing pose detection and user calibration.
When receiving function calls from the main loop, the GUI instance renders corresponding graphics to the screen.
"""

from typing import Optional
import os
import math
from time import time as tm
import pygame
from pygame.color import Color

from context import Context
from mapping import ControlFeature
from presets import Preset
from utils import *


class GUI:
    """
    Graphical user interface built using Pygame.
    """

    UI_SCALE_FACTOR = 0.6
    UI_IMG_ROOT = "UI_Icons"

    def __init__(self, ctx: Context, reso: tuple, fps: float):
        self.ctx: Context = ctx
        ctx.gui = self
        self.reso: tuple = reso
        self.fps: float = fps

        pygame.init()
        win_cfg = ctx.cfg["Window"]
        self.caption = win_cfg["caption"]
        pygame.display.set_caption(self.caption)
        self.win_resolution = self.reso
        self.screen = pygame.display.set_mode(self.win_resolution, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.delta_time: float = 0.0
        self.running_time: float = 0.0
        self._running_start_time: float = tm()

        self._fps_accum_time: int = 0
        self._fps_accum_count: int = 0
        self._smoothed_fps: int = 0

        self.calibration_mode = True
        set_window_topmost(True)
        self._set_calibration_mode(self.calibration_mode)
        self._load_ui_icons()

        # do not close tkparam window
        if check_os() != "Darwin":
            ctx.tkparam.root.protocol("WM_DELETE_WINDOW", fold_tkparam_win_on_close)

        # Load configuration parameters
        visual_cfg = ctx.cfg["Feature.visual"]
        pref_cfg = ctx.cfg["Preferences"]
        self.show_caption_fps = win_cfg.getboolean("show_caption_fps")
        self._fps_accum_target: int = win_cfg.getint("smooth_fps_accum_frames")
        self.wheel_rot_max_angle = visual_cfg.getfloat("ui_wheel_rot_max_angle")
        self.fist_center_circle_radius: int = visual_cfg.getint("fist_center_circle_radius")
        self.fist_center_circle_color: Color = Color(visual_cfg.get("fist_center_circle_color"))
        self.steer_wheel_fill_color: Color = Color(visual_cfg.get("steer_wheel_fill_color"))
        calibration_key = pref_cfg.get("calibration_mode_toggle_key").lower()
        self.calibration_mode_toggle_key: int = key2pygame_mapping.get(calibration_key, pygame.K_BACKSLASH)

        # Tkparam
        if check_os() == "Darwin":
            self.show_cam_capture: float = 0.0
            self.show_pose_estimation: float = 0.0
        else:
            self.show_cam_capture = ctx.tkparam.button_bool("show camera capture", True)
            self.show_pose_estimation = ctx.tkparam.button_bool("show pose estimation", True)

        ctx.preset_mgr.register_preset_update_callback(self.__on_update_preset)

    def _get_pos_from_per(self, per):
        return per[0] * self.reso[0], per[1] * self.reso[1]

    def _set_calibration_mode(self, mode: bool) -> None:
        """Set calibration mode"""
        if check_os() == "Darwin":
            return
        self.calibration_mode = mode
        set_window_transparency(not mode)
        tkparam_win = self.ctx.tkparam.root
        if mode:
            tkparam_win.deiconify()
        else:
            tkparam_win.withdraw()
        print(f"Calibration mode: {mode}")

    def __on_update_preset(self, preset: Preset) -> None:
        """
        Called when the active preset is updated.
        """
        if check_os() == "Darwin":
            self.show_cam_capture: float = preset.visual["show camera capture"]
            self.show_pose_estimation: float = preset.visual["show pose estimation"]
        else:
            self.ctx.tkparam.load_param_from_dict(preset.visual)

    def _load_ui_icons(self) -> None:
        """
        Load UI icons from UI_Icons folder and scale them.
        """
        self.brake_icon = self.__load_scaled_img("break.png", self.UI_SCALE_FACTOR)
        self.throttle_icon = self.__load_scaled_img("throttle.png", self.UI_SCALE_FACTOR)
        self.wheel_icon = self.__load_scaled_img("wheel.png", self.UI_SCALE_FACTOR)
        self.wheel_track_icon = self.__load_scaled_img("wheel_track.png", self.UI_SCALE_FACTOR)
        self.steer_wheel_icon = self.__load_scaled_img("steer_wheel.png", self.UI_SCALE_FACTOR)

    def __load_scaled_img(self, name: str, scale_factor: float):
        path = os.path.join(os.path.dirname(__file__), self.UI_IMG_ROOT, name)
        try:
            original_wheel2 = pygame.image.load(path).convert_alpha()
            new_size = (int(original_wheel2.get_width() * scale_factor),
                        int(original_wheel2.get_height() * scale_factor))
            return pygame.transform.smoothscale(original_wheel2, new_size)
        except Exception as e:
            print(f"Cannot load UI icon {path}: {e}")
            return None

    def clock_tick(self) -> float:
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

    def __calc_smooth_fps(self) -> None:
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

    def clear_color(self) -> None:
        """
        Clear the screen with black (transparent when colorkey is enabled).
        """
        self.screen.fill((0, 0, 0))  # 黑色背景将完全透明

    @staticmethod
    def update_display() -> None:
        """
        Update the display with the rendered graphics.
        """
        pygame.display.flip()

    def render_np_frame(self, np_frame) -> None:
        """
        Visualize the webcam capture to the screen.
        """
        if not self.calibration_mode or (not self.show_cam_capture and not self.show_pose_estimation):
            return
        frame = pygame.surfarray.make_surface(np_frame)
        frame = pygame.transform.rotate(frame, -90)
        self.screen.blit(frame, (0, 0))

    def render_pose_features(self, f: ControlFeature):
        if not self.calibration_mode:
            return

        # Fists
        pos_l = self._get_pos_from_per(f.hand_left_center)
        pos_r = self._get_pos_from_per(f.hand_right_center)

        # Draw virtual steer wheel
        diameter = math.dist(pos_l, pos_r)
        scale_factor = diameter / self.steer_wheel_icon.get_width()
        scaled_wheel_icon = pygame.transform.rotozoom(self.steer_wheel_icon, -f.steer_angle, scale_factor)
        center_pos = self._get_pos_from_per(f.hands_center)
        rect = scaled_wheel_icon.get_rect(center=center_pos)
        self.screen.blit(scaled_wheel_icon, rect)

        fist_center = (pos_l[0]+pos_r[0])//2, (pos_l[1]+pos_r[1])//2
        if self.show_pose_estimation:
            pygame.draw.circle(
                self.screen, self.fist_center_circle_color, pos_l, self.fist_center_circle_radius, 0)
            pygame.draw.circle(
                self.screen, self.fist_center_circle_color, pos_r, self.fist_center_circle_radius, 0)
            r: float = self.ctx.mapper.features.brake_radius_min * self.reso[0]
            pygame.draw.circle(self.screen, self.fist_center_circle_color, fist_center, r, 1)
            r = self.ctx.mapper.features.brake_radius_max * self.reso[0]
            pygame.draw.circle(self.screen, self.fist_center_circle_color, fist_center, r, 1)
            r = self.ctx.mapper.features.throttle_radius_min * self.reso[0]
            pygame.draw.circle(self.screen, self.fist_center_circle_color, fist_center, r, 1)
            r = self.ctx.mapper.features.throttle_radius_max * self.reso[0]
            pygame.draw.circle(self.screen, self.fist_center_circle_color, fist_center, r, 1)

    def render_game_controls(self, feat: ControlFeature) -> None:
        self.__render_game_controls(feat.brake_pressure, feat.throttle_pressure, feat.handbrake_active,
                                    feat.left_pressure, feat.right_pressure)

    def __render_game_controls(self,
                               brake_pressure=0.0, throttle_pressure=0.0, handbrake_active=False,
                               left_pressure=0.0, right_pressure=0.0) -> None:
        """
        Render game-style control UI elements in the bottom-right corner.
        :param brake_pressure: 0.0-1.0, brake pedal pressure
        :param throttle_pressure: 0.0-1.0, throttle pedal pressure
        :param handbrake_active: bool, handbrake status (not used)
        :param left_pressure: 0.0-1.0, left turn pressure (A key)
        :param right_pressure: 0.0-1.0, right turn pressure (D key)
        """
        # 基础位置（右下角）
        base_x = self.win_resolution[0] - 200
        base_y = self.win_resolution[1] - 280

        # 1. 绘制按钮组（Y, X, B, A）在下方
        button_x = base_x + 60
        button_y = base_y + 180
        # self.__draw_button_cluster(button_x, button_y)

        # 2. 绘制踏板在按钮上方
        # 刹车在左边（再往左移）
        brake_x = base_x - 170
        brake_y = base_y
        self.__draw_pedal(brake_x, brake_y, brake_pressure, (255, 100, 100), "Brake")

        # 油门在刹车右边（左移一些）
        throttle_x = base_x + 20
        throttle_y = base_y
        self.__draw_pedal(throttle_x, throttle_y, throttle_pressure, (100, 255, 100), "Throttle")

        # 3. 先绘制方向盘轨道(wheel2)在左下角，与YB按键平齐
        wheel_x = base_x - 200  # 往左移动
        wheel_y = button_y - 30  # 与按键Y平齐，再往上移30
        self.__draw_wheel(wheel_x, wheel_y, left_pressure, right_pressure)

    def __draw_pedal(self, x, y, pressure, color, label):
        """
        Draw a pedal using icon image with fill based on pressure.
        Selects brake or throttle icon based on label.
        """
        # 根据标签选择对应的图标
        if label == "Brake":
            icon = self.brake_icon
        elif label == "Throttle":
            icon = self.throttle_icon
        else:
            icon = None
            return

        icon_width, icon_height = icon.get_size()

        # 创建结果表面
        result_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA)

        # 1. 绘制半透明的完整图标作为背景（未填充部分）
        dimmed_icon = icon.copy()
        dimmed_icon.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        result_surface.blit(dimmed_icon, (0, 0))

        # 2. 绘制填充部分（从下往上，更透明）
        fill_height = int(icon_height * pressure)

        if fill_height > 0:
            # 创建一个临时表面用于填充部分
            fill_surface = pygame.Surface((icon_width, fill_height), pygame.SRCALPHA)

            # 复制图标的底部部分
            fill_surface.blit(icon, (0, -(icon_height - fill_height)))

            # 设置为更透明
            fill_surface.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)

            # 绘制填充部分到结果表面
            result_surface.blit(fill_surface, (0, icon_height - fill_height))

        # 贴到主屏幕
        self.screen.blit(result_surface, (x, y))

    def __rotate_at_pivot(self, surface, ori_rect, pivot, angle):
        """Rotate an image around a pivot point"""
        rotated_image = pygame.transform.rotozoom(surface, angle, 1.0)
        original_center = ori_rect.center

        # Vector from the original center to the pivot point
        vector_to_pivot = (pivot[0] - original_center[0], pivot[1] - original_center[1])

        # Rotate the vector
        radians = math.radians(angle)
        rot_vector_x = vector_to_pivot[0] * math.cos(radians) - vector_to_pivot[1] * math.sin(radians)
        rot_vector_y = vector_to_pivot[0] * math.sin(radians) + vector_to_pivot[1] * math.cos(radians)

        new_center = (pivot[0] + rot_vector_x, pivot[1] - rot_vector_y)
        new_rect = rotated_image.get_rect(center=new_center)

        return rotated_image, new_rect

    def __draw_wheel(self, x, y, left_pressure, right_pressure):
        """
        Draw steering wheel with left/right fill from center.
        Args:
            x, y: position
            left_pressure: 0.0-1.0, left turn pressure (A key)
            right_pressure: 0.0-1.0, right turn pressure (D key)
        """

        icon_width, icon_height = self.wheel_icon.get_size()
        result_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA)

        # Fill transparent background
        dimmed_icon = self.wheel_icon.copy()
        dimmed_icon.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        result_surface.blit(dimmed_icon, (0, 0))

        center_x = icon_width // 2

        # Fill left
        if left_pressure > 0:
            fill_width = int(center_x * left_pressure)
            if fill_width > 0:
                fill_surface = pygame.Surface((fill_width, icon_height), pygame.SRCALPHA)
                source_x = center_x - fill_width
                fill_surface.blit(self.wheel_icon, (-source_x, 0))
                fill_surface.fill(self.steer_wheel_fill_color, special_flags=pygame.BLEND_RGBA_MULT)
                result_surface.blit(fill_surface, (center_x - fill_width, 0))

        # Fill right
        if right_pressure > 0:
            fill_width = int(center_x * right_pressure)
            if fill_width > 0:
                fill_surface = pygame.Surface((fill_width, icon_height), pygame.SRCALPHA)
                fill_surface.blit(self.wheel_icon, (-center_x, 0))
                fill_surface.fill(self.steer_wheel_fill_color, special_flags=pygame.BLEND_RGBA_MULT)
                result_surface.blit(fill_surface, (center_x, 0))

        if left_pressure > 0:
            rot = left_pressure * self.wheel_rot_max_angle
        elif right_pressure > 0:
            rot = -right_pressure * self.wheel_rot_max_angle
        else:
            rot = 0

        result_surface_rect = result_surface.get_rect()
        result_surface_rect.topleft = x, y
        wheel_track_rect = self.wheel_track_icon.get_rect()
        midbottom = result_surface_rect.midbottom
        wheel_track_rect.midbottom = midbottom
        rot_center = midbottom[0], midbottom[1]+result_surface_rect.height*11.4
        result_surface, result_surface_rect = self.__rotate_at_pivot(result_surface, result_surface_rect, rot_center, rot)
        wheel_track_rect.y += wheel_track_rect.height * 0.2

        self.screen.blit(result_surface, result_surface_rect)
        self.screen.blit(self.wheel_track_icon, wheel_track_rect)

    def __draw_handbrake(self, x, y, active):
        """
        Draw handbrake indicator (horizontal bar - white with transparency).
        """
        bar_width = 120
        bar_height = 30

        # 创建半透明 Surface
        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

        # 根据激活状态设置透明度
        alpha = 220 if active else 100
        bar_rect = pygame.Rect(0, 0, bar_width, bar_height)
        pygame.draw.rect(bar_surface, (255, 255, 255, alpha), bar_rect, border_radius=15)

        # 边框
        pygame.draw.rect(bar_surface, (255, 255, 255, 255), bar_rect, 2, border_radius=15)

        # 贴到主屏幕
        self.screen.blit(bar_surface, (x, y))

        # 图标/文字（白色）
        font = pygame.font.Font(None, 24)
        text = font.render("HANDBRAKE" if active else "---", True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.screen.blit(text, text_rect)

    def __draw_button_cluster(self, x, y):
        """
        Draw Xbox-style button cluster (white with transparency).
        """
        button_radius = 16  # 缩小从20到16
        button_spacing = 45  # 缩小从50到45

        buttons = [
            {'pos': (x, y - button_spacing), 'label': 'Y'},  # 上
            {'pos': (x - button_spacing, y), 'label': 'X'},  # 左
            {'pos': (x + button_spacing, y), 'label': 'B'},  # 右
            {'pos': (x, y + button_spacing), 'label': 'A'},  # 下
        ]

        for btn in buttons:
            # 创建半透明按钮 Surface
            btn_size = (button_radius * 2 + 6) * 2
            btn_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            center = (btn_size // 2, btn_size // 2)

            # 按钮主体（白色半透明，与踏板透明度一致）
            pygame.draw.circle(btn_surface, (255, 255, 255, 100), center, button_radius)

            # 字母（白色，更不透明）- 使用抗锯齿字体确保居中
            font = pygame.font.Font(None, 30)
            text = font.render(btn['label'], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = center  # 明确设置中心点
            btn_surface.blit(text, text_rect)

            # 贴到主屏幕
            surface_pos = (btn['pos'][0] - btn_size // 2, btn['pos'][1] - btn_size // 2)
            self.screen.blit(btn_surface, surface_pos)

    def _save_tkparam_preset(self):
        if check_os() == "Darwin":
            return
        preset = self.ctx.active_preset
        dump = self.ctx.tkparam.dump_param_to_dict()
        for k in preset.visual.keys():
            preset.visual[k] = dump[k]
        for k in preset.mapping.keys():
            preset.mapping[k] = dump[k]
        self.ctx.preset_mgr.save_active_to_file()

    def handle_events(self) -> bool:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if save_preset_on_close():
                    self._save_tkparam_preset()
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == self.calibration_mode_toggle_key:
                    self._set_calibration_mode(not self.calibration_mode)
        return True

    @staticmethod
    def quit():
        """
        Close the pygame window and release resources
        """
        pygame.quit()
