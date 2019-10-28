import logging
import sys
import unittest

sys.path.append(".")
sys.path.append("..")

import jim.logger


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.server = logging.getLogger("messenger.server")

    def test_server(self):
        timed_fh, stream_fh = self.server.handlers
        self.assertIsInstance(
            timed_fh, logging.handlers.TimedRotatingFileHandler
        )
        self.assertEqual(timed_fh.level, logging.DEBUG)

        self.assertIsInstance(stream_fh, logging.StreamHandler)
        self.assertEqual(stream_fh.level, logging.ERROR)


if __name__ == "__main__":
    unittest.main()
