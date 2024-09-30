"""Test utils functions"""

import os
import unittest
from typing import List, Optional, Tuple

from ..utils import find_file_path, get_secret, load_secrets_from_file


class TestUtils(unittest.TestCase):
    """Test utils functions"""

    def tearDown(self) -> None:
        """Clean up environment variables"""
        file_path: Optional[str] = find_file_path(
            target_file_name="creds.env",
            source_file_name=__file__,
        )

        if file_path is None:
            return

        with open(file=file_path, mode="r", encoding="utf-8") as creds_file:
            secrets_values: str = creds_file.read()
            secrets_values_list: List[str] = secrets_values.split(sep="\n")

        for secret_pair in secrets_values_list:
            if secret_pair.startswith("#"):
                continue
            split_secret: List[str] = secret_pair.split(sep="=")
            if os.environ.get(split_secret[0], default=None):
                os.environ.pop(split_secret[0])

    def test_find_file_path(self) -> None:
        """Test find_file_path function"""
        file_path: Optional[str] = find_file_path(
            target_file_name="creds.env",
            source_file_name=__file__,
        )
        if file_path is None:
            return

        self.assertIsInstance(obj=file_path, cls=str)
        self.assertIn(member="creds.env", container=file_path)

    def test_load_secrets_from_file(self) -> None:
        """Test load_secrets_from_file function"""
        source_file_name: str = __file__
        test_cases: List[Tuple[str, Optional[str], Optional[int], str]] = [
            ("creds.env", source_file_name, 1, "Failed dir_level 1"),
            ("creds.env", source_file_name, 2, "Failed dir_level 2"),
            ("creds.env", None, 2, "Failed dir_level 2"),
            ("creds.env", source_file_name, 3, "Success dir_level 3"),
            ("creds.text", source_file_name, None, "Failed not .env file"),
        ]
        for test_case in test_cases:
            target_file_name: str = test_case[0]
            source_file_passed: Optional[str] = test_case[1]
            dir_level: Optional[int] = test_case[2]
            test_name: str = test_case[3]
            with unittest.TestCase.subTest(self=self, msg=test_name):
                if "Failed" in test_name:
                    self.assertRaises(
                        ValueError,
                        load_secrets_from_file,
                        target_file_name,
                        source_file_passed,
                        dir_level,
                    )
                if "Success" in test_name and source_file_passed:
                    self.assertFalse(expr=os.environ.get("PGADMIN_USERNAME"))
                    load_secrets_from_file(  # pylint: disable=E1121
                        target_file_name=target_file_name,
                        source_file_name=source_file_passed,
                    )
                    self.assertTrue(expr=os.environ.get("PGADMIN_USERNAME"))

    def test_get_secret(self) -> None:
        """Test get_secret function"""
        load_secrets_from_file(
            target_file_name="creds.env",
            source_file_name=__file__,
        )
        test_cases: List[Tuple[str, str]] = [
            ("PGADMIN_USERNAME", "Success PGADMIN_USERNAME"),
            ("DOES_NOT_EXIST", "Failed DOES_NOT_EXIST"),
        ]
        for test_case in test_cases:
            secret_name: str = test_case[0]
            test_name: str = test_case[1]
            with unittest.TestCase.subTest(self=self, msg=test_name):
                if "Failed" in test_name:
                    self.assertRaises(ValueError, get_secret, secret_name)
                if "Success" in test_name:
                    self.assertEqual(
                        first=get_secret(secret_name=secret_name),
                        second="huaccho@email.com",
                    )
