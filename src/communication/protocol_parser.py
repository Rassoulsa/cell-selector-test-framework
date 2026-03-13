from core.exceptions import CommandError

""" baste be noe payam vorudi miyaym in tabe haro estefade mikonim ta payam vorudi ro bekhunim                     """
class ProtocolParser:
    @staticmethod
    def parse_status(response: str) -> str:
        """
        Example: STATUS:READY
        """
        if response.startswith("STATUS:"):
            return response.split(":", 1)[1]
        raise CommandError(f"Invalid status response: {response}")

    @staticmethod
    def parse_position(response: str) -> float:
        """
        Example: POS:123.45
        """
        if response.startswith("POS:"):
            try:
                return float(response.split(":", 1)[1])
            except ValueError as e:
                raise CommandError(f"Invalid position value: {response}") from e
        raise CommandError(f"Invalid position response: {response}")

    @staticmethod
    def is_ok(response: str) -> bool:
        """
        Example: OK
        """
        return response.strip() == "OK"

    @staticmethod
    def parse_error(response: str) -> str:
        """
        Example: ERROR:TIMEOUT
        """
        if response.startswith("ERROR:"):
            return response.split(":", 1)[1]
        raise CommandError(f"Invalid error response: {response}")