"""Test utils functions"""

import unittest
import os
from typing import List
from ..utils import find_file_path, load_secrets_from_file, get_secret


class TestUtils(unittest.TestCase):
    """Test utils functions"""

    def tearDown(self):
        """Clean up environment variables"""
        file_path: str = find_file_path("creds.env", __file__)

        with open(file_path, "r", encoding="utf-8") as creds_file:
            secrets_values: str = creds_file.read()
            secrets_values_list: List[str] = secrets_values.split("\n")

        for secret_pair in secrets_values_list:
            if secret_pair.startswith("#"):
                continue
            split_secret: List[str] = secret_pair.split("=")
            if os.environ.get(split_secret[0], None):
                os.environ.pop(split_secret[0])

    def test_find_file_path(self):
        """Test find_file_path function"""
        file_path = find_file_path("creds.env", __file__)
        self.assertIsInstance(file_path, str)
        self.assertIn("creds.env", file_path)
        self.assertEqual(find_file_path("creds.env", __file__, 1), None)

    def test_load_secrets_from_file(self):
        """Test load_secrets_from_file function"""
        source_file_name = __file__
        test_cases = [
            ("creds.env", source_file_name, 1, "Failed dir_level 1"),
            ("creds.env", source_file_name, 2, "Failed dir_level 2"),
            ("creds.env", None, 2, "Failed dir_level 2"),
            ("creds.env", source_file_name, 3, "Success dir_level 3"),
            ("creds.text", source_file_name, None, "Failed not .env file"),
        ]
        for test_case in test_cases:
            target_file_name = test_case[0]
            source_file_passed = test_case[1]
            dir_level = test_case[2]
            test_name = test_case[3]
            with unittest.TestCase.subTest(self, msg=test_name):
                if "Failed" in test_name:
                    self.assertRaises(
                        ValueError,
                        load_secrets_from_file,
                        target_file_name,
                        source_file_passed,
                        dir_level,
                    )
                if "Success" in test_name:
                    self.assertFalse(os.environ.get("PGADMIN_USERNAME"))
                    load_secrets_from_file(
                        target_file_name,
                        source_file_passed,
                        dir_level,
                    )
                    self.assertTrue(os.environ.get("PGADMIN_USERNAME"))

    def test_get_secret(self):
        """Test get_secret function"""
        load_secrets_from_file("creds.env", __file__)
        test_cases = [
            ("PGADMIN_USERNAME", "Success PGADMIN_USERNAME"),
            ("DOES_NOT_EXIST", "Failed DOES_NOT_EXIST"),
        ]
        for test_case in test_cases:
            secret_name = test_case[0]
            test_name = test_case[1]
            with unittest.TestCase.subTest(self, msg=test_name):
                if "Failed" in test_name:
                    self.assertRaises(ValueError, get_secret, secret_name)
                if "Success" in test_name:
                    self.assertEqual(get_secret(secret_name), "huaccho@email.com")
