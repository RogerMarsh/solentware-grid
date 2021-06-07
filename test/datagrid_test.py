# datagrid_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datagrid tests"""

import unittest
from copy import copy, deepcopy

from .. import datagrid


class DataGridBase(unittest.TestCase):

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


class DataGridReadOnly(unittest.TestCase):

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


class DataGrid(unittest.TestCase):

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


def suite__dgb():
    return unittest.TestLoader().loadTestsFromTestCase(DataGridBase)


def suite__dgro():
    return unittest.TestLoader().loadTestsFromTestCase(DataGridReadOnly)


def suite__dg():
    return unittest.TestLoader().loadTestsFromTestCase(DataGrid)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__dgb())
    unittest.TextTestRunner(verbosity=2).run(suite__dgro())
    unittest.TextTestRunner(verbosity=2).run(suite__dg())
