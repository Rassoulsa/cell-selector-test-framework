import pytest

from devices.motor_controller import MotorController
from devices.robot_arm import RobotArm
from devices.camera_module import CameraModule


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


@pytest.mark.integration
def test_module_command_sequence():
    fake_client = FakeSerialClient(responses=[
        "OK",                  # camera init
        "IMAGE_ID:img_001",    # capture
        "OK",                  # motor move
        "OK",                  # robot move
        "OK",                  # robot pick
    ])

    camera = CameraModule(fake_client)
    motor = MotorController(fake_client)
    robot = RobotArm(fake_client)

    camera.initialize()
    image_id = camera.capture_image()
    motor.move_to(120.0)
    robot.move_to_target(10, 20)
    robot.pick()

    assert fake_client.commands_sent == [
        "CAMERA_INIT",
        "CAPTURE",
        "MOVE 120.0",
        "ROBOT_MOVE 10,20",
        "PICK"
    ]