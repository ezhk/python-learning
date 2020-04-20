#!/usr/bin/env python

import sys
import unittest

sys.path.append(".")
from first import *


class TestFirst(unittest.TestCase):
    def test_multiplication_table(self):
        result = """-  --  --  --  --  --  --  --  --  --
1   2   3   4   5   6   7   8   9  10
2   4   6   8  10  12  14  16  18  20
3   6   9  12  15  18  21  24  27  30
4   8  12  16  20  24  28  32  36  40
5  10  15  20  25  30  35  40  45  50
-  --  --  --  --  --  --  --  --  --"""

        self.assertEqual(multiplication_table(10, 5), result)


if __name__ == "__main__":
    unittest.main()
