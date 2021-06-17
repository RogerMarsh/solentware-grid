# test_datarow.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""datarow tests"""

import unittest

from .. import datarow


class ModuleConstants(unittest.TestCase):
    def test_001_constants_001(self):
        self.assertEqual(
            sorted(k for k in dir(datarow) if k.isupper()),
            [
                "BOOKMARK_COLOUR",
                "GRID_COLUMNCONFIGURE",
                "GRID_CONFIGURE",
                "NULL_COLOUR",
                "ROW",
                "ROW_UNDER_POINTER_COLOUR",
                "SELECTION_AND_BOOKMARK_COLOUR",
                "SELECTION_COLOUR",
                "SELECTION_CYCLE_COLOUR",
                "WIDGET",
                "WIDGET_CONFIGURE",
            ],
        )
        self.assertEqual(datarow.NULL_COLOUR, "#d9d9d9")
        self.assertEqual(datarow.SELECTION_COLOUR, "#76d9d9")
        self.assertEqual(datarow.BOOKMARK_COLOUR, "#86d929")
        self.assertEqual(datarow.SELECTION_CYCLE_COLOUR, "#eb3010")
        self.assertEqual(datarow.SELECTION_AND_BOOKMARK_COLOUR, "#e0f113")
        self.assertEqual(datarow.ROW_UNDER_POINTER_COLOUR, "yellow")
        self.assertEqual(datarow.GRID_COLUMNCONFIGURE, 1)
        self.assertEqual(datarow.GRID_CONFIGURE, 2)
        self.assertEqual(datarow.WIDGET_CONFIGURE, 3)
        self.assertEqual(datarow.WIDGET, 4)
        self.assertEqual(datarow.ROW, 5)
        self.assertEqual(datarow._widget_configure, {"background", "font"})


class DataHeader(unittest.TestCase):
    def setUp(self):
        class Widget:
            def __init__(self, *a, **k):
                pass

            def bind(self, *a, **k):
                pass

            configure = bind
            grid_configure = bind
            grid_columnconfigure = bind

        self.Widget = Widget
        self.dataheader = datarow.DataHeader()
        self.specification = (
            {
                datarow.WIDGET_CONFIGURE: {},
                datarow.WIDGET: self.Widget,
                datarow.GRID_CONFIGURE: {"column": 1},
                datarow.GRID_COLUMNCONFIGURE: None,
            },
        )

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
            datarow.DataHeader,
            *(None,),
        )

    def test_002_grid_header_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_header_row\(\) missing 1 required positional ",
                    "argument: 'specification'",
                )
            ),
            self.dataheader.grid_header_row,
        )

    def test_002_grid_header_row_002(self):
        self.assertEqual(
            self.dataheader.grid_header_row({}),
            self.dataheader.make_header_widgets,
        )

    def test_003_make_header_widgets_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "make_header_widgets\(\) missing 2 required positional ",
                    "arguments: 'widgetpool' and 'parent'",
                )
            ),
            self.dataheader.make_header_widgets,
        )

    def test_003_make_header_widgets_002(self):
        def widgetpool(spec):
            return self.Widget()

        self.dataheader.header_specification = self.specification
        row = self.dataheader.make_header_widgets(widgetpool, self.Widget())
        self.assertEqual(len(row), 1)
        self.assertEqual(len(row[0]), 1)
        self.assertEqual(len(row[0][0]), 2)
        self.assertIsInstance(row[0][0][0], self.Widget)
        self.assertEqual(
            row[0][0][1], self.specification[0][datarow.GRID_CONFIGURE]
        )

    def test_003_make_header_widgets_003(self):
        def widgetpool(spec):
            return None

        self.dataheader.header_specification = self.specification
        row = self.dataheader.make_header_widgets(widgetpool, self.Widget())
        self.assertEqual(len(row), 1)
        self.assertEqual(len(row[0]), 1)
        self.assertEqual(len(row[0][0]), 2)
        self.assertIsInstance(row[0][0][0], self.Widget)
        self.assertEqual(
            row[0][0][1], self.specification[0][datarow.GRID_CONFIGURE]
        )


class DataRow(unittest.TestCase):
    def setUp(self):
        class Widget:
            def __init__(self, *a, **k):
                pass

            def bind(self, *a, **k):
                pass

            configure = bind
            grid_configure = bind
            grid_columnconfigure = bind

            def winfo_rootx(self, *a, **k):
                return "100"

            def winfo_rooty(self, *a, **k):
                return "150"

            def winfo_height(self, *a, **k):
                return "10"

            def winfo_width(self, *a, **k):
                return "15"

        self.Widget = Widget
        self.datarow = datarow.DataRow()
        self.specification = (
            {
                datarow.WIDGET_CONFIGURE: {},
                datarow.WIDGET: self.Widget,
                datarow.GRID_CONFIGURE: {"column": 1},
                datarow.GRID_COLUMNCONFIGURE: None,
            },
        )
        self.items = ("text1", "text2")

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
            datarow.DataRow,
            *(None,),
        )

    def test_002_set_background_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background\(\) missing 2 required positional ",
                    "arguments: 'widgets' and 'background'",
                )
            ),
            self.datarow.set_background,
        )

    def test_002_set_background_002(self):
        self.assertEqual(
            self.datarow.set_background([(self.Widget(), None)], None), None
        )

    def test_003_set_background_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_bookmark\(\) missing 1 required ",
                    "positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_bookmark,
        )

    def test_003_set_background_bookmark_002(self):
        self.assertEqual(
            self.datarow.set_background_bookmark([(self.Widget(), None)]), None
        )

    def test_004_set_background_bookmarked_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_bookmarked_selection\(\) missing 1 ",
                    "required positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_bookmarked_selection,
        )

    def test_004_set_background_bookmarked_selection_002(self):
        self.assertEqual(
            self.datarow.set_background_bookmarked_selection(
                [(self.Widget(), None)]
            ),
            None,
        )

    def test_005_set_background_normal_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_normal\(\) missing 1 ",
                    "required positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_normal,
        )

    def test_005_set_background_normal_002(self):
        self.assertEqual(
            self.datarow.set_background_normal([(self.Widget(), None)]), None
        )

    def test_006_set_background_row_under_pointer_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_row_under_pointer\(\) missing 1 ",
                    "required positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_row_under_pointer,
        )

    def test_006_set_background_row_under_pointer_002(self):
        self.assertEqual(
            self.datarow.set_background_row_under_pointer(
                [(self.Widget(), None)]
            ),
            None,
        )

    def test_007_set_background_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_selection\(\) missing 1 ",
                    "required positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_selection,
        )

    def test_007_set_background_selection_002(self):
        self.assertEqual(
            self.datarow.set_background_selection([(self.Widget(), None)]),
            None,
        )

    def test_008_set_background_selection_cycle_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_background_selection_cycle\(\) missing 1 ",
                    "required positional argument: 'widgets'",
                )
            ),
            self.datarow.set_background_selection_cycle,
        )

    def test_008_set_background_selection_cycle_002(self):
        self.assertEqual(
            self.datarow.set_background_selection_cycle(
                [(self.Widget(), None)]
            ),
            None,
        )

    def test_009_form_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "form_row\(\) missing 2 ",
                    "required positional arguments: 'parent' and 'rowsizer'",
                )
            ),
            self.datarow.form_row,
        )

    def test_009_form_row_002(self):
        self.assertRaisesRegex(
            datarow.DataRowError,
            "form_row not implemented",
            self.datarow.form_row,
            *(None, None),
        )

    def test_010_grid_row_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row\(\) takes from 1 to 2 ",
                    "positional arguments but 3 were given",
                )
            ),
            self.datarow.grid_row,
            *(None, None),
        )

    def test_010_grid_row_002(self):
        widgets, textitems, configure = self.datarow.grid_row(
            self.items, **dict(background=1, font=2, x=3)
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(configure, dict(background=1, font=2))

    def test_011_grid_row_bookmark_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_bookmark\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_bookmark,
            *(None,),
        )

    def test_011_grid_row_bookmark_002(self):
        widgets, textitems, configure = self.datarow.grid_row_bookmark(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(configure, dict(background=datarow.BOOKMARK_COLOUR))

    def test_012_grid_row_bookmarked_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_bookmarked_selection\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_bookmarked_selection,
            *(None,),
        )

    def test_012_grid_row_bookmarked_selection_002(self):
        widgets, textitems, conf = self.datarow.grid_row_bookmarked_selection(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(
            conf, dict(background=datarow.SELECTION_AND_BOOKMARK_COLOUR)
        )

    def test_013_grid_row_normal_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_normal\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_normal,
            *(None,),
        )

    def test_013_grid_row_normal_002(self):
        widgets, textitems, configure = self.datarow.grid_row_normal(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(configure, dict(background=datarow.NULL_COLOUR))

    def test_014_grid_row_under_pointer_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_under_pointer\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_under_pointer,
            *(None,),
        )

    def test_014_grid_row_under_pointer_002(self):
        widgets, textitems, configure = self.datarow.grid_row_under_pointer(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(
            configure, dict(background=datarow.ROW_UNDER_POINTER_COLOUR)
        )

    def test_015_grid_row_selection_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_selection\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_selection,
            *(None,),
        )

    def test_015_grid_row_selection_002(self):
        widgets, textitems, configure = self.datarow.grid_row_selection(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(configure, dict(background=datarow.SELECTION_COLOUR))

    def test_016_grid_row_selection_cycle_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "grid_row_selection_cycle\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.grid_row_selection_cycle,
            *(None,),
        )

    def test_016_grid_row_selection_cycle_002(self):
        widgets, textitems, configure = self.datarow.grid_row_selection_cycle(
            textitems=self.items
        )
        self.assertEqual(widgets, self.datarow.make_row_widgets)
        self.assertEqual(textitems, self.items)
        self.assertEqual(
            configure, dict(background=datarow.SELECTION_CYCLE_COLOUR)
        )

    def test_017___call___001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "__call__\(\) takes 1 ",
                    "positional argument but 2 were given",
                )
            ),
            self.datarow.__call__,
            *(None,),
        )

    def test_017___call___002(self):
        self.assertEqual(isinstance(self.datarow(), tuple), True)

    def test_018_make_row_widgets_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "make_row_widgets\(\) missing 3 required positional ",
                    "arguments: 'widgetpool', 'parent', and 'items'",
                )
            ),
            self.datarow.make_row_widgets,
        )

    def test_018_make_row_widgets_002(self):
        def widgetpool(spec):
            return self.Widget()

        self.datarow.row_specification = self.specification
        self.assertEqual(len(self.datarow._row_widgets), 0)
        self.assertIs(
            self.datarow.make_row_widgets(
                widgetpool, self.Widget(), self.items
            ),
            self.datarow,
        )
        self.assertEqual(len(self.datarow._row_widgets), 1)

    def test_018_make_row_widgets_003(self):
        def widgetpool(spec):
            return None

        self.datarow.row_specification = self.specification
        self.assertEqual(len(self.datarow._row_widgets), 0)
        self.assertIs(
            self.datarow.make_row_widgets(
                widgetpool, self.Widget(), self.items
            ),
            self.datarow,
        )
        self.assertEqual(len(self.datarow._row_widgets), 1)

    def test_019_populate_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "populate_widget\(\) missing 1 required positional ",
                    "argument: 'widget'",
                )
            ),
            self.datarow.populate_widget,
        )

    def test_019_populate_widget_002(self):
        self.assertEqual(self.datarow.populate_widget(self.Widget()), None)

    def test_020_highlight_row_on_pointer_enter_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "highlight_row_on_pointer_enter\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datarow.highlight_row_on_pointer_enter,
        )

    def test_020_highlight_row_on_pointer_enter_002(self):
        self.assertEqual(
            self.datarow.highlight_row_on_pointer_enter(None), None
        )

    def test_021_highlight_row_on_pointer_leave_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "highlight_row_on_pointer_leave\(\) missing 1 required ",
                    "positional argument: 'event'",
                )
            ),
            self.datarow.highlight_row_on_pointer_leave,
        )

    def test_021_highlight_row_on_pointer_leave_002(self):
        self.assertEqual(
            self.datarow.highlight_row_on_pointer_leave(None), None
        )

    def test_022_set_popup_state_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "set_popup_state\(\) takes from 1 to 2 ",
                    "positional arguments but 3 were given",
                )
            ),
            self.datarow.set_popup_state,
            *(None, None),
        )

    def test_022_set_popup_state_002(self):
        self.assertEqual(self.datarow.set_popup_state(), None)

    def test_023_is_row_under_pointer_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    "is_row_under_pointer\(\) missing 2 required ",
                    "positional arguments: 'pointerx' and 'pointery'",
                )
            ),
            self.datarow.is_row_under_pointer,
        )

    def test_023_is_row_under_pointer_002(self):
        self.assertEqual(len(self.datarow._row_widgets), 0)
        self.assertEqual(self.datarow.is_row_under_pointer(None, None), False)

    def test_023_is_row_under_pointer_003(self):
        self.datarow._row_widgets = [[self.Widget()]]
        self.assertEqual(self.datarow.is_row_under_pointer(None, 140), False)

    def test_023_is_row_under_pointer_004(self):
        self.datarow._row_widgets = [[self.Widget()]]
        self.assertEqual(self.datarow.is_row_under_pointer(None, 170), False)

    def test_023_is_row_under_pointer_005(self):
        self.datarow._row_widgets = [[self.Widget()]]
        self.assertEqual(self.datarow.is_row_under_pointer(90, 155), False)

    def test_023_is_row_under_pointer_006(self):
        self.datarow._row_widgets = [[self.Widget()]]
        self.assertEqual(self.datarow.is_row_under_pointer(120, 155), False)

    def test_023_is_row_under_pointer_007(self):
        self.datarow._row_widgets = [[self.Widget()]]
        self.assertEqual(self.datarow.is_row_under_pointer(110, 155), True)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(ModuleConstants))
    runner().run(loader(DataHeader))
    runner().run(loader(DataRow))
