"""
Group: Keyboard Liberators
This program applies MediaPipe to detect user pose and obtain landmarks.
When receiving invocation from the main loop, it will call the detector instance for pose landmarks.
"""
import numpy as np

try:
    import mediapipe as mp
except Exception as e:
    import os
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    print("Mediapipe importing error, using 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python'")
    import mediapipe as mp

import cv2
import numpy as np
from context import Context
from presets import Preset


class Detector:
    """
    Detect user pose, obtaining landmarks
    """
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.detector = self

        # Initialize the MediaPipe detector instance
        # MediaPipe Pose detects 33 landmark including head, body, arms and hands
        cfg = ctx.cfg["MediaPipe"]
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,  # for video
            model_complexity=cfg.getint("model_complexity"),
            smooth_landmarks=cfg.getboolean("smooth_landmarks"),
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=cfg.getfloat("min_detection_confidence"),
            min_tracking_confidence=cfg.getfloat("min_tracking_confidence")
        )

        self.visualize_landmarks: bool = True
        self.show_cam_capture: bool = False
        ctx.preset_mgr.register_preset_update_callback(self.__on_update_preset)  # Register preset update callback

    def __on_update_preset(self, preset: Preset) -> None:
        """
        Apply the new preset.
        """
        self.visualize_landmarks = preset.visual["show_pose_estimation"]
        self.show_cam_capture = preset.visual["show_cam_capture"]

    def get_landmarks(self, frame):
        """
        Detect user pose of upper body, obtain and return landmarks. frame is an RGB image.
        :returns: pose landmarks or None is no pose detected, and a frame visualizing pose landmarks
        """

        frame.flags.writeable = False
        results = self.pose.process(frame)
        frame.flags.writeable = True

        if results.pose_landmarks:
            if not self.show_cam_capture:
                frame = np.zeros_like(frame)  # set frame to pure black
            # Visualize the pose landmarks
            if self.visualize_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            return results.pose_landmarks, frame
        else:
            return None, frame
    
    def close(self):
        """
        Release MediaPipe resources
        """
        if self.pose:
            self.pose.close()



