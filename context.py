"""
Group: Keyboard Liberators
"""


class Context:
    """
    Application context storing component references.
    """
    def __init__(self, config):
        self.cfg = config  # configuration object reference
        self.detector = None  # pose detector instance
        self.gui = None  # GUI window reference
        self.mapper = None  # pose-control mapper instance
        self.gamepad = None  # virtual gamepad reference
        self.tkparam = None  # tkparam window reference

    def close(self):
        if self.tkparam:
            self.tkparam.quit()
