"""
Group: Keyboard Liberators
"""
from tkparam import TKParamWindow


class Context:
    """
    Application context storing component references.
    """
    def __init__(self, config):
        self.cfg = config  # configuration object reference
        self.detector = None  # pose detector instance
        self.gui = None  # GUI window reference
        self.preset_mgr = None  # GUI settings reference
        self.mapper = None  # pose-control mapper instance
        self.gamepad = None  # virtual gamepad reference
        self.tkparam = TKParamWindow()  # tkparam window reference

    @property
    def active_preset(self):
        return self.preset_mgr.active_preset

    def close(self):
        if self.tkparam:
            self.tkparam.quit()
