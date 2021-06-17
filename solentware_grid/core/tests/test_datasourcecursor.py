# test_datasourcecursor.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datasourcecursor tests"""

import unittest

from .. import datasourcecursor


class _DataSourceCursor(unittest.TestCase):
    def setUp(self):
        class Dbhome:
            def create_recordset_cursor(*a):
                return Cursor()

            def recordlist_nil(*a):
                return RecordList(dbhome=self.dbhome, dbset="dbset")

            def get_table_connection(*a):
                pass

            def exists(self, dbset, dbname):
                if dbset == "dbset" and dbname == "dbname":
                    return True
                return False

            is_primary = exists
            is_recno = exists

        class _Recordset:
            def __init__(self, dbhome, dbset):
                self.dbhome = dbhome
                self.dbset = dbset
                self.dbidentity = id(dbhome)

            def close(self):
                pass

        class RecordList:
            def __init__(self, dbhome, dbset):
                self.dbhome = dbhome
                self.recordset = _Recordset(dbhome, dbset)

        class Cursor:
            pass

        self.Dbhome = Dbhome
        self.dbhome = self.Dbhome()
        self._Recordset = _Recordset
        self.RecordList = RecordList
        self.Cursor = Cursor

    def tearDown(self):
        pass


class DataSourceCursor(_DataSourceCursor):
    def setUp(self):
        super().setUp()
        self.datasourcecursor = datasourcecursor.DataSourceCursor(
            self.dbhome, "dbset", "dbname"
        )

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) missing 3 required positional arguments: ",
                    "'dbhome', 'dbset', and 'dbname'",
                )
            ),
            datasourcecursor.DataSourceCursor,
        )

    def test_001___init___002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes from 4 to 5 positional arguments ",
                    "but 6 were given",
                )
            ),
            datasourcecursor.DataSourceCursor,
            *(None, None, None, None, None),
        )

    def test_002_get_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_cursor\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datasourcecursor.get_cursor,
            *(None,),
        )

    def test_002_get_cursor_002(self):
        self.assertEqual(bool(self.datasourcecursor.recordset is None), True)
        self.assertEqual(
            isinstance(self.datasourcecursor.get_cursor(), self.Cursor), True
        )

    def test_002_get_cursor_003(self):
        cursor = self.datasourcecursor.get_cursor()
        self.datasourcecursor.recordset = self.RecordList(self.dbhome, "dbset")
        self.assertEqual(isinstance(cursor, self.Cursor), True)

    def test_002_get_cursor_004(self):
        self.datasourcecursor.recordset = self.RecordList(
            self.Dbhome(), "dbset"
        )
        self.assertNotEqual(
            self.datasourcecursor.recordset.recordset.dbidentity,
            self.datasourcecursor.dbidentity,
        )
        self.assertRaisesRegex(
            datasourcecursor.DataSourceCursorError,
            "Recordset and DataSource are for different databases",
            self.datasourcecursor.get_cursor,
        )

    def test_003_set_recordset_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_recordset\(\) missing 1 required positional ",
                    "argument: 'recordset'",
                )
            ),
            self.datasourcecursor.set_recordset,
        )

    def test_003_set_recordset_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_recordset\(\) takes 2 positional arguments ",
                    "but 3 were given",
                )
            ),
            self.datasourcecursor.set_recordset,
            *(None, None),
        )

    def test_003_set_recordset_003(self):
        recordset = self.RecordList(self.Dbhome(), "dbset")
        self.assertEqual(bool(self.datasourcecursor.recordset), False)
        self.assertNotEqual(
            self.datasourcecursor.dbidentity, recordset.recordset.dbidentity
        )
        self.assertRaisesRegex(
            datasourcecursor.DataSourceCursorError,
            "New Recordset and DataSource are for different databases",
            self.datasourcecursor.set_recordset,
            *(recordset,),
        )

    def test_003_set_recordset_004(self):
        recordset = self.RecordList(self.dbhome, "dbset")
        recordset.recordset.dbidentity = self.datasourcecursor.dbidentity
        self.assertEqual(bool(self.datasourcecursor.recordset), False)
        self.assertEqual(
            self.datasourcecursor.set_recordset(recordset) is None, True
        )

    def test_003_set_recordset_005(self):
        dsc = self.datasourcecursor
        recordset = self.RecordList(self.dbhome, "dbset")
        recordset.recordset.dbidentity = dsc.dbidentity
        dsc.recordset = self.RecordList(self.dbhome, "dbset")
        dsc.recordset.dbidentity = dsc.dbidentity
        self.assertEqual(dsc.set_recordset(recordset) is None, True)

    def test_003_set_recordset_006(self):
        dsc = self.datasourcecursor
        recordset = self.RecordList(self.dbhome, "dbset")
        recordset.recordset.dbidentity = dsc.dbidentity
        dsc.recordset = self.RecordList(self.dbhome, "dbset")
        dsc.recordset.dbidentity = None
        self.assertRaisesRegex(
            datasourcecursor.DataSourceCursorError,
            "New and existing Recordsets are for different databases",
            self.datasourcecursor.set_recordset,
            *(recordset,),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DataSourceCursor))
