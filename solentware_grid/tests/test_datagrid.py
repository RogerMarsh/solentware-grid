# test_datagrid.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datagrid tests"""

import unittest
import tkinter

from .. import datagrid


class _DataGridBase(unittest.TestCase):
    def setUp(self):
        self.parent = tkinter.Tk()

        class Cursor:
            def set_partial_key(self, partial):
                pass

            def setat(self, record):
                return record

            def next(self):
                return None

            def first(self):
                return None

            def last(self):
                return None

            def prev(self):
                return None

            def get_record_at_position(self, position):
                return None

            def count_records(self):
                return 0

            def get_position_of_record(self, record):
                return 0

            def nearest(self, key):
                return None

            def close(self):
                return None

            # Defining these here may be confusing two levels of cursor.
            def refresh_recordset(self, instance):
                return None

            def database_cursor_exists(self):
                return False

        class Datasource:
            def get_cursor(self):
                return Cursor()

        self.Datasource = Datasource

        def header_maker(*a):
            return []

        self.header_maker = header_maker

        class Datarow:
            def set_background_bookmark(*a):
                pass

            def __call__(*a):
                return ()

            def is_row_under_pointer(*a):
                return True

            def set_background_row_under_pointer(*a):
                pass

            def set_background_normal(*a):
                pass

            def get_keys(*a):
                return []

            def set_background_selection(*a):
                pass

            def set_background_bookmarked_selection(*a):
                pass

            def set_background_selection_cycle(*a):
                pass

            def grid_row_normal(*a, **k):
                pass

            def grid_row_bookmark(*a, **k):
                pass

            def grid_row_selection(*a, **k):
                pass

            def grid_row_selection_cycle(*a, **k):
                pass

            def grid_row_bookmarked_selection(*a, **k):
                pass

            def set_popup_state(*a, **k):
                pass

        self.Datarow = Datarow

        class Widget:
            pass

        self.Widget = Widget

        # Sometimes it is too messy to patch things with detailed dummies.
        # Calls to DataGridBase.fill_view() are often like this: so the
        # patch is self.datagridbase.fill_view = self.null_method in these
        # cases.
        def null_method(*a, **k):
            pass

        self.null_method = null_method

    def tearDown(self):
        self.parent.destroy()


class DataGridBase(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)

    def test_001___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'parent'",
                )
            ),
            datagrid.DataGridBase,
        )

    def test_002_add_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"add_bookmark\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.add_bookmark,
        )

    def test_002_add_bookmark_002(self):
        self.assertEqual(self.datagridbase.bookmarks, [])
        self.datagridbase.bookmarks.append("key")
        self.assertEqual(self.datagridbase.add_bookmark("key"), None)

    def test_002_add_bookmark_003(self):
        self.assertEqual(self.datagridbase.bookmarks, [])
        self.assertEqual("key" not in self.datagridbase.keys, True)
        self.assertEqual("key" not in self.datagridbase.objects, True)
        self.assertEqual("key" not in self.datagridbase.gridrows_for_key, True)
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.add_bookmark("key"), None)

    def test_002_add_bookmark_004(self):
        self.assertEqual(self.datagridbase.bookmarks, [])
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.add_bookmark("key"), None)

    def test_003_add_selection_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"add_selection_bookmark\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.add_selection_bookmark,
            *(None,),
        )

    def test_003_add_selection_bookmark_002(self):
        self.assertEqual(bool(self.datagridbase.selection), False)
        self.assertEqual(self.datagridbase.add_selection_bookmark(), None)

    def test_003_add_selection_bookmark_003(self):
        self.datagridbase.selection.append(("key", None))
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.add_selection_bookmark(), None)

    def test_004__add_record_to_view_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_add_record_to_view\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase._add_record_to_view,
            *(None,),
        )

    def test_004__add_record_to_view_002(self):
        self.assertEqual(self.datagridbase.cursor is not None, False)
        self.assertEqual(self.datagridbase._add_record_to_view(), None)

    def test_005_add_widget_to_spare_pool_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"add_widget_to_spare_pool\(\) missing 1 required ",
                    "positional argument: 'widget'",
                )
            ),
            self.datagridbase.add_widget_to_spare_pool,
        )

    def test_005_add_widget_to_spare_pool_002(self):
        self.assertEqual(self.datagridbase._spare_rows, {})
        self.assertEqual(
            self.datagridbase.add_widget_to_spare_pool(self.Widget()), None
        )
        self.assertEqual(len(self.datagridbase._spare_rows), 1)
        self.assertEqual(len(self.datagridbase._spare_rows[self.Widget]), 1)
        self.assertEqual(
            self.datagridbase.add_widget_to_spare_pool(self.Widget()), None
        )
        self.assertEqual(len(self.datagridbase._spare_rows), 1)
        self.assertEqual(len(self.datagridbase._spare_rows[self.Widget]), 2)

    def test_006_bind_off_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_off\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.bind_off,
            *(None,),
        )

    def test_006_bind_off_002(self):
        self.assertEqual(self.datagridbase.bind_off(), None)

    def test_007_bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_on\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.bind_on,
            *(None,),
        )

    def test_007_bind_on_002(self):
        self.assertEqual(self.datagridbase.bind_on(), None)

    def test_008___bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__bind_on\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.__bind_on,
            *(None,),
        )

    def test_008___bind_on_002(self):
        self.assertEqual(self.datagridbase.__bind_on(), None)

    def test_009_bookmark_down_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bookmark_down\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.bookmark_down,
            *(None,),
        )

    def test_009_bookmark_down_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_003(self):
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    # More '009' tests required.

    def test_010_bookmark_up_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bookmark_up\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.bookmark_up,
            *(None,),
        )

    def test_010_bookmark_up_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_003(self):
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    # More '010' tests required.

    def test_011_cancel_selection_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_selection_bookmark\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.cancel_selection_bookmark,
            *(None,),
        )

    def test_011_cancel_selection_bookmark_002(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.cancel_selection_bookmark(), None)

    def test_011_cancel_selection_bookmark_003(self):
        self.datagridbase.selection.append(("key", None))
        self.assertEqual(self.datagridbase.cancel_selection_bookmark(), None)

    def test_012_cancel_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_bookmark\(\) missing 1 required positional ",
                    "argument: 'key'",
                )
            ),
            self.datagridbase.cancel_bookmark,
        )

    def test_012_cancel_bookmark_002(self):
        self.assertEqual(self.datagridbase.bookmarks, [])
        self.assertEqual("key" not in self.datagridbase.keys, True)
        self.assertEqual("key" not in self.datagridbase.objects, True)
        self.assertEqual("key" not in self.datagridbase.gridrows_for_key, True)
        self.assertEqual(self.datagridbase.cancel_bookmark("key"), None)

    def test_012_cancel_bookmark_003(self):
        self.datagridbase.bookmarks.append("key")
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.cancel_bookmark("key"), None)

    # More '012 cancel_bookmark' tests in DataGridBase_dummy_fill_view.

    def test_013_cancel_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_selection\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.cancel_selection,
            *(None,),
        )

    def test_013_cancel_selection_002(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.cancel_selection(), None)

    def test_013_cancel_selection_003(self):
        self.datagridbase.selection.append(("key", None))
        self.assertEqual(self.datagridbase.cancel_selection(), None)

    def test_014_cancel_visible_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_visible_selection\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.cancel_visible_selection,
        )

    def test_014_cancel_visible_selection_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(
            self.datagridbase.cancel_visible_selection("key"), None
        )

    def test_014_cancel_visible_selection_003(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]
        self.assertEqual(
            self.datagridbase.cancel_visible_selection("key"), None
        )

    def test_015_clear_client_keys_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"clear_client_keys\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.clear_client_keys,
            *(None,),
        )

    def test_015_clear_client_keys_002(self):
        self.assertEqual(self.datagridbase.clear_client_keys(), None)

    def test_016_clear_grid_description_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"clear_grid_description\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.clear_grid_description,
            *(None,),
        )

    def test_016_clear_grid_description_002(self):
        self.assertEqual(self.datagridbase.clear_grid_description(), None)

    def test_017_clear_grid_keys_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"clear_grid_keys\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.clear_grid_keys,
            *(None,),
        )

    def test_017_clear_grid_keys_002(self):
        self.assertEqual(self.datagridbase.clear_grid_keys(), None)

    def test_018_fill_data_grid_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_data_grid\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.fill_data_grid,
            *(None,),
        )

    # More '018 fill_data_grid' tests in DataGridBase_fill_data_grid.

    def test_019_fill_view_001(self):
        self.assertRaisesRegex(
            TypeError,
            r"fill_view\(\) got an unexpected keyword argument 'badkey'",
            self.datagridbase.fill_view,
            **dict(
                currentkey=None,
                down=True,
                topstart=True,
                exclude=True,
                badkey=None,
            ),
        )

    def test_020_fill_view_from_bottom_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_from_bottom\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.fill_view_from_bottom,
            *(None,),
        )

    def test_021_fill_view_from_item_index_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_from_item_index\(\) missing 1 required ",
                    "positional argument: 'index'",
                )
            ),
            self.datagridbase.fill_view_from_item_index,
        )

    def test_022_fill_view_from_position_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_from_position\(\) missing 1 required ",
                    "positional argument: 'position'",
                )
            ),
            self.datagridbase.fill_view_from_position,
        )

    def test_023_fill_view_from_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_from_record\(\) missing 1 required ",
                    "positional argument: 'record'",
                )
            ),
            self.datagridbase.fill_view_from_record,
        )

    def test_024_fill_view_from_top_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_from_top\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.fill_view_from_top,
            *(None,),
        )

    def test_025_fill_view_to_item_index_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_to_item_index\(\) missing 1 required ",
                    "positional argument: 'index'",
                )
            ),
            self.datagridbase.fill_view_to_item_index,
        )

    def test_026_fill_view_to_position_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_to_position\(\) missing 1 required ",
                    "positional argument: 'position'",
                )
            ),
            self.datagridbase.fill_view_to_position,
        )

    def test_027_fill_view_to_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_to_record\(\) missing 1 required ",
                    "positional argument: 'record'",
                )
            ),
            self.datagridbase.fill_view_to_record,
        )

    def test_028_fill_view_to_top_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"fill_view_to_top\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.fill_view_to_top,
            *(None,),
        )

    def test_029_focus_set_frame_001(self):
        self.assertRaisesRegex(
            TypeError,
            r"focus_set_frame\(\) got an unexpected keyword argument 'badkey'",
            self.datagridbase.focus_set_frame,
            **dict(event=None, badkey=None),
        )

    def test_029_focus_set_frame_002(self):
        self.assertEqual(self.datagridbase.focus_set_frame(), None)

    def test_030_focus_set_grid_on_click_child_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"focus_set_grid_on_click_child_widget\(\) missing 1 ",
                    "required positional argument: 'widget'",
                )
            ),
            self.datagridbase.focus_set_grid_on_click_child_widget,
        )

    def test_030_focus_set_grid_on_click_child_widget_002(self):
        self.assertEqual(
            self.datagridbase.focus_set_grid_on_click_child_widget(
                self.datagridbase.frame
            ),
            None,
        )

    def test_031_get_client_item_and_record_counts_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_client_item_and_record_counts\(\) takes ",
                    "1 positional argument but 2 were given",
                )
            ),
            self.datagridbase.get_client_item_and_record_counts,
            *(None,),
        )

    def test_031_get_client_item_and_record_counts_002(self):
        self.datagridbase.datasource = self.Datasource()
        self.assertEqual(
            self.datagridbase.get_client_item_and_record_counts(), (0, 0, 0)
        )

    def test_032_get_client_item_count_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_client_item_count\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_client_item_count,
            *(None,),
        )

    def test_032_get_client_item_count_002(self):
        self.assertEqual(self.datagridbase.get_client_item_count(), 0)

    def test_033_get_row_widgets_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_row_widgets\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.get_row_widgets,
        )

    def test_033_get_row_widgets_002(self):
        def widget_row():
            return ((None, None),)

        self.datagridbase.gridrows_for_key["key"] = widget_row
        self.assertEqual(
            self.datagridbase.get_row_widgets("key"), [None, None]
        )

    def test_034_get_data_canvas_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_data_canvas\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_data_canvas,
            *(None,),
        )

    def test_034_get_data_canvas_002(self):
        self.assertIs(
            self.datagridbase.get_data_canvas(), self.datagridbase.gcanvas
        )

    def test_035_get_data_frame_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_data_frame\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_data_frame,
            *(None,),
        )

    def test_035_get_data_frame_002(self):
        self.assertIs(
            self.datagridbase.get_data_frame(), self.datagridbase.data
        )

    def test_036_get_frame_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_frame\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_frame,
            *(None,),
        )

    def test_036_get_frame_002(self):
        self.assertIs(self.datagridbase.get_frame(), self.datagridbase.frame)

    def test_037_get_horizontal_scrollbar_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_horizontal_scrollbar\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_horizontal_scrollbar,
            *(None,),
        )

    def test_037_get_horizontal_scrollbar_002(self):
        self.assertIs(
            self.datagridbase.get_horizontal_scrollbar(),
            self.datagridbase.hsbar,
        )

    def test_038_get_selected_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_selected_record\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_selected_record,
            *(None,),
        )

    def test_038_get_selected_record_002(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.get_selected_record(), None)

    def test_038_get_selected_record_003(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.get_selected_record(), None)

    def test_038_get_selected_record_004(self):
        self.datagridbase.selection.append("key")
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = "object"
        self.assertEqual(self.datagridbase.get_selected_record(), "object")

    def test_039_get_spare_row_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_spare_row_widget\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.get_spare_row_widget,
            **dict(widget_type=None, badkey=None),
        )

    def test_039_get_spare_row_widget_002(self):
        self.assertEqual(len(self.datagridbase._spare_rows), 0)
        self.assertEqual(self.datagridbase.get_spare_row_widget(), None)

    def test_039_get_spare_row_widget_003(self):
        self.datagridbase._spare_rows[tkinter.Label] = set(("widget",))
        self.assertEqual(self.datagridbase.get_spare_row_widget(), "widget")
        self.assertEqual(len(self.datagridbase._spare_rows[tkinter.Label]), 0)
        self.assertEqual(self.datagridbase.get_spare_row_widget(), None)

    def test_040_get_vertical_scrollbar_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_vertical_scrollbar\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_vertical_scrollbar,
            *(None,),
        )

    def test_040_get_vertical_scrollbar_002(self):
        self.assertIs(
            self.datagridbase.get_vertical_scrollbar(), self.datagridbase.vsbar
        )

    def test_041_get_visible_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_visible_key\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.get_visible_key,
        )

    def test_041_get_visible_key_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.get_visible_key("key"), None)

    def test_041_get_visible_key_003(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.get_visible_key("key"), "key")

    def test_042_get_visible_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_visible_record\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.get_visible_record,
        )

    def test_042_get_visible_record_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.get_visible_record("key"), None)

    def test_042_get_visible_record_003(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = "record"
        self.assertEqual(self.datagridbase.get_visible_record("key"), "record")

    def test_043_get_visible_selected_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_visible_selected_key\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.get_visible_selected_key,
            *(None,),
        )

    def test_043_get_visible_selected_key_002(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.get_visible_selected_key(), None)

    def test_043_get_visible_selected_key_003(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.get_visible_selected_key(), None)

    def test_043_get_visible_selected_key_004(self):
        self.datagridbase.selection.append("key")
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.get_visible_selected_key(), "key")

    def test_044_is_load_direction_down_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"is_load_direction_down\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.is_load_direction_down,
            *(None,),
        )

    def test_044_is_load_direction_down_002(self):
        self.assertEqual(self.datagridbase.is_load_direction_down(), True)

    def test_045_load_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"load_data_change\(\) missing 2 required ",
                    "positional arguments: 'oldkeys' and 'newkeys'",
                )
            ),
            self.datagridbase.load_data_change,
        )

    def test_045_load_data_change_006_newkeys_is_false(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.load_data_change([], False), None)

    # More '045 load_data_change' tests in DataGridBase_dummy_fill_view.

    def test_046_load_new_index_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"load_new_index\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.load_new_index,
            *(None,),
        )

    def test_046_load_new_index_002(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.load_new_index(), None)

    def test_047_load_new_partial_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"load_new_partial_key\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.load_new_partial_key,
        )

    def test_047_load_new_partial_key_002(self):
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.load_new_partial_key("key"), None)

    def test_048_make_header_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"make_header\(\) missing 1 required ",
                    "positional argument: 'specification'",
                )
            ),
            self.datagridbase.make_header,
        )

    def test_048_make_header_002(self):
        self.assertEqual(self.datagridbase.dataheader, None)
        self.assertEqual(self.datagridbase.make_header(None), None)

    def test_048_make_header_003(self):
        class DataHeader:
            def grid_header_row(*a):
                def make_header_widgets():
                    pass

                return make_header_widgets

        self.datagridbase.dataheader = DataHeader
        self.assertEqual(self.datagridbase.make_header(None), None)

    def test_049_make_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"make_row\(\) missing 1 required ",
                    "positional argument: 'record'",
                )
            ),
            self.datagridbase.make_row,
        )

    def test_049_make_row_002(self):
        def row_maker(*a):
            def newrow():
                return [[[self.datagridbase.frame]]]

            return newrow

        mr = self.datagridbase.make_row((row_maker, None, dict()))
        self.assertEqual(mr.__name__, row_maker().__name__)
        self.assertEqual(mr.__class__, row_maker().__class__)

    def test_050_move_slider_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"move_slider\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.move_slider,
            **dict(event=None, badkey=None),
        )

    def test_050_move_slider_002(self):
        self.assertEqual(self.datagridbase.vsbar_number, None)
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_051_encode_navigate_grid_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"encode_navigate_grid_key\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.encode_navigate_grid_key,
        )

    def test_051_encode_navigate_grid_key_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"encode_navigate_grid_key\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.encode_navigate_grid_key,
            **dict(encoding=None, badkey=None),
        )

    def test_051_encode_navigate_grid_key_003(self):
        class Dbhome:
            def encode_record_selector(self, key):
                return key

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.datasource.dbhome = Dbhome()
        self.assertEqual(
            self.datagridbase.encode_navigate_grid_key("key"), "key"
        )

    def test_052_navigate_grid_by_key_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"navigate_grid_by_key\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.navigate_grid_by_key,
            **dict(event=None, badkey=None),
        )

    def test_052_navigate_grid_by_key_002(self):
        self.assertRaisesRegex(
            AttributeError,
            "'NoneType' object has no attribute 'widget'",
            self.datagridbase.navigate_grid_by_key,
        )

    def test_052_navigate_grid_by_key_003(self):
        class Event:
            widget = tkinter.Label()

        self.assertEqual(
            self.datagridbase.navigate_grid_by_key(event=Event()), False
        )

    def test_052_navigate_grid_by_key_004(self):
        class Event:
            widget = tkinter.Entry()

        class Dbhome:
            def encode_record_selector(self, key):
                return key

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.datasource.dbhome = Dbhome()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(
            self.datagridbase.navigate_grid_by_key(event=Event()), True
        )

    def test_053_move_to_row_in_grid_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"move_to_row_in_grid\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.move_to_row_in_grid,
        )

    def test_053_move_to_row_in_grid_002(self):
        class Event:
            widget = tkinter.Entry()

        class Dbhome:
            def encode_record_selector(self, key):
                return key

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.datasource.dbhome = Dbhome()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.move_to_row_in_grid("key"), None)

    def test_054_on_configure_canvas_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_configure_canvas\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.on_configure_canvas,
            **dict(event=None, badkey=None),
        )

    def test_054_on_configure_canvas_001(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.on_configure_canvas(), None)

    def test_055_on_data_change_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"on_data_change\(\) missing 1 required ",
                    "positional argument: 'instance'",
                )
            ),
            self.datagridbase.on_data_change,
        )

    def test_055_on_data_change_002_instance_is_None_no_keys(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.on_data_change(None), None)

    def test_055_on_data_change_004_instance_is_not_None(self):
        class Instance:
            def __init__(self):
                self.newrecord = None

            def get_keys(*a):
                return []

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.on_data_change(Instance()), None)

    def test_055_on_data_change_005_instance_is_not_None(self):
        class Instance:
            def __init__(self):
                self.newrecord = False

            def get_keys(*a):
                return []

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.on_data_change(Instance()), None)

    def test_055_on_data_change_006_instance_is_not_None(self):
        class Instance:
            def __init__(self):
                self.newrecord = object()

            def get_keys(*a):
                return []

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.on_data_change(Instance()), None)

    def test_056_reverse_add_record_direction_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"reverse_add_record_direction\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.reverse_add_record_direction,
            *(None,),
        )

    def test_056_reverse_add_record_direction_002(self):
        self.assertEqual(self.datagridbase.down, True)
        self.assertEqual(self.datagridbase.topkey, None)
        self.assertEqual(
            self.datagridbase.reverse_add_record_direction(), None
        )

    def test_056_reverse_add_record_direction_003(self):
        self.datagridbase.down = False
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.assertEqual(
            self.datagridbase.reverse_add_record_direction(), None
        )

    def test_056_reverse_add_record_direction_003(self):
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.assertEqual(self.datagridbase.down, True)
        self.datagridbase.topkey = "key"
        self.assertEqual(
            self.datagridbase.reverse_add_record_direction(), None
        )

    def test_056_reverse_add_record_direction_004(self):
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.down = False
        self.datagridbase.bottomkey = "key"
        self.assertEqual(
            self.datagridbase.reverse_add_record_direction(), None
        )

    def test_057_scroll_grid_down_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"scroll_grid_down_one_line\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.scroll_grid_down_one_line,
            *(None,),
        )

    def test_057_scroll_grid_down_one_line_002(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.scroll_grid_down_one_line(), None)

    def test_058_scroll_grid_up_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"scroll_grid_up_one_line\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.scroll_grid_up_one_line,
            *(None,),
        )

    def test_058_scroll_grid_up_one_line_002(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.assertEqual(self.datagridbase.scroll_grid_up_one_line(), None)

    def test_059_select_cycle_down_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_cycle_down\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.select_cycle_down,
            *(None,),
        )

    def test_059_select_cycle_down_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.select_cycle_down(), None)

    def test_059_select_cycle_down_003(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.select_cycle_down(), None)

    def test_059_select_cycle_down_004(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.selection.append("sel")
        self.assertEqual(self.datagridbase.select_cycle_down(), None)

    def test_059_select_cycle_down_005(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.select_cycle_down(), None)

    def test_060_select_cycle_up_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_cycle_up\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.select_cycle_up,
            *(None,),
        )

    def test_060_select_cycle_up_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.select_cycle_up(), None)

    def test_060_select_cycle_up_003(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.select_cycle_up(), None)

    def test_060_select_cycle_up_004(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.selection.append("sel")
        self.assertEqual(self.datagridbase.select_cycle_up(), None)

    def test_060_select_cycle_up_005(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.select_cycle_up(), None)

    def test_061_select_down_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_down\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.select_down,
            *(None,),
        )

    def test_061_select_down_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.select_down(), None)

    # More '061 select_down' tests in DataGridBase_select_down_select_up.

    def test_062_select_up_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_up\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.select_up,
            *(None,),
        )

    def test_062_select_up_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.select_up(), None)

    # More '062 select_up' tests in DataGridBase_select_down_select_up.

    def test_063_set_data_header_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_data_header\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.set_data_header,
            **dict(header=None, badkey=None),
        )

    def test_063_on_configure_canvas_001(self):
        self.assertEqual(self.datagridbase.set_data_header(), None)

    def test_064_set_fill_parameters_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_fill_parameters\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.set_fill_parameters,
            **dict(
                currentkey=None,
                down=True,
                topstart=True,
                exclude=True,
                badkey=None,
            ),
        )

    def test_064_set_fill_parameters_002(self):
        def cf(*a):
            return None

        self.assertEqual(self.datagridbase.topkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(currentkey="key"), None
        )

    def test_064_set_fill_parameters_003(self):
        def cf(*a):
            return None

        self.datagridbase.topkey = "key"
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(currentkey="key"), None
        )

    def test_064_set_fill_parameters_004(self):
        def cf(*a):
            return None

        self.assertEqual(self.datagridbase.bottomkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(
                currentkey="key", down=False
            ),
            None,
        )

    def test_064_set_fill_parameters_005(self):
        def cf(*a):
            return None

        self.datagridbase.bottomkey = "key"
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(
                currentkey="key", down=False
            ),
            None,
        )

    def test_064_set_fill_parameters_007(self):
        def cf(*a):
            return "key"

        self.assertEqual(self.datagridbase.topkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(currentkey="key"), None
        )

    def test_064_set_fill_parameters_008(self):
        def cf(*a):
            return "key"

        self.assertEqual(self.datagridbase.topkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(
                currentkey="key", exclude=False
            ),
            None,
        )

    def test_064_set_fill_parameters_008(self):
        def cf(*a):
            return "key"

        self.assertEqual(self.datagridbase.topkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.datagridbase.cursor.setat = cf
        self.assertEqual(
            self.datagridbase.set_fill_parameters(
                currentkey="key", exclude=False, down=False
            ),
            None,
        )

    def test_064_set_fill_parameters_013(self):
        self.assertEqual(self.datagridbase.topkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.assertEqual(self.datagridbase.set_fill_parameters(), None)

    def test_064_set_fill_parameters_014(self):
        self.datagridbase.topkey = "key"
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.assertEqual(self.datagridbase.set_fill_parameters(), None)

    def test_064_set_fill_parameters_015(self):
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.assertEqual(
            self.datagridbase.set_fill_parameters(topstart=False), None
        )

    def test_064_set_fill_parameters_016(self):
        self.datagridbase.bottomkey = "key"
        self.datagridbase.cursor = self.Datasource().get_cursor()
        self.assertEqual(
            self.datagridbase.set_fill_parameters(topstart=False), None
        )

    def test_065_set_grid_properties_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_grid_properties\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.set_grid_properties,
            *(None,),
        )

    def test_065_set_grid_properties_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.set_grid_properties(), None)

    # More '065 set_grid_properties' tests in DataGridBase_set_properties.

    def test_066_set_properties_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_properties\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.set_properties,
        )

    def test_066_set_properties_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_properties\(\) got an unexpected ",
                    "keyword argument 'badkey'",
                )
            ),
            self.datagridbase.set_properties,
            *(None,),
            **dict(dodefaultaction=True, badkey=None),
        )

    def test_066_set_properties_003(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_005(self):
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.datagridbase.keys.append("key")
        self.assertEqual(
            self.datagridbase.set_properties("key", dodefaultaction=False),
            False,
        )

    # More '066 set_properties' tests in DataGridBase_set_properties.

    def test_067_set_row_under_pointer_background_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_row_under_pointer_background\(\) missing ",
                    "1 required positional argument: 'key'",
                )
            ),
            self.datagridbase.set_row_under_pointer_background,
        )

    def test_067_set_row_under_pointer_background_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertRaisesRegex(
            KeyError,
            "'key'",
            self.datagridbase.set_row_under_pointer_background,
            *("key",),
        )

    def test_067_set_row_under_pointer_background_003(self):
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]
        self.assertEqual(
            self.datagridbase.set_row_under_pointer_background("key"), None
        )

    def test_068_set_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_row\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.set_row,
        )

    def test_068_set_row_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_row\(\) got multiple values for ",
                    "argument 'dodefaultaction'",
                )
            ),
            self.datagridbase.set_row,
            *(None, None),
            **dict(extraarg=None, dodefaultaction=True),
        )

    def test_068_set_row_003(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_004(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(
            self.datagridbase.set_row("key", dodefaultaction=False), None
        )

    # More '068 set_row' tests in DataGridBase_set_properties.

    def test_069_set_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_selection\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagridbase.set_selection,
        )

    def test_069_set_selection_002(self):
        def fill_view(*a, **k):
            self.datagridbase.objects["key"] = self.Datarow()

        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.fill_data_grid = fill_view
        self.assertEqual(len(self.datagridbase.objects), 0)
        self.assertEqual(self.datagridbase.set_selection("key"), None)

    def test_070_set_yscrollbar_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_yscrollbar\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.datagridbase.set_yscrollbar,
            *(None,),
        )

    def test_070_set_yscrollbar_002(self):
        self.assertEqual(self.datagridbase.datasource, None)
        self.assertEqual(self.datagridbase.set_yscrollbar(), None)

    def test_070_set_yscrollbar_003(self):
        self.datagridbase.datasource = self.Datasource()
        self.assertEqual(self.datagridbase.set_yscrollbar(), None)

    def test_071_set_xview_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_xview\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.set_xview,
            **dict(scroll=None, number=True, scrollunit=True, badkey=None),
        )

    def test_071_set_xview_002(self):
        self.assertEqual(self.datagridbase.set_xview(), None)

    def test_072_set_yview_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"set_yview\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.set_yview,
            **dict(scroll=None, number=None, scrollunit=None, badkey=None),
        )

    def test_072_set_yview_002(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.set_yview(), None)

    def test_072_set_yview_003(self):
        self.datagridbase.keys.append("keys")
        self.assertEqual(self.datagridbase.set_yview(), None)

    def test_072_set_yview_004(self):
        self.datagridbase.keys.append("keys")
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"int\(\) argument must be a string, a bytes-like object ",
                    "or a number, not 'NoneType'",
                )
            ),
            self.datagridbase.set_yview,
            **dict(scroll="scroll", number=None, scrollunit=None),
        )

    def test_072_set_yview_005(self):
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(scroll="scroll", number=1), None
        )

    def test_072_set_yview_006(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(
                scroll="scroll", number=1, scrollunit="pages"
            ),
            None,
        )

    def test_072_set_yview_007(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(
                scroll="scroll", number=1, scrollunit="units"
            ),
            None,
        )

    def test_072_set_yview_008(self):
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(scroll="scroll", number=-1), None
        )

    def test_072_set_yview_009(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(
                scroll="scroll", number=-1, scrollunit="pages"
            ),
            None,
        )

    def test_072_set_yview_010(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.keys.append("keys")
        self.assertEqual(
            self.datagridbase.set_yview(
                scroll="scroll", number=-1, scrollunit="units"
            ),
            None,
        )

    def test_072_set_yview_011(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(
            self.datagridbase.set_yview(scroll="moveto", number=10), None
        )

    def test_073_select_row_by_click_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_row_by_click\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.select_row_by_click,
            **dict(event=None, badkey=None),
        )

    def test_073_select_row_by_click_002(self):
        self.assertRaisesRegex(
            AttributeError,
            "'NoneType' object has no attribute 'widget'",
            self.datagridbase.select_row_by_click,
        )

    def test_073_select_row_by_click_003(self):
        self.widget = tkinter.Entry()

        def row():
            return [[[self.widget, None]]]

        self.datagridbase.gridrows_for_key["key"] = row

        class Event:
            widget = self.widget

        self.assertEqual(
            self.datagridbase.select_row_by_click(event=Event()), None
        )

    def test_073_show_popup_menu_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_popup_menu\(\) takes 1 positional ",
                    "argument but 2 were given",
                )
            ),
            self.datagridbase.show_popup_menu,
            *(None,),
        )

    def test_073_show_popup_menu_002(self):
        self.assertEqual(self.datagridbase.show_popup_menu(), None)

    def test_074_show_popup_menu_no_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_popup_menu_no_row\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.show_popup_menu_no_row,
            **dict(event=None, badkey=None),
        )

    def test_074_show_popup_menu_no_row_002(self):
        self.assertEqual(self.datagridbase.show_popup_menu_no_row(), None)

    def test_075_show_grid_or_row_popup_menu_at_top_left_by_keypress_001(self):
        dgb = self.datagridbase
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_grid_or_row_popup_menu_at_top_left_by_keypress",
                    r"\(\) got an unexpected keyword argument 'badkey'",
                )
            ),
            dgb.show_grid_or_row_popup_menu_at_top_left_by_keypress,
            **dict(event=None, badkey=None),
        )

    # More '075' tests in DataGridBase_pointerxy.

    def test_076_show_grid_or_row_popup_menu_at_pointer_by_keypress_001(self):
        dgb = self.datagridbase
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_grid_or_row_popup_menu_at_pointer_by_keypress",
                    r"\(\) got an unexpected keyword argument 'badkey'",
                )
            ),
            dgb.show_grid_or_row_popup_menu_at_pointer_by_keypress,
            **dict(event=None, badkey=None),
        )

    # More '076' tests in DataGridBase_pointerxy.

    def test_077_move_selection_to_popup_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"move_selection_to_popup_selection\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagridbase.move_selection_to_popup_selection,
            *(None,),
        )

    def test_077_move_selection_to_popup_selection_002(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.pointer_popup_selection = "key"
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(
            self.datagridbase.move_selection_to_popup_selection(), None
        )

    def test_077_move_selection_to_popup_selection_003(self):
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.pointer_popup_selection = "key"
        self.datagridbase.selection.append("oldkey")
        self.assertEqual(
            self.datagridbase.move_selection_to_popup_selection(), None
        )

    def test_078_exit_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"exit_popup\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.exit_popup,
            **dict(event=None, badkey=None),
        )

    def test_078_exit_popup_002(self):
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.pointer_popup_selection = "key"
        self.assertEqual(self.datagridbase.exit_popup(), None)

    def test_079_enter_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"enter_popup\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridbase.enter_popup,
            **dict(event=None, badkey=None),
        )

    def test_079_enter_popup_002(self):
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.pointer_popup_selection = "key"
        self.assertEqual(self.datagridbase.enter_popup(), None)

    def test_080_get_pointerxy_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"get_pointerxy\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagridbase.get_pointerxy,
            *(None,),
        )

    def test_080_get_pointerxy_002(self):
        pointer_xy = self.datagridbase.get_pointerxy()
        self.assertEqual(isinstance(pointer_xy, tuple), True)
        self.assertEqual(len(pointer_xy), 2)
        self.assertEqual(isinstance(pointer_xy[0], int), True)
        self.assertEqual(isinstance(pointer_xy[1], int), True)

    def test_081__fill_down_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_fill_down\(\) missing 2 required ",
                    "positional arguments: 'rows' and 'cheight'",
                )
            ),
            self.datagridbase._fill_down,
        )

    # More '081 _fill_down' tests in DataGridBase__fill_down__fill_up.

    def test_082__fill_up_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_fill_up\(\) missing 2 required ",
                    "positional arguments: 'rows' and 'cheight'",
                )
            ),
            self.datagridbase._fill_up,
        )

    # More '082 _fill_up' tests in DataGridBase__fill_down__fill_up.

    def test_083__get_row_reqheight_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_get_row_reqheight\(\) missing 1 required ",
                    "positional argument: 'rows'",
                )
            ),
            self.datagridbase._get_row_reqheight,
        )

    def test_083__get_row_reqheight_002(self):
        rows = [[[self.datagridbase.frame]]]
        self.assertEqual(
            isinstance(self.datagridbase._get_row_reqheight(rows), int), True
        )


class DataGridBase_bookmark_down_bookmark_up(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.keys.extend(["key4", "key5", "key6"])
        self.datagridbase.bookmarks.extend(["key3", "key5", "key7"])
        self.datagridbase.objects["key7"] = self.Datarow()
        self.datagridbase.objects["key3"] = self.Datarow()
        self.datagridbase.objects["key5"] = self.Datarow()
        self.datagridbase.fill_view = self.null_method

    def test_009_bookmark_down_004(self):
        self.datagridbase.selection.append("key5")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_005(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_006(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.datagridbase.gridrows_for_key["key5"] = self.datagridbase.objects[
            "key5"
        ]
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_007(self):
        self.datagridbase.selection.append("key7")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_008(self):
        self.datagridbase.keys.append("key7")
        self.datagridbase.selection.append("key7")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_009(self):
        self.datagridbase.selection.append("key8")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_010(self):
        self.datagridbase.keys.insert(0, "key8")
        self.datagridbase.keys.append("key9")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_009_bookmark_down_011(self):
        self.datagridbase.keys.insert(0, "key1")
        self.datagridbase.keys.append("key2")
        self.assertEqual(self.datagridbase.bookmark_down(), None)

    def test_010_bookmark_up_004(self):
        self.datagridbase.selection.append("key5")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_005(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_006(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.datagridbase.gridrows_for_key["key5"] = self.datagridbase.objects[
            "key5"
        ]
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_007(self):
        self.datagridbase.selection.append("key8")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_008(self):
        self.datagridbase.selection.append("key3")
        self.datagridbase.keys.append("key3")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_009(self):
        self.datagridbase.selection.append("key7")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_010(self):
        self.datagridbase.selection.append("key4")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_011(self):
        self.datagridbase.keys.insert(0, "key8")
        self.datagridbase.keys.append("key9")
        self.assertEqual(self.datagridbase.bookmark_up(), None)

    def test_010_bookmark_up_012(self):
        self.datagridbase.keys.insert(0, "key1")
        self.datagridbase.keys.append("key2")
        self.assertEqual(self.datagridbase.bookmark_up(), None)


class DataGridBase__add_record_to_view__cursor_exists(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datasource = self.Datasource()
        self.datagridbase.cursor = self.datasource.get_cursor()

    # Default values of currentkey, startkey, and down, cause
    # _add_record_to_view to do nothing.  Variations on currentkey and
    # down do the same because the dummy cursor operations return None.

    def test_004__add_record_to_view_003(self):
        self.assertEqual(self.datagridbase.currentkey, None)
        self.assertEqual(self.datagridbase.startkey, None)
        self.assertEqual(self.datagridbase.down, True)
        self.assertEqual(self.datagridbase._add_record_to_view(), None)

    def test_004__add_record_to_view_004(self):
        self.datagridbase.down = False
        self.assertEqual(self.datagridbase._add_record_to_view(), None)

    def test_004__add_record_to_view_005(self):
        self.datagridbase.currentkey = False
        self.assertEqual(self.datagridbase._add_record_to_view(), None)

    def test_004__add_record_to_view_006(self):
        self.datagridbase.currentkey = False
        self.datagridbase.down = False
        self.assertEqual(self.datagridbase._add_record_to_view(), None)


class DataGridBase__add_record_to_view__with_startkey(_DataGridBase):
    def setUp(self):
        super().setUp()

        class Datasource(self.Datasource):
            dbhome = None
            dbset = None
            dbname = None

        self.Datasource = Datasource

        class Datarow(self.Datarow):
            def load_instance(*a, **k):
                return None

        self.Datarow = Datarow

        def new_row():
            return self.Datarow()

        self.new_row = new_row

        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datasource = self.Datasource()
        self.datagridbase.cursor = self.datasource.get_cursor()

    # 'bool(startkey) is True' causes _add_record_to_view to attempt to
    # get records when 'currentkey is False'.

    def test_004__add_record_to_view_007(self):
        self.datagridbase.currentkey = False
        self.datagridbase.startkey = ("key", None)
        self.datagridbase.datasource = self.datasource
        self.datasource.new_row = self.new_row
        self.assertEqual(
            self.datagridbase._add_record_to_view(), ("key", None)
        )

    def test_004__add_record_to_view_008(self):
        self.datagridbase.currentkey = False
        self.datagridbase.down = False
        self.datagridbase.startkey = ("key", None)
        self.datagridbase.datasource = self.datasource
        self.datasource.new_row = self.new_row
        self.assertEqual(
            self.datagridbase._add_record_to_view(), ("key", None)
        )


class DataGridBase_on_data_change_instance_is_None(_DataGridBase):
    def setUp(self):
        super().setUp()

        class Datarow(self.Datarow):
            def load_instance(*a, **k):
                return None

        class Datasource(self.Datasource):
            def new_row(self):
                return Datarow()

        self.Datasource = Datasource

        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datasource = self.Datasource()
        self.datagridbase.datasource = self.datasource
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.cursor = self.datasource.get_cursor()
        self.datagridbase.fill_data_grid = self.null_method

    def test_055_on_data_change_003(self):
        self.datagridbase.keys.append(("key", None))
        self.assertEqual(self.datagridbase.on_data_change(None), None)


class DataGridBase_select_down_select_up(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker
        self.datagridbase.fill_data_grid = self.null_method
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.objects["next"] = self.Datarow()
        self.datagridbase.objects["prev"] = self.Datarow()
        self.datagridbase.gridrows_for_key["prev"] = self.datagridbase.objects[
            "prev"
        ]
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]
        self.datagridbase.gridrows_for_key["next"] = self.datagridbase.objects[
            "next"
        ]
        self.datagridbase.keys.extend(("prev", "key", "next"))

    def test_061_select_down_003(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.select_down(), None)

    def test_061_select_down_004(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.select_down(), None)

    def test_061_select_down_005(self):
        self.datagridbase.selection.append("new")
        self.assertEqual(self.datagridbase.select_down(), None)

    def test_061_select_down_006(self):
        self.datagridbase.selection.append("prev")
        self.assertEqual(self.datagridbase.select_down(), None)

    def test_061_select_up_007(self):
        self.datagridbase.selection.append("next")
        self.assertRaisesRegex(
            IndexError,
            "list index out of range",
            self.datagridbase.select_down,
        )

    def test_062_select_up_003(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.select_up(), None)

    def test_062_select_up_004(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.select_up(), None)

    def test_062_select_up_005(self):
        self.datagridbase.selection.append("new")
        self.assertEqual(self.datagridbase.select_up(), None)

    def test_062_select_up_006(self):
        self.datagridbase.selection.append("next")
        self.assertEqual(self.datagridbase.select_up(), None)

    def test_062_select_up_007(self):
        self.datagridbase.selection.append("prev")
        self.assertRaisesRegex(
            IndexError,
            "list index out of range",
            self.datagridbase.select_up,
        )


class DataGridBase_set_properties(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.datagridbase.gridrows_for_key["key"] = self.datagridbase.objects[
            "key"
        ]

    def test_065_set_grid_properties_003(self):
        self.assertEqual(self.datagridbase.set_grid_properties(), None)

    def test_066_set_properties_004(self):
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_006(self):
        self.datagridbase.bookmarks.append("key")
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_007(self):
        self.datagridbase.bookmarks.append("key")
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_008(self):
        self.datagridbase.selection.extend(("key", "secondkey"))
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_009(self):
        self.datagridbase.selection.extend(("key", "key"))
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_066_set_properties_010(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.set_properties("key"), True)

    def test_068_set_row_005(self):
        self.assertEqual(len(self.datagridbase.bookmarks), 0)
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_006(self):
        self.datagridbase.bookmarks.append("key")
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_007(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_008(self):
        self.datagridbase.selection.extend(("key", "other"))
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_009(self):
        self.datagridbase.selection.extend(("key", "key"))
        self.assertEqual(self.datagridbase.set_row("key"), None)

    def test_068_set_row_010(self):
        self.datagridbase.bookmarks.append("key")
        self.datagridbase.selection.append("key")
        self.assertEqual(self.datagridbase.set_row("key"), None)


class DataGridBase_pointerxy(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)

        class Event:
            x_root = 200
            x = 20
            y_root = 100
            y = 10
            widget = tkinter.Frame()

        self.Event = Event

    def test_075_show_grid_or_row_popup_menu_at_top_left_by_keypress_002(self):
        dgb = self.datagridbase
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(
            dgb.show_grid_or_row_popup_menu_at_top_left_by_keypress(
                event=self.Event()
            ),
            "break",
        )

    def test_075_show_grid_or_row_popup_menu_at_top_left_by_keypress_003(self):
        dgb = self.datagridbase
        self.datagridbase.selection.append("key")
        self.datagridbase.gridrows_for_key["key"] = None
        self.assertEqual(
            dgb.show_grid_or_row_popup_menu_at_top_left_by_keypress(
                event=self.Event()
            ),
            "break",
        )

    def test_076_show_grid_or_row_popup_menu_at_pointer_by_keypress_002(self):
        dgb = self.datagridbase
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(
            dgb.show_grid_or_row_popup_menu_at_pointer_by_keypress(
                event=self.Event()
            ),
            "break",
        )

    def test_076_show_grid_or_row_popup_menu_at_pointer_by_keypress_003(self):
        dgb = self.datagridbase
        self.datagridbase.selection.append("key")
        self.datagridbase.gridrows_for_key["key"] = None
        self.assertEqual(
            dgb.show_grid_or_row_popup_menu_at_pointer_by_keypress(
                event=self.Event()
            ),
            "break",
        )


class DataGridBase_dummy_fill_view(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.fill_view = self.null_method

    def test_012_cancel_bookmark_004(self):
        self.datagridbase.bookmarks.append("key")
        self.assertEqual("key" not in self.datagridbase.keys, True)
        self.assertEqual(self.datagridbase.cancel_bookmark("key"), None)

    def test_045_load_data_change_002_newkeys_is_none(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.load_data_change([], None), None)

    def test_045_load_data_change_003_newkeys_is_none(self):
        self.datagridbase.selection.append("key")
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.load_data_change([], None), None)

    def test_045_load_data_change_004_newkeys_is_none(self):
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.datagridbase.keys.append("akey")
        self.assertEqual(self.datagridbase.load_data_change([], None), None)

    def test_045_load_data_change_005_newkeys_is_none(self):
        self.datagridbase.selection.append("key")
        self.datagridbase.keys.append("akey")
        self.assertEqual(self.datagridbase.load_data_change([], None), None)

    def test_045_load_data_change_007_newkeys_is_false(self):
        self.datagridbase.selection.append("key")
        self.datagridbase.objects["oldkey"] = self.Datarow()
        self.assertEqual(
            self.datagridbase.load_data_change(["oldkey"], False), None
        )

    def test_045_load_data_change_008_newkeys_and_oldkeys(self):
        self.datagridbase.objects["newkey"] = self.Datarow()
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(
            self.datagridbase.load_data_change(
                ["oldkey", "okey"], ["newkey", "nkey"]
            ),
            None,
        )

    def test_045_load_data_change_009_newkeys_and_oldkeys(self):
        self.datagridbase.objects["newkey"] = self.Datarow()
        self.assertEqual(len(self.datagridbase.selection), 0)
        self.assertEqual(
            self.datagridbase.load_data_change(
                ["oldkey", "key1"], ["newkey", "key1"]
            ),
            None,
        )

    def test_045_load_data_change_010_newkeys_and_oldkeys(self):
        self.datagridbase.objects["newkey"] = self.Datarow()
        self.datagridbase.selection.append("newkey")
        self.datagridbase.keys.append("key")
        self.assertEqual(
            self.datagridbase.load_data_change(
                ["oldkey", "okey"], ["newkey", "nkey"]
            ),
            None,
        )

    def test_045_load_data_change_011_newkeys_and_oldkeys(self):
        self.datagridbase.objects["newkey"] = self.Datarow()
        self.datagridbase.selection.append("key1")
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key1"] = self.Datarow()
        self.assertEqual(
            self.datagridbase.load_data_change(
                ["oldkey", "key1"], ["newkey", "key1"]
            ),
            None,
        )


class DataGridBase_dummy_fill_data_grid(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.fill_data_grid = self.null_method
        self.datagridbase.datasource = self.Datasource()

    def test_019_fill_view_002(self):
        self.assertEqual(self.datagridbase.fill_view(), None)

    def test_020_fill_view_from_bottom_002(self):
        self.assertEqual(self.datagridbase.fill_view_from_bottom(), None)

    def test_021_fill_view_from_item_index_002(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.fill_view_from_item_index(0), None)

    def test_022_fill_view_from_position_002(self):
        self.assertEqual(self.datagridbase.fill_view_from_position(10), None)

    def test_023_fill_view_from_record_002(self):
        self.assertEqual(
            self.datagridbase.fill_view_from_record(("key", None)), None
        )

    def test_024_fill_view_from_top_002(self):
        self.assertEqual(self.datagridbase.fill_view_from_top(), None)

    def test_025_fill_view_to_item_index_002(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.fill_view_to_item_index(0), None)

    def test_026_fill_view_to_position_002(self):
        self.assertEqual(self.datagridbase.fill_view_to_position(10), None)

    def test_027_fill_view_to_record_002(self):
        self.assertEqual(
            self.datagridbase.fill_view_from_record(("key", None)), None
        )

    def test_028_fill_view_to_top_002(self):
        self.assertEqual(self.datagridbase.fill_view_to_top(), None)


class DataGridBase_fill_data_grid(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)

        def header_maker(*a):
            return [
                [
                    [
                        tkinter.Label(master=self.datagridbase.data),
                        {"sticky": tkinter.NSEW},
                    ]
                ]
            ]

        self.header_maker = header_maker
        self.datagridbase.header_maker = self.header_maker
        tkinter.Text(master=self.datagridbase.data).grid_configure(
            row=4, column=4
        )

        def winfo_height():
            return 100

        self.datagridbase.gcanvas.winfo_height = winfo_height

        def _fill_down(rows, cheight):
            rows.extend(
                [
                    [tkinter.Text(master=self.datagridbase.data)],
                    [tkinter.Text(master=self.datagridbase.data)],
                ]
            )
            return cheight + 50

        self.datagridbase._fill_down = _fill_down

        def _fill_up(rows, cheight):
            rows.extend(
                [
                    [tkinter.Text(master=self.datagridbase.data)],
                    [tkinter.Text(master=self.datagridbase.data)],
                ]
            )
            return cheight + 50

        self.datagridbase._fill_up = _fill_up

        # _fill_down and _fill_up are not perfect emulations of the real
        # methods: populate 'keys', 'objects', and 'gridrows_for_key', with
        # stuff so 'fill_down' ends up with something to remove.
        # The intent is to have something sensible happen with 'cheight'.
        self.datagridbase.keys = ["k1", "k2", "k3", "k4", "k5"]
        self.datagridbase.objects = {k: None for k in self.datagridbase.keys}

        def row_maker():
            return [
                [
                    [
                        tkinter.Text(master=self.datagridbase.data),
                        {"sticky": tkinter.NSEW},
                    ]
                ]
            ]

        self.datagridbase.gridrows_for_key = {
            k: row_maker for k in self.datagridbase.keys
        }

    def test_018_fill_data_grid_002(self):
        self.assertEqual(self.datagridbase.partial, None)
        self.assertEqual(self.datagridbase.down, True)
        self.assertEqual(len(self.datagridbase.keys), 5)
        self.assertEqual(len(self.datagridbase.objects), 5)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 5)
        self.datagridbase.fill_data_grid()
        self.assertEqual(len(self.datagridbase.keys), 4)
        self.assertEqual(len(self.datagridbase.objects), 4)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 4)

    def test_018_fill_data_grid_003(self):
        self.datagridbase.down = False
        self.assertEqual(len(self.datagridbase.keys), 5)
        self.assertEqual(len(self.datagridbase.objects), 5)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 5)
        self.datagridbase.fill_data_grid()
        self.assertEqual(len(self.datagridbase.keys), 4)
        self.assertEqual(len(self.datagridbase.objects), 4)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 4)

    def test_018_fill_data_grid_004(self):
        self.datagridbase.partial = False
        self.assertEqual(len(self.datagridbase.keys), 5)
        self.assertEqual(len(self.datagridbase.objects), 5)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 5)
        self.datagridbase.fill_data_grid()
        self.assertEqual(len(self.datagridbase.keys), 5)
        self.assertEqual(len(self.datagridbase.objects), 5)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 5)

    def test_018_fill_data_grid_005(self):
        self.assertEqual(self.datagridbase.partial, None)
        self.assertEqual(self.datagridbase.down, True)
        self.datagridbase.keys.clear()
        self.datagridbase.objects.clear()
        self.datagridbase.gridrows_for_key.clear()
        self.datagridbase.fill_data_grid()
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(len(self.datagridbase.objects), 0)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 0)

    def test_018_fill_data_grid_006(self):
        self.datagridbase.down = False
        self.datagridbase.keys.clear()
        self.datagridbase.objects.clear()
        self.datagridbase.gridrows_for_key.clear()
        self.datagridbase.fill_data_grid()

        # _fill_down and _fill_up are not perfect emulations of the real
        # methods: hence 0 not 4.
        # The intent is to have something sensible happen with 'cheight'.
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(len(self.datagridbase.objects), 0)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 0)

    def test_018_fill_data_grid_007(self):
        self.datagridbase.partial = False
        self.datagridbase.keys.clear()
        self.datagridbase.objects.clear()
        self.datagridbase.gridrows_for_key.clear()
        self.datagridbase.fill_data_grid()

        # _fill_down and _fill_up are not perfect emulations of the real
        # methods: hence 0 not 4.
        # The intent is to have something sensible happen with 'cheight'.
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(len(self.datagridbase.objects), 0)
        self.assertEqual(len(self.datagridbase.gridrows_for_key), 0)


class DataGridBase__fill_down__fill_up(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)

        def winfo_height():
            return 100

        self.datagridbase.gcanvas.winfo_height = winfo_height

        class Datarow:
            def make_row_widgets(self, widgetpool, parent, items, **kargs):
                row = []
                for item in items:
                    row.append((tkinter.Label(master=parent, text=item), {}))
                self._row_widgets = row
                return self

            def grid_row_normal(self, *a, **k):
                return self.make_row_widgets, ("item1", "item2"), {}

            def __call__(self):
                return (self._row_widgets,)

        self.Datarow = Datarow
        self.rows = [
            [
                [tkinter.Text(), tkinter.Text()],
                [tkinter.Text(), tkinter.Text()],
            ]
        ]

    def test_081_fill_down_001(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.topkey, None)
        self.assertEqual(self.datagridbase._fill_down([], 110), 110)
        self.assertEqual(self.datagridbase.topkey, None)

    def test_081_fill_down_002(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.topkey, None)
        self.assertEqual(self.datagridbase._fill_down([], 110), 110)
        self.assertEqual(self.datagridbase.topkey, "key")

    def test_081_fill_down_003(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.topkey, None)
        self.assertEqual(self.datagridbase._fill_down([], 0), 0)
        self.assertEqual(self.datagridbase.topkey, None)

    def test_081_fill_down_004(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.assertEqual(self.datagridbase.topkey, None)
        self.assertEqual(self.datagridbase._fill_down([], 0), 19)
        self.assertEqual(self.datagridbase.topkey, "key")

    def test_082_fill_up_001(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.assertEqual(self.datagridbase._fill_up([], 110), 110)
        self.assertEqual(self.datagridbase.bottomkey, None)

    def test_082_fill_up_002(self):
        self.datagridbase.keys.append("key")
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.assertEqual(self.datagridbase._fill_up([], 110), 110)
        self.assertEqual(self.datagridbase.bottomkey, "key")

    def test_082_fill_up_003(self):
        self.assertEqual(len(self.datagridbase.keys), 0)
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.assertEqual(self.datagridbase._fill_up([], 0), 0)
        self.assertEqual(self.datagridbase.bottomkey, None)

    def test_082_fill_up_004(self):
        self.datagridbase.keys.append("key")
        self.datagridbase.objects["key"] = self.Datarow()
        self.assertEqual(self.datagridbase.bottomkey, None)
        self.assertEqual(self.datagridbase._fill_up([], 0), 19)
        self.assertEqual(self.datagridbase.bottomkey, "key")


class DataGridBase_move_slider(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridbase = datagrid.DataGridBase(self.parent)
        self.datagridbase.datasource = self.Datasource()
        self.datagridbase.header_maker = self.header_maker

    def test_050_move_slider_003(self):
        self.datagridbase.vsbar_number = -1
        self.assertEqual(self.datagridbase.record_count, None)
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_004(self):
        self.datagridbase.vsbar_number = 2
        self.assertEqual(self.datagridbase.record_count, None)
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_005(self):
        self.datagridbase.vsbar_number = 0.5
        self.assertEqual(self.datagridbase.record_count, None)
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_006(self):
        self.datagridbase.vsbar_number = -1
        self.datagridbase.record_count = 10
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_007(self):
        self.datagridbase.vsbar_number = 2
        self.datagridbase.record_count = 10
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_008(self):
        self.datagridbase.vsbar_number = 0.5
        self.datagridbase.record_count = 10
        self.assertEqual(self.datagridbase.move_slider(), None)

    def test_050_move_slider_009(self):
        self.assertEqual(self.datagridbase.partial, None)
        self.datagridbase.partial = False
        self.datagridbase.vsbar_number = 0.6
        self.datagridbase.record_count = 11
        self.assertEqual(self.datagridbase.move_slider(), None)


class DataGridReadOnly(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridreadonly = datagrid.DataGridReadOnly(self.parent)

    def test_501___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'parent'",
                )
            ),
            datagrid.DataGridReadOnly,
        )

    def test_501_bind_off_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_off\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagridreadonly.bind_off,
            *(None,),
        )

    def test_501_bind_off_002(self):
        self.assertEqual(self.datagridreadonly.bind_off(), None)

    def test_502_bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_on\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagridreadonly.bind_on,
            *(None,),
        )

    def test_502_bind_on_002(self):
        self.assertEqual(self.datagridreadonly.bind_on(), None)

    def test_503___bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__bind_on\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagridreadonly.__bind_on,
            *(None,),
        )

    def test_503___bind_on_002(self):
        self.assertEqual(self.datagridreadonly.__bind_on(), None)

    def test_504_up_one_page_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"up_one_page\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.up_one_page,
        )

    # More '504' tests in DataGridReadOnly_dummy_fill_view.

    def test_505_down_one_page_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"down_one_page\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.down_one_page,
        )

    # More '505' tests in DataGridReadOnly_dummy_fill_view.

    def test_506_down_all_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"down_all\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridreadonly.down_all,
            **dict(event=None, badkey=None),
        )

    # More '506' tests in DataGridReadOnly_dummy_fill_view.

    def test_507_up_all_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"up_all\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridreadonly.up_all,
            **dict(event=None, badkey=None),
        )

    # More '507' tests in DataGridReadOnly_dummy_fill_view.

    def test_508_up_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"up_one_line\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.up_one_line,
        )

    # More '508' tests in DataGridReadOnly_dummy_fill_view.

    def test_509_up_one_line_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"up_one_line_selection\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.up_one_line_selection,
        )

    # More '509' tests in DataGridReadOnly_dummy_fill_view.

    def test_510_down_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"down_one_line\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.down_one_line,
        )

    # More '510' tests in DataGridReadOnly_dummy_fill_view.

    def test_511_down_one_line_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"down_one_line_selection\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.down_one_line_selection,
        )

    # More '511' tests in DataGridReadOnly_dummy_fill_view.

    def test_512_select_bookmark_up_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_bookmark_up_one_line\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.select_bookmark_up_one_line,
        )

    # More '512' tests in DataGridReadOnly_dummy_fill_view.

    def test_513_select_up_one_line_shift_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_up_one_line_shift\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.select_up_one_line_shift,
        )

    # More '513' tests in DataGridReadOnly_dummy_fill_view.

    def test_514_select_up_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_up_one_line\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridreadonly.select_up_one_line,
            **dict(event=None, badkey=None),
        )

    # More '514' tests in DataGridReadOnly_dummy_fill_view.

    def test_515_select_up_one_line_control_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_up_one_line_control\(\) got an unexpected ",
                    "keyword argument 'badkey'",
                )
            ),
            self.datagridreadonly.select_up_one_line_control,
            **dict(event=None, badkey=None),
        )

    # More '515' tests in DataGridReadOnly_dummy_fill_view.

    def test_516_select_bookmark_down_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_bookmark_down_one_line\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.select_bookmark_down_one_line,
        )

    # More '516' tests in DataGridReadOnly_dummy_fill_view.

    def test_517_select_down_one_line_shift_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_down_one_line_shift\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.select_down_one_line_shift,
        )

    # More '517' tests in DataGridReadOnly_dummy_fill_view.

    def test_518_select_down_one_line_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_down_one_line\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagridreadonly.select_down_one_line,
            **dict(event=None, badkey=None),
        )

    # More '518' tests in DataGridReadOnly_dummy_fill_view.

    def test_519_select_down_one_line_control_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"select_down_one_line_control\(\) got an unexpected ",
                    "keyword argument 'badkey'",
                )
            ),
            self.datagridreadonly.select_down_one_line_control,
            **dict(event=None, badkey=None),
        )

    # More '519' tests in DataGridReadOnly_dummy_fill_view.

    def test_520_add_bookmark_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"add_bookmark_event\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.add_bookmark_event,
        )

    def test_520_add_bookmark_event_002(self):
        self.assertEqual(self.datagridreadonly.add_bookmark_event(None), None)

    def test_521_cancel_bookmark_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_bookmark_event\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.cancel_bookmark_event,
        )

    def test_521_cancel_bookmark_event_002(self):
        self.assertEqual(
            self.datagridreadonly.cancel_bookmark_event(None), None
        )

    def test_522_cancel_selection_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"cancel_selection_event\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datagridreadonly.cancel_selection_event,
        )

    def test_522_cancel_selection_event_002(self):
        self.assertEqual(
            self.datagridreadonly.cancel_selection_event(None), None
        )


class DataGridReadOnly_dummy_fill_view(_DataGridBase):
    def setUp(self):
        super().setUp()
        self.datagridreadonly = datagrid.DataGridReadOnly(self.parent)
        self.datagridreadonly.fill_view = self.null_method

    def test_504_up_one_page_002(self):
        self.assertEqual(self.datagridreadonly.up_one_page(None), None)

    def test_505_down_one_page_002(self):
        self.assertEqual(self.datagridreadonly.down_one_page(None), None)

    def test_506_down_all_002(self):
        self.assertEqual(self.datagridreadonly.topkey, None)
        self.assertEqual(self.datagridreadonly.bottomkey, None)
        self.assertEqual(self.datagridreadonly.down_all(event=None), None)

    def test_507_up_all_002(self):
        self.assertEqual(self.datagridreadonly.topkey, None)
        self.assertEqual(self.datagridreadonly.bottomkey, None)
        self.assertEqual(self.datagridreadonly.up_all(event=None), None)

    def test_508_up_one_line_002(self):
        self.assertEqual(self.datagridreadonly.up_one_line(None), None)

    def test_509_up_one_line_selection_002(self):
        self.assertEqual(
            self.datagridreadonly.up_one_line_selection(None), None
        )

    def test_510_down_one_line_002(self):
        self.assertEqual(self.datagridreadonly.down_one_line(None), None)

    def test_511_down_one_line_selection_002(self):
        self.assertEqual(
            self.datagridreadonly.down_one_line_selection(None), None
        )

    def test_512_select_bookmark_up_one_line_002(self):
        self.assertEqual(
            self.datagridreadonly.select_bookmark_up_one_line(None), None
        )

    def test_513_select_up_one_line_shift_002(self):
        self.assertEqual(
            self.datagridreadonly.select_up_one_line_shift(None), None
        )

    def test_514_select_up_one_line_002(self):
        self.assertEqual(len(self.datagridreadonly.selection), 0)
        self.assertEqual(self.datagridreadonly.select_up_one_line(None), None)

    def test_514_select_up_one_line_003(self):
        self.datagridreadonly.selection.append("key")
        self.assertEqual(len(self.datagridreadonly.keys), 0)
        self.assertEqual(self.datagridreadonly.select_up_one_line(None), None)

    def test_514_select_up_one_line_004(self):
        self.datagridreadonly.selection.append("key")
        self.datagridreadonly.keys.append("key")
        self.datagridreadonly.objects["key"] = self.Datarow()
        self.datagridreadonly.gridrows_for_key[
            "key"
        ] = self.datagridreadonly.objects["key"]
        self.assertEqual(self.datagridreadonly.select_up_one_line(None), None)

    def test_515_select_up_one_line_control_002(self):
        self.assertEqual(len(self.datagridreadonly.selection), 0)
        self.assertEqual(
            self.datagridreadonly.select_up_one_line_control(None), None
        )

    def test_515_select_up_one_line_control_003(self):
        self.datagridreadonly.selection.append("key")
        self.assertEqual(len(self.datagridreadonly.keys), 0)
        self.assertEqual(
            self.datagridreadonly.select_up_one_line_control(None), None
        )

    def test_515_select_up_one_line_control_004(self):
        self.datagridreadonly.selection.append("key")
        self.datagridreadonly.keys.append("key")
        self.datagridreadonly.objects["key"] = self.Datarow()
        self.datagridreadonly.gridrows_for_key[
            "key"
        ] = self.datagridreadonly.objects["key"]
        self.assertEqual(
            self.datagridreadonly.select_up_one_line_control(None), None
        )

    def test_516_select_bookmark_down_one_line_002(self):
        self.assertEqual(
            self.datagridreadonly.select_bookmark_down_one_line(None), None
        )

    def test_517_select_down_one_line_shift_002(self):
        self.assertEqual(
            self.datagridreadonly.select_down_one_line_shift(None), None
        )

    def test_518_select_down_one_line_002(self):
        self.assertEqual(len(self.datagridreadonly.selection), 0)
        self.assertEqual(
            self.datagridreadonly.select_down_one_line(None), None
        )

    def test_518_select_down_one_line_003(self):
        self.datagridreadonly.selection.append("key")
        self.assertEqual(len(self.datagridreadonly.keys), 0)
        self.assertEqual(
            self.datagridreadonly.select_down_one_line(None), None
        )

    def test_518_select_down_one_line_004(self):
        self.datagridreadonly.selection.append("key")
        self.datagridreadonly.keys.append("key")
        self.datagridreadonly.objects["key"] = self.Datarow()
        self.datagridreadonly.gridrows_for_key[
            "key"
        ] = self.datagridreadonly.objects["key"]
        self.assertEqual(
            self.datagridreadonly.select_down_one_line(None), None
        )

    def test_519_select_down_one_line_control_002(self):
        self.assertEqual(len(self.datagridreadonly.selection), 0)
        self.assertEqual(
            self.datagridreadonly.select_down_one_line_control(None), None
        )

    def test_519_select_down_one_line_control_003(self):
        self.datagridreadonly.selection.append("key")
        self.assertEqual(len(self.datagridreadonly.keys), 0)
        self.assertEqual(
            self.datagridreadonly.select_down_one_line_control(None), None
        )

    def test_519_select_down_one_line_control_004(self):
        self.datagridreadonly.selection.append("key")
        self.datagridreadonly.keys.append("key")
        self.datagridreadonly.objects["key"] = self.Datarow()
        self.datagridreadonly.gridrows_for_key[
            "key"
        ] = self.datagridreadonly.objects["key"]
        self.assertEqual(
            self.datagridreadonly.select_down_one_line_control(None), None
        )


class DataGrid(_DataGridBase):
    def setUp(self):
        super().setUp()

        class Instance:
            def delete_row(*a):
                return Object()

            def edit_row(*a):
                return Object()

            def show_row(*a):
                return Object()

            def empty(*a):
                pass

            def clone(*a):
                pass

            def get_keys(*a):
                return []

        self.Instance = Instance

        class Datasource:
            new_row = self.Instance

        self.Datasource = Datasource

        class Object:
            def set_data_source(*a):
                pass

            def on_data_change(*a):
                pass

        class Event:
            state = 0

        self.Event = Event
        self.datagrid = datagrid.DataGrid(self.parent)
        self.datagrid.datasource = self.Datasource()

    def test_701___init___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__init__\(\) missing 1 required positional argument: ",
                    "'parent'",
                )
            ),
            datagrid.DataGrid,
        )

    def test_701_bind_off_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_off\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.bind_off,
            *(None,),
        )

    def test_701_bind_off_002(self):
        self.assertEqual(self.datagrid.bind_off(), None)

    def test_702_bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"bind_on\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.bind_on,
            *(None,),
        )

    def test_702_bind_on_002(self):
        self.assertEqual(self.datagrid.bind_on(), None)

    def test_703___bind_on_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"__bind_on\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.__bind_on,
            *(None,),
        )

    def test_703___bind_on_002(self):
        self.assertEqual(self.datagrid.__bind_on(), None)

    def test_704_create_delete_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_delete_dialog\(\) missing 3 required positional ",
                    "arguments: 'instance', 'oldobject', and 'modal'",
                )
            ),
            self.datagrid.create_delete_dialog,
        )

    def test_704_create_delete_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_delete_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.create_delete_dialog,
            *(None, None, None),
            **dict(title=None, badkey=None),
        )

    def test_704_create_delete_dialog_003(self):
        self.assertEqual(
            self.datagrid.create_delete_dialog(self.Instance(), None, None),
            None,
        )

    def test_705_create_edit_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_edit_dialog\(\) missing 5 required positional ",
                    "arguments: 'instance', 'newobject', 'oldobject', ",
                    "'showinitial', and 'modal'",
                )
            ),
            self.datagrid.create_edit_dialog,
        )

    def test_705_create_edit_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_edit_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.create_edit_dialog,
            *(None, None, None, None, None),
            **dict(title=None, badkey=None),
        )

    def test_705_create_edit_dialog_003(self):
        self.assertEqual(
            self.datagrid.create_edit_dialog(
                self.Instance(), None, None, None, None
            ),
            None,
        )

    def test_706_create_show_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_show_dialog\(\) missing 3 required positional ",
                    "arguments: 'instance', 'oldobject', and 'modal'",
                )
            ),
            self.datagrid.create_show_dialog,
        )

    def test_706_create_show_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"create_show_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.create_show_dialog,
            *(None, None, None),
            **dict(title=None, badkey=None),
        )

    def test_706_create_show_dialog_003(self):
        self.assertEqual(
            self.datagrid.create_show_dialog(self.Instance(), None, None), None
        )

    def test_707_edit_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit_dialog\(\) missing 2 required positional ",
                    "arguments: 'key' and 'event'",
                )
            ),
            self.datagrid.edit_dialog,
        )

    def test_707_edit_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.edit_dialog,
            *(None, None),
            **dict(modal=True, badkey=None),
        )

    def test_707_edit_dialog_003(self):
        self.assertEqual(len(self.datagrid.keys), 0)
        self.assertEqual(self.datagrid.edit_dialog(None, None), None)

    def test_707_edit_dialog_004(self):
        self.datagrid.keys.append("key")
        self.assertEqual(len(self.datagrid.objects), 0)
        self.assertEqual(self.datagrid.edit_dialog("key", self.Event()), None)

    def test_707_edit_dialog_005(self):
        self.datagrid.keys.append("key")
        self.datagrid.objects["key"] = self.Instance()
        event = self.Event()
        event.state = datagrid.SHIFTDOWN
        self.assertEqual(self.datagrid.edit_dialog("key", event), None)

    def test_707_edit_dialog_006(self):
        self.datagrid.keys.append("key")
        self.datagrid.objects["key"] = self.Instance()
        event = self.Event()
        event.state = datagrid.CONTROLDOWN
        self.assertEqual(self.datagrid.edit_dialog("key", event), None)

    def test_708_edit_dialog_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit_dialog_event\(\) missing 1 required positional ",
                    "argument: 'event'",
                )
            ),
            self.datagrid.edit_dialog_event,
        )

    def test_708_edit_dialog_event_002(self):
        self.assertEqual(len(self.datagrid.selection), 0)
        self.assertEqual(self.datagrid.edit_dialog_event(self.Event()), None)

    def test_708_edit_dialog_event_003(self):
        self.datagrid.selection.append("key")
        self.assertEqual(self.datagrid.edit_dialog_event(self.Event()), None)

    def test_709_delete_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delete_dialog\(\) missing 2 required positional ",
                    "arguments: 'key' and 'event'",
                )
            ),
            self.datagrid.delete_dialog,
        )

    def test_709_delete_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delete_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.delete_dialog,
            *(None, None),
            **dict(modal=True, badkey=None),
        )

    def test_709_delete_dialog_003(self):
        self.assertEqual(len(self.datagrid.keys), 0)
        self.assertEqual(self.datagrid.delete_dialog(None, None), None)

    def test_709_delete_dialog_004(self):
        self.datagrid.keys.append("key")
        self.assertEqual(len(self.datagrid.objects), 0)
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(
            self.datagrid.delete_dialog("key", self.Event()), None
        )

    def test_710_delete_dialog_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delete_dialog_event\(\) missing 1 required positional ",
                    "argument: 'event'",
                )
            ),
            self.datagrid.delete_dialog_event,
        )

    def test_710_delete_dialog_event_002(self):
        self.assertEqual(len(self.datagrid.selection), 0)
        self.assertEqual(self.datagrid.delete_dialog_event(self.Event()), None)

    def test_710_delete_dialog_event_003(self):
        self.datagrid.selection.append("key")
        self.assertEqual(self.datagrid.delete_dialog_event(self.Event()), None)

    def test_711_show_dialog_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_dialog\(\) missing 2 required positional ",
                    "arguments: 'key' and 'event'",
                )
            ),
            self.datagrid.show_dialog,
        )

    def test_711_show_dialog_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_dialog\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.show_dialog,
            *(None, None),
            **dict(modal=True, badkey=None),
        )

    def test_711_show_dialog_003(self):
        self.assertEqual(len(self.datagrid.keys), 0)
        self.assertEqual(self.datagrid.show_dialog(None, None), None)

    def test_711_show_dialog_004(self):
        self.datagrid.keys.append("key")
        self.assertEqual(len(self.datagrid.objects), 0)
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.show_dialog("key", self.Event()), None)

    def test_712_show_dialog_event_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_dialog_event\(\) missing 1 required positional ",
                    "argument: 'event'",
                )
            ),
            self.datagrid.show_dialog_event,
        )

    def test_712_show_dialog_event_002(self):
        self.assertEqual(len(self.datagrid.selection), 0)
        self.assertEqual(self.datagrid.show_dialog_event(self.Event()), None)

    def test_712_show_dialog_event_003(self):
        self.datagrid.selection.append("key")
        self.assertEqual(self.datagrid.show_dialog_event(self.Event()), None)

    def test_713_delete_from_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"delete_from_popup\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.delete_from_popup,
            *(None,),
        )

    def test_713_delete_from_popup_002(self):
        self.datagrid.pointer_popup_selection = "key"
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.delete_from_popup(), None)

    def test_714_edit_from_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit_from_popup\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.edit_from_popup,
            *(None,),
        )

    def test_714_edit_from_popup_002(self):
        self.datagrid.pointer_popup_selection = "key"
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.edit_from_popup(), None)

    def test_715_edit_show_from_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"edit_show_from_popup\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.edit_show_from_popup,
            *(None,),
        )

    def test_715_edit_show_from_popup_002(self):
        self.datagrid.pointer_popup_selection = "key"
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.edit_show_from_popup(), None)

    def test_716_insert_from_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"insert_from_popup\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.insert_from_popup,
            *(None,),
        )

    def test_716_insert_from_popup_002(self):
        # self.datagrid.pointer_popup_selection = "key"
        # self.datagrid.objects['key'] = self.Instance()
        self.assertEqual(self.datagrid.insert_from_popup(), None)

    def test_717_show_from_popup_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_from_popup\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datagrid.show_from_popup,
            *(None,),
        )

    def test_717_show_from_popup_002(self):
        self.datagrid.pointer_popup_selection = "key"
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.show_from_popup(), None)

    def test_718_launch_edit_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_edit_record\(\) missing 1 required positional ",
                    "argument: 'key'",
                )
            ),
            self.datagrid.launch_edit_record,
        )

    def test_718_launch_edit_record_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_edit_record\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.launch_edit_record,
            *(None,),
            **dict(modal=True, badkey=None),
        )

    def test_718_launch_edit_record_003(self):
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.launch_edit_record("key"), None)

    def test_719_launch_edit_show_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_edit_show_record\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagrid.launch_edit_show_record,
        )

    def test_719_launch_edit_show_record_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_edit_show_record\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.launch_edit_show_record,
            *(None,),
            **dict(modal=True, badkey=None),
        )

    def test_719_launch_edit_show_record_003(self):
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.launch_edit_show_record("key"), None)

    def test_720_launch_insert_new_record_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_insert_new_record\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.launch_insert_new_record,
            **dict(modal=True, badkey=None),
        )

    def test_720_launch_insert_new_record_002(self):
        self.assertEqual(self.datagrid.launch_insert_new_record(), None)

    def test_721_launch_show_record_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_show_record\(\) missing 1 required ",
                    "positional argument: 'key'",
                )
            ),
            self.datagrid.launch_show_record,
        )

    def test_721_launch_show_record_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"launch_show_record\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.datagrid.launch_show_record,
            *(None,),
            **dict(modal=True, badkey=None),
        )

    def test_721_launch_show_record_003(self):
        self.datagrid.objects["key"] = self.Instance()
        self.assertEqual(self.datagrid.launch_show_record("key"), None)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DataGridBase))
    runner().run(loader(DataGridBase_bookmark_down_bookmark_up))
    runner().run(loader(DataGridBase__add_record_to_view__cursor_exists))
    runner().run(loader(DataGridBase__add_record_to_view__with_startkey))
    runner().run(loader(DataGridBase_on_data_change_instance_is_None))
    runner().run(loader(DataGridBase_select_down_select_up))
    runner().run(loader(DataGridBase_set_properties))
    runner().run(loader(DataGridBase_pointerxy))
    runner().run(loader(DataGridBase_dummy_fill_view))
    runner().run(loader(DataGridBase_dummy_fill_data_grid))
    runner().run(loader(DataGridBase_fill_data_grid))
    runner().run(loader(DataGridBase__fill_down__fill_up))
    runner().run(loader(DataGridBase_move_slider))
    runner().run(loader(DataGridReadOnly))
    runner().run(loader(DataGridReadOnly_dummy_fill_view))
    runner().run(loader(DataGrid))
