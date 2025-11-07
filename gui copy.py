"""
Group: Keyboard Liberators
This program builds a graphical user interface for visualizing pose detection and user calibration.
When receiving function calls from the main loop, the GUI instance renders corresponding graphics to the screen.
"""

from context import Context
from time import time as tm
import pygame
import cv2


class GUI:
    """
    Graphical user interface built using Pygame.
    """
    def __init__(self, ctx: Context, reso: tuple, fps: float):
        self.ctx: Context = ctx
        ctx.gui = self
        self.reso: tuple = reso
        self.fps: float = fps

        pygame.init()
        self.caption = ctx.cfg.get("window", "caption")
        pygame.display.set_caption(self.caption)
        self.win_resolution = self.reso
        self.screen = pygame.display.set_mode(self.win_resolution)
        self.clock = pygame.time.Clock()

        self.show_caption_fps = ctx.cfg.getboolean('window', "show_caption_fps")
        self.delta_time: float = 0.0
        self.running_time: float = 0.0
        self._running_start_time: float = tm()
        self._fps_accum_target: int = ctx.cfg.getint('window', "smooth_fps_accum_frames")
        self._fps_accum_time: int = 0
        self._fps_accum_count: int = 0
        self._smoothed_fps: int = 0

    def clock_tick(self):
        """
        Update the clock and return the elapsed time in seconds.
        """
        self.running_time = tm() - self._running_start_time
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        if self.show_caption_fps:
            self.__calc_smooth_fps()
            caption = f"{self.caption}  FPS: {self._smoothed_fps}"
            pygame.display.set_caption(caption)
        return self.delta_time

    def __calc_smooth_fps(self):
        """
        Calculate the smoothed FPS based on the accumulated FPS values.
        """
        self._fps_accum_count += 1
        self._fps_accum_time += self.delta_time
        if self._fps_accum_count >= self._fps_accum_target:
            self._smoothed_fps = round(self._fps_accum_count / self._fps_accum_time)
            pygame.display.set_caption(f"{self.caption}  FPS: {self._smoothed_fps}")
            self._fps_accum_count = 0
            self._fps_accum_time = 0.0

    def clear_color(self):
        """
        Clear the screen with the specified color.
        """
        self.screen.fill((255, 255, 255))

    @staticmethod
    def update_display():
        """
        Update the display with the rendered graphics.
        """
        pygame.display.flip()

    def render_webcam_capture(self, np_frame):
        """
        Visualize the webcam capture to the screen.
        """
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        self.screen.blit(frame, (0, 0))

    def render_pose_landmarks(self, landmarks):
        """
        Visualize the pose landmarks (links) to the screen.
        TODO: Given Mediapipe upper body pose landmarks, visualize the pose landmarks (links) to the screen.
        """

    def render_pose_features(self, features):
        """
        Visualize the pose features to the screen.
        TODO: Given PoseFeature instance, visualize the data on the screen
        """

    @staticmethod
    def handle_events() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    @staticmethod
    def quit():
        """
        Close the pygame window and release resources
        """
        pygame.quit()
