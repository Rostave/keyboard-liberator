"""
Group: Keyboard Liberators
Main entrance of the program. The code initializes components and maintain the main loop.
The loop handles the process flow from image capturing to landmark detection to pose-control mapping.
"""

import pygame
import cv2
import configparser

from context import Context
from detector import Detector
from gamepad import VGamepad
from mapping import PoseFeature, PoseControlMapper
from gui import GUI

# Load configuration
config = configparser.ConfigParser()
config.read('sysconfig.ini')

# Initialize components
ctx = Context(config)
camera = cv2.VideoCapture(0)
FPS = camera.get(cv2.CAP_PROP_FPS)
RESO = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
gui = GUI(ctx, RESO, FPS)
detector = Detector(ctx)
mapper = PoseControlMapper(ctx)
gamepad = VGamepad()
ctx.gamepad = gamepad

# Main loop
while True:
    if not gui.handle_events():
        print("Quit application")
        break

    gui.clock_tick()
    gui.clear_color()

    ret, frame = camera.read()
    if not ret:
        print("Cannot capture frame")
        break

    gui.render_webcam_capture(frame)  # Draw webcam capture
    landmarks = detector.get_landmarks(frame)  # Detect pose landmarks
    gui.render_pose_landmarks(landmarks)  # Draw pose landmarks
    features = mapper.extract_features(landmarks)  # Extract pose features
    gui.render_pose_features(features)  # Draw pose features
    mapper.trigger_control()  # Map pose features to gamepad controls
    gui.update_display()  # Update GUI display

# Release resources
camera.release()
gamepad.release()
gui.quit()
ctx.close()
