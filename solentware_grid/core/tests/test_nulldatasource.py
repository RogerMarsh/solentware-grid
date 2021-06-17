# test_nulldatasource.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""nulldatasource tests"""

import unittest

from .. import nulldatasource


class _NullDataSource(unittest.TestCase):
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


class NullDataSource(_NullDataSource):
    def setUp(self):
        super().setUp()
        self.nulldatasource = nulldatasource.NullDataSource(
            self.dbhome, "dbset", "dbname"
        )

    def test_001_get_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_cursor\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.nulldatasource.get_cursor,
            *(None,),
        )

    def test_001_get_cursor_002(self):
        self.assertEqual(
            isinstance(
                self.nulldatasource.get_cursor(), nulldatasource.CursorNull
            ),
            True,
        )

    def test_002_set_recordset_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_recordset\(\) missing 1 required positional ",
                    "argument: 'records'",
                )
            ),
            self.nulldatasource.set_recordset,
        )

    def test_002_set_recordset_002(self):
        self.assertEqual(self.nulldatasource.set_recordset(None) is None, True)


class CursorNull(unittest.TestCase):
    def setUp(self):
        self.cursornull = nulldatasource.CursorNull()

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            nulldatasource.CursorNull,
            *(None,),
        )

    def test_002_close_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "close\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.close,
            *(None,),
        )

    def test_002_close_002(self):
        self.assertEqual(self.cursornull.close() is None, True)

    def test_003_count_records_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "count_records\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.count_records,
            *(None,),
        )

    def test_003_count_records_002(self):
        self.assertEqual(self.cursornull.count_records(), 0)

    def test_004_database_cursor_exists_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "database_cursor_exists\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.database_cursor_exists,
            *(None,),
        )

    def test_004_database_cursor_exists_002(self):
        self.assertEqual(self.cursornull.database_cursor_exists(), False)

    def test_005_first_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "first\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.first,
            *(None,),
        )

    def test_005_first_002(self):
        self.assertEqual(self.cursornull.first() is None, True)

    def test_006_get_position_of_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_position_of_record\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.get_position_of_record,
            *(None,),
        )

    def test_006_get_position_of_record_002(self):
        self.assertEqual(self.cursornull.get_position_of_record(), 0)

    def test_007_get_record_at_position_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_record_at_position\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.get_record_at_position,
            *(None,),
        )

    def test_007_get_record_at_position_002(self):
        self.assertEqual(
            self.cursornull.get_record_at_position() is None, True
        )

    def test_008_last_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "last\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.last,
            *(None,),
        )

    def test_008_last_002(self):
        self.assertEqual(self.cursornull.last() is None, True)

    def test_009_set_partial_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_partial_key\(\) missing 1 required positional ",
                    "argument: 'partial'",
                )
            ),
            self.cursornull.set_partial_key,
        )

    def test_009_set_partial_key_002(self):
        self.assertEqual(self.cursornull.set_partial_key(None) is None, True)

    def test_010_nearest_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "nearest\(\) missing 1 required positional ",
                    "argument: 'key'",
                )
            ),
            self.cursornull.nearest,
        )

    def test_010_nearest_002(self):
        self.assertEqual(self.cursornull.nearest(None) is None, True)

    def test_011_next_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "next\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.next,
            *(None,),
        )

    def test_011_next_002(self):
        self.assertEqual(self.cursornull.next() is None, True)

    def test_012_prev_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "prev\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.prev,
            *(None,),
        )

    def test_012_prev_002(self):
        self.assertEqual(self.cursornull.prev() is None, True)

    def test_013_refresh_recordset_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "refresh_recordset\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.cursornull.refresh_recordset,
            *(None,),
        )

    def test_013_refresh_recordset_002(self):
        self.assertEqual(self.cursornull.refresh_recordset() is None, True)

    def test_014_setat_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "setat\(\) missing 1 required positional ",
                    "argument: 'record'",
                )
            ),
            self.cursornull.setat,
        )

    def test_014_setat_002(self):
        self.assertEqual(self.cursornull.setat(None) is None, True)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(NullDataSource))
    runner().run(loader(CursorNull))
