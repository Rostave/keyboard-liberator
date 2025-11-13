"""
Group: Keyboard Liberators
This code provides a simpler way to send gamepad controls to the virtual controller.
For Mac and Linux users.
"""

from control.controller import VRacingController
from pynput.keyboard import Controller


class KeyboardController(VRacingController):
    def __init__(self):
        self.keyboard = Controller()
        self.steering_keys = {
            "left": "a",
            "right": "d",
            "throttle": "w",
            "brake": "s"
        }
        self.is_steer_left = False
        self.is_steer_right = False
        self.is_throttle = False
        self.is_brake = False
        self.trigger_thresh = 0.0001

    def steer(self, value: float):
        if abs(value) < self.trigger_thresh:
            # print("release steering")
            if self.is_steer_left:
                self.keyboard.release(self.steering_keys["left"])
                self.is_steer_left = False
            if self.is_steer_right:
                self.keyboard.release(self.steering_keys["right"])
                self.is_steer_right = False
        elif value < 0:
            if not self.is_steer_left:
                self.keyboard.press(self.steering_keys["left"])
                self.is_steer_left = True
        elif value > 0:
            if not self.is_steer_right:
                self.keyboard.press(self.steering_keys["right"])
                self.is_steer_right = True

    def throttle(self, value: float):
        if abs(value) < self.trigger_thresh:
            if self.is_throttle:
                self.keyboard.release(self.steering_keys["throttle"])
                self.is_throttle = False
        elif value > 0:
            if not self.is_throttle:
                self.keyboard.press(self.steering_keys["throttle"])
                self.is_throttle = True

    def brake(self, value: float):
        if abs(value) < self.trigger_thresh:
            if self.is_brake:
                self.keyboard.release(self.steering_keys["brake"])
                self.is_brake = False
        elif value > 0:
            if not self.is_brake:
                self.keyboard.press(self.steering_keys["brake"])
                self.is_brake = True

    def close(self):
        if self.is_steer_left:
            self.keyboard.release(self.steering_keys["left"])
            self.is_steer_left = False
        if self.is_steer_right:
            self.keyboard.release(self.steering_keys["right"])
            self.is_steer_right = False
        if self.is_throttle:
            self.keyboard.release(self.steering_keys["throttle"])
            self.is_throttle = False
        if self.is_brake:
            self.keyboard.release(self.steering_keys["brake"])
            self.is_brake = False
        del self.keyboard
