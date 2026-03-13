import pytest

from devices.camera_module import CameraModule
from core.exceptions import CameraError, DeviceStateError


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
def test_camera_initialize_success():
    fake_client = FakeSerialClient(responses=["OK"])
    camera = CameraModule(fake_client)

    camera.initialize()

    assert fake_client.commands_sent == ["CAMERA_INIT"]


@pytest.mark.smoke
def test_camera_capture_success():
    fake_client = FakeSerialClient(responses=["IMAGE_ID:img_001"])
    camera = CameraModule(fake_client)

    image_id = camera.capture_image()

    assert fake_client.commands_sent == ["CAPTURE"]
    assert image_id == "img_001"


@pytest.mark.regression
def test_camera_get_status_success():
    fake_client = FakeSerialClient(responses=["STATUS:READY"])
    camera = CameraModule(fake_client)

    status = camera.get_status()

    assert fake_client.commands_sent == ["CAMERA_STATUS"]
    assert status == "READY"


@pytest.mark.regression
def test_camera_initialize_failure():
    fake_client = FakeSerialClient(responses=["ERROR:INIT_FAILED"])
    camera = CameraModule(fake_client)

    with pytest.raises(CameraError):
        camera.initialize()


@pytest.mark.regression
def test_camera_capture_failure():
    fake_client = FakeSerialClient(responses=["ERROR:NO_IMAGE"])
    camera = CameraModule(fake_client)

    with pytest.raises(CameraError):
        camera.capture_image()


@pytest.mark.regression
def test_camera_invalid_status_response():
    fake_client = FakeSerialClient(responses=["BAD_STATUS"])
    camera = CameraModule(fake_client)

    with pytest.raises(DeviceStateError):
        camera.get_status()