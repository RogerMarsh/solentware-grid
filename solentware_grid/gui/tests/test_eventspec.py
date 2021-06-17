# test_eventspec.py
# Copyright 2012 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""eventspec tests"""

import unittest

from .. import eventspec


class EventSpec(unittest.TestCase):
    def test_001_event_specifications_001(self):
        self.assertEqual(
            sorted(
                k
                for k in dir(eventspec.EventSpec)
                if not k.startswith("__") and not k.endswith("__")
            ),
            [
                "bookmark_selected_line",
                "down_all",
                "down_one_bookmarked_line_move_select",
                "down_one_line",
                "down_one_line_in_selection",
                "down_one_line_move_select",
                "down_one_page",
                "give_focus_to_datagridbase",
                "grid_or_row_popup_at_pointer",
                "grid_or_row_popup_at_top_left",
                "insert_row_in_datagrid",
                "launch_delete_dialog",
                "launch_edit_and_show_dialog",
                "launch_edit_dialog",
                "launch_insert_dialog",
                "launch_show_dialog",
                "move_select_down_one_line_after_align",
                "move_select_up_one_line_after_align",
                "move_visible_select_down_one_line",
                "move_visible_select_up_one_line",
                "remove_selected_line_from_bookmark",
                "remove_selected_line_from_selection",
                "select_row_in_datagridbase",
                "up_all",
                "up_one_bookmarked_line_move_select",
                "up_one_line",
                "up_one_line_in_selection",
                "up_one_line_move_select",
                "up_one_page",
            ],
        )

    def test_001_event_specifications_002(self):
        es = eventspec.EventSpec
        ae = self.assertEqual
        ae(es.give_focus_to_datagridbase, "<Button-1>")
        ae(es.select_row_in_datagridbase, "<Button-3>")
        ae(es.insert_row_in_datagrid, "<Button-3>")

        ae(
            es.grid_or_row_popup_at_top_left,
            (
                "<Shift-KeyPress-F10>",
                "Popup Menu at Top Left",
                "Shift F10",
            ),
        )
        ae(
            es.grid_or_row_popup_at_pointer,
            (
                "<Ctrl-KeyPress-F10>",
                "Popup Menu at Pointer",
                "Ctrl F10",
            ),
        )
        ae(es.up_one_page, ("<KeyPress-Prior>", "Page Up", "Page Up"))
        ae(es.down_one_page, ("<KeyPress-Next>", "Page Down", "Page Down"))
        ae(es.down_all, ("<Shift-KeyPress-End>", "End", "Shift End"))
        ae(es.up_all, ("<Shift-KeyPress-Home>", "Start", "Shift Home"))
        ae(es.up_one_line, ("<KeyPress-Up>", "Line Up", "Up"))
        ae(
            es.up_one_line_in_selection,
            (
                "<Control-KeyPress-Up>",
                "Cycle Up Selection",
                "Ctrl Up",
            ),
        )
        ae(es.down_one_line, ("<KeyPress-Down>", "Line Down", "Down"))
        ae(
            es.down_one_line_in_selection,
            (
                "<Control-KeyPress-Down>",
                "Cycle Down Selection",
                "Ctrl Down",
            ),
        )
        ae(
            es.move_visible_select_up_one_line,
            (
                "<KeyPress-Left>",
                "Select Line Up",
                "Left",
            ),
        )
        ae(
            es.up_one_bookmarked_line_move_select,
            (
                "<Alt-KeyPress-Left>",
                "Cycle Up Bookmarks",
                "Alt Left",
            ),
        )
        ae(
            es.up_one_line_move_select,
            (
                "<Control-KeyPress-Left>",
                "Move Select Line Up",
                "Ctrl Left",
            ),
        )
        ae(
            es.move_select_up_one_line_after_align,
            (
                "<Shift-KeyPress-Left>",
                "Align Select Line Up",
                "Shift Left",
            ),
        )
        ae(
            es.move_visible_select_down_one_line,
            (
                "<KeyPress-Right>",
                "Select Line Down",
                "Right",
            ),
        )
        ae(
            es.down_one_bookmarked_line_move_select,
            (
                "<Alt-KeyPress-Right>",
                "Cycle Down Bookmarks",
                "Alt Right",
            ),
        )
        ae(
            es.down_one_line_move_select,
            (
                "<Control-KeyPress-Right>",
                "Move Select Line Down",
                "Ctrl Right",
            ),
        )
        ae(
            es.move_select_down_one_line_after_align,
            (
                "<Shift-KeyPress-Right>",
                "Align Select Line Down",
                "Shift Right",
            ),
        )
        ae(
            es.bookmark_selected_line,
            (
                "<Alt-KeyPress-Insert>",
                "Bookmark Selection",
                "Alt Insert",
            ),
        )
        ae(
            es.remove_selected_line_from_bookmark,
            (
                "<Alt-KeyPress-Delete>",
                "Remove Bookmark",
                "Alt Delete",
            ),
        )
        ae(
            es.remove_selected_line_from_selection,
            (
                "<Control-KeyPress-Delete>",
                "Remove Select",
                "Ctrl Delete",
            ),
        )

        ae(es.launch_show_dialog, ("<KeyPress-Return>", "Show", "Enter"))
        ae(
            es.launch_edit_dialog,
            ("<Shift-KeyPress-Insert>", "Edit", "Shift Insert"),
        )
        ae(es.launch_delete_dialog, ("<KeyPress-Delete>", "Delete", "Delete"))
        ae(es.launch_insert_dialog, ("<KeyPress-Insert>", "Insert", "Insert"))
        ae(
            es.launch_edit_and_show_dialog,
            (
                "<Control-KeyPress-Insert>",
                "Edit and show",
                "Ctrl Insert",
            ),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(EventSpec))
