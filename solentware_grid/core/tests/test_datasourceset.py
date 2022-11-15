# test_datasourceset.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datasourceset tests"""

import unittest

from .. import datasourceset


class _DataSourceSet(unittest.TestCase):
    def setUp(self):
        class Dbhome:
            def exists(self, dbset, dbname):
                if dbset == "dbset" and dbname == "dbname":
                    return True
                return False

            is_primary = exists
            is_recno = exists

        self.Dbhome = Dbhome
        self.dbhome = self.Dbhome()

    def tearDown(self):
        pass


class DataSourceSet(_DataSourceSet):
    def setUp(self):
        super().setUp()
        self.datasourceset = datasourceset.DataSourceSet(
            dbhome=self.dbhome, dbset="dbset", dbname="dbname"
        )

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes 1 positional argument ",
                    "but 6 were given",
                )
            ),
            datasourceset.DataSourceSet,
            *(None, None, None, None, None),
        )

    def test_002_close_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"close\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datasourceset.close,
            *(None,),
        )

    def test_002_close_002(self):
        self.assertEqual(self.datasourceset.close() is None, True)

    def test_003_get_recordset_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_recordset\(\) missing 1 required positional ",
                    "argument: 'dbname'",
                )
            ),
            self.datasourceset.get_recordset,
        )

    def test_003_get_recordset_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_recordset\(\) takes from 2 to 4 positional ",
                    "arguments but 5 were given",
                )
            ),
            self.datasourceset.get_recordset,
            *(None, None, None, None),
        )

    def test_003_get_recordset_003(self):
        self.assertRaisesRegex(
            datasourceset.DataSourceSetNotImplemented,
            "'get_recordset\(\)' not implemented",
            self.datasourceset.get_recordset,
            *("dbname",),
        )

    def test_003_get_recordset_004(self):
        self.assertRaisesRegex(
            datasourceset.DataSourceSetNotImplemented,
            "'get_recordset\(\)' not implemented",
            self.datasourceset.get_recordset,
            *("dbname",),
            **dict(from_="k"),
        )

    def test_003_get_recordset_005(self):
        self.assertRaisesRegex(
            datasourceset.DataSourceSetNotImplemented,
            "'get_recordset\(\)' not implemented",
            self.datasourceset.get_recordset,
            *("dbname",),
            **dict(key="k"),
        )

    def test_003_get_recordset_006(self):
        self.assertRaisesRegex(
            datasourceset.DataSourceSetNotImplemented,
            "'get_recordset\(\)' not implemented",
            self.datasourceset.get_recordset,
            *("dbname",),
            **dict(from_="k", key="k"),
        )

    def test_004_set_recordsets_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_recordsets\(\) missing 1 required positional ",
                    "argument: 'dbname'",
                )
            ),
            self.datasourceset.set_recordsets,
        )

    def test_004_set_recordsets_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_recordsets\(\) takes from 2 to 6 positional ",
                    "arguments but 7 were given",
                )
            ),
            self.datasourceset.set_recordsets,
            *(None, None, None, None, None, None),
        )

    def test_005__clear_recordsets_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_clear_recordsets\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datasourceset._clear_recordsets,
            *(None,),
        )

    def test_005__clear_recordsets_002(self):
        self.assertEqual(self.datasourceset._clear_recordsets() is None, True)

    def test_006_get_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_cursor\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datasourceset.get_cursor,
            *(None,),
        )

    def test_006_get_cursor_002(self):
        self.assertRaisesRegex(
            datasourceset.DataSourceSetNotImplemented,
            "'get_cursor\(\)' not implemented",
            self.datasourceset.get_cursor,
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DataSourceSet))
