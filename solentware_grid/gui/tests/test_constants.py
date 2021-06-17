# test_constants.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""constants tests"""

import unittest

from .. import constants


class Constants(unittest.TestCase):
    def test_001_constants_001(self):
        self.assertEqual(
            sorted(
                k
                for k in dir(constants)
                if not k.startswith("__") and not k.endswith("__")
            ),
            [
                "ALTDOWN",
                "CAPSLOCKDOWN",
                "CONTROLDOWN",
                "NUMLOCKDOWN",
                "SHIFTDOWN",
                "START_MSWINDOWS",
            ],
        )
        self.assertEqual(constants.ALTDOWN, 8)
        self.assertEqual(constants.CAPSLOCKDOWN, 2)
        self.assertEqual(constants.CONTROLDOWN, 4)
        self.assertEqual(constants.NUMLOCKDOWN, 16)
        self.assertEqual(constants.SHIFTDOWN, 1)
        self.assertEqual(constants.START_MSWINDOWS, 64)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Constants))
