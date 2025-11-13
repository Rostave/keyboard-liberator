"""
Group: Keyboard Liberators
This program processes the pose data and maps it to control signals and send them to the virtual controller.
"""

import math
from typing import List
from context import Context
from presets import Preset
from utils import *


class ControlFeature:
    """
    Containing process landmark features and game control parameters.
    """
    def __init__(self, ctx: Context):
        self.ctx = ctx

        # Visualizing parameters
        self.hand_left_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.hand_right_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.hands_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.steer_angle: float = 0.0  # [-180,180] estimated steering angle in degrees
        self.torso_pitch: float = 0.0  # estimated torso pitch in degrees

        self.left_pressure: float = 0.0  # [0,1] left joystick input strength (left)
        self.right_pressure: float = 0.0  # [0,1] left joystick input strength (right)
        self.brake_pressure: float = 0.0  # [0,1] brake trigger strength
        self.throttle_pressure: float = 0.0  # [0,1] throttle trigger strength
        self.handbrake_active: bool = False  # whether handbrake is active

        # Control parameters
        # Steering sensitivity
        self.steering_safe_angle = ctx.tkparam.scalar("steering safe angle", 7.0, 0.0, 30.0)
        self.steering_left_border_angle = ctx.tkparam.scalar("steering left border", 45.0, 0.0, 80.0)
        self.steering_right_border_angle = ctx.tkparam.scalar("steering right border", 45.0, 0.0, 80.0)

        # throttle and brake
        # -max_dist ---- -safe_dist --- 0 --- safe_dist --- max_dist
        # |<-     brake     ->|                 |<-  throttle  ->|
        self.throttle_dist_ratio_center = ctx.tkparam.scalar("throttle measure center", 6.0, 0.0, 9.0)
        self.throttle_dist_ratio_safe_dist = ctx.tkparam.scalar("throttle safe distance", 0.6, 0.0, 2.0)
        self.throttle_dist_ratio_max_dist = ctx.tkparam.scalar("throttle max distance", 2.0, 0.0, 5.0)


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
    body_shoulder_indices = [11, 12]
    body_hip_indices = [23, 24]
    body_indices = [11, 12, 23, 24]

    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.mapper = self
        self.features = ControlFeature(ctx)

        # previous button states, trigger press/release only on state changes
        self._prev_menu_pressed = False
        self._prev_y_pressed = False

        ctx.preset_mgr.register_preset_update_callback(self.__on_update_preset)

    def __on_update_preset(self, preset: Preset) -> None:
        self.ctx.tkparam.load_param_from_dict(preset.mapping)

    def extract_features(self, landmarks) -> ControlFeature:
        """
        Update extracted features from the given landmarks, and store them in the PoseFeature instance
        """

        f = self.features
        if landmarks is None:
            return f

        # Get center of hands
        left_points = [L(landmarks, i) for i in self.left_hand_indices]
        right_points = [L(landmarks, i) for i in self.right_hand_indices]

        lcx, lcy, lcz = avg(left_points)
        rcx, rcy, rcz = avg(right_points)
        f.hand_left_center = [1-lcx, lcy]
        f.hand_right_center = [1-rcx, rcy]
        f.hands_center = [1-(lcx+rcx)/2.0, (lcy+rcy)/2.0]

        # Horizontal - 0 degree; Steer right to 90 degree; Steer left to -90
        f.steer_angle = math.degrees(math.atan2(rcx-lcx, rcy-lcy))+90.0
        safe_angle = f.steering_safe_angle.get()
        f.left_pressure = clamp01((-f.steer_angle-safe_angle) / f.steering_left_border_angle.get())\
            if f.steer_angle < 0 else 0.0
        f.right_pressure = clamp01((f.steer_angle-safe_angle) / f.steering_right_border_angle.get()) \
            if f.steer_angle > 0 else 0.0

        # Throttle and brake
        shoulder_pts = [L(landmarks, i) for i in self.body_shoulder_indices]
        hip_pts = [L(landmarks, i) for i in self.body_hip_indices]

        len_s = dist_pow(*shoulder_pts, e=4)
        len_h = dist_pow(*hip_pts, e=4)
        throttle_ratio = len_s / len_h

        # # pitch: positive when shoulders are closer (leaning forward)
        # sx, sy, sz = avg(shoulder_pts)
        # hx, hy, hz = avg(hip_pts)
        # # vector from hips center to shoulders center
        # vy = sy - hy
        # vz = sz - hz
        # # use atan2(-vz, vy) so that more negative vz (shoulders closer) => positive pitch
        # torso_pitch_radian = math.atan2(-vz, vy) if (vy != 0 or vz != 0) else 0.0
        # f.torso_pitch = math.degrees(torso_pitch_radian)
        # print(f"{len_s/len_h}, {f.torso_pitch}")

        # Normalize
        throttle_center = f.throttle_dist_ratio_center.get()
        throttle_dist = f.throttle_dist_ratio_max_dist.get()
        throttle_safe_dist = f.throttle_dist_ratio_safe_dist.get()
        throttle_real_dist = throttle_dist - throttle_safe_dist
        throttle_thresh = throttle_center + throttle_safe_dist
        brake_thresh = throttle_center - throttle_safe_dist
        if throttle_ratio >= throttle_thresh:  # throttling
            f.throttle_pressure = clamp01((throttle_ratio - throttle_thresh) / throttle_real_dist)
            f.brake_pressure = 0.0
        elif throttle_ratio <= brake_thresh:  # braking
            f.throttle_pressure = 0.0
            f.brake_pressure = clamp01((brake_thresh - throttle_ratio) / throttle_real_dist)

        return f

    def trigger_control(self):
        """
        Trigger corresponding game control to the virtual controller based on the extracted features.
        """

        gp = self.ctx.gamepad
        f = self.features

        # steering control
        gp.left_joystick(f.right_pressure - f.left_pressure, 0.0)

        # throttle and brake
        gp.right_trigger(f.throttle_pressure)
        gp.left_trigger(f.brake_pressure)

