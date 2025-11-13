"""
Group: Keyboard Liberators
This module contains utility functions
"""
import math
import sys
import pygame
import ctypes
from tkinter import messagebox
from typing import Union, List
import platform


def L(landmarks, i):
    """
    Get i th landmark coordinates
    """
    lm = landmarks.landmark[i]
    return lm.x, lm.y, lm.z


def avg(landmark_points):
    """
    Get the average of landmark points
    """
    n = len(landmark_points)
    sx = sum(p[0] for p in landmark_points)
    sy = sum(p[1] for p in landmark_points)
    sz = sum(p[2] for p in landmark_points)
    return sx / n, sy / n, sz / n


def clamp01(x: float) -> float:
    """
    Clamp x to the range [0, 1]
    """
    return max(0.0, min(1.0, x))


def dist_pow(p1: Union[List, tuple], p2: Union[List, tuple], e) -> float:
    return ((p1[0]-p2[0])**e + (p1[1]-p2[1])**e) / e


def set_window_topmost(set_topmost: bool) -> None:
    """Set window topmost on Windows platform."""
    # TODO: not work!
    if sys.platform == 'win32':
        hwnd = pygame.display.get_wm_info()['window']
        if set_topmost:
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003)
        else:
            ctypes.windll.user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0003)


def set_window_transparency(set_transparent: bool) -> None:
    """
    Set window transparency and topmost on Windows platform.

    :param set_transparent: bool, if True, set the window background to transparent.
    :param set_topmost: bool, if True, set the window to always stay on top of other windows.
    """
    if sys.platform == 'win32':
        try:
            # Get window handle
            hwnd = pygame.display.get_wm_info()['window']

            # Windows API constants
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_TOPMOST = 0x00000008
            LWA_ALPHA = 0x2
            LWA_COLORKEY = 0x1

            # Get current window style
            current_style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)

            # Set window style based on parameters
            if set_transparent:
                # Set window as layered window
                ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, current_style | WS_EX_LAYERED)
                # Set color key to black (RGB(0, 0, 0))
                color_key = 0x000000
                ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 200, LWA_COLORKEY | LWA_ALPHA)
                # print("Window transparency enabled based on color key (black)")
            else:
                if WS_EX_LAYERED & current_style:
                    # Cancel layered window
                    new_style = current_style ^ WS_EX_LAYERED
                    ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, new_style)
                    # print("Window transparency disabled")

        except Exception as e:
            print(f"Failed to set window attributes: {e}")


key2pygame_mapping = {
    # a-z
    'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c, 'd': pygame.K_d, 'e': pygame.K_e,
    'f': pygame.K_f, 'g': pygame.K_g, 'h': pygame.K_h, 'i': pygame.K_i, 'j': pygame.K_j,
    'k': pygame.K_k, 'l': pygame.K_l, 'm': pygame.K_m, 'n': pygame.K_n, 'o': pygame.K_o,
    'p': pygame.K_p, 'q': pygame.K_q, 'r': pygame.K_r, 's': pygame.K_s, 't': pygame.K_t,
    'u': pygame.K_u, 'v': pygame.K_v, 'w': pygame.K_w, 'x': pygame.K_x, 'y': pygame.K_y,
    'z': pygame.K_z,

    # 0-9
    '0': pygame.K_0, '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4,
    '5': pygame.K_5, '6': pygame.K_6, '7': pygame.K_7, '8': pygame.K_8, '9': pygame.K_9,

    # F1 to F12
    'f1': pygame.K_F1, 'f2': pygame.K_F2, 'f3': pygame.K_F3, 'f4': pygame.K_F4, 'f5': pygame.K_F5,
    'f6': pygame.K_F6, 'f7': pygame.K_F7, 'f8': pygame.K_F8, 'f9': pygame.K_F9, 'f10': pygame.K_F10,
    'f11': pygame.K_F11, 'f12': pygame.K_F12,

    # Others
    'space': pygame.K_SPACE, 'enter': pygame.K_RETURN,
    'slash': pygame.K_SLASH, 'backslash': pygame.K_BACKSLASH,
}
"""Mapping key strings to pygame key constants"""


def fold_tkparam_win_on_close():
    messagebox.showinfo("Cannot close", "Calibration window will be closed together with pygame window.")


def save_preset_on_close() -> bool:
    return messagebox.askyesno("Save preset?", "Do you want to save the current preset?")


def check_os() -> str:
    os_name = platform.system()
    if os_name not in ["Windows", "Darwin"]:
        print(f"Not supported OS: '{os_name}', program quit!")
        exit(-1)
    return os_name

