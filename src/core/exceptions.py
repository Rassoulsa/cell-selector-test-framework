class FrameworkError(Exception):
    """Base exception for the test framework."""


class ConnectionError(FrameworkError):
    """Raised when a device connection fails."""


class CommandError(FrameworkError):
    """Raised when a command is invalid or rejected."""


class DeviceStateError(FrameworkError):
    """Raised when a device is in an invalid state."""


class MotionError(FrameworkError):
    """Raised when motor or robot motion fails."""


class CameraError(FrameworkError):
    """Raised when camera operation fails."""