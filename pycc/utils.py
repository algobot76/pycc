"""Utility functions"""
from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap_optional(value: Optional[T]) -> T:
    """Unwraps the optional type and returns new type if type is not None.

    Args:
        value: The value to be unwrapped.

    Returns:
        The unwrapped value.
    """

    if value is None:
        raise Exception(f"{value} is None")

    new_value: T = value

    return new_value
