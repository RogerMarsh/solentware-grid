# test_datashow.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datashow tests"""

import unittest
import tkinter

from .. import datashow


class ModuleConstants(unittest.TestCase):
    def test_001_constants_001(self):
        self.assertEqual(
            sorted(k for k in dir(datashow) if k.isupper()),
            [
                "MINIMUM_HEIGHT",
                "MINIMUM_WIDTH",
            ],
        )
        self.assertEqual(datashow.MINIMUM_HEIGHT, 200)
        self.assertEqual(datashow.MINIMUM_WIDTH, 600)


class _DataClient(unittest.TestCase):
    def setUp(self):
        class Instance:
            def delete_record(*a):
                pass

        self.parent = tkinter.Tk()

        class Oldview:

            top_widget = tkinter.Frame(master=self.parent)
            takefocus_widget = top_widget

            def get_top_widget(self):
                return self.top_widget

        class Dbhome:
            def exists(self, dbset, dbname):
                if dbset == "dbset" and dbname == "dbname":
                    return True
                return False

            is_primary = exists
            is_recno = exists

            def start_transaction(self):
                pass

            def commit(self):
                pass

            def get_table_connection(self, dbset):
                if dbset == "dbset":
                    return True
                return None

        class Datasource:
            dbhome = None
            dbset = None

            def refresh_widgets(*a):
                pass

        self.Dbhome = Dbhome
        self.dbhome = self.Dbhome()
        self.Datasource = Datasource
        self.datasource = self.Datasource()
        self.datasource.dbhome = self.dbhome
        self.Instance = Instance
        self.instance = self.Instance()
        self.Oldview = Oldview
        self.oldview = self.Oldview()

    def tearDown(self):
        self.parent.destroy()


class RecordShow(_DataClient):
    def setUp(self):
        super().setUp()
        self.recorddelete = datashow.RecordShow(self.instance)
        self.recorddelete.datasource = self.datasource

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'instance'",
                )
            ),
            datashow.RecordShow,
        )

    def test_002_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_data_change\(\) missing 1 required positional ",
                    "argument: 'instance'",
                )
            ),
            self.recorddelete.on_data_change,
        )

    def test_002_on_data_change_002(self):
        self.assertEqual(self.recorddelete.blockchange, False)
        self.assertEqual(self.recorddelete.on_data_change(None), None)
        self.assertEqual(self.recorddelete.blockchange, False)

    def test_002_on_data_change_003(self):
        self.assertEqual(self.recorddelete.blockchange, False)
        self.assertEqual(self.recorddelete.on_data_change(self.instance), None)
        self.assertEqual(self.recorddelete.blockchange, True)


class DataShow(_DataClient):
    def setUp(self):
        super().setUp()

        class _DataShow(datashow.DataShow):
            def try_command(self, method, buttons):
                return method

            def try_event(self, method):
                return method

        self.datashow = _DataShow(
            self.instance, self.parent, self.oldview, "title"
        )

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 4 required positional arguments: ",
                    "'instance', 'parent', 'oldview', and 'title'",
                )
            ),
            datashow.DataShow,
        )

    def test_002_dialog_clear_error_markers_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_clear_error_markers\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datashow.dialog_clear_error_markers,
            *(None,),
        )

    def test_002_dialog_clear_error_markers_002(self):
        self.assertEqual(self.datashow.dialog_clear_error_markers(), None)

    def test_003_dialog_status_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_status\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datashow.dialog_status,
            *(None,),
        )

    def test_003_dialog_status_002(self):
        self.assertIs(self.datashow.dialog_status(), self.datashow.status)

    def test_004_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_data_change\(\) missing 1 required positional ",
                    "argument: 'instance'",
                )
            ),
            self.datashow.on_data_change,
        )

    def test_004_on_data_change_002(self):
        self.assertEqual(self.datashow.blockchange, False)
        self.assertIsInstance(self.datashow.ok, tkinter.Button)
        self.assertIs(self.datashow.on_data_change(self.instance), None)
        self.assertEqual(self.datashow.blockchange, True)
        self.assertEqual(self.datashow.ok, None)

    def test_004_on_data_change_003(self):
        self.assertEqual(self.datashow.blockchange, False)
        self.assertIsInstance(self.datashow.ok, tkinter.Button)
        self.assertIs(self.datashow.on_data_change(None), None)
        self.assertEqual(self.datashow.blockchange, False)
        self.assertIsInstance(self.datashow.ok, tkinter.Button)

    def test_005_dialog_ok_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_ok\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datashow.dialog_ok,
            *(None,),
        )

    def test_005_dialog_ok_002(self):
        self.assertEqual(self.datashow.datasource, None)
        self.assertIs(self.datashow.dialog_ok(), None)

    def test_005_dialog_ok_003(self):
        self.datashow.datasource = self.datasource
        self.assertEqual(self.datasource.dbset, None)
        self.assertIs(self.datashow.dialog_ok(), False)

    def test_005_dialog_ok_004(self):
        self.datashow.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.assertIs(self.datashow.dialog_ok(), True)

    # See DataDeleteOverridetearDown for other tests of dialog_on_ok.
    def test_006_dialog_on_ok_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_on_ok\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datashow.dialog_on_ok,
            *(None,),
        )

    # See DataDeleteOverridetearDown for other tests of ok_by_keypress_binding.
    def test_007_ok_by_keypress_binding_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"ok_by_keypress_binding\(\) takes from 1 to 2 ",
                    "positional arguments but 3 were given",
                )
            ),
            self.datashow.ok_by_keypress_binding,
            *(None, None),
        )

    def test_008_bind_buttons_to_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_buttons_to_widget\(\) takes 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.datashow.bind_buttons_to_widget,
            *(None, None),
        )

    def test_008_bind_buttons_to_widget_002(self):
        self.assertIs(
            self.datashow.bind_buttons_to_widget(tkinter.Text()), None
        )

    def test_009_on_destroy_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_destroy\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.datashow.on_destroy,
            *(None, None),
        )

    def test_009_on_destroy_002(self):
        class Event:
            widget = None

        self.assertEqual(self.datashow.on_destroy(event=Event()), None)

    def test_009_on_destroy_003(self):
        class Event:
            widget = self.datashow.parent

        self.assertEqual(self.datashow.on_destroy(event=Event()), None)

    def test_010_tidy_on_destroy_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"tidy_on_destroy\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datashow.tidy_on_destroy,
            *(None,),
        )

    def test_010_tidy_on_destroy_002(self):
        self.assertEqual(self.datashow.tidy_on_destroy(), None)


# Unittests do tkinter destroy() so override tearDown().
class DataDeleteOverridetearDown(_DataClient):
    def setUp(self):
        super().setUp()

        class _DataShow(datashow.DataShow):
            def try_command(self, method, buttons):
                return method

        self.datashow = _DataShow(
            self.instance, self.parent, self.oldview, "title"
        )

    def tearDown(self):
        pass

    def test_006_dialog_on_ok_002(self):
        self.datashow.blockchange = True
        self.assertIs(self.datashow.dialog_on_ok(), None)

    def test_006_dialog_on_ok_003(self):
        self.assertEqual(self.datashow.blockchange, False)
        self.assertEqual(self.datashow.datasource, None)
        self.assertIs(self.datashow.dialog_on_ok(), None)

    def test_006_dialog_on_ok_004(self):
        self.assertEqual(self.datashow.blockchange, False)
        self.datashow.datasource = self.datasource
        self.assertIs(self.datashow.dialog_on_ok(), None)

    def test_006_dialog_on_ok_005(self):
        self.assertEqual(self.datashow.blockchange, False)
        self.datashow.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.assertIs(self.datashow.dialog_on_ok(), None)

    def test_007_ok_by_keypress_binding_002(self):
        self.assertIs(self.datashow.ok_by_keypress_binding(), None)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(ModuleConstants))
    runner().run(loader(RecordShow))
    runner().run(loader(DataShow))
    runner().run(loader(DataDeleteOverridetearDown))
