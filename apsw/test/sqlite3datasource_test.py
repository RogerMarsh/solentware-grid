# sqlite3datasource_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""sqlite3datasource tests"""

import unittest
from copy import copy, deepcopy

from .. import sqlite3datasource


class Sqlite3DataSource(unittest.TestCase):

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


def suite__sds():
    return unittest.TestLoader().loadTestsFromTestCase(Sqlite3DataSource)


def suite__crs():
    return unittest.TestLoader().loadTestsFromTestCase(CursorRS)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__sds())
    unittest.TextTestRunner(verbosity=2).run(suite__crs())
