"""
Group: Keyboard Liberators
This program processes the pose data and maps it to control signals and send them to the virtual controller.
"""

from typing import List
from context import Context


class PoseFeature:
    """
    Static pose feature class
    """
    # Features
    hand_left_center: List = [0.0, 0.0]
    hand_right_center: List = [0.0, 0.0]
    hands_center: List = [0.0, 0.0]

    # Trigger detection parameters
    steering_thresh_y = 0.1


class PoseControlMapper:

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
        self.features = PoseFeature()

    def extract_features(self, landmarks) -> PoseFeature:
        """
        Update extracted features from the given landmarks, and store them in the PoseFeature instance
        TODO: Input is the landmark features detected by MediaPipe, implement feature extraction, update the fields in the PoseFeature instance, return the PoseFeature instance
        """

        return self.features

    def trigger_control(self):
        """
        Trigger corresponding game control ti the virtual controller based on the extracted features
        TODO: Given the updated features in the PoseFeature instance, trigger the corresponding game control signal to the virtual controller ctx.gamepad
        """

