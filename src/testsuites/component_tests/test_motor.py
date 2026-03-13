import pytest

from devices.motor_controller import MotorController
from core.exceptions import MotionError, DeviceStateError


class FakeSerialClient:
    def __init__(self, responses):
        self.responses = responses
        self.commands_sent = []

    def send_command(self, command: str) -> None:
        self.commands_sent.append(command)

    def read_response(self) -> str:
        if not self.responses:
            return ""
        return self.responses.pop(0)


@pytest.mark.smoke
def test_motor_home_success():
    fake_client = FakeSerialClient(responses=["OK"])
    motor = MotorController(fake_client)

    motor.home()

    assert fake_client.commands_sent == ["HOME"]


@pytest.mark.smoke
def test_motor_move_success():
    fake_client = FakeSerialClient(responses=["OK"])
    motor = MotorController(fake_client)

    motor.move_to(150)

    assert fake_client.commands_sent == ["MOVE 150"]


@pytest.mark.regression
def test_motor_stop_success():
    fake_client = FakeSerialClient(responses=["OK"])
    motor = MotorController(fake_client)

    motor.stop()

    assert fake_client.commands_sent == ["STOP"]


@pytest.mark.regression
def test_motor_get_position_success():
    fake_client = FakeSerialClient(responses=["POS:123.5"])
    motor = MotorController(fake_client)

    position = motor.get_position()

    assert fake_client.commands_sent == ["GET_POS"]
    assert position == 123.5


@pytest.mark.regression
def test_motor_get_status_success():
    fake_client = FakeSerialClient(responses=["STATUS:READY"])
    motor = MotorController(fake_client)

    status = motor.get_status()

    assert fake_client.commands_sent == ["GET_STATUS"]
    assert status == "READY"


@pytest.mark.regression
def test_motor_home_failure():
    fake_client = FakeSerialClient(responses=["ERROR:HOME_FAILED"])
    motor = MotorController(fake_client)

    with pytest.raises(MotionError):
        motor.home()


@pytest.mark.regression
def test_motor_get_position_invalid_response():
    fake_client = FakeSerialClient(responses=["INVALID_RESPONSE"])
    motor = MotorController(fake_client)

    with pytest.raises(DeviceStateError):
        motor.get_position()