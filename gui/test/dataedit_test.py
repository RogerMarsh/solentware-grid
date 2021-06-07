# dataedit_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dataedit tests"""

import unittest
from copy import copy, deepcopy

from .. import dataedit


class RecordEdit(unittest.TestCase):

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


class DataEdit(unittest.TestCase):

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


def suite__re():
    return unittest.TestLoader().loadTestsFromTestCase(RecordEdit)


def suite__de():
    return unittest.TestLoader().loadTestsFromTestCase(DataEdit)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__re())
    unittest.TextTestRunner(verbosity=2).run(suite__de())
