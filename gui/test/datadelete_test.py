# datadelete_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datadelete tests"""

import unittest
from copy import copy, deepcopy

from .. import datadelete


class RecordDelete(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__raises(self):
        """"""
        pass

    def test__copy(self):
        """"""
        pass

    def test__assumptions(self):
        """"""
        msg = 'Failure of this test invalidates all other tests'


class DataDelete(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__raises(self):
        """"""
        pass

    def test__copy(self):
        """"""
        pass

    def test__assumptions(self):
        """"""
        msg = 'Failure of this test invalidates all other tests'


def suite__rd():
    return unittest.TestLoader().loadTestsFromTestCase(RecordDelete)


def suite__dd():
    return unittest.TestLoader().loadTestsFromTestCase(DataDelete)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__rd())
    unittest.TextTestRunner(verbosity=2).run(suite__dd())
