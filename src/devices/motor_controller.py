from core.logger import setup_logger
from core.exceptions import MotionError, DeviceStateError, CommandError
from communication.serial_client import SerialClient
from communication.protocol_parser import ProtocolParser


class MotorController:
    def __init__(self, client: SerialClient):
        self.client = client
        self.logger = setup_logger(__name__)
        self.parser = ProtocolParser()

    def home(self) -> None:
        self.logger.info("Sending HOME command")
        self.client.send_command("HOME")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Failed to home motor: {response}")

        self.logger.info("Motor homing successful")

    def move_to(self, position: float) -> None:
        self.logger.info(f"Sending MOVE command to position {position}")
        self.client.send_command(f"MOVE {position}")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Failed to move motor to {position}: {response}")

        self.logger.info(f"Motor move command accepted for position {position}")

    def stop(self) -> None:
        self.logger.info("Sending STOP command")
        self.client.send_command("STOP")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise MotionError(f"Failed to stop motor: {response}")

        self.logger.info("Motor stop successful")

    def get_position(self) -> float:
        self.logger.info("Requesting motor position")
        self.client.send_command("GET_POS")
        response = self.client.read_response()

        try:
            position = self.parser.parse_position(response)
            self.logger.info(f"Motor position is {position}")
            return position
        except CommandError as e:
            raise DeviceStateError(f"Could not get motor position: {response}") from e

    def get_status(self) -> str:
        self.logger.info("Requesting motor status")
        self.client.send_command("GET_STATUS")
        response = self.client.read_response()

        try:
            status = self.parser.parse_status(response)
            self.logger.info(f"Motor status is {status}")
            return status
        except CommandError as e:
            raise DeviceStateError(f"Could not get motor status: {response}") from e