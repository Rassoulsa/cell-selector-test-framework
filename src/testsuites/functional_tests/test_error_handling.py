import pytest

from devices.motor_controller import MotorController
from devices.camera_module import CameraModule
from devices.robot_arm import RobotArm
from core.exceptions import MotionError, CameraError, DeviceStateError


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


@pytest.mark.regression
def test_motor_error_response_handling():
    fake_client = FakeSerialClient(responses=["ERROR:MOTOR_BLOCKED"])
    motor = MotorController(fake_client)

    with pytest.raises(MotionError):
        motor.move_to(100)


@pytest.mark.regression
def test_camera_error_response_handling():
    fake_client = FakeSerialClient(responses=["ERROR:NO_SIGNAL"])
    camera = CameraModule(fake_client)

    with pytest.raises(CameraError):
        camera.initialize()


@pytest.mark.regression
def test_robot_error_response_handling():
    fake_client = FakeSerialClient(responses=["ERROR:TARGET_UNREACHABLE"])
    robot = RobotArm(fake_client)

    with pytest.raises(MotionError):
        robot.move_to_target(10, 20)


@pytest.mark.regression
def test_invalid_status_response_handling():
    fake_client = FakeSerialClient(responses=["BROKEN_STATUS"])
    robot = RobotArm(fake_client)

    with pytest.raises(DeviceStateError):
        robot.get_status()