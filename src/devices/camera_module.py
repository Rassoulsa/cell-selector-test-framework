from core.logger import setup_logger
from core.exceptions import CameraError, DeviceStateError, CommandError
from communication.serial_client import SerialClient
from communication.protocol_parser import ProtocolParser


class CameraModule:
    def __init__(self, client: SerialClient):
        self.client = client
        self.logger = setup_logger(__name__)
        self.parser = ProtocolParser()

    def initialize(self) -> None:
        self.logger.info("Sending CAMERA_INIT command")
        self.client.send_command("CAMERA_INIT")
        response = self.client.read_response()

        if not self.parser.is_ok(response):
            raise CameraError(f"Camera initialization failed: {response}")

        self.logger.info("Camera initialized successfully")

    def capture_image(self) -> str:
        self.logger.info("Sending CAPTURE command")
        self.client.send_command("CAPTURE")
        response = self.client.read_response()

        if response.startswith("IMAGE_ID:"):
            image_id = response.split(":", 1)[1]
            self.logger.info(f"Image captured successfully: {image_id}")
            return image_id

        raise CameraError(f"Image capture failed: {response}")

    def get_status(self) -> str:
        self.logger.info("Requesting camera status")
        self.client.send_command("CAMERA_STATUS")
        response = self.client.read_response()

        try:
            status = self.parser.parse_status(response)
            self.logger.info(f"Camera status is {status}")
            return status
        except CommandError as e:
            raise DeviceStateError(f"Could not get camera status: {response}") from e