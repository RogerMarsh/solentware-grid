# dbdatasource_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dbdatasource tests"""

import unittest
from copy import copy, deepcopy

from .. import dbdatasource


class DBDataSource(unittest.TestCase):

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


def suite__dds():
    return unittest.TestLoader().loadTestsFromTestCase(DBDataSource)


def suite__crs():
    return unittest.TestLoader().loadTestsFromTestCase(CursorRS)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__dds())
    unittest.TextTestRunner(verbosity=2).run(suite__crs())
