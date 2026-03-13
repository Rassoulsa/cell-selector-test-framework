from dataclasses import dataclass


@dataclass(frozen=True)
class SerialConfig:
    port: str = "COM3"
    baudrate: int = 9600
    timeout: float = 1.0


@dataclass(frozen=True)
class MotionConfig:
    min_position: int = 0
    max_position: int = 1000
    tolerance: float = 0.5


@dataclass(frozen=True)
class CameraConfig:
    enabled: bool = True
    resolution: tuple[int, int] = (1920, 1080)


@dataclass(frozen=True)
class AppConfig:
    serial: SerialConfig = SerialConfig()
    motion: MotionConfig = MotionConfig()
    camera: CameraConfig = CameraConfig()