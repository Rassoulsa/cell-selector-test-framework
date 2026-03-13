from core.logger import setup_logger
from core.exceptions import MotionError, DeviceStateError, CommandError
from communication.serial_client import SerialClient
from communication.protocol_parser import ProtocolParser


class RobotArm:
    def __init__(self, client: SerialClient):
        self.client = client
        self.logger = setup_logger(__name__)
        self.parser = ProtocolParser()

    def move_to_target(self, x: float, y: float) -> None:
        self.logger.info(f"Sending robot move command to X={x}, Y={y}")
        self.client.send_command(f"ROBOT_MOVE {x},{y}")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Robot failed to move to target ({x}, {y}): {response}")

        self.logger.info(f"Robot move command accepted for target ({x}, {y})")

    def pick(self) -> None:
        self.logger.info("Sending PICK command")
        self.client.send_command("PICK")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Robot pick failed: {response}")

        self.logger.info("Robot pick successful")

    def place(self) -> None:
        self.logger.info("Sending PLACE command")
        self.client.send_command("PLACE")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Robot place failed: {response}")

        self.logger.info("Robot place successful")

    def get_status(self) -> str:
        self.logger.info("Requesting robot status")
        self.client.send_command("ROBOT_STATUS")
        response = self.client.read_response()

        try:
            status = self.parser.parse_status(response)
            self.logger.info(f"Robot status is {status}")
            return status
        except CommandError as e:
            raise DeviceStateError(f"Could not get robot status: {response}") from e