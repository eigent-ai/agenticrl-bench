"""OpenCV compatibility layer."""
CAP_PROP_FPS = 5
CAP_PROP_FRAME_WIDTH = 3
CAP_PROP_FRAME_HEIGHT = 4
CAP_PROP_FRAME_COUNT = 7


class VideoCapture:
    def __init__(self, source=None):
        self._source = source
        self._opened = source is not None

    def isOpened(self):
        return self._opened

    def read(self):
        return False, None

    def get(self, prop_id):
        return 0.0

    def release(self):
        pass


def __getattr__(name):
    raise AttributeError(f"module 'cv2' has no attribute '{name}'")
