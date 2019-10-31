import logging
import sys
import unittest

sys.path.append(".")
sys.path.append("..")

import jim.logger


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.server = logging.getLogger("messenger.server")
        self.client = logging.getLogger("messenger.client")

    def test_server(self):
        timed_fh, stream_fh = self.server.handlers
        self.assertIsInstance(
            timed_fh, logging.handlers.TimedRotatingFileHandler
        )
        self.assertEqual(timed_fh.level, logging.DEBUG)

        self.assertIsInstance(stream_fh, logging.StreamHandler)
        self.assertEqual(stream_fh.level, logging.ERROR)

    def test_client(self):
        file_fh, stream_fh = self.client.handlers
        self.assertIsInstance(file_fh, logging.FileHandler)
        self.assertEqual(file_fh.level, logging.ERROR)

        self.assertIsInstance(stream_fh, logging.StreamHandler)
        self.assertEqual(stream_fh.level, logging.INFO)


if __name__ == "__main__":
    unittest.main()
