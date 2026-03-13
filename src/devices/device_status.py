from core.logger import setup_logger
from core.exceptions import DeviceStateError


class DeviceStatus:
    def __init__(self):
        self.logger = setup_logger(__name__)

    def check_motor(self, motor) -> bool:
        self.logger.info("Checking motor status")
        status = motor.get_status()
        if status != "READY":
            raise DeviceStateError(f"Motor not ready: {status}")
        self.logger.info("Motor is ready")
        return True

    def check_robot(self, robot) -> bool:
        self.logger.info("Checking robot status")
        status = robot.get_status()
        if status != "READY":
            raise DeviceStateError(f"Robot not ready: {status}")
        self.logger.info("Robot is ready")
        return True

    def check_camera(self, camera) -> bool:
        self.logger.info("Checking camera status")
        status = camera.get_status()
        if status != "READY":
            raise DeviceStateError(f"Camera not ready: {status}")
        self.logger.info("Camera is ready")
        return True

    def check_all(self, motor, robot, camera) -> bool:
        self.logger.info("Performing full system health check")
        self.check_motor(motor)
        self.check_robot(robot)
        self.check_camera(camera)
        self.logger.info("All devices are ready")
        return True