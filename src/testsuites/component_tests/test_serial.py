import pytest

from communication.protocol_parser import ProtocolParser
from communication.connection_manager import ConnectionManager
from core.exceptions import CommandError, ConnectionError


class FakeSerialClient:
    def __init__(self, fail_times=0):
        self.fail_times = fail_times
        self.connect_calls = 0
        self.disconnected = False

    def connect(self):
        self.connect_calls += 1
        if self.connect_calls <= self.fail_times:
            raise Exception("Connection failed")

    def disconnect(self):
        self.disconnected = True


@pytest.mark.smoke
def test_parse_status_success():
    parser = ProtocolParser()
    status = parser.parse_status("STATUS:READY")
    assert status == "READY"


@pytest.mark.smoke
def test_parse_position_success():
    parser = ProtocolParser()
    position = parser.parse_position("POS:123.45")
    assert position == 123.45


@pytest.mark.smoke
def test_is_ok_success():
    parser = ProtocolParser()
    assert parser.is_ok("OK") is True


@pytest.mark.regression
def test_parse_error_success():
    parser = ProtocolParser()
    error = parser.parse_error("ERROR:TIMEOUT")
    assert error == "TIMEOUT"


@pytest.mark.regression
def test_parse_status_invalid():
    parser = ProtocolParser()
    with pytest.raises(CommandError):
        parser.parse_status("BAD_RESPONSE")


@pytest.mark.regression
def test_parse_position_invalid():
    parser = ProtocolParser()
    with pytest.raises(CommandError):
        parser.parse_position("POS:abc")


@pytest.mark.regression
def test_connection_manager_open_success():
    fake_client = FakeSerialClient(fail_times=0)
    manager = ConnectionManager(fake_client, max_retries=3)

    manager.open()

    assert fake_client.connect_calls == 1


@pytest.mark.regression
def test_connection_manager_open_with_retry_success():
    fake_client = FakeSerialClient(fail_times=2)
    manager = ConnectionManager(fake_client, max_retries=3)

    manager.open()

    assert fake_client.connect_calls == 3


@pytest.mark.regression
def test_connection_manager_open_failure():
    fake_client = FakeSerialClient(fail_times=5)
    manager = ConnectionManager(fake_client, max_retries=3)

    with pytest.raises(ConnectionError):
        manager.open()


@pytest.mark.regression
def test_connection_manager_close():
    fake_client = FakeSerialClient()
    manager = ConnectionManager(fake_client)

    manager.close()

    assert fake_client.disconnected is True