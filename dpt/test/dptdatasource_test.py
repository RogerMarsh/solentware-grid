# dptdatasource_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dptdatasource tests"""

import unittest
from copy import copy, deepcopy

from .. import dptdatasource


class DPTDataSource(unittest.TestCase):

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


class CursorRS(unittest.TestCase):

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


def suite__dptds():
    return unittest.TestLoader().loadTestsFromTestCase(DPTDataSource)


def suite__crs():
    return unittest.TestLoader().loadTestsFromTestCase(CursorRS)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__dptds())
    unittest.TextTestRunner(verbosity=2).run(suite__crs())
