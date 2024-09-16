"""Utility functions"""

import os
from typing import Optional, List
import logging
from logging import Logger, StreamHandler
from dotenv import load_dotenv


def find_file_path(
    target_file_name: str,
    source_file_name: Optional[str | None] = None,
    dir_level: Optional[int | None] = None,
) -> Optional[str | None]:
    """Find the path to the file

    Args:
        target_file_name (str): The name of the target file.
        source_file_name (Optional[str  |  None], optional): name of the file you are using this function in. Defaults to None.
        dir_level (Optional[int  |  None], optional): Specify the level of the directory you are using this function in. Defaults to None.
            1 = Directory of thr file you are using this function in. Example: dir_1/dir_2/this_dir/file_name
            2 = 2nd level down. Example: dir_1/this_dir/dir_3/file_name
            3 = 3rd level down. Example: this_dir/dir_3/dir_4/file_name

    Raises:
        ValueError: Source file name is not specified
        ValueError: File `target_file_name` exists in multiple directories
        ValueError: File `target_file_name` not found

    Returns:
        Optional[str | None]: The path to the file or None if not found
    """
    if not source_file_name:
        raise ValueError("Source file name is not specified")
    first_dir: str = os.path.dirname(source_file_name)
    second_down_dir: str = os.path.abspath(os.path.join(first_dir, os.pardir))
    third_down_dir: str = os.path.abspath(os.path.join(second_down_dir, os.pardir))

    first_dir_items: List[str] = os.listdir(first_dir)
    second_down_dir_items: List[str] = os.listdir(second_down_dir)
    third_down_dir_items: List[str] = os.listdir(third_down_dir)

    first_dir_file: Optional[str | None] = (
        os.path.join(first_dir, target_file_name)
        if target_file_name in first_dir_items
        else None
    )
    second_down_dir_file: Optional[str | None] = (
        os.path.join(second_down_dir, target_file_name)
        if target_file_name in second_down_dir_items
        else None
    )
    third_down_dir_file: Optional[str | None] = (
        os.path.join(third_down_dir, target_file_name)
        if target_file_name in third_down_dir_items
        else None
    )

    if (
        (first_dir_file and second_down_dir_file)
        or (first_dir_file and third_down_dir_file)
        or (second_down_dir_file and third_down_dir_file)
        and not dir_level
    ):
        raise ValueError(f"File {target_file_name} exists in multiple directories")

    if not first_dir_file and not second_down_dir_file and not third_down_dir_file:
        raise ValueError(f"File {target_file_name} not found")

    if dir_level == 1:
        return first_dir_file
    elif dir_level == 2:
        return second_down_dir_file
    elif dir_level == 3:
        return third_down_dir_file

    if first_dir_file:
        return first_dir_file
    if second_down_dir_file:
        return second_down_dir_file
    if third_down_dir_file:
        return third_down_dir_file


def load_secrets_from_file(
    target_file_name: str,
    source_file_name: Optional[str | None] = None,
    dir_level: Optional[int | None] = None,
) -> None:
    """Load secrets from .env file

    Args:
        target_file_name (str): The name of the target file.
        source_file_name (Optional[str  |  None]): name of the file you are using this function in. Defaults to None.
        dir_level (Optional[int  |  None], optional): Specify the level of the directory you are using this function in. Defaults to None.
            1 = Directory of thr file you are using this function in. Example: dir_1/dir_2/this_dir/file_name
            2 = 2nd level down. Example: dir_1/this_dir/dir_3/file_name
            3 = 3rd level down. Example: this_dir/dir_3/dir_4/file_name

    Raises:
        ValueError: File name must end with .env
        ValueError: File `target_file_name` not found
    """
    if not target_file_name.endswith(".env"):
        raise ValueError("File name must end with .env")
    dotenv_path: Optional[str | None] = find_file_path(
        target_file_name, source_file_name, dir_level
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
