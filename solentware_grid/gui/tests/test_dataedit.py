# test_dataedit.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dataedit tests"""

import unittest
import tkinter

from .. import dataedit


class ModuleConstants(unittest.TestCase):
    def test_001_constants_001(self):
        self.assertEqual(
            sorted(k for k in dir(dataedit) if k.isupper()),
            [
                "MINIMUM_HEIGHT",
                "MINIMUM_WIDTH",
            ],
        )
        self.assertEqual(dataedit.MINIMUM_HEIGHT, 300)
        self.assertEqual(dataedit.MINIMUM_WIDTH, 800)


class _DataClient(unittest.TestCase):
    def setUp(self):
        class Key:
            pass

        class Instance:
            key = Key()

            def edit_record(*a):
                pass

            def set_database(*a):
                pass

            def put_record(*a):
                pass

        self.parent = tkinter.Tk()

        class View:

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
            dbname = None

            def refresh_widgets(*a):
                pass

        self.Dbhome = Dbhome
        self.dbhome = self.Dbhome()
        self.Datasource = Datasource
        self.datasource = self.Datasource()
        self.datasource.dbhome = self.dbhome
        self.Instance = Instance
        self.newobject = self.Instance()
        self.oldobject = self.Instance()
        self.View = View
        self.oldview = self.View()
        self.newview = self.View()

    def tearDown(self):
        self.parent.destroy()


class RecordEdit(_DataClient):
    def setUp(self):
        super().setUp()
        self.recordedit = dataedit.RecordEdit(self.newobject, self.oldobject)
        self.recordedit.datasource = self.datasource

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 2 required positional arguments: ",
                    "'newobject' and 'oldobject'",
                )
            ),
            dataedit.RecordEdit,
        )

    def test_002_edit_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit\(\) takes from 1 to 2 positional arguments ",
                    "but 3 were given",
                )
            ),
            self.recordedit.edit,
            *(None, None),
        )

    def test_002_edit_002(self):
        self.assertEqual(self.recordedit.edit(), None)

    def test_002_edit_003(self):
        self.assertEqual(self.recordedit.edit(commit=False), None)

    def test_003_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_data_change\(\) missing 1 required ",
                    "positional argument: 'instance'",
                )
            ),
            self.recordedit.on_data_change,
        )

    def test_003_on_data_change_002(self):
        self.assertEqual(self.recordedit.blockchange, False)
        self.assertEqual(self.recordedit.on_data_change(None), None)
        self.assertEqual(self.recordedit.blockchange, False)

    def test_003_on_data_change_003(self):
        self.assertEqual(self.recordedit.blockchange, False)
        self.assertEqual(self.recordedit.on_data_change(self.oldobject), None)
        self.assertEqual(self.recordedit.blockchange, True)

    def test_004_put_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"put\(\) takes from 1 to 2 positional arguments ",
                    "but 3 were given",
                )
            ),
            self.recordedit.put,
            *(None, None),
        )

    def test_004_put_002(self):
        self.assertEqual(self.recordedit.put(), None)

    def test_004_put_003(self):
        self.assertEqual(self.recordedit.put(commit=False), None)


class DataEdit(_DataClient):
    def setUp(self):
        super().setUp()

        class _DataEdit(dataedit.DataEdit):
            def try_command(self, method, buttons):
                return method

            def try_event(self, method):
                return method

        self._DataEdit = _DataEdit
        self.dataedit = _DataEdit(
            self.newobject,
            self.parent,
            self.oldobject,
            self.newview,
            "title",
            oldview=self.oldview,
        )

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) takes from 1 to 7 positional arguments ",
                    "but 8 were given",
                )
            ),
            dataedit.DataEdit,
            *(None, None, None, None, None, None, None),
        )

    def test_001___init___002(self):
        self.assertEqual(
            isinstance(
                self._DataEdit(
                    self.newobject,
                    self.parent,
                    self.oldobject,
                    self.newview,
                    "title",
                ),
                self._DataEdit,
            ),
            True,
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
            self.dataedit.dialog_clear_error_markers,
            *(None,),
        )

    def test_002_dialog_clear_error_markers_002(self):
        self.assertEqual(self.dataedit.dialog_clear_error_markers(), None)

    # See DataDeleteOverridetearDown for other tests of dialog_on_cancel.
    def test_003_dialog_on_cancel_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_on_cancel\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataedit.dialog_on_cancel,
            *(None,),
        )

    def test_004_dialog_status_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_status\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataedit.dialog_status,
            *(None,),
        )

    def test_004_dialog_status_002(self):
        self.assertIs(self.dataedit.dialog_status(), self.dataedit.status)

    def test_005_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_data_change\(\) missing 1 required positional ",
                    "argument: 'instance'",
                )
            ),
            self.dataedit.on_data_change,
        )

    def test_005_on_data_change_002(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.assertIsInstance(self.dataedit.ok, tkinter.Button)
        self.assertIs(self.dataedit.on_data_change(self.oldobject), None)
        self.assertEqual(self.dataedit.blockchange, True)
        self.assertEqual(self.dataedit.ok, None)

    def test_005_on_data_change_003(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.assertIsInstance(self.dataedit.ok, tkinter.Button)
        self.assertIs(self.dataedit.on_data_change(None), None)
        self.assertEqual(self.dataedit.blockchange, False)
        self.assertIsInstance(self.dataedit.ok, tkinter.Button)

    def test_006_dialog_on_ok_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_on_ok\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataedit.dialog_on_ok,
            *(None,),
        )

    def test_006_dialog_on_ok_002(self):
        self.dataedit.blockchange = True
        self.assertIs(self.dataedit.dialog_on_ok(), None)

    def test_006_dialog_on_ok_003(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.assertEqual(self.dataedit.datasource, None)
        self.assertRaisesRegex(
            AttributeError,
            "'NoneType' object has no attribute 'dbhome'",
            self.dataedit.dialog_on_ok,
        )

    def test_006_dialog_on_ok_004(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.dataedit.datasource = self.datasource
        self.assertIs(self.dataedit.oldview, self.oldview)
        self.assertIs(self.dataedit.dialog_on_ok(), None)

    # See DataDeleteOverridetearDown for other tests of dialog_on_ok.
    def test_006_dialog_on_ok_005(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.dataedit.datasource = self.datasource
        self.dataedit.oldview = None
        self.assertIs(self.dataedit.dialog_on_ok(), None)

    def test_007_dialog_ok_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"dialog_ok\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataedit.dialog_ok,
            *(None,),
        )

    def test_007_dialog_ok_002(self):
        self.assertEqual(self.dataedit.datasource, None)
        self.assertRaisesRegex(
            AttributeError,
            "'NoneType' object has no attribute 'dbhome'",
            self.dataedit.dialog_ok,
        )

    def test_007_dialog_ok_003(self):
        self.dataedit.datasource = self.datasource
        self.assertEqual(self.datasource.dbset, None)
        self.assertIs(self.dataedit.dialog_ok(), False)

    def test_007_dialog_ok_004(self):
        self.dataedit.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.assertEqual(self.dataedit.oldobject is not None, True)
        self.assertNotEqual(self.dataedit.newobject, self.dataedit.oldobject)
        self.assertIs(self.dataedit.dialog_ok(), True)

    def test_007_dialog_ok_005(self):
        self.dataedit.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.assertEqual(self.dataedit.oldobject is not None, True)
        self.dataedit.newobject = self.dataedit.oldobject
        self.assertIs(self.dataedit.dialog_ok(), False)

    def test_007_dialog_ok_006(self):
        self.dataedit.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.dataedit.oldobject = None
        self.assertIs(self.dataedit.dialog_ok(), True)
        self.assertEqual(self.dataedit.newobject.key.recno, None)

    def test_008_ok_by_keypress_binding_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"ok_by_keypress_binding\(\) takes from 1 to 2 ",
                    "positional arguments but 3 were given",
                )
            ),
            self.dataedit.ok_by_keypress_binding,
            *(None, None),
        )

    def test_008_ok_by_keypress_binding_002(self):
        self.dataedit.datasource = self.datasource
        self.assertIs(self.dataedit.ok_by_keypress_binding(), None)

    # See DataDeleteOverridetearDown for other tests of
    # cancel_by_keypress_binding.
    def test_009_cancel_by_keypress_binding_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_by_keypress_binding\(\) takes from 1 to 2 ",
                    "positional arguments but 3 were given",
                )
            ),
            self.dataedit.cancel_by_keypress_binding,
            *(None, None),
        )

    def test_010_bind_buttons_to_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_buttons_to_widget\(\) takes 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.dataedit.bind_buttons_to_widget,
            *(None, None),
        )

    def test_010_bind_buttons_to_widget_002(self):
        self.assertIs(
            self.dataedit.bind_buttons_to_widget(tkinter.Text()), None
        )

    def test_011_on_destroy_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_destroy\(\) takes from 1 to 2 positional ",
                    "arguments but 3 were given",
                )
            ),
            self.dataedit.on_destroy,
            *(None, None),
        )

    def test_011_on_destroy_002(self):
        class Event:
            widget = None

        self.assertEqual(self.dataedit.on_destroy(event=Event()), None)

    def test_011_on_destroy_003(self):
        class Event:
            widget = self.dataedit.parent

        self.assertEqual(self.dataedit.on_destroy(event=Event()), None)

    def test_012_tidy_on_destroy_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"tidy_on_destroy\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.dataedit.tidy_on_destroy,
            *(None,),
        )

    def test_012_tidy_on_destroy_002(self):
        self.assertEqual(self.dataedit.tidy_on_destroy(), None)


# Unittests do tkinter destroy() so override tearDown().
class DataDeleteOverridetearDown(_DataClient):
    def setUp(self):
        super().setUp()

        class _DataEdit(dataedit.DataEdit):
            def try_command(self, method, buttons):
                return method

        self.dataedit = _DataEdit(
            self.newobject, self.parent, self.oldobject, self.newview, "title"
        )

    def tearDown(self):
        pass

    def test_003_dialog_on_cancel_002(self):
        self.assertEqual(self.dataedit.dialog_on_cancel(), None)

    def test_006_dialog_on_ok_006(self):
        self.assertEqual(self.dataedit.blockchange, False)
        self.dataedit.datasource = self.datasource
        self.datasource.dbset = "dbset"
        self.assertIs(self.dataedit.dialog_on_ok(), None)

    def test_009_cancel_by_keypress_binding_002(self):
        self.assertIs(self.dataedit.cancel_by_keypress_binding(), None)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(ModuleConstants))
    runner().run(loader(RecordEdit))
    runner().run(loader(DataEdit))
    runner().run(loader(DataDeleteOverridetearDown))
