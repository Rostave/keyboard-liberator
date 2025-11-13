"""
Group: Keyboard Liberators
This code provides a simpler way to send gamepad controls to the virtual controller.
For Windows users.
"""

import vgamepad as vg
from vgamepad import XUSB_BUTTON
from control.controller import VRacingController


class VGamepadWin(VRacingController):
    """
    Virtual controller (supports skip mode for macOS/testing)
    """

    # Button constants - only defined if vgamepad available
    UP = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    DOWN = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    LEFT = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    RIGHT = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    A = XUSB_BUTTON.XUSB_GAMEPAD_A
    B = XUSB_BUTTON.XUSB_GAMEPAD_B
    X = XUSB_BUTTON.XUSB_GAMEPAD_X
    Y = XUSB_BUTTON.XUSB_GAMEPAD_Y
    START = XUSB_BUTTON.XUSB_GAMEPAD_START
    BACK = XUSB_BUTTON.XUSB_GAMEPAD_BACK
    GUIDE = XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

    def __init__(self, skip=False):
        if not skip:
            self._gamepad = vg.VX360Gamepad()
        else:
            self._gamepad = None

    def brake(self, value: float):
        if self._gamepad:
            self._gamepad.left_trigger_float(value)  # [0.0, 1.0]
            self._gamepad.update()

    def throttle(self, value: float):
        if self._gamepad:
            self._gamepad.right_trigger_float(value)  # [0.0, 1.0]
            self._gamepad.update()

    def steer(self, value: float):
        if self._gamepad:
            self._gamepad.left_joystick_float(value, 0)  # [-1.0, 1.0]
            self._gamepad.update()

    def press_button(self, button):
        if self._gamepad:
            self._gamepad.press_button(button)
            self._gamepad.update()

    def release_button(self, button):
        if self._gamepad:
            self._gamepad.release_button(button)
            self._gamepad.update()

    def close(self):
        if self._gamepad:
            self._gamepad.reset()
            self._gamepad.update()
