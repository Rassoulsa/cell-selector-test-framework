import serial

from core.logger import setup_logger
from core.exceptions import ConnectionError, CommandError
from config.settings import AppConfig

"""az serialClient ye shey misazim va ba connect vasl mishim. self.connection dar hame ja hamune
dakhele init hast. chin self dare har tabe mitune jodagane azash estefade kone    """
class SerialClient:
    def __init__(self, config: AppConfig | None = None):
        self.config = config or AppConfig()
        self.logger = setup_logger(__name__)
        self.connection = None

    def connect(self) -> None:
        try:
            self.connection = serial.Serial(
                port=self.config.serial.port,
                baudrate=self.config.serial.baudrate,
                timeout=self.config.serial.timeout,
            )
            self.logger.info(f"Connected to serial port {self.config.serial.port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to serial port: {e}")
            raise ConnectionError(f"Could not connect to {self.config.serial.port}") from e

    def disconnect(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
            self.logger.info("Serial connection closed")

    def send_command(self, command: str) -> None:
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Serial connection is not open")

        try:
            self.connection.write((command + "\n").encode("utf-8"))
            self.logger.info(f"Sent command: {command}")
        except Exception as e:
            self.logger.error(f"Failed to send command: {e}")
            raise CommandError(f"Could not send command: {command}") from e

    def read_response(self) -> str:
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Serial connection is not open")

        try:
            response = self.connection.readline().decode("utf-8").strip()
            self.logger.info(f"Received response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to read response: {e}")
            raise CommandError("Could not read response from device") from e