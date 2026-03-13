import pytest

from devices.motor_controller import MotorController
from devices.robot_arm import RobotArm
from devices.camera_module import CameraModule
from devices.device_status import DeviceStatus


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


class FakeVisionSystem:
    def detect_target(self, image_id: str) -> tuple[float, float]:
        # pretend image processing found target coordinates
        return 200.0, 80.0


@pytest.mark.e2e
def test_full_system_workflow():
    fake_client = FakeSerialClient(responses=[
        "STATUS:READY",        # motor status
        "STATUS:READY",        # robot status
        "STATUS:READY",        # camera status
        "OK",                  # camera init
        "IMAGE_ID:img_001",    # capture
        "OK",                  # motor move
        "OK",                  # robot move
        "OK",                  # robot pick
        "OK",                  # robot place
    ])

    motor = MotorController(fake_client)
    robot = RobotArm(fake_client)
    camera = CameraModule(fake_client)
    status_checker = DeviceStatus()
    vision = FakeVisionSystem()

    # 1. health check
    assert status_checker.check_all(motor, robot, camera) is True

    # 2. initialize camera and capture image
    camera.initialize()
    image_id = camera.capture_image()

    # 3. detect target
    target_x, target_y = vision.detect_target(image_id)

    # 4. move motion system
    motor.move_to(target_x)

    # 5. robot action
    robot.move_to_target(target_x, target_y)
    robot.pick()
    robot.place()

    assert fake_client.commands_sent == [
        "GET_STATUS",
        "ROBOT_STATUS",
        "CAMERA_STATUS",
        "CAMERA_INIT",
        "CAPTURE",
        "MOVE 200.0",
        "ROBOT_MOVE 200.0,80.0",
        "PICK",
        "PLACE",
    ]