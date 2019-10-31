import logging
import sys
import unittest

sys.path.append(".")
sys.path.append("..")

import jim.logger


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.client = logging.getLogger("messenger.client")

    def test_client(self):
        file_fh, stream_fh = self.client.handlers
        self.assertIsInstance(file_fh, logging.FileHandler)
        self.assertEqual(file_fh.level, logging.ERROR)

        self.assertIsInstance(stream_fh, logging.StreamHandler)
        self.assertEqual(stream_fh.level, logging.INFO)


if __name__ == "__main__":
    unittest.main()
