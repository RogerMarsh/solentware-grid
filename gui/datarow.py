# datarow.py
# Copyright 2007 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Define basic interface for setting properties of a row in a datagrid.

DataRow provides methods to set background colour of row to match selection
state.  Subclasses will supply methods appropriate to application.

List of classes:

DataRowError - Exceptions
DataHeader
DataRow

"""

import tkinter

from basesup.tools.callbackexception import CallbackException

NULL_COLOUR = '#d9d9d9' # system backgound
SELECTION_COLOUR = '#76d9d9' # a light blue
BOOKMARK_COLOUR = '#86d929' # a light green
SELECTION_CYCLE_COLOUR = '#eb3010' # a dark orange
SELECTION_AND_BOOKMARK_COLOUR = '#e0f113' # a pale yellow
ROW_UNDER_POINTER_COLOUR = 'yellow'

# keys for header and row specification dictionaries
GRID_COLUMNCONFIGURE = 1
GRID_CONFIGURE = 2
WIDGET_CONFIGURE = 3
WIDGET = 4
ROW = 5

_widget_configure = {
    'background', 'font'}


class DataRowError(Exception):
    pass


class DataHeader(object):
    
    """Provide methods to create a new header and configure its widgets.

    Methods added:

    grid_header_row
    make_header_widgets

    Methods overridden:

    None

    Methods extended:

    __init__

    """
    def __init__(self):
        """Extend with placeholder for header specification."""
        super(DataHeader, self).__init__()
        self.header_specification = ()

    # Not necessarily best but minimum change to get this out of DataRow
    # Now we are there: is this method needed at all?
    def grid_header_row(self, specification):
        """Return (<method>)

        master for header row widget is not known when header created.
        
        """
        self.header_specification = specification
        return (self.make_header_widgets)

    def make_header_widgets(self, widget, parent):
        """Return row of populated widgets with grid configuration arguments.

        widget - widget pool manager
        parent - master for row widget

        """
        # Maybe return dictionary of widgets with (row, col) as keys?
        # If spec per instance set spec[TEXT] in grid_row() call?
        row = []
        for spec in self.header_specification:
            wconf = spec[WIDGET_CONFIGURE].copy()
            w = widget(spec[WIDGET])
            if w is None:
                w = spec[WIDGET](master=parent)
            w.bind('<Enter>', '')
            w.bind('<Leave>', '')
            w.configure(background=NULL_COLOUR, **wconf)
            w.grid_configure(spec[GRID_CONFIGURE])
            parent.grid_columnconfigure(
                spec[GRID_CONFIGURE]['column'],
                spec[GRID_COLUMNCONFIGURE])
            row.append((w, spec[GRID_CONFIGURE]))
        return (row,)


class DataRow(CallbackException):
    
    """Provide methods to create a new row and set background colour of a row.

    Set row properties based on selection status.
    Subclass must override methods grid_row.
    
    Typical use is
    class FooRecord(Record):
        ...
    class FooRow(FooRecord, DataRow):
        ...

    Methods added:

    background colour
    bookmarked row
    __call__
    form_row - raise DataRow error 'form_row not implemented'
    grid_row
    grid_row_bookmark - Return new row with bookmarked background colour
    grid_row_bookmarked_selection - Return new row with selected bookmarked
    grid_row_normal - Return new row with default background colour
    grid_row_selection - Return new row with active selection background colour
    grid_row_selection_cycle - Return new row with selcted background colour
    highlight_row_on_pointer_enter
    highlight_row_on_pointer_leave
    make_row_widgets
    set_background - Set row background colour
    set_background_bookmark - Set background colour for bookmarked row
    set_background_bookmarked_selection - Set background colour for selected
    set_background_normal - Set default background colour for row
    set_background_row_under_pointer
    set_background_selection - Set background colour for active selected row
    set_background_selection_cycle - Set background colour for selected rows

    Methods overridden:

    None

    Methods extended:

    __init__
    
    """
    # background argument to be put in kargs throughout.
    # This becomes obvious thing to do with removal of row widget

    def __init__(self):
        """"""
        super(DataRow, self).__init__()
        self._row_widgets = ()
        self._current_row_background = NULL_COLOUR
        self._pointer_popup_active = False

    def set_background(self, widgets, background):
        """Set background colour of widgets.

        widgets - list((widget, specification), ...).
        background - the background colour.

        Each element of widgets will have been created by make_row_widgets()
        or DataHeader.make_header_widgets() and reused by DataGrid instance
        in a data row.

        """
        for w in widgets:
            w[0].configure(background=background)

    def set_background_bookmark(self, widgets):
        self._current_row_background = BOOKMARK_COLOUR
        self.set_background(widgets, self._current_row_background)

    def set_background_bookmarked_selection(self, widgets):
        self._current_row_background = SELECTION_AND_BOOKMARK_COLOUR
        self.set_background(widgets, self._current_row_background)

    def set_background_normal(self, widgets):
        self._current_row_background = NULL_COLOUR
        self.set_background(widgets, self._current_row_background)

    def set_background_row_under_pointer(self, widgets):
        self.set_background(widgets, ROW_UNDER_POINTER_COLOUR)

    def set_background_selection(self, widgets):
        self._current_row_background = SELECTION_COLOUR
        self.set_background(widgets, self._current_row_background)

    def set_background_selection_cycle(self, widgets):
        self._current_row_background = SELECTION_CYCLE_COLOUR
        self.set_background(widgets, self._current_row_background)

    def form_row(self, parent, rowsizer):
        '''Not implemented.'''
        # Arguments unchanged from wxPython revisions
        raise DataRowError('form_row not implemented')

    def grid_row(self, textitems=(), **kargs):
        """Subclasses return (<row maker method>, <data items>, <configuration>)
        """
        configure = dict()
        for attr in kargs:
            if attr in _widget_configure:
                configure[attr] = kargs[attr]
        return (self.make_row_widgets, textitems, configure)

    def grid_row_bookmark(self, **kargs):
        self._current_row_background = BOOKMARK_COLOUR
        return self.grid_row(background=BOOKMARK_COLOUR, **kargs)

    def grid_row_bookmarked_selection(self, **kargs):
        self._current_row_background = SELECTION_AND_BOOKMARK_COLOUR
        return self.grid_row(background=SELECTION_AND_BOOKMARK_COLOUR, **kargs)

    def grid_row_normal(self, **kargs):
        self._current_row_background = NULL_COLOUR
        return self.grid_row(background=NULL_COLOUR, **kargs)

    def grid_row_under_pointer(self, **kargs):
        return self.grid_row(background=ROW_UNDER_POINTER_COLOUR, **kargs)

    def grid_row_selection(self, **kargs):
        self._current_row_background = SELECTION_COLOUR
        return self.grid_row(background=SELECTION_COLOUR, **kargs)

    def grid_row_selection_cycle(self, **kargs):
        self._current_row_background = SELECTION_CYCLE_COLOUR
        return self.grid_row(background=SELECTION_CYCLE_COLOUR, **kargs)

    def __call__(self):
        """Hack to check that make_row_widgets return self enables pointer."""
        return (self._row_widgets,)

    def make_row_widgets(self, widget, parent, items, **kargs):
        """Return row of populated widgets with grid configuration arguments.

        widget - function that returns an existing available widget or None
        parent - master for row of widgets
        items - tuple of text option values for widget configure command.
        **kargs - widget configure options to override spec for all row widgets

        """
        # Maybe return dictionary of widgets with (row, col) as keys?
        # If spec per instance set spec[TEXT] in grid_row() call?
        row = []
        for item, spec in zip(items, self.row_specification):
            wconf = spec[WIDGET_CONFIGURE].copy()
            for attr in kargs:
                if attr not in wconf:
                    wconf[attr] = kargs[attr]
            w = widget(spec[WIDGET])
            if w is None:
                w = spec[WIDGET](master=parent)
            w.bind(
                '<Enter>',
                self.try_event(self.highlight_row_on_pointer_enter))
            w.bind(
                '<Leave>',
                self.try_event(self.highlight_row_on_pointer_leave))
            # populate_widget is Tkinter.Label.configure by default
            # Typical subclass override is populate and format the Text widget
            # passed as w argument from the item passed as text argument.
            self.populate_widget(w, text=item, **wconf)
            row.append((w, spec[GRID_CONFIGURE]))
        self._row_widgets = row
        return self


    def populate_widget(self, widget, cnf=None, text=None, **kw):
        """Default wrapper for assumed tkinter.Label widget configure method."""
        # Replaces the class attribute set by
        # populate_widget = tkinter.Label.configure
        # at Python 2.n version of this module
        widget.configure(cnf=cnf, text=text, **kw)

    def highlight_row_on_pointer_enter(self, event):
        self.set_background_row_under_pointer(self._row_widgets)

    def highlight_row_on_pointer_leave(self, event):
        if not self._pointer_popup_active:
            self.set_background(self._row_widgets, self._current_row_background)

    def set_popup_state(self, state=True):
        self._pointer_popup_active = bool(state)

    def is_row_under_pointer(self, pointerx, pointery):
        for r in self._row_widgets:
            w = r[0]
            wx = int(w.winfo_rootx())
            wy = int(w.winfo_rooty())
            if pointery < wy:
                pass
            elif pointery > wy + int(w.winfo_height()):
                pass
            elif pointerx < wx:
                pass
            elif pointerx > wx + int(w.winfo_width()):
                pass
            else:
                return True
        return False
