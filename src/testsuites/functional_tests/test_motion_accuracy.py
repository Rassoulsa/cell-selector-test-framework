import pytest

from devices.motor_controller import MotorController
from config.settings import AppConfig


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


def is_within_tolerance(target: float, actual: float, tolerance: float) -> bool:
    return abs(target - actual) <= tolerance


@pytest.mark.smoke
def test_motor_reaches_target_within_tolerance():
    config = AppConfig()
    target_position = 150.0

    fake_client = FakeSerialClient(responses=[
        "OK",           # response to MOVE
        "POS:150.3"     # response to GET_POS
    ])

    motor = MotorController(fake_client)

    motor.move_to(target_position)
    actual_position = motor.get_position()

    assert fake_client.commands_sent == ["MOVE 150.0", "GET_POS"]
    assert is_within_tolerance(
        target=target_position,
        actual=actual_position,
        tolerance=config.motion.tolerance
    )


@pytest.mark.regression
def test_motor_reaches_exact_position():
    config = AppConfig()
    target_position = 200.0

    fake_client = FakeSerialClient(responses=[
        "OK",
        "POS:200.0"
    ])

    motor = MotorController(fake_client)

    motor.move_to(target_position)
    actual_position = motor.get_position()

    assert is_within_tolerance(
        target=target_position,
        actual=actual_position,
        tolerance=config.motion.tolerance
    )


@pytest.mark.regression
def test_motor_position_out_of_tolerance():
    config = AppConfig()
    target_position = 300.0

    fake_client = FakeSerialClient(responses=[
        "OK",
        "POS:302.0"
    ])

    motor = MotorController(fake_client)

    motor.move_to(target_position)
    actual_position = motor.get_position()

    assert not is_within_tolerance(
        target=target_position,
        actual=actual_position,
        tolerance=config.motion.tolerance
    )