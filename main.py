"""
Group: Keyboard Liberators
Main entrance of the program. The code initializes components and maintain the main loop.
The loop handles the process flow from image capturing to landmark detection to pose-control mapping.
"""

from utils import check_os
if check_os() == "Windows1":
    from control.gamepad import VGamepadWin
    gamepad = VGamepadWin(skip=False)
else:
    from control.keyboard import KeyboardController
    gamepad = KeyboardController()

import cv2
import configparser
from context import Context
from presets import PresetManager
from detector import Detector
from mapping import PoseControlMapper
from gui import GUI

# Load configuration
config = configparser.ConfigParser()
config.read('sysconfig.ini')
os_name = check_os()

# Initialize components
ctx = Context(config)
preset_mgr = PresetManager(ctx)
camera = cv2.VideoCapture(0)
CAP_SETTING = [(640, 480), 30]  # [resolution, fps]
# RESO = [(1280, 720), 30]
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_SETTING[0][0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_SETTING[0][1])
gui = GUI(ctx, CAP_SETTING[0], CAP_SETTING[1])
detector = Detector(ctx)
mapper = PoseControlMapper(ctx)
ctx.gamepad = gamepad
preset_mgr.load_presets()

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

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Turn BGR image format to RGB
    landmarks, frame = detector.get_landmarks(frame)  # Detect pose landmarks

    if landmarks:
        gui.render_np_frame(frame)  # Draw webcam capture
        feats = mapper.extract_features(landmarks)  # Extract pose features
        gui.render_pose_features(feats)  # Draw pose features on GUI
        gui.render_game_controls(feats)  # Draw game controls based on extracted features
        mapper.trigger_control()  # Map pose features to gamepad controls
    else:
        gui.render_np_frame(frame)

    gui.update_display()  # Update GUI display

# Release resources
camera.release()
gamepad.close()
detector.close()
ctx.close()
gui.quit()
