# datarow_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datarow tests"""

import unittest
from copy import copy, deepcopy

from .. import datarow


class DataHeader(unittest.TestCase):

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


class DataRow(unittest.TestCase):

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


def suite__dh():
    return unittest.TestLoader().loadTestsFromTestCase(DataHeader)


def suite__dr():
    return unittest.TestLoader().loadTestsFromTestCase(DataRow)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__dh())
    unittest.TextTestRunner(verbosity=2).run(suite__dr())
