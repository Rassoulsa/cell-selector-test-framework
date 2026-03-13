from core.exceptions import CommandError
from config.settings import AppConfig


def validate_position(position: float) -> None:
    config = AppConfig()

    if not isinstance(position, (int, float)):
        raise CommandError(f"Position must be numeric, got {type(position)}")

    if position < config.motion.min_position:
        raise CommandError(
            f"Position {position} is below minimum {config.motion.min_position}"
        )

    if position > config.motion.max_position:
        raise CommandError(
            f"Position {position} exceeds maximum {config.motion.max_position}"
        )


def validate_coordinates(x: float, y: float) -> None:
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise CommandError("Coordinates must be numeric")

    if x < 0 or y < 0:
        raise CommandError("Coordinates must be positive")


def validate_status(status: str) -> None:
    valid_statuses = {"READY", "BUSY", "ERROR", "IDLE"}

    if status not in valid_statuses:
        raise CommandError(f"Invalid device status: {status}")


def validate_not_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise CommandError(f"{field_name} cannot be empty")