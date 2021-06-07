# dataclient_test.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dataclient tests"""

import unittest
from copy import copy, deepcopy

from .. import dataclient


class DataNotify(unittest.TestCase):

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


class _DataAccess(unittest.TestCase):

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


class DataClient(unittest.TestCase):

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


class DataLookup(unittest.TestCase):

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


class DataSource(unittest.TestCase):

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


def suite__dn():
    return unittest.TestLoader().loadTestsFromTestCase(DataNotify)


def suite___da():
    return unittest.TestLoader().loadTestsFromTestCase(_DataAccess)


def suite__dc():
    return unittest.TestLoader().loadTestsFromTestCase(DataClient)


def suite__dl():
    return unittest.TestLoader().loadTestsFromTestCase(DataLookup)


def suite__ds():
    return unittest.TestLoader().loadTestsFromTestCase(DataSource)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite__dn())
    unittest.TextTestRunner(verbosity=2).run(suite___da())
    unittest.TextTestRunner(verbosity=2).run(suite__dc())
    unittest.TextTestRunner(verbosity=2).run(suite__dl())
    unittest.TextTestRunner(verbosity=2).run(suite__ds())
