import sys
import unittest

sys.path.append(".")
sys.path.append("..")

from jim.decorators import log


class TestUtils(unittest.TestCase):
    def _testing_function(self):
        return 42

    def test_unchanged(self):
        """
        Our decorator should not change init funcion behaviour.
        """
        self.assertEqual(
            log(self._testing_function)(), self._testing_function()
        )


if __name__ == "__main__":
    unittest.main()
