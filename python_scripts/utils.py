"""Utility functions"""

import os
from pathlib import Path, PosixPath
from typing import Optional
import logging
from logging import Logger, StreamHandler

from dotenv import load_dotenv


def find_file_path(
    target_file_name: str,
    source_file_name: str,
) -> Optional[str | None]:
    """Find the path to the file

    Args:
        target_file_name (str): The name of the target file.
        source_file_name (Optional[str  |  None], optional): name of the file you are using this function in. Defaults to None.

    Raises:
        ValueError: Source file name is not specified
        ValueError: File `target_file_name` exists in multiple directories
        ValueError: File `target_file_name` not found

    Returns:
        Optional[str | None]: The path to the file or None if not found
    """
    if not source_file_name:
        raise ValueError("Source file name is not specified")

    source_file_path: PosixPath = Path(source_file_name)

    # Check in the same directory, parent directory, and grandparent directory
    for directory in [
        source_file_path.parent,
        source_file_path.parent.parent,
        source_file_path.parent.parent.parent,
    ]:
        if directory.joinpath(target_file_name).exists():
            return str(directory.joinpath(target_file_name))

    else:
        raise ValueError(f"File {target_file_name} not found")


def load_secrets_from_file(
    target_file_name: str,
    source_file_name: Optional[str | None] = None,
) -> None:
    """Load secrets from .env file

    Args:
        target_file_name (str): The name of the target file.
        source_file_name (Optional[str  |  None]): name of the file you are using this function in. Defaults to None.

    Raises:
        ValueError: File name must end with .env
        ValueError: File `target_file_name` not found
    """
    if not target_file_name.endswith(".env"):
        raise ValueError("File name must end with .env")
    dotenv_path: Optional[str | None] = find_file_path(
        target_file_name, source_file_name
    )
    if not dotenv_path:
        raise ValueError(f"File {target_file_name} not found")
    load_dotenv(dotenv_path)


def get_secret(secret_name: str) -> str:
    """Get secret from environment

    Args:
        secret_name (str): The name of the secret.

    Raises:
        ValueError: Secret `secret_name` not found

    Returns:
        str: The value of the secret
    """
    secret_value: Optional[str | None] = os.environ.get(secret_name, None)
    if not secret_value:
        raise ValueError(f"Secret {secret_name} not found")
    return secret_value


def configure_logger(name: str, logging_level: str) -> logging:
    """Create logger

    Args:
        name (str): The name of the file you are using this function in.
            Pass __name__ to get the name of the file you are using this function in.
        logging_level (str): The level of the logger.

    Raises:
        ValueError: Invalid logging level

    Returns:
        logger (Logger): The logger
    """
    logging_level: str = logging_level.upper()
    if logging_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError("Invalid logging level")
    if logging_level == "DEBUG":
        logging_level = logging.DEBUG
    elif logging_level == "INFO":
        logging_level = logging.INFO
    elif logging_level == "WARNING":
        logging_level = logging.WARNING
    elif logging_level == "ERROR":
        logging_level = logging.ERROR
    elif logging_level == "CRITICAL":
        logging_level = logging.CRITICAL

    logger: Logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    console_handler: StreamHandler = StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)

    return logger
