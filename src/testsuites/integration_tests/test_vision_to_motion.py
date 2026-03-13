import pytest

from devices.motor_controller import MotorController
from devices.camera_module import CameraModule
from core.exceptions import MotionError


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
    def detect_target(self, image_id: str) -> float:
        # pretend vision processed image and found X coordinate
        return 250.0


@pytest.mark.integration
def test_vision_pipeline_triggers_motor_motion():
    fake_client = FakeSerialClient(responses=[
        "IMAGE_ID:img_001",  # camera capture
        "OK",                # motor move
    ])

    camera = CameraModule(fake_client)
    motor = MotorController(fake_client)
    vision = FakeVisionSystem()

    image_id = camera.capture_image()
    target_position = vision.detect_target(image_id)
    motor.move_to(target_position)

    assert fake_client.commands_sent == [
        "CAPTURE",
        "MOVE 250.0"
    ]