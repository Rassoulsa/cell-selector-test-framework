from core.logger import setup_logger
from core.exceptions import ConnectionError
from communication.serial_client import SerialClient


class ConnectionManager:
    def __init__(self, client: SerialClient, max_retries: int = 3):
        self.client = client
        self.max_retries = max_retries
        self.logger = setup_logger(__name__)

    def open(self) -> None:
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Connection attempt {attempt}/{self.max_retries}")
                self.client.connect()
                self.logger.info("Connection established successfully")
                return
            except Exception as e:
                last_error = e
                self.logger.warning(f"Connection attempt {attempt} failed: {e}")

        raise ConnectionError("Could not establish connection after retries") from last_error

    def close(self) -> None:
        self.client.disconnect()
        self.logger.info("Connection closed")

    def reconnect(self) -> None:
        self.logger.info("Reconnecting device...")
        self.close()
        self.open()