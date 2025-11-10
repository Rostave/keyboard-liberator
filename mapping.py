"""
Group: Keyboard Liberators
This program processes the pose data and maps it to control signals and send them to the virtual controller.
"""

from typing import List
from context import Context
import math
from presets import PresetManager


class ControlFeature:
    """
    Containing process landmark features and game control parameters.
    """
    def __init__(self, ctx: Context):
        self.ctx = ctx

        # Triggering parameters
        self.torso_pitch: float = 0.0

        # Visualizing parameters
        self.hand_left_center: List = [0.0, 0.0]
        self.hand_right_center: List = [0.0, 0.0]
        self.hands_center: List = [0.0, 0.0]
        self.brake_pressure: float = 0.0
        self.throttle_pressure: float = 0.0
        self.handbrake_active: bool = False
        self.left_pressure: float = 0.0
        self.right_pressure: float = 0.0

        # Control parameters
        # self.steering_left_border_angle = ctx.tkparam.get_scalar()
        # self.steering_left_border_angle


class PoseControlMapper:
    """
    Mapping pose data to control signals.
    """

    # Indices of landmarks of body parts
    head_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    left_hand_indices = [15, 17, 19, 21]
    right_hand_indices = [16, 18, 20, 22]
    hand_indices = [15, 16, 17, 18, 19, 20, 21, 22]
    body_left_indices = [11, 23]
    body_right_indices = [12, 24]
    body_up_indices = [11, 12]
    body_indices = [11, 12, 23, 24]

    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.mapper = self
        self.features = ControlFeature(ctx)

        # previous button states, trigger press/release only on state changes
        self._prev_menu_pressed = False
        self._prev_y_pressed = False

    def extract_features(self, landmarks) -> ControlFeature:
        """
        Update extracted features from the given landmarks, and store them in the PoseFeature instance
        """

        # Reset features to defaults first
        f = self.features
        f.hand_left_center = [0.0, 0.0]
        f.hand_right_center = [0.0, 0.0]
        f.hands_center = [0.0, 0.0]

        # default dynamic features
        f.torso_pitch = 0.0  # positive = leaning forward, negative = leaning backward
        f.left_fist = False
        f.right_fist = False
        f.hands_behind = False

        if landmarks is None:
            return f

        def L(i):
            """
            Get i th landmark coordinates
            """
            lm = landmarks.landmark[i]
            return lm.x, lm.y, lm.z

        # 计算左右手中心：对指定的手部关节点取平均，作为手部中心坐标
        left_points = [L(i) for i in self.left_hand_indices]
        right_points = [L(i) for i in self.right_hand_indices]

        def avg(points):
            n = len(points)
            sx = sum(p[0] for p in points)
            sy = sum(p[1] for p in points)
            sz = sum(p[2] for p in points)
            return sx / n, sy / n, sz / n

        lcx, lcy, lcz = avg(left_points)
        rcx, rcy, rcz = avg(right_points)
        f.hand_left_center = [1-lcx, lcy]
        f.hand_right_center = [1-rcx, rcy]
        f.hands_center = [1 - (lcx+rcx)/2.0, (lcy+rcy)/2.0]

        angle_to_hori = math.degrees(math.atan2(rcy-lcy, rcx-lcx))
        print(angle_to_hori)

        return f

        # 躯干俯仰角估算：使用双肩与双臀（或髋）中点，估计前倾/后仰角度
        shoulder_pts = [L(i) for i in self.body_up_indices]
        hip_pts = [L(i) for i in [23, 24]]
        sx, sy, sz = avg(shoulder_pts)
        hx, hy, hz = avg(hip_pts)

        # vector from hips to shoulders
        vx = sx - hx
        vy = sy - hy
        vz = sz - hz

        # pitch: positive when shoulders are closer (leaning forward)
        # use atan2(-vz, vy) so that more negative vz (shoulders closer) => positive pitch
        f.torso_pitch = math.atan2(-vz, vy) if (vy != 0 or vz != 0) else 0.0

        # 握拳检测：通过指尖与手腕的二维距离判断是否握拳（距离较小表示握拳）
        # 指尖索引（近似）：左手19,21；右手20,22
        def dist(a, b):
            return math.hypot(a[0] - b[0], a[1] - b[1])

        # left wrist is index 15, right wrist 16
        lw = L(15)
        rw = L(16)
        left_tips = [L(19), L(21)]
        right_tips = [L(20), L(22)]
        left_avg_tip = ((left_tips[0][0] + left_tips[1][0]) / 2.0, (left_tips[0][1] + left_tips[1][1]) / 2.0)
        right_avg_tip = ((right_tips[0][0] + right_tips[1][0]) / 2.0, (right_tips[0][1] + right_tips[1][1]) / 2.0)

        left_wrist_xy = (lw[0], lw[1])
        right_wrist_xy = (rw[0], rw[1])

        left_tip_dist = dist(left_avg_tip, left_wrist_xy)
        right_tip_dist = dist(right_avg_tip, right_wrist_xy)

        # 使用配置的阈值判断是否握拳
        fist_thresh = self.ctx.active_preset.mapping["fist_thresh"]
        f.left_fist = left_tip_dist < fist_thresh
        f.right_fist = right_tip_dist < fist_thresh

        # 双手向后摆检测：比较手的z值与躯干中点z，若都显著更大则视为向后摆
        behind_thresh = self.ctx.active_preset.mapping["behind_thresh"]
        body_mid_z = (sz + hz) / 2.0
        if (lcz - body_mid_z) > behind_thresh and (rcz - body_mid_z) > behind_thresh:
            f.hands_behind = True
        else:
            f.hands_behind = False

        return f

    def trigger_control(self):
        # 将提取到的特征映射为虚拟手柄输入：触发器、摇杆、按键等
        """
        Trigger corresponding game control to the virtual controller based on the extracted features.

        Mappings implemented:
        1) torso_pitch -> right_trigger (lean forward) and left_trigger (lean backward)
        2) angle between hands -> left joystick X axis
        3) fist (either hand) -> START button (menu)
        4) both hands swung behind -> Y button
        """

        gp = self.ctx.gamepad
        f = self.features

        # gp.right_trigger(float(rt_value))
        # gp.left_trigger(float(lt_value))

    # --- 左摇杆X轴映射：根据双手相对连线的角度控制左右转向 ---
    # 计算从左手到右手连线的角度，映射为[-1,1]区间
        lx, ly = f.hand_left_center
        rx, ry = f.hand_right_center
        dx = rx - lx
        dy = ry - ly
        angle = math.atan2(dy, dx) if (dx != 0 or dy != 0) else 0.0
        # map angle in [-pi/2,pi/2] to joystick [-1,1], apply steering scale
        joy_x = max(-1.0, min(1.0, (angle / (math.pi / 2)) * self.steering_scale))
        # 应用摇杆死区以避免抖动
        if abs(joy_x) < self.joystick_deadzone:
            joy_x = 0.0
        # gp.left_joystick(float(joy_x), 0.0)

        # --- 按键映射：握拳触发 START（菜单键），双手向后摆触发 Y 键 ---
        menu_pressed = (f.left_fist or f.right_fist)
        y_pressed = f.hands_behind

        # START (menu)
        if menu_pressed and not self._prev_menu_pressed:
            ...
            # gp.press_button(# gp.START)
        if not menu_pressed and self._prev_menu_pressed:
            ...
            # gp.release_button(# gp.START)
        self._prev_menu_pressed = menu_pressed

        # Y button
        if y_pressed and not self._prev_y_pressed:
            ...
            # gp.press_button(# gp.Y)
        if not y_pressed and self._prev_y_pressed:
            ...
            # gp.release_button(# gp.Y)
        self._prev_y_pressed = y_pressed

