"""
Group: Keyboard Liberators
This program applies MediaPipe to detect user pose and obtain landmarks.
When receiving invocation from the main loop, it will call the detector instance for pose landmarks.
"""

import mediapipe as mp
import cv2
from context import Context


class Detector:
    """
    Detect user pose, obtaining landmarks
    """
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.detector = self
        # Initialize the MediaPipe detector instance
        self.mp_pose = mp.solutions.pose
        # 初始化姿态检测器，设置检测和跟踪置信度阈值
        # MediaPipe Pose检测全身33个landmark点（包括头部、身体、手臂、手等）
        # 根据mapping.py中使用的索引（包括23, 24等），需要完整检测全身姿态
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,  # False表示视频流模式，True表示静态图像模式
            model_complexity=1,  # 0=轻量, 1=标准, 2=高精度（1是速度和精度的平衡）
            smooth_landmarks=True,  # 启用landmark平滑，减少抖动
            enable_segmentation=False,  # 不启用分割（不需要分割功能）
            smooth_segmentation=True,
            min_detection_confidence=0.5,  # 检测置信度阈值
            min_tracking_confidence=0.5  # 跟踪置信度阈值
        )

    def get_landmarks(self, frame):
        """
        Use the detector instance to detect user pose of upper body, obtain and return landmarks.
        使用检测器实例检测用户上半身姿态，获取并返回landmarks。
        
        Args:
            frame: BGR格式的图像帧（从cv2.VideoCapture读取）
        
        Returns:
            landmarks: MediaPipe检测到的姿态landmarks，如果未检测到则返回None
        """
        # 将BGR图像转换为RGB格式（MediaPipe需要RGB格式）
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # 进行姿态检测
        results = self.pose.process(image_rgb)
        
        # 恢复图像可写状态
        image_rgb.flags.writeable = True
        
        # 返回检测到的landmarks
        # results.pose_landmarks 是一个 NormalizedLandmarkList 对象
        # 包含33个landmark点，每个点有x, y, z坐标和visibility属性
        # 在mapping.py中可以通过landmarks.landmark[i]访问第i个landmark
        # 在gui.py中可以直接使用landmarks进行可视化绘制
        if results.pose_landmarks:
            return results.pose_landmarks
        else:
            return None
    
    def close(self):
        """
        释放MediaPipe资源
        Release MediaPipe resources
        """
        if hasattr(self, 'pose') and self.pose:
            self.pose.close()



