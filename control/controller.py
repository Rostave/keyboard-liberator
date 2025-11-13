"""
Group: Keyboard Liberators
This module defines the virtual racing control types, needs to be implemented.
"""

from abc import ABC, abstractmethod


class VRacingController(ABC):
    @abstractmethod
    def steer(self, value: float):
        """
        Steer the wheel.
        :param value: steering value between -1.0 and 1.0
        """

    @abstractmethod
    def throttle(self, value: float):
        """
        Throttle to speed up.
        :param value: throttle value between 0.0 and 1.0
        """

    @abstractmethod
    def brake(self, value: float):
        """
        Throttle to speed up.
        :param value: brake value between 0.0 and 1.0
        """

    def close(self):
        """
        Release the controller resources.
        """
