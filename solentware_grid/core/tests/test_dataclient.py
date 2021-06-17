# test_dataclient.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dataclient tests"""

import unittest

from .. import dataclient


class _DataNotify(unittest.TestCase):
    def setUp(self):
        class Newrow:
            def load_instance(self, *a):
                pass

        class Cursor:
            dce = None

            def close(self):
                pass

            def database_cursor_exists(self):
                return self.dce

            def set_partial_key(self, partial):
                pass

            def setat(self, record):
                return record

            def refresh_recordset(self, instance):
                pass

        class Database:
            def get(self, key):
                d = {"k1": "v1", "k2": "v2"}
                if key in d:
                    return key, d[key]
                return None

        class Datasource:
            def __init__(self):
                self.recno = None
                self.dbhome = None
                self.dbset = None
                self.dbname = None

            def register_in(self, client, callback):
                pass

            def register_out(self, client):
                pass

            def refresh_widgets(self, instance):
                pass

            def get_cursor(self):
                return Cursor()

            def get_database(self):
                return Database()

            def new_row(self):
                return Newrow()

            def new_row_for_database(self):
                return self.new_row()

        self.newrow = Newrow
        self.cursor = Cursor
        self.database = Database
        self.datasource = Datasource

    def tearDown(self):
        pass


class DataNotify(_DataNotify):
    def setUp(self):
        super().setUp()
        self.datanotify = dataclient.DataNotify()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            dataclient.DataNotify,
            *(None,),
        )

    def test_002_get_data_source_001(self):
        self.assertEqual(self.datanotify.get_data_source(), None)

    def test_003_register_in_001(self):
        self.assertEqual(self.datanotify.register_in(None, None), None)

    def test_003_register_in_002(self):
        self.assertEqual(
            self.datanotify.register_in(self.datasource(), None), None
        )

    def test_004_register_out_001(self):
        self.assertEqual(self.datanotify.register_out(None), None)

    def test_004_register_out_002(self):
        self.assertEqual(self.datanotify.register_out(self.datasource()), None)

    def test_005_refresh_widgets_001(self):
        self.assertIs(self.datanotify.datasource, None)
        self.datanotify.refresh_widgets(None)

    def test_006_refresh_widgets_001(self):
        self.datanotify.datasource = self.datasource()
        self.assertIsInstance(self.datanotify.datasource, self.datasource)
        self.datanotify.refresh_widgets(None)

    def test_007_set_data_source_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_data_source\(\) takes from 1 to 3 positional ",
                    "arguments but 4 were given",
                )
            ),
            self.datanotify.set_data_source,
            *(None, None, None),
        )

    def test_007_set_data_source_002(self):
        self.assertEqual(None in self.datanotify._datasources, False)
        self.assertEqual(None, self.datanotify.datasource)
        self.assertIs(
            self.datanotify.set_data_source(source=None, callback=None), None
        )

    def test_007_set_data_source_003(self):
        self.datanotify._datasources[None] = None
        self.assertEqual(None in self.datanotify._datasources, True)
        self.assertEqual(None, self.datanotify.datasource)
        self.assertIs(
            self.datanotify.set_data_source(source=None, callback=None), None
        )

    def test_007_set_data_source_004(self):
        self.datanotify.datasource = "source"
        self.assertEqual(None in self.datanotify._datasources, False)
        self.assertEqual("source", self.datanotify.datasource)
        self.assertIs(
            self.datanotify.set_data_source(source="source", callback=None),
            None,
        )

    def test_007_set_data_source_005(self):
        self.datanotify.datasource = "source"
        self.assertEqual(None in self.datanotify._datasources, False)
        self.assertEqual("source", self.datanotify.datasource)
        self.assertIs(
            self.datanotify.set_data_source(source=None, callback=None), None
        )

    def test_008_set_named_data_sources_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_named_data_sources\(\) missing 1 required ",
                    "positional argument: 'sources'",
                )
            ),
            self.datanotify.set_named_data_sources,
        )

    def test_008_set_named_data_sources_002(self):
        self.assertIs(self.datanotify.set_named_data_sources(None), None)

    def test_008_set_named_data_sources_003(self):
        class Dbhome:
            def exists(self, dbset, dbname):
                if dbset == "dbset" and dbname == "dbname":
                    return True
                return False

            is_primary = exists
            is_recno = exists

        datasource = dataclient.DataSource(Dbhome(), None, None)
        self.datanotify._datasources = {"source1": "callback"}
        sources = {
            None: "callback",
            "source1": datasource,
            "source2": datasource,
            "source3": "callback",
        }
        self.assertIs(self.datanotify.set_named_data_sources(sources), None)
        self.assertEqual(self.datanotify._datasources["source1"], "callback")
        self.assertEqual(
            isinstance(
                self.datanotify._datasources["source2"], dataclient.DataSource
            ),
            True,
        )
        self.assertEqual(len(self.datanotify._datasources), 2)


class _DataAccess(_DataNotify):
    def setUp(self):
        super().setUp()
        self._dataaccess = dataclient._DataAccess()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            dataclient._DataAccess,
            *(None,),
        )

    def test_002_get_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_record\(\) missing 1 required positional ",
                    "argument: 'record'",
                )
            ),
            self._dataaccess.get_record,
        )

    def test_002_get_record_002(self):
        record = ("k", "v")
        self.assertEqual(self._dataaccess.partial, None)
        self.assertEqual(self._dataaccess.get_record(record), record)

    def test_002_get_record_003(self):
        record = ("k", "v")
        self._dataaccess.partial = "k"
        self.assertEqual(self._dataaccess.partial, "k")
        self.assertEqual(self._dataaccess.get_record(record), record)

    def test_002_get_record_004(self):
        record = ("k", "v")
        self._dataaccess.partial = "m"
        self.assertEqual(self._dataaccess.partial, "m")
        self.assertEqual(self._dataaccess.get_record(record), None)

    def test_002_get_record_005(self):
        record = "kve"
        self._dataaccess.partial = "k"
        self.assertEqual(self._dataaccess.partial, "k")
        self.assertEqual(self._dataaccess.get_record(record), None)

    def test_003_set_partial_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_partial_key\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self._dataaccess.set_partial_key,
            *(None, None),
        )

    def test_003_set_partial_key_002(self):
        self.assertEqual(self._dataaccess.set_partial_key(), None)
        self.assertEqual(self._dataaccess.partial, None)

    def test_003_set_partial_key_003(self):
        self.assertEqual(self._dataaccess.set_partial_key(key=False), None)
        self.assertEqual(self._dataaccess.partial, False)

    def test_003_set_partial_key_004(self):
        self.assertEqual(self._dataaccess.set_partial_key(key="key"), None)
        self.assertEqual(self._dataaccess.partial, "key")

    def test_003_set_partial_key_005(self):
        self.assertEqual(self._dataaccess.set_partial_key(key=""), None)
        self.assertEqual(self._dataaccess.partial, None)

    def test_004_get_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_cursor\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self._dataaccess.get_cursor,
            *(None,),
        )

    def test_004_get_cursor_002(self):
        self.assertEqual(self._dataaccess.datasource, None)
        self.assertEqual(self._dataaccess.get_cursor(), None)

    def test_004_get_cursor_003(self):
        self._dataaccess.datasource = self.datasource()
        self.assertIsInstance(self._dataaccess.datasource, self.datasource)
        self.assertIsInstance(self._dataaccess.get_cursor(), self.cursor)

    def test_005_get_database_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "get_database\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self._dataaccess.get_database,
            *(None,),
        )

    def test_005_get_database_002(self):
        self.assertEqual(self._dataaccess.datasource, None)
        self.assertEqual(self._dataaccess.get_database(), None)

    def test_005_get_database_003(self):
        self._dataaccess.datasource = self.datasource()
        self.assertIsInstance(self._dataaccess.datasource, self.datasource)
        self.assertIsInstance(self._dataaccess.get_database(), self.database)

    def test_006_is_recno_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "is_recno\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self._dataaccess.is_recno,
            *(None,),
        )

    def test_006_is_recno_002(self):
        self.assertEqual(self._dataaccess.datasource, None)
        self.assertEqual(self._dataaccess.is_recno(), None)

    def test_006_is_recno_003(self):
        self._dataaccess.datasource = self.datasource()
        self._dataaccess.datasource.recno = True
        self.assertIsInstance(self._dataaccess.datasource, self.datasource)
        self.assertEqual(self._dataaccess.is_recno(), True)

    def test_007_new_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "new_row\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self._dataaccess.new_row,
            *(None,),
        )

    def test_007_new_row_002(self):
        self.assertEqual(self._dataaccess.datasource, None)
        self.assertEqual(self._dataaccess.new_row(), None)

    def test_007_new_row_003(self):
        self._dataaccess.datasource = self.datasource()
        self.assertIsInstance(self._dataaccess.datasource, self.datasource)
        self.assertIsInstance(self._dataaccess.new_row(), self.newrow)

    def test_008_new_row_for_database_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "new_row_for_database\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self._dataaccess.new_row_for_database,
            *(None,),
        )

    def test_008_new_row_for_database_002(self):
        self.assertEqual(self._dataaccess.datasource, None)
        self.assertEqual(self._dataaccess.new_row_for_database(), None)

    def test_008_new_row_for_database_003(self):
        self._dataaccess.datasource = self.datasource()
        self.assertIsInstance(self._dataaccess.datasource, self.datasource)
        self.assertIsInstance(
            self._dataaccess.new_row_for_database(), self.newrow
        )


class DataClient(_DataNotify):
    def setUp(self):
        super().setUp()
        self.dataclient = dataclient.DataClient()

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            dataclient.DataClient,
            *(None,),
        )

    def test_002_clear_client_keys_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "clear_client_keys\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.dataclient.clear_client_keys,
            *(None,),
        )

    def test_002_clear_client_keys_002(self):
        self.assertEqual(self.dataclient.clear_client_keys(), None)

    def test_003_close_client_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "close_client_cursor\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.dataclient.close_client_cursor,
            *(None,),
        )

    def test_003_close_client_cursor_002(self):
        self.assertEqual(self.dataclient.cursor, None)
        self.assertEqual(self.dataclient.close_client_cursor(), None)
        self.assertEqual(self.dataclient.cursor, None)

    def test_003_close_client_cursor_003(self):
        self.dataclient.cursor = self.cursor()
        self.assertEqual(self.dataclient.close_client_cursor(), None)
        self.assertEqual(self.dataclient.cursor, None)

    def test_004_make_client_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "make_client_cursor\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.dataclient.make_client_cursor,
            *(None, None),
        )

    def test_004_make_client_cursor_002(self):
        self.dataclient.datasource = self.datasource()
        self.assertEqual(bool(self.dataclient.cursor), False)
        self.assertEqual(self.dataclient.make_client_cursor(), None)

    def test_004_make_client_cursor_003(self):
        self.dataclient.datasource = self.datasource()
        self.dataclient.cursor = self.cursor()
        self.assertEqual(bool(self.dataclient.cursor), True)
        self.assertEqual(
            bool(self.dataclient.cursor.database_cursor_exists()), False
        )
        self.assertEqual(self.dataclient.make_client_cursor(), None)

    def test_004_make_client_cursor_004(self):
        self.dataclient.datasource = self.datasource()
        self.dataclient.cursor = self.cursor()
        self.dataclient.cursor.dce = True
        self.assertEqual(bool(self.dataclient.cursor), True)
        self.assertEqual(
            bool(self.dataclient.cursor.database_cursor_exists()), True
        )
        self.assertEqual(self.dataclient.make_client_cursor(), None)

    def test_004_make_client_cursor_005(self):
        record = ("k", "v")
        self.dataclient.datasource = self.datasource()
        self.assertEqual(bool(self.dataclient.cursor), False)
        self.assertEqual(
            self.dataclient.make_client_cursor(record=record), record
        )

    def test_004_make_client_cursor_006(self):
        record = ("k", "v")
        self.dataclient.datasource = self.datasource()
        self.dataclient.cursor = self.cursor()
        self.assertEqual(bool(self.dataclient.cursor), True)
        self.assertEqual(
            bool(self.dataclient.cursor.database_cursor_exists()), False
        )
        self.assertEqual(
            self.dataclient.make_client_cursor(record=record), record
        )

    def test_004_make_client_cursor_007(self):
        record = ("k", "v")
        self.dataclient.datasource = self.datasource()
        self.dataclient.cursor = self.cursor()
        self.dataclient.cursor.dce = True
        self.assertEqual(bool(self.dataclient.cursor), True)
        self.assertEqual(
            bool(self.dataclient.cursor.database_cursor_exists()), True
        )
        self.assertEqual(
            self.dataclient.make_client_cursor(record=record), record
        )

    def test_005_load_object_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "load_object\(\) missing 1 required positional ",
                    "argument: 'key'",
                )
            ),
            self.dataclient.load_object,
        )

    def test_005_load_object_002(self):
        self.dataclient.datasource = self.datasource()
        self.assertEqual(self.dataclient.load_object("key"), None)

    def test_006_refresh_cursor_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "refresh_cursor\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.dataclient.refresh_cursor,
            *(None, None),
        )

    def test_006_refresh_cursor_002(self):
        self.assertEqual(self.dataclient.cursor, None)
        self.assertEqual(self.dataclient.refresh_cursor(), None)

    def test_006_refresh_cursor_003(self):
        self.dataclient.cursor = self.cursor()
        self.assertEqual(self.dataclient.refresh_cursor(), None)

    def test_007_set_partial_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_partial_key\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.dataclient.set_partial_key,
            *(None, None),
        )

    def test_007_set_partial_key_002(self):
        self.assertEqual(self.dataclient.cursor, None)
        self.assertEqual(self.dataclient.set_partial_key(), None)

    def test_007_set_partial_key_003(self):
        self.dataclient.cursor = self.cursor()
        self.assertEqual(self.dataclient.set_partial_key(), None)


class DataLookup(_DataNotify):
    def setUp(self):
        super().setUp()
        self.datalookup = dataclient.DataLookup()

    def test_001___init__(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            dataclient.DataLookup,
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
            self.datalookup.close,
            *(None,),
        )

    def test_002_close_002(self):
        self.assertEqual(self.datalookup.close(), None)

    def test_003_load_cache_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "load_cache\(\) missing 1 required positional ",
                    "argument: 'key'",
                )
            ),
            self.datalookup.load_cache,
        )

    def test_003_load_cache_002(self):
        self.datalookup.cache["key"] = self.newrow()
        self.assertIsInstance(self.datalookup.load_cache("key"), self.newrow)

    def test_003_load_cache_003(self):
        self.datalookup.datasource = self.datasource()
        self.assertEqual(len(self.datalookup.cache), 0)
        self.assertIsInstance(self.datalookup.load_cache("k1"), self.newrow)
        self.assertEqual(len(self.datalookup.cache), 1)

    def test_003_load_cache_004(self):
        self.datalookup.datasource = self.datasource()
        self.assertEqual(len(self.datalookup.cache), 0)
        self.assertEqual(self.datalookup.load_cache("key"), None)
        self.assertEqual(len(self.datalookup.cache), 0)

    def test_003_load_cache_005(self):
        self.datalookup.datasource = self.datasource()
        self.assertEqual(len(self.datalookup.cache), 0)
        self.assertEqual(self.datalookup.rowmax, 100)
        self.assertEqual(self.datalookup.rowmin, 10)
        for i in range(self.datalookup.rowmax + 2):
            self.datalookup.cache[i] = i
            self.datalookup.keys.append(i)
        self.assertEqual(
            bool(len(self.datalookup.keys) > self.datalookup.rowmax), True
        )
        self.assertEqual(len(self.datalookup.keys), len(self.datalookup.cache))
        self.assertIsInstance(self.datalookup.load_cache("k1"), self.newrow)
        self.assertEqual(len(self.datalookup.cache), self.datalookup.rowmin)
        self.assertEqual(len(self.datalookup.keys), len(self.datalookup.cache))
        self.assertEqual(len(self.datalookup.keys), self.datalookup.rowmin)
        self.assertEqual(bool("k1" in self.datalookup.cache), True)
        self.assertEqual(self.datalookup.keys[-1], "k1")

    def test_004_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "on_data_change\(\) missing 1 required positional ",
                    "argument: 'instance'",
                )
            ),
            self.datalookup.on_data_change,
        )

    def test_004_on_data_change_002(self):
        self.assertRaisesRegex(
            RuntimeError,
            "Not implemented",
            self.datalookup.on_data_change,
            *("k"),
        )


class DataSource(unittest.TestCase):
    def setUp(self):
        class Dbhome:
            def database_cursor(*a):
                pass

            def get_table_connection(*a):
                pass

            def exists(self, dbset, dbname):
                if dbset == "dbset" and dbname == "dbname":
                    return True
                return False

            is_primary = exists
            is_recno = exists

        class Newrow:
            def set_database(*a):
                pass

        self.dbhome = Dbhome
        self.newrow = Newrow
        self.datasource = dataclient.DataSource(
            Dbhome(), "dbset", "dbname", newrow=Newrow
        )

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__init__\(\) missing 3 required positional arguments: ",
                    "'dbhome', 'dbset', and 'dbname'",
                )
            ),
            dataclient.DataSource,
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
            dataclient.DataSource,
            *(None, None, None, None, None),
        )

    def test_002_get_cursor_001(self):
        self.assertEqual(self.datasource.get_cursor(), None)

    def test_003_get_database_001(self):
        self.assertEqual(self.datasource.get_database(), None)

    def test_004_new_row_001(self):
        self.assertIsInstance(self.datasource.new_row(), self.newrow)

    def test_004_new_row_002(self):
        newrow = self.datasource.new_row_for_database()
        self.assertIsInstance(newrow, self.newrow)
        self.assertEqual(newrow.dbname, "dbname")

    def test_005_register_in_001(self):
        self.assertEqual(self.datasource.clients, {})
        self.datasource.register_in("client", "callback")
        self.assertEqual(self.datasource.clients, {})

    def test_005_register_in_002(self):
        def f():
            pass

        self.assertEqual(self.datasource.clients, {})
        self.datasource.register_in("client", f)
        self.assertEqual(self.datasource.clients, {"client": f})

    def test_006_register_out_001(self):
        self.datasource.clients["client"] = "callback"
        self.assertEqual(self.datasource.clients, {"client": "callback"})
        self.datasource.register_out("client")
        self.assertEqual(self.datasource.clients, {})
        self.datasource.register_out("client")
        self.assertEqual(self.datasource.clients, {})

    def test_007_refresh_widgets_001(self):
        def f(a):
            self.assertEqual(a, "instance")

        self.datasource.clients["client"] = f
        self.assertEqual(self.datasource.clients, {"client": f})
        self.datasource.refresh_widgets("instance")

    def test_008_dbidentity_001(self):
        self.assertEqual(self.datasource.dbidentity, id(None))


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DataNotify))
    runner().run(loader(_DataAccess))
    runner().run(loader(DataClient))
    runner().run(loader(DataLookup))
    runner().run(loader(DataSource))
