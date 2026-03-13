import pytest

from devices.motor_controller import MotorController
from core.exceptions import MotionError, DeviceStateError


class FakeTimeoutSerialClient:
    def __init__(self, responses):
        self.responses = responses
        self.commands_sent = []

    def send_command(self, command: str) -> None:
        self.commands_sent.append(command)

    def read_response(self) -> str:
        if not self.responses:
            return ""
        return self.responses.pop(0)


@pytest.mark.regression
def test_motor_move_timeout_behavior():
    fake_client = FakeTimeoutSerialClient(responses=[""])
    motor = MotorController(fake_client)

    with pytest.raises(MotionError):
        motor.move_to(100)


@pytest.mark.regression
def test_motor_status_timeout_behavior():
    fake_client = FakeTimeoutSerialClient(responses=[""])
    motor = MotorController(fake_client)

    with pytest.raises(DeviceStateError):
        motor.get_status()


@pytest.mark.regression
def test_motor_position_timeout_behavior():
    fake_client = FakeTimeoutSerialClient(responses=[""])
    motor = MotorController(fake_client)

    with pytest.raises(DeviceStateError):
        motor.get_position()