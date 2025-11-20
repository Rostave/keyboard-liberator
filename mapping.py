"""
Group: Controller Liberators
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
        self.fist_diameter: float = 0.0  # diameter of a circle made by two fists

        self.left_pressure: float = 0.0  # [0,1] left joystick input strength (left)
        self.right_pressure: float = 0.0  # [0,1] left joystick input strength (right)
        self.brake_pressure: float = 0.0  # [0,1] brake trigger strength
        self.throttle_pressure: float = 0.0  # [0,1] throttle trigger strength
        self.handbrake_active: bool = False  # whether handbrake is active

        if check_os() == "Darwin":
            self.steering_safe_angle: float = 0.0
            self.steering_left_border_angle: float = 0.0
            self.steering_right_border_angle: float = 0.0
            # self.throttle_dist_ratio_center: float = 0.0
            # self.throttle_dist_ratio_safe_dist: float = 0.0
            # self.throttle_dist_ratio_max_dist: float = 0.0
            self.brake_radius_min: float = 0.0
            self.brake_radius_max: float = 0.0
            self.throttle_radius_min: float = 0.0
            self.throttle_radius_max: float = 0.0
        else:
            # Control parameters
            # Steering sensitivity
            self.steering_safe_angle = ctx.tkparam.scalar("steering safe angle", 7.0, 0.0, 30.0)
            self.steering_left_border_angle = ctx.tkparam.scalar("steering left border", 45.0, 0.0, 80.0)
            self.steering_right_border_angle = ctx.tkparam.scalar("steering right border", 45.001, 0.0, 80.0)

            # throttle and brake
            # -max_dist ---- -safe_dist --- 0 --- safe_dist --- max_dist
            # |<-     brake     ->|                 |<-  throttle  ->|
            # self.throttle_dist_ratio_center = ctx.tkparam.scalar("throttle measure center", 6.0, 0.0, 9.0)
            # self.throttle_dist_ratio_safe_dist = ctx.tkparam.scalar("throttle safe distance", 0.6, 0.0, 2.0)
            # self.throttle_dist_ratio_max_dist = ctx.tkparam.scalar("throttle max distance", 2.0, 0.0, 5.0)
            self.brake_radius_min = ctx.tkparam.scalar("brake radius min", 6.0, 0.0, 1.0)
            self.brake_radius_max = ctx.tkparam.scalar("brake radius max", 6.001, 0.0, 1.0)
            self.throttle_radius_min = ctx.tkparam.scalar("throttle radius min", 6.002, 0.0, 1.0)
            self.throttle_radius_max = ctx.tkparam.scalar("throttle radius max", 6.003, 0.0, 1.0)


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
    mouth_indices = [9, 10]
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
        if check_os() == "Darwin":
            f = self.features
            f.steering_safe_angle = preset.mapping["steering safe angle"]
            f.steering_left_border_angle = preset.mapping["steering left border"]
            f.steering_right_border_angle = preset.mapping["steering right border"]
            # f.throttle_dist_ratio_center = preset.mapping["throttle measure center"]
            # f.throttle_dist_ratio_safe_dist = preset.mapping["throttle safe distance"]
            # f.throttle_dist_ratio_max_dist = preset.mapping["throttle max distance"]
            f.brake_radius_min = preset.mapping["brake radius min"]
            f.brake_radius_max = preset.mapping["brake radius max"]
            f.throttle_radius_min = preset.mapping["throttle radius min"]
            f.throttle_radius_max = preset.mapping["throttle radius max"]
        else:
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
        safe_angle = f.steering_safe_angle
        f.left_pressure = clamp01((-f.steer_angle-safe_angle) / f.steering_left_border_angle)\
            if f.steer_angle < 0 else 0.0
        f.right_pressure = clamp01((f.steer_angle-safe_angle) / f.steering_right_border_angle) \
            if f.steer_angle > 0 else 0.0

        # Throttle and brake
        fist_dist = math.dist(f.hand_left_center, f.hand_right_center)
        fist_radius = fist_dist * 0.5
        if fist_radius < f.brake_radius_max:  # brake
            f.brake_pressure = clamp01((f.brake_radius_max - fist_radius) / (f.brake_radius_max - f.brake_radius_min))
            f.throttle_pressure = 0.0
        if fist_radius > f.throttle_radius_min:  # throttle
            f.throttle_pressure = clamp01((fist_radius - f.throttle_radius_min) / (f.throttle_radius_max - f.throttle_radius_min))
            f.brake_pressure = 0.0

        shoulder_pts = [L(landmarks, i) for i in self.body_shoulder_indices]
        hip_pts = [L(landmarks, i) for i in self.body_hip_indices]
        len_s = dist_pow(*shoulder_pts, e=4)
        len_h = dist_pow(*hip_pts, e=4)
        throttle_ratio = len_s / len_h
        throttle_center = f.throttle_dist_ratio_center
        throttle_dist = f.throttle_dist_ratio_max_dist
        throttle_safe_dist = f.throttle_dist_ratio_safe_dist
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
        gp.steer(f.right_pressure - f.left_pressure)

        # throttle and brake
        gp.throttle(f.throttle_pressure)
        gp.brake(f.brake_pressure)

