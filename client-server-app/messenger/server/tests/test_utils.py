import logging
import sys
import unittest

sys.path.append(".")
sys.path.append("..")

import jim.utils as utils
import jim.messages as messages
import jim.exceptions as exceptions


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_data = b'{"test_key": "test_value"}'
        self.parse_data = {"test_key": "test_value"}

    def test_json_operation(self):
        self.assertEqual(utils.parse_raw_json(self.raw_data), self.parse_data)
        self.assertEqual(utils.make_raw_json(self.parse_data), self.raw_data)


if __name__ == "__main__":
    unittest.main()
